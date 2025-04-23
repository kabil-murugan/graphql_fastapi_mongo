"""Object Types for Test Results."""

from datetime import datetime
from typing import Optional

import strawberry

from backend.graphql.types.common import (
    VALUE,
    ParamGroupTypeEnum,
    TestData,
    TestStatusEnum,
    User,
)
from backend.graphql.types.test_plan import TestPlanValue


@strawberry.type
class SampleOffset:
    """Sample Offset Object Type."""

    id: strawberry.ID
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    start_pos: Optional[float]
    end_pos: Optional[float]


@strawberry.type
class TestResultValue:
    """Test Result Value Object Type."""

    id: strawberry.ID
    test_result_Group_id: strawberry.ID
    test_result_Group_type: Optional[ParamGroupTypeEnum]
    test_result_Group_name: Optional[str]
    test_result_Name: Optional[str]
    test_result_Value: VALUE  # type: ignore
    unit: Optional[str]


@strawberry.type
class TestPlanData:
    """Test Plan data."""

    id: strawberry.ID
    name: Optional[str]
    planned_values: Optional[list[TestPlanValue]]


@strawberry.type
class TestResult:
    """Test Result Object Type."""

    id: strawberry.ID
    name: Optional[str]
    test_id: strawberry.ID  # Test reference
    test: Optional[TestData]
    test_plan_id: strawberry.ID  # Test Plan reference
    test_plan: Optional[TestPlanData]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    test_result_values: Optional[list[TestResultValue]]
    test_plan_time: Optional[datetime]
    start_position: Optional[float]
    end_position: Optional[float]
    status: Optional[TestStatusEnum]
    sensor_offsets: Optional[list[SampleOffset]]
    equipment_offsets: Optional[list[SampleOffset]]
    version: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    created_by: Optional[User]
    modified_by: Optional[User]
