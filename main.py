import sys
import asyncio
from urllib.parse import urlparse
from scraper.fetcher import fetch_html
from models.products import ProductDetails
from scraper.amazon import parse_product
from services.price_tracker import track_price
import time
from services.email_service import send_email
from utils.retry import retry_async
from utils.logger import setup_logger
from database.db import create_table
from database.db import save_product

def is_valid_url(url: str) -> bool:
    # print(url)
    parsed_url = urlparse(url)
    return parsed_url.scheme in ("http", "https") and parsed_url.netloc != ""


def get_url_input() -> list[str]:
    """
        Accept single or multiple URLs (comma-separated). CLI argument or user input.

    Returns:
        str: list of valid URLs
    """
    # CLI input
    if len(sys.argv) > 1:
        raw_input = sys.argv[1]
        urls = [u.strip() for u in raw_input.split(",")]

        valid_urls = [url for url in urls if is_valid_url(url)]

        if valid_urls:
            return list(set(valid_urls))
        else:
            raise ValueError("Invalid url provided in command line")
    # Manual Input
    while True:
        raw_input = input("Enter Product URL(s):").strip()
        urls = [url.strip() for url in raw_input.split(",")]
        valid_urls = [url for url in urls if is_valid_url(url)]
        if valid_urls:
            return list(set(valid_urls))

        print(" ❌ Invalid URL. Example: https://www.amazon.in/dp/XXXXX")


def run_tracker(urls:str):
    
    create_table()
    try:

        for url in urls:
            html = asyncio.run(retry_async(fetch_html,url))

            pd = parse_product(html)

            print(f"Tracking: {url}")
            result = track_price(pd, url)
           
            time.sleep(2)
            print(f"Status:{result['status']}")

            if result["status"] == "dropped":

                send_email(
                    subject=f"🔥 Price Drop: {pd.title[:50]}",
                    body=f"""
                    🔥 Price Dropped!
                    
                    {pd.title}
                    
                    Old Price: ₹{result['old_price']}
                    New Price: ₹{result['new_price']}
                    Drop Percent: {result['change_percent']}:.2f%
                    Link: {url}
                    """,
                )
            elif result["status"] == "increased":
                send_email(
                    subject="📈 Price increased",
                    body=f"""
                    📈 Price increased
                    
                    {pd.title}
                    
                    Old Price: ₹{result['old_price']}
                    New Price: ₹{result['new_price']}
                    Change Percent: {result['change_percent']}:.2f%
                    Link: {url}
                    """,
                )
    except Exception as e:
        print(f"Exception in main:{e}")
   

def main():

    setup_logger()
    urls = get_url_input()
    run_tracker(urls)


if __name__ == "__main__":
    main()
