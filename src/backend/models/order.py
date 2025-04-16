"""Document model for orders collection."""

from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order status enum."""

    PENDING = "pending"
    ORDERED = "ordered"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Order item model."""

    product_id: Optional[str] = Field(None)
    quantity: Optional[int] = Field(None)


class Order(Document):
    """Order model."""

    user_id: Optional[str] = Field(None)
    items: Optional[List[OrderItem]] = Field(None)
    status: Optional[OrderStatus] = Field(None)

    class Settings:
        name = "orders"
