"""Document model for test collection."""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from backend.models.common import TestStatus, User


class TestType(str, Enum):
    """Enum for Test Type."""

    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    INTEGRATION = "INTEGRATION"
    REGRESSION = "REGRESSION"
    UNIT = "UNIT"


class TestStep(BaseModel):
    """Test Step model."""

    id: Optional[PydanticObjectId] = None
    step_name: Optional[str] = None
    description: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[Union[str, None]] = None
    status: Optional[TestStatus] = None
    executed_at: Optional[datetime] = None


class TestEnvironment(BaseModel):
    """Test Environment model."""

    environment_name: Optional[str] = None
    os: Optional[str] = None
    browser: Optional[str] = None
    version: Optional[str] = None
    hardware: Optional[str] = None


class TestLog(BaseModel):
    """Test Log model."""

    timestamp: Optional[datetime] = None
    message: Optional[str] = None
    level: Optional[str] = None


class Test(Document):
    """Test Collection model."""

    name: Optional[str] = None
    description: Optional[str] = None
    test_type: Optional[TestType] = None
    status: Optional[TestStatus] = None
    steps: Optional[list[TestStep]] = None
    environment: Optional[TestEnvironment] = None
    logs: Optional[list[TestLog]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    version: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    created_by: Optional[User] = None
    modified_by: Optional[User] = None

    class Settings:
        name = "tests"
