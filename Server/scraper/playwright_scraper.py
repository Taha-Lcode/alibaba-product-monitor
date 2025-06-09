from playwright.sync_api import sync_playwright
import sys
import os
import random
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def scrape_alibaba(keyword="solar panel", max_results=10):
    products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False) 
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
        ]

        ua = random.choice(user_agents)
        context = browser.new_context(
            user_agent=ua,
            viewport={"width": 1280, "height": 720},
            is_mobile=False,
            java_script_enabled=True,
            locale="en-US"
        )
        page = context.new_page()

        search_url = f"https://www.alibaba.com/trade/search?SearchText={keyword.replace(' ', '+')}"
        
        page.goto(search_url, timeout=30000, wait_until="domcontentloaded")

        page.wait_for_selector(".J-search-card-wrapper", timeout=10000)

        for _ in range(3):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(1000)

        page.wait_for_selector(".J-search-card-wrapper", timeout=20000)

        product_cards = page.query_selector_all(".J-search-card-wrapper")
        print(f"[DEBUG] Found {len(product_cards)} product cards")

        for card in product_cards:
            if len(products) >= max_results:
                break

            try:
                title_elem = card.query_selector("a[data-spm='d_title']")
                if not title_elem:
                    print("Skipping product due to missing title")
                    continue
                
                title = title_elem.inner_text().strip()
                url = title_elem.get_attribute("href")
                if url and not url.startswith("http"):
                    url = "https:" + url

                supplier = card.query_selector(".search-card-e-company")
                supplier_name = supplier.inner_text().strip() if supplier else "Unknown"

                price_elem = card.query_selector(".search-card-e-price-main")
                price = price_elem.inner_text().strip() if price_elem else "N/A"

                rate_elem = card.query_selector(".search-card-e-review")
                rating = rate_elem.inner_text().strip() if rate_elem else "N/A"

                moq = None
                moq_items = card.query_selector_all(".search-card-m-sale-features__item")
                for item in moq_items:
                    text = item.inner_text().strip().lower()
                    if any(unit in text for unit in ["pcs", "piece", "set", "box", "unit", "pair"]):
                        match = re.search(r"\d[\d,\.]*", text)
                        if match:
                            digits_only = match.group().replace(",", "")
                            moq = int(float(digits_only))
                        break
                
                products.append({
                    "product_title": title,
                    "product_url": url,
                    "supplier_name": supplier_name,
                    "price": price,
                    "moq": moq,
                    "rating": rating
                })

            except Exception as e:
                print("Skipped product due to error:", e)
                continue

        browser.close()

    return products

if __name__ == "__main__":
    from db.models import insert_product, close_connection, initialize_db, insert_keyword
    from notifier.email_notify import send_email

    initialize_db()

    keyword = input("Enter product keyword: ")
    max_results = int(input("Max number of results to fetch: ") or "10")
    receiver = input("Enter your email to receive alerts: ")

    insert_keyword(keyword)

    results = scrape_alibaba(keyword=keyword, max_results=max_results)

    for product in results:
        is_new = insert_product(product)
        
        print("\n📦 Product Details:")
        print(f"Title   : {product['product_title']}")
        print(f"URL     : {product['product_url']}")
        print(f"Supplier: {product['supplier_name']}")
        print(f"Price   : {product['price']}")
        print(f"MOQ     : {product['moq']}")
        print(f"Rating  : {product['rating']}")
        
        if is_new:
            print(f"[NEW] Product found: {product['product_title']}")
            subject = f"🛒 New Product: {product['product_title'][:50]}"
            body = (
                f"Title   : {product['product_title']}\n"
                f"Price   : {product['price']}\n"
                f"MOQ     : {product['moq']}\n"
                f"Supplier: {product['supplier_name']}\n"
                f"Rating  : {product['rating']}\n"
                f"URL     : {product['product_url']}"
            )
            send_email(subject, body, to_address=receiver)

    close_connection()

    print("\nAll data saved to products.db.")