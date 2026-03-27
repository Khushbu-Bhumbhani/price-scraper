import sqlite3
from datetime import datetime
from models.products import ProductDetails
class Database:
    def __init__(self,db_name="products.db"):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
    def create_table(self):
        self.cursor.execute(
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
        self.conn.commit() 
        
    def save_product(self,url,pd:ProductDetails):
        self.cursor.execute(
        """INSERT INTO products (url,title,price,ratings,created_at) 
           VALUES (?,?,?,?,?)
        """,(url,pd.title,pd.price,pd.rating,datetime.now().isoformat())
        )   
        self.conn.commit
        
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
    