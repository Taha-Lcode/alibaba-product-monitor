import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def scrape_alibaba_by_category(category_keyword):
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    await page.goto("https://sale.alibaba.com/p/new_launches/index.html", waitUntil="networkidle0")

    await page.waitForSelector(".hugo-dotelement.tab-item")
    
    await page.waitForSelector(".hugo4-pc-grid-item .hugo4-product-element.subject")
    initial_title = await page.evaluate("""
        () => {
            const first = document.querySelector('.hugo4-pc-grid-item .hugo4-product-element.subject');
            return first ? first.innerText.trim() : '';
        }
    """)

    tab_clicked = await page.evaluate(f"""
        () => {{
            const tabs = Array.from(document.querySelectorAll('.hugo-dotelement.tab-item'));
            const tab = tabs.find(t => t.innerText.toLowerCase().includes("{category_keyword.lower()}"));
            if (tab) {{
                tab.click();
                return true;
            }}
            return false;
        }}
    """)

    if not tab_clicked:
        print(f"[!] Category '{category_keyword}' not found.")
        await browser.close()
        return []

    max_retries = 15
    for _ in range(max_retries):
        await asyncio.sleep(1)
        new_title = await page.evaluate("""
            () => {
                const first = document.querySelector('.hugo4-pc-grid-item .hugo4-product-element.subject');
                return first ? first.innerText.trim() : '';
            }
        """)
        if new_title != initial_title and new_title.strip() != '':
            break

    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    product_sections = soup.select(".hugo4-pc-grid-item")
    results = []

    for card in product_sections:
        try:
            name = card.select_one('.hugo4-product-element.subject').get_text(strip=True)
            price = card.select_one('.hugo4-product-element.price').get_text(strip=True)
            moq = card.select_one('.moq-number').get_text(strip=True)
            img = card.select_one('img')
            img_url = img['src'] if img else 'N/A'
            href = card.select_one('a')['href']
            product_url = 'https:' + href if href.startswith('//') else href

            results.append({
                "product_title": name,
                "price": price,
                "moq": moq,
                "image": img_url,
                "product_url": product_url,
            })
        except:
            continue

    await browser.close()

    print(f"\n✅ Filtered results for category: {category_keyword} ({len(results)} items)\n")
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['product_title']}")
        print(f"   Price: {item['price']}")
        print(f"   MOQ: {item['moq']}")
        print(f"   Image: {item['image']}")
        print(f"   Link: {item['product_url']}\n")

    return results

if __name__ == "__main__":
    category = "Shoes & Accessories"
    asyncio.run(scrape_alibaba_by_category(category))
