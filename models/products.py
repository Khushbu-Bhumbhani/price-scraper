from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ProductDetails:
    title: Optional[str]
    price: Optional[str]
    rating: Optional[str]
