"""Document model for test results collection."""

from datetime import datetime
from enum import Enum
from typing import Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


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

    name: str
    email: str


class SampleOffset(BaseModel):
    """Sample Offset model."""

    _id: PydanticObjectId
    start_time: datetime
    end_time: datetime
    start_pos: float
    end_pos: float


class TestResultValue(BaseModel):
    """Test Result Value model."""

    _id: PydanticObjectId
    test_result_Group_id: PydanticObjectId
    test_result_Group_type: ParamGroupType
    test_result_Group_name: str
    test_result_Name: str
    test_result_Value: Union[str, float]
    unit: str


class TestResult(Document):
    """Test Results model."""

    name: str
    test_id: PydanticObjectId  # test reference
    test_plan_id: PydanticObjectId  # test_plan reference
    start_time: datetime
    end_time: datetime
    test_result_values: list[TestResultValue]
    test_plan_time: datetime
    start_position: float
    end_position: float
    status: TestStatus
    sensor_offsets: list[SampleOffset]
    equipment_offsets: list[SampleOffset]
    version: int
    created_at: datetime
    modified_at: datetime
    created_by: User
    modified_by: User

    class Settings:
        name = "test_results"
