import sqlite3
from datetime import datetime
from models.products import ProductDetails

DB_NAME = "products.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        title TEXT,
        price REAL,
        ratings REAL,
        created_at TIMESTAMP
    )
    """
    )
    conn.commit()
    conn.close() 
        
def save_product(url,pd:ProductDetails):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
    """INSERT INTO products (url,title,price,ratings,created_at) 
        VALUES (?,?,?,?,?)
    """,(url,pd.title,pd.price,pd.ratings,datetime.now().isoformat())
    )
    conn.commit()
    conn.close()   
        
def get_last_price(url):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
    """SELECT price FROM products WHERE url=? ORDER BY created_at DESC
    """,(url,)
    )
    result=cursor.fetchone()
    conn.close()
    return result[0] if result else None
               
def get_all_products():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT url, title, price, created_at FROM products ORDER BY created_at DESC")
    rows=cursor.fetchall()
    conn.close()
    return rows

    
    