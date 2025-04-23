"""Document model for test collection."""

from datetime import datetime
from enum import Enum
from typing import Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class TestType(str, Enum):
    """Enum for Test Type."""

    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    INTEGRATION = "INTEGRATION"
    REGRESSION = "REGRESSION"
    UNIT = "UNIT"


class TestStatus(str, Enum):
    """Enum for Test Status."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class User(BaseModel):
    """User model for created_by and modified_by fields."""

    name: str
    email: str


class TestStep(BaseModel):
    """Test Step model."""

    _id: PydanticObjectId
    step_name: str
    description: str
    expected_result: str
    actual_result: Union[str, None]
    status: TestStatus
    executed_at: datetime


class TestEnvironment(BaseModel):
    """Test Environment model."""

    environment_name: str
    os: str
    browser: str
    version: str
    hardware: str


class TestLog(BaseModel):
    """Test Log model."""

    timestamp: datetime
    message: str
    level: str


class Test(Document):
    """Test Collection model."""

    name: str
    description: str
    test_type: TestType
    status: TestStatus
    steps: list[TestStep]
    environment: TestEnvironment
    logs: list[TestLog]
    start_time: datetime
    end_time: datetime
    duration: float
    version: int
    created_at: datetime
    modified_at: datetime
    created_by: User
    modified_by: User

    class Settings:
        name = "tests"
