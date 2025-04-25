"""Document model for test results collection."""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from backend.models.test_plan import TestPlanValue


class TestStatus(str, Enum):
    """Enum for Test Status."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ParamGroupType(str, Enum):
    """Enum for Test Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


class User(BaseModel):
    """User model for created_by and modified_by fields."""

    name: Optional[str] = None
    email: Optional[str] = None


class SampleOffset(BaseModel):
    """Sample Offset model."""

    id: Optional[PydanticObjectId] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    start_pos: Optional[float] = None
    end_pos: Optional[float] = None


class TestResultValue(BaseModel):
    """Test Result Value model."""

    id: Optional[PydanticObjectId] = None
    test_result_group_id: PydanticObjectId
    test_result_group_type: Optional[ParamGroupType] = None
    test_result_group_name: Optional[str] = None
    test_result_name: Optional[str] = None
    test_result_value: Optional[Union[str, float]] = None
    unit: Optional[str] = None


class TestResult(Document):
    """Test Results model."""

    name: Optional[str] = None
    test_id: PydanticObjectId  # test reference
    test_plan_id: PydanticObjectId  # test_plan reference
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    test_result_values: Optional[list[TestResultValue]] = None
    test_plan_time: Optional[datetime] = None
    start_position: Optional[float] = None
    end_position: Optional[float] = None
    status: Optional[TestStatus] = None
    sensor_offsets: Optional[list[SampleOffset]] = None
    equipment_offsets: Optional[list[SampleOffset]] = None
    version: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    created_by: Optional[User] = None
    modified_by: Optional[User] = None

    class Settings:
        name = "test_results"


class TestData(BaseModel):
    """Test Data."""

    id: Optional[PydanticObjectId] = None
    name: Optional[str] = None


class TestPlanData(BaseModel):
    """Test Plan data."""

    id: Optional[PydanticObjectId] = None
    name: Optional[str] = None
    planned_values: Optional[list[TestPlanValue]] = None


class TestResultOutput(TestResult):
    """Test Result Output model."""

    test: Optional[TestData] = None
    test_plan: Optional[TestPlanData] = None
