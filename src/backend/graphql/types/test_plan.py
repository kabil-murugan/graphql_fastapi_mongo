"""Object Types for Test Plans."""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

import strawberry


@strawberry.enum
class ParamGroupTypeEnum(Enum):
    """Enum for Test Plan Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


@strawberry.type
class User:
    """User Object Type."""

    name: Optional[str]
    email: Optional[str]


@strawberry.type
class TestPlanValue:
    """Test Plan Value Object Type."""

    id: strawberry.ID
    test_plan_Group_id: strawberry.ID
    test_plan_Group_type: Optional[ParamGroupTypeEnum]
    test_plan_Group_name: Optional[str]
    test_plan_Name: Optional[str]
    test_plan_Value: Optional[Union[str, float]]
    unit: Optional[str]


@strawberry.type
class TestData:
    """Test Data."""

    id: strawberry.ID
    name: Optional[str]


@strawberry.type
class TestPlan:
    """Test Plan Object Type."""

    id: strawberry.ID
    name: Optional[str]
    schema_test_plan_condition: Optional[str]
    test_id: strawberry.Private[strawberry.ID]
    test_data: Optional[TestData]
    test_planning_notes: Optional[str]
    test_planned_values: Optional[list[TestPlanValue]]
    created_by: Optional[User]
    modified_by: Optional[User]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    version: Optional[int]
