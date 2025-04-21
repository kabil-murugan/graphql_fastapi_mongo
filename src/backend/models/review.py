from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class Review(Document):
    """Review model for storing product reviews."""

    product_id: PydanticObjectId = Field(...)
    user_id: PydanticObjectId = Field(...)
    rating: Optional[int] = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "reviews"
