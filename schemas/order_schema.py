from pydantic import BaseModel, Field
from typing import List


class OrderItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=100
    )
    items: List[OrderItemCreate]