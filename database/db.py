import sqlite3
from datetime import datetime
from models.products import ProductDetails

DB_NAME = "products.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # PRODUCTS TABLE
    # -------------------------
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # -------------------------
    # PRICE HISTORY TABLE
    # -------------------------
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        price REAL,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """
    )

    conn.commit()
    conn.close()


def get_or_create_product(url, title):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if exists
    cursor.execute("SELECT id from products WHERE url=?", (url,))
    result = cursor.fetchone()

    if result:
        product_id = result[0]
    else:
        cursor.execute(
            """
                       INSERT INTO products (url,title) values (?,?)
                       """,
            (url, title),
        )
        product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return product_id


def save_price_history(product_id, pd: ProductDetails):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO price_history (product_id,price,status,created_at) 
        VALUES (?,?,?,?)
    """,
        (product_id, pd.price, pd.status, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_last_price(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT price FROM price_history WHERE product_id=? ORDER BY created_at DESC
    """,
        (product_id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
            p.id,
            p.url,
            p.title,
            ph.price,
            ph.status,
            ph.created_at
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        ORDER BY ph.created_at DESC"""
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_product(url: str):
    conn = get_connection()
    cusror = conn.cursor()
    #Get product id
    cusror.execute("""
                   SELECT id FROM products WHERE url=?
                   """,(url,))
    result=cusror.fetchone()
    
    if result:
        product_id=result[0]
        #delete price history first
        cusror.execute(
           """DELETE FROM price_history WHERE product_id = ?
            """,
        (product_id,),
         )
        
        #delete the product
        cusror.execute("""
                       DELETE FROM products where id=?
                       """,(product_id,))
        
    conn.commit()
    conn.close()
