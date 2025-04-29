"""Document model for test results collection."""

from datetime import datetime
from typing import Optional, Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from backend.models.common import ParamGroupType, TestData, TestStatus, User
from backend.models.test_plan import TestPlanValue


class SampleOffset(BaseModel):
    """Sample Offset model."""

    id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    start_pos: Optional[float] = None
    end_pos: Optional[float] = None


class TestResultValue(BaseModel):
    """Test Result Value model."""

    id: Optional[str] = None
    test_result_group_id: Optional[PydanticObjectId] = None
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


class TestPlanData(BaseModel):
    """Test Plan data."""

    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    name: Optional[str] = None
    test_planned_values: Optional[list[TestPlanValue]] = None


class TestResultOutput(TestResult):
    """Test Result Output model."""

    test: Optional[TestData] = None
    test_plan: Optional[TestPlanData] = None
