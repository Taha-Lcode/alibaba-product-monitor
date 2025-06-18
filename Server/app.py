from flask import Flask, request, jsonify
from scraper.new_launch_scraper import scrape_new_launches_by_category
from db.models import insert_product, initialize_db, close_connection, get_all_keywords, insert_keyword
from notifier.email_notify import send_email
from flask_cors import CORS
import os
from dotenv import load_dotenv
import traceback
import threading
from bs4 import BeautifulSoup
import requests

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = Flask(__name__)
CORS(app, origins=[FRONTEND_URL])

initialize_db()

@app.route("/new-launches", methods=["POST"])
def new_launches():
    try:
        data = request.get_json()
        category = data.get("category")
        receiver = data.get("receiver")

        if not category:
            return jsonify({"error": "Missing category"}), 400

        insert_keyword(category)
        results = scrape_new_launches_by_category(category)

        if receiver:
            def notify_in_background():
                for product in results:
                    is_new = insert_product(product)
                    if is_new:
                        subject = f"🛒 New Product: {product['product_title'][:50]}"
                        body = (
                            f"Image   : {product.get('image', 'N/A')}\n"
                            f"Title   : {product['product_title']}\n"
                            f"Price   : {product['price']}\n"
                            f"MOQ     : {product.get('moq', 'N/A')}\n"
                            f"Supplier: {product.get('supplier_name', 'N/A')}\n"
                            f"URL     : {product['product_url']}"
                        )
                        send_email(subject, body, to_address=receiver)
                close_connection()

            threading.Thread(target=notify_in_background).start()

        return jsonify({
            "message": "Search successful",
            "products": results,
            "total": len(results)
        })

    except Exception as e:
        print("🔥 ERROR in /new-launches:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/keywords", methods=["GET"])
def get_keywords():
    try:
        keywords = get_all_keywords()
        return jsonify({"keywords": keywords})
    except Exception as e:
        print("🔥 ERROR while fetching keywords:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

@app.route("/categories", methods=["GET"])
def get_categories():
    try:
        url = "https://sale.alibaba.com/p/new_launches/index.html"
        response = requests.get(
            "https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": SCRAPINGBEE_API_KEY,
                "url": url,
                "render_js": "true"
            }
        )
        soup = BeautifulSoup(response.text, "html.parser")

        categories = []
        tabs = soup.select(".hugo-dotelement.tab-item")
        for tab in tabs:
            name = tab.get_text(strip=True)
            if name:
                categories.append(name)

        return jsonify(categories)

    except Exception as e:
        print("🔥 ERROR in /categories:", e)
        return jsonify({"error": "Failed to fetch categories"}), 500



if __name__ == "__main__":
    app.run(debug=True)
