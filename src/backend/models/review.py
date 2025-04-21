"""Models for Reviews."""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import Field


class Review(Document):
    """Review model for storing product reviews."""

    product_id: Optional[PydanticObjectId] = Field(None)
    user_id: Optional[PydanticObjectId] = Field(None)
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "reviews"
