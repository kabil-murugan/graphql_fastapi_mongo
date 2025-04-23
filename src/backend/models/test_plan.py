"""Document model for test plans collection."""

from datetime import datetime
from enum import Enum
from typing import Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class ParamGroupType(str, Enum):
    """Enum for Test Plan Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


class User(BaseModel):
    """User model for created_by and modified_by fields."""

    name: str
    email: str


class TestPlanValue(BaseModel):
    """Test Plan Value model."""

    _id: PydanticObjectId
    test_plan_Group_id: PydanticObjectId
    test_plan_Group_type: ParamGroupType
    test_plan_Group_name: str
    test_plan_Name: str
    test_plan_Value: Union[str, float]
    unit: str


class TestPlan(Document):
    """Test Plan model."""

    name: str
    schema_test_plan_condition: str
    test_id: PydanticObjectId
    test_planning_notes: str
    test_planned_values: list[TestPlanValue]
    created_by: User
    modified_by: User
    created_at: datetime
    modified_at: datetime
    version: int

    class Settings:
        name = "test_plans"
