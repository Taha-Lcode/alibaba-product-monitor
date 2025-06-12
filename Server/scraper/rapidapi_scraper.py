import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_URL = os.getenv("RAPIDAPI_URL") 
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def scrape_alibaba(keyword="solar panel", max_results=10):
    params = {
        "q": keyword,
        "page": "1"
    }

    try:
        response = requests.get(RAPIDAPI_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        products = []

        items = data.get("result", {}).get("resultList", [])

        for obj in items[:max_results]:
            item = obj.get("item", {})
            sku = item.get("sku", {}).get("def", {})
            price = sku.get("priceModule", {}).get("priceFormatted")
            moq = sku.get("quantityModule", {}).get("minOrder", {}).get("quantityFormatted")

            company_info = item.get("company", {})
            store_info = item.get("seller", {})

            supplier = (
                company_info.get("companyName")
                or store_info.get("storeName")
                or "Alibaba Seller"
            )

            products.append({
                "product_title": item.get("title"),
                "product_url": item.get("itemUrl"),
                "image": f"https:{item.get('image')}" if item.get('image') else None,
                "supplier_name": supplier,
                "price": price or "N/A",
                "moq": moq or "N/A",
            })
        
        return products

    except requests.RequestException as e:
        print("❌ API Error:", e)
        return []

if __name__ == "__main__":
    keyword = input("Enter product keyword: ")
    results = scrape_alibaba(keyword=keyword, max_results=2)
    
    for idx, p in enumerate(results, 1):
        print(f"Image   : {p['image']}")
        print(f"\n🔹 Product {idx}")
        print(f"Title   : {p['product_title']}")
        print(f"URL     : {p['product_url']}")
        print(f"Supplier: {p['supplier_name']}")
        print(f"Price   : {p['price']}")
        print(f"MOQ     : {p['moq']}")
