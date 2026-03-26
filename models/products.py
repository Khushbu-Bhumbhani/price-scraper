from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ProductDetails:
    id:int
    title: Optional[str]
    price: Optional[str]
    rating: Optional[str]
    seller_name:Optional[str]
    link:str
