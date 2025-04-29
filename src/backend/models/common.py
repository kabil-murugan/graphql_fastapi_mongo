"""Common models used across the application."""

from enum import Enum
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for created_by and modified_by fields."""

    name: Optional[str] = None
    email: Optional[str] = None


class TestData(BaseModel):
    """Test Data."""

    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    name: Optional[str] = None


class ParamGroupType(str, Enum):
    """Enum for Test Plan Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


class TestStatus(str, Enum):
    """Enum for Test Status."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
