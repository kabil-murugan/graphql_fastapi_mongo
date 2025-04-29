"""Document model for test plans collection."""

from datetime import datetime
from typing import Optional, Union

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from backend.models.common import ParamGroupType, TestData, User


class TestPlanValue(BaseModel):
    """Test Plan Value model."""

    id: Optional[PydanticObjectId] = None
    test_plan_group_id: Optional[PydanticObjectId] = None
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


class TestPlanOutput(TestPlan):
    """Test Plan Output model."""

    test: Optional[TestData] = None
