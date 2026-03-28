import sqlite3
from datetime import datetime
from models.products import ProductDetails
class Database:
    def __init__(self,db_name="products.db"):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        
    def __del__(self):
        self.conn.close()
        
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
        """,(url,pd.title,pd.price,pd.ratings,datetime.now().isoformat())
        )   
        self.conn.commit()
        
    def get_last_price(self,url):
        self.cursor.execute(
        """SELECT price FROM products WHERE url=? ORDER BY created_at DESC
        """,(url,)
        )
        result=self.cursor.fetchone()
        return result[0] if result else None
               
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
    