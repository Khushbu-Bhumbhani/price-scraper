import sys
import asyncio
from urllib.parse import urlparse
from scraper.fetcher import fetch_html
from models.products import ProductDetails
from scraper.amazon import parse_product
from database.db import Database
from services.price_tracker import PriceTracker
import time

def is_valid_url(url:str)->bool:
    #print(url)
    parsed_url=urlparse(url)
    return parsed_url.scheme in ("http","https") and parsed_url.netloc!=""

def get_url_input() -> list[str]:
    """
        Accept single or multiple URLs (comma-separated). CLI argument or user input.
 
    Returns:
        str: list of valid URLs
    """
    # CLI input
    if len(sys.argv) > 1:
        raw_input= sys.argv[1]
        urls=   [u.strip() for u in raw_input.split(",")]
        
        valid_urls=[url for url in urls if is_valid_url(url)]
        
        if valid_urls:
            return list(set(valid_urls))
        else:
            raise ValueError("Invalid url provided in command line")
    # Manual Input
    while True:
      raw_input=input("Enter Product URL(s):").strip()
      urls=[url.strip() for url in raw_input.split(",")]
      valid_urls=[url for url in urls if is_valid_url(url)]
      if valid_urls:
          return list(set(valid_urls))
      
      print(" ❌ Invalid URL. Example: https://www.amazon.in/dp/XXXXX")
      
def main():
    db=Database()
    db.create_table()
    try:
        urls=get_url_input()
        
        #html=fetch_html(url)
        for url in urls:
            html= asyncio.run(fetch_html(url))
                 
            pd=parse_product(html)
            
            tracker=PriceTracker(db)    
            print(f"Tracking: {url}")
            result=tracker.track_price(pd,url)
            db.save_product(url,pd)
            
            time.sleep(2)
        # print(f"Status:{result['status']}")
            for k,v in result.items():
                print(f"{k.upper():<10}:{v}")
           
    finally:
        db.close()
    
    

if __name__ == "__main__":
    main()