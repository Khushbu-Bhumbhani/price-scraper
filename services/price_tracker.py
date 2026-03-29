from models.products import ProductDetails
from database.db import Database

class PriceTracker:
    def __init__(self,db):
        self.db=db

    def track_price(self,product:ProductDetails,url:str):
        latest_price=self.db.get_last_price(url)
        status="same"
        if latest_price is not None:
            if product.price < latest_price:
                print("🔥 PRICE DROPPED!")
                status="dropped"
                change_percent=((latest_price-product.price)/latest_price)*100
            elif product.price > latest_price:
                print("📈 Price increased")
                status="increased"
                change_percent=((product.price-latest_price)/latest_price)*100
            else:
                print("Same Price")
        else:
            print("First time tracking")
            
        return {
            "status":status,
            "old_price":latest_price,
            "new_price":product.price,
            "change_percent": change_percent
        }
    
    