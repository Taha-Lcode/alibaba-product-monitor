from flask import Flask, request, jsonify
from scraper.playwright_scraper import scrape_alibaba
from db.models import insert_product, initialize_db, close_connection
from notifier.email_notify import send_email

app = Flask(__name__)
initialize_db()


@app.route("/search", methods=["POST"])

def search_and_notify():
    data = request.get_json()
    keyword = data.get("keyword")
    max_results = int(data.get("max_results", 10))
    receiver = data.get("receiver")

    if not keyword or not receiver:
        return jsonify({"error": "keyword and receiver are required"}), 400

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
            "products": new_products
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        close_connection()


if __name__ == "__main__":
    app.run(debug=True)
