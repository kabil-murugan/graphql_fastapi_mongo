"""Document model for test plans collection."""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class ParamGroupType(str, Enum):
    """Enum for Test Plan Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


class User(BaseModel):
    """User model for created_by and modified_by fields."""

    name: Optional[str] = None
    email: Optional[str] = None


class TestPlanValue(BaseModel):
    """Test Plan Value model."""

    id: Optional[PydanticObjectId] = Field(None)
    test_plan_group_id: PydanticObjectId
    test_plan_group_type: Optional[ParamGroupType] = None
    test_plan_group_name: Optional[str] = None
    test_plan_name: Optional[str] = None
    test_plan_value: Optional[Union[str, float]] = None
    unit: Optional[str] = None


class TestPlan(Document):
    """Test Plan model."""

    name: Optional[str] = None
    schema_test_plan_condition: Optional[str] = None
    test_id: PydanticObjectId  # test reference
    test_planning_notes: Optional[str] = None
    test_planned_values: Optional[list[TestPlanValue]] = None
    created_by: Optional[User] = None
    modified_by: Optional[User] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    version: Optional[int] = None

    class Settings:
        name = "test_plans"


class TestData(BaseModel):
    """Test Data."""

    id: Optional[PydanticObjectId] = None
    name: Optional[str] = None


class TestPlanOutput(TestPlan):
    """Test Plan Output model."""

    test: Optional[TestData] = None
