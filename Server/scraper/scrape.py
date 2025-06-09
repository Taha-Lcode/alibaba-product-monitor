from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_products(keyword="solar panel", max_moq=None, max_results=20):
    search_url = f"https://www.alibaba.com/trade/search?SearchText={keyword.replace(' ', '+')}"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    time.sleep(5) 

    # Scroll to load dynamic content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.save_screenshot("debug.png")

    # Wait for product containers to load
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "J-search-card-wrapper")))

    product_containers = driver.find_elements(By.CLASS_NAME, "J-search-card-wrapper")
    print(f"[DEBUG] Found {len(product_containers)} product containers")

    products = []

    for container in product_containers:
        try:
            # Extract product title and URL
            try:
                title_elem = container.find_element(By.CLASS_NAME, "d_title")
                title = title_elem.text.strip()
                url = title_elem.get_attribute("href")
                if url and not url.startswith("http"):
                     url = "https:" + url
            except NoSuchElementException:
                title = "N/A"
                url = None

            # Extract company name
            try:
                supplier_elem = container.find_element(By.CLASS_NAME, "search-card-e-company")
                supplier = supplier_elem.text.strip()
            except NoSuchElementException:
                supplier = "Unknown"

            # Extract price
            try:
                price_elem = container.find_element(By.CLASS_NAME, "search-card-e-price-main")
                price = price_elem.text.strip()
            except NoSuchElementException:
                price = "N/A"

            # Extract MOQ
            try:
                moq_elem = container.find_element(By.CLASS_NAME, "search-card-m-sale-features__item")
                moq_text = moq_elem.text.strip().split()[0]
                moq = int(''.join(filter(str.isdigit, moq_text)))
            except:
                 moq = None

            print(f"[DEBUG] Title: {title}")
            print(f"[DEBUG] URL: {url}")
            print(f"[DEBUG] MOQ: {moq}")

            if url and (max_moq is None or (moq is not None and moq <= max_moq)):
                products.append({
                    "product_title": title,
                    "product_url": url,
                    "supplier_name": supplier,
                    "price": price,
                    "moq": moq
                })

            if len(products) >= max_results:
                break

        except Exception as e:
            print(f"Skipped one product due to error: {e}")
            continue
    driver.quit()
    
    return products

if __name__ == "__main__":
    keyword = "solar panel"
    max_moq = 500

    items = scrape_products(keyword=keyword, max_moq=max_moq)

    for idx, product in enumerate(items, 1):
        print(f"\n🔹 Product {idx}")
        print(f"Title   : {product['product_title']}")
        print(f"URL     : {product['product_url']}")
        print(f"Supplier: {product['supplier_name']}")
        print(f"Price   : {product['price']}")
        print(f"MOQ     : {product['moq']}")
