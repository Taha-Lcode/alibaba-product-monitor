from flask import Flask, request, jsonify
from scraper.rapidapi_scraper import scrape_alibaba
from db.models import insert_product, initialize_db, close_connection, get_all_keywords, insert_keyword
from notifier.email_notify import send_email
from flask_cors import CORS
import os
from dotenv import load_dotenv
import traceback
import threading

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

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

        insert_keyword(keyword)
        results = scrape_alibaba(keyword, max_results)

        return jsonify({"products": results, "total": len(results)})

    except Exception as e:
        print("🔥 ERROR in /search:", e)
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

@app.route("/search-and-notify", methods=["POST"])
def search_and_notify():
    try:
        data = request.get_json()
        keyword = data.get("keyword")
        max_results = int(data.get("max_results", 10))
        receiver = data.get("receiver")

        if not keyword or not receiver:
            return jsonify({"error": "keyword and receiver are required"}), 400

        insert_keyword(keyword)
        results = scrape_alibaba(keyword, max_results)

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
                        f"Supplier: {product['supplier_name']}\n"
                        f"URL     : {product['product_url']}"
                    )
                    send_email(subject, body, to_address=receiver)

            close_connection()

        threading.Thread(target=notify_in_background).start()

        return jsonify({
            "message": "Results sent to frontend. Notification is being sent in background.",
            "products": results,
            "total": len(results)
        })

    except Exception as e:
        print("🔥 ERROR in /search-and-notify:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)