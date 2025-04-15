"""Document model for users collection."""

from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Profile model for user information."""

    age: Optional[int] = Field(None, ge=0)
    location: Optional[str] = Field(None)


class User(Document):
    """User model for the database."""

    name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    profile: Optional[Profile] = Field(None)

    class Settings:
        name = "users"
