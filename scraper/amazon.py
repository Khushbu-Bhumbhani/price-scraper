import asyncio
import re
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

from models.products import ProductDetails


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


def _clean_text(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    cleaned = " ".join(value.split())
    return cleaned or None


def _extract_price(soup: BeautifulSoup) -> Optional[str]:
    selectors = [
        ".a-price.aok-align-center .a-offscreen",
        ".a-price .a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#priceblock_saleprice",
        ".apexPriceToPay .a-offscreen",
    ]
    for selector in selectors:
        node = soup.select_one(selector)
        text = _clean_text(node.get_text(strip=True) if node else None)
        if text:
            return text
    return None


def _extract_rating(soup: BeautifulSoup) -> Optional[str]:
    selectors = [
        "span[data-hook='rating-out-of-text']",
        "#acrPopover",
        ".a-icon-alt",
    ]
    for selector in selectors:
        node = soup.select_one(selector)
        if not node:
            continue
        text = _clean_text(
            node.get("title") if selector == "#acrPopover" else node.get_text(strip=True)
        )
        if text:
            match = re.search(r"(\d+(?:\.\d+)?)\s+out of\s+5", text, re.IGNORECASE)
            return match.group(1) if match else text
    return None


def parse_product_details(html: str) -> ProductDetails:
    soup = BeautifulSoup(html, "html.parser")

    title_node = soup.select_one("#productTitle")
    title = _clean_text(title_node.get_text(strip=True) if title_node else None)
    price = _extract_price(soup)
    rating = _extract_rating(soup)

    return ProductDetails(title=title, price=price, rating=rating)


async def fetch_product_details(url: str, timeout: int = 20) -> ProductDetails:
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(headers=HEADERS, timeout=client_timeout) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return parse_product_details(html)


async def main(url: str) -> None:
    details = await fetch_product_details(url)
    print(f"Title: {details.title}")
    print(f"Price: {details.price}")
    print(f"Rating: {details.rating}")


if __name__ == "__main__":
    amazon_url = input("Enter Amazon product URL: ").strip()
    asyncio.run(main(amazon_url))
