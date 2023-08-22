from typing import List, Optional

from pydantic import BaseModel


class Items(BaseModel):
    product_id: int
    quantity: int
    price: float


class Order(BaseModel):
    id: str
    total_price: float
    user_id: int
    items: List[Items]
    created_at: Optional[int]
    delivery_lat: float
    delivery_lon: float
