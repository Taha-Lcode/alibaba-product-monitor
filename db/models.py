import sqlite3
from datetime import datetime

conn = sqlite3.connect("products.db", check_same_thread=False)
cursor = conn.cursor()

def initialize_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_title TEXT,
        product_url TEXT UNIQUE,
        supplier_name TEXT,
        price TEXT,
        moq INTEGER,
        rating TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

def insert_keyword(keyword):
    try:
        cursor.execute("INSERT INTO search_history (keyword) VALUES (?)", (keyword.strip().lower(),))
        conn.commit()
        print(f"[DB] Keyword '{keyword}' added to history.")
    except sqlite3.IntegrityError:
        print(f"[DB] Keyword '{keyword}' already in history.")

def get_all_keywords():
    cursor.execute("SELECT keyword FROM search_history")
    return [row[0] for row in cursor.fetchall()]

def insert_product(product):
    try:
        cursor.execute("""
            INSERT INTO products (
                product_title, product_url, supplier_name,
                price, moq, rating, date_scraped
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product["product_title"],
            product["product_url"],
            product["supplier_name"],
            product["price"],
            product["moq"],
            product["rating"],
            datetime.now().isoformat()
        ))

        conn.commit()

        print(f"Saved: {product['product_title']}")
        return True
    
    except sqlite3.IntegrityError:
        print(f"Skipped duplicate: {product['product_title']}")
        return False

def get_products_by_keyword(keyword):
    cursor.execute("""
        SELECT * FROM products
        WHERE LOWER(product_title) LIKE ?
        ORDER BY date_scraped DESC
    """, (f"%{keyword.lower()}%",))

    return cursor.fetchall()

def close_connection():
    conn.close()

