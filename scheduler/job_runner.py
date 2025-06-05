import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import schedule
import time
from db.models import (
    initialize_db,
    get_all_keywords,
    insert_product,
    close_connection
)
from scraper.playwright_scraper import scrape_alibaba
from notifier.email_notify import send_email


def run_monitor():

    print("\nRunning Alibaba Product Monitor...")

    initialize_db()
    receiver = "mohdtahasaleem@gmail.com"

    keywords = get_all_keywords()
    print(f"[INFO] Monitoring {len(keywords)} keyword(s): {keywords}")

    for keyword in keywords:
        print(f"\nChecking for keyword: {keyword}")
        results = scrape_alibaba(keyword=keyword, max_results=1)

        for product in results:
            is_new = insert_product(product)
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
    print("Monitoring cycle complete.\n")


schedule.every(2).minutes.do(run_monitor)

if __name__ == "__main__":
    print("Alibaba Monitor Scheduler started.")
    run_monitor()

    while True:
        schedule.run_pending()
        time.sleep(60)
