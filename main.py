import sys
import asyncio
from urllib.parse import urlparse
from scraper.fetcher import fetch_html
from models.products import ProductDetails
from scraper.amazon import parse_product

def is_valid_url(url:str)->bool:
    parsed_url=urlparse(url)
    return all([parsed_url.scheme,parsed_url.netloc])

def get_url_input() -> str:
    """
        Gets product URL from CLI argument or user input.
 
    Returns:
        str: Valid product URL
    """
    if len(sys.argv) > 1:
        url= sys.argv[1]
        if is_valid_url(url):
            return url
        else:
            raise ValueError("Invalid url provided in command line")
    
    while True:
      url=input("Enter Product URL:").strip()
      if is_valid_url(url):
          return url
      
      print(" ❌ Invalid URL. Example: https://www.amazon.in/dp/XXXXX")
      
def main():
    url=get_url_input()
    
    #html=fetch_html(url)
    html= asyncio.run(fetch_html(url))
    
    #print(html[:500])
    pd=parse_product(html)
    print(pd)
    

if __name__ == "__main__":
    main()