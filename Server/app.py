from flask import Flask, request, jsonify
from scraper.playwright_scraper import scrape_alibaba
from db.models import insert_product, initialize_db, close_connection
from notifier.email_notify import send_email
from flask_cors import CORS
from db.models import get_all_keywords
import traceback
from db.models import insert_keyword
import os
from dotenv import load_dotenv

load_dotenv() 

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = Flask(__name__)
CORS(app, origins=[FRONTEND_URL])

initialize_db()

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        keyword = data.get("keyword")
        max_results = int(data.get("max_results", 5))
        receiver = data.get("receiver")

        if not keyword:
            return jsonify({"error": "Missing keyword"}), 400

        results = scrape_alibaba(keyword, max_results)

        return jsonify({"products": results, "total": len(results)})

    except Exception as e:
        print("🔥 ERROR in /search:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/keywords", methods=["GET"])
def get_keywords():
    try:
        keywords = get_all_keywords()
        return jsonify({ "keywords": keywords })
    except Exception as e:
        print("🔥 ERROR while fetching keywords:")
        import traceback
        traceback.print_exc()
        return jsonify({ "error": str(e) }), 500

def search_and_notify():
    data = request.get_json()
    keyword = data.get("keyword")
    max_results = int(data.get("max_results", 10))
    receiver = data.get("receiver", "default@gmail.com") 
    insert_keyword(keyword) 

    if not keyword:
        return jsonify({"error": "keyword is required"}), 400

    try:
        results = scrape_alibaba(keyword=keyword, max_results=max_results)
        new_products = []

        for product in results:
            is_new = insert_product(product)
            if is_new:
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
                new_products.append(product)

        return jsonify({
            "message": f"{len(new_products)} new products found and notified.",
            "products": new_products,
            "total": len(results)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection()

if __name__ == "__main__":
    app.run(debug=True)
