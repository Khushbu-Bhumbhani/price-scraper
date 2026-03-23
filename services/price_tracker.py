import re
from dataclasses import dataclass
from typing import Optional

from database.db import (
    get_product_by_url,
    get_latest_price_record,
    init_db,
    insert_price_history,
    upsert_product,
)
from models.products import ProductDetails
from scraper.amazon import fetch_product_details


@dataclass(slots=True)
class TrackingResult:
    title: Optional[str]
    price: Optional[str]
    rating: Optional[str]
    previous_price: Optional[str]
    alert_message: Optional[str]


def _parse_price_value(price_text: Optional[str]) -> Optional[float]:
    if not price_text:
        return None
    normalized = price_text.replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)", normalized)
    if not match:
        return None
    return float(match.group(1))


def _build_alert(
    details: ProductDetails,
    previous_price_value: Optional[float],
    current_price_value: Optional[float],
    previous_price_text: Optional[str],
) -> Optional[str]:
    if previous_price_value is None or current_price_value is None:
        return None
    if current_price_value >= previous_price_value:
        return None
    return (
        f"Price dropped for {details.title or 'product'}: "
        f"{previous_price_text or previous_price_value} -> {details.price or current_price_value}"
    )


async def track_product_price(url: str) -> TrackingResult:
    init_db()

    existing_product = get_product_by_url(url)
    previous_record = None
    if existing_product:
        previous_record = get_latest_price_record(int(existing_product["id"]))

    details = await fetch_product_details(url)
    current_price_value = _parse_price_value(details.price)
    previous_price_value = (
        float(previous_record["price_value"])
        if previous_record and previous_record["price_value"] is not None
        else None
    )
    previous_price_text = (
        str(previous_record["price_text"])
        if previous_record and previous_record["price_text"]
        else None
    )

    alert_message = _build_alert(
        details=details,
        previous_price_value=previous_price_value,
        current_price_value=current_price_value,
        previous_price_text=previous_price_text,
    )

    product_id = upsert_product(
        url=url,
        title=details.title,
        price_text=details.price,
        price_value=current_price_value,
        rating=details.rating,
    )
    insert_price_history(
        product_id=product_id,
        price_text=details.price,
        price_value=current_price_value,
        rating=details.rating,
    )

    return TrackingResult(
        title=details.title,
        price=details.price,
        rating=details.rating,
        previous_price=previous_price_text,
        alert_message=alert_message,
    )
