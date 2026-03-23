import asyncio
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.price_tracker import track_product_price


async def run(url: str) -> None:
    result = await track_product_price(url)
    print(f"Title: {result.title}")
    print(f"Price: {result.price}")
    print(f"Rating: {result.rating}")
    if result.previous_price:
        print(f"Previous Price: {result.previous_price}")
    if result.alert_message:
        print(f"ALERT: {result.alert_message}")
    else:
        print("ALERT: No price drop detected.")


def get_product_url() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else input("Enter Amazon product URL: ").strip()


if __name__ == "__main__":
    asyncio.run(run(get_product_url()))
