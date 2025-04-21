"""Document model for products collection."""

from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import Field


class Product(Document):
    """Product model."""

    name: Optional[str] = Field(None)
    price: Optional[float] = Field(None)
    review_ids: Optional[list[PydanticObjectId]] = Field(None)

    class Settings:
        name = "products"
