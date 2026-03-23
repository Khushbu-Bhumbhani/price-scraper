import asyncio
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scraper.amazon import fetch_product_details


async def run(url: str) -> None:
    details = await fetch_product_details(url)
    print(f"Title: {details.title}")
    print(f"Price: {details.price}")
    print(f"Rating: {details.rating}")


def get_product_url() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else input("Enter Amazon product URL: ").strip()


if __name__ == "__main__":
    asyncio.run(run(get_product_url()))
