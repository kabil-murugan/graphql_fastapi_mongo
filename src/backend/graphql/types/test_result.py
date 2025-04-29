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

    id: Optional[strawberry.ID]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    start_pos: Optional[float]
    end_pos: Optional[float]


@strawberry.type
class TestResultValue:
    """Test Result Value Object Type."""

    id: Optional[strawberry.ID]
    test_result_group_id: Optional[strawberry.ID]
    test_result_group_type: Optional[ParamGroupTypeEnum]
    test_result_group_name: Optional[str]
    test_result_name: Optional[str]
    test_result_value: VALUE  # type: ignore
    unit: Optional[str]


@strawberry.type
class TestPlanData:
    """Test Plan data."""

    id: Optional[strawberry.ID]
    name: Optional[str]
    test_planned_values: Optional[list[TestPlanValue]]


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

    # @classmethod
    # def create_test_result_instance(cls, data: dict) -> "TestResult":
    #     """
    #     Converts a dictionary into a TestResult instance.
    #     If any field is missing in the data, it is set to None.

    #     Args:
    #         data (dict): The input dictionary.

    #     Returns:
    #         TestResult: An instance of TestResult.
    #     """
    #     return cls(
    #         id=data.get("_id"),
    #         name=data.get("name"),
    #         test_id=data.get("test_id"),
    #         test=(
    #             TestData(
    #                 id=data["test"].get("_id"), name=data["test"].get("name")
    #             )
    #             if data.get("test")
    #             else None
    #         ),
    #         test_plan_id=data.get("test_plan_id"),
    #         test_plan=(
    #             TestPlanData(
    #                 id=data["test_plan"].get("_id"),
    #                 name=data["test_plan"].get("name"),
    #                 test_planned_values=(
    #                     [
    #                         TestPlanValue(
    #                             id=value.get("id"),
    #                             test_plan_group_id=value.get(
    #                                 "test_plan_group_id"
    #                             ),
    #                             test_plan_group_type=(
    #                                 ParamGroupTypeEnum(
    #                                     value.get("test_plan_group_type")
    #                                 )
    #                                 if value.get("test_plan_group_type")
    #                                 else None
    #                             ),
    #                             test_plan_group_name=value.get(
    #                                 "test_plan_group_name"
    #                             ),
    #                             test_plan_name=value.get("test_plan_name"),
    #                             test_plan_value=value.get("test_plan_value"),
    #                             unit=value.get("unit"),
    #                         )
    #                         for value in data["test_plan"].get(
    #                             "test_planned_values", []
    #                         )
    #                     ]
    #                     if data["test_plan"].get("test_planned_values")
    #                     else None
    #                 ),
    #             )
    #             if data.get("test_plan")
    #             else None
    #         ),
    #         start_time=data.get("start_time"),
    #         end_time=data.get("end_time"),
    #         test_result_values=(
    #             [
    #                 TestResultValue(
    #                     id=value.get("_id"),
    #                     test_result_group_id=value.get("test_result_group_id"),
    #                     test_result_group_type=(
    #                         ParamGroupTypeEnum(
    #                             value.get("test_result_group_type")
    #                         )
    #                         if value.get("test_result_group_type")
    #                         else None
    #                     ),
    #                     test_result_group_name=value.get(
    #                         "test_result_group_name"
    #                     ),
    #                     test_result_name=value.get("test_result_name"),
    #                     test_result_value=value.get("test_result_value"),
    #                     unit=value.get("unit"),
    #                 )
    #                 for value in data.get("test_result_values", [])
    #             ]
    #             if data.get("test_result_values")
    #             else None
    #         ),
    #         test_plan_time=data.get("test_plan_time"),
    #         start_position=data.get("start_position"),
    #         end_position=data.get("end_position"),
    #         status=(TestStatusEnum(data.get("status"))),
    #         sensor_offsets=(
    #             [
    #                 SampleOffset(
    #                     id=offset.get("id"),
    #                     start_time=offset.get("start_time"),
    #                     end_time=offset.get("end_time"),
    #                     start_pos=offset.get("start_pos"),
    #                     end_pos=offset.get("end_pos"),
    #                 )
    #                 for offset in data.get("sensor_offsets", [])
    #             ]
    #             if data.get("sensor_offsets")
    #             else None
    #         ),
    #         equipment_offsets=(
    #             [
    #                 SampleOffset(
    #                     id=offset.get("id"),
    #                     start_time=offset.get("start_time"),
    #                     end_time=offset.get("end_time"),
    #                     start_pos=offset.get("start_pos"),
    #                     end_pos=offset.get("end_pos"),
    #                 )
    #                 for offset in data.get("equipment_offsets", [])
    #             ]
    #             if data.get("equipment_offsets")
    #             else None
    #         ),
    #         version=data.get("version"),
    #         created_at=data.get("created_at"),
    #         modified_at=data.get("modified_at"),
    #         created_by=(
    #             User(
    #                 name=data["created_by"].get("name"),
    #                 email=data["created_by"].get("email"),
    #             )
    #             if data.get("created_by")
    #             else None
    #         ),
    #         modified_by=(
    #             User(
    #                 name=data["modified_by"].get("name"),
    #                 email=data["modified_by"].get("email"),
    #             )
    #             if data.get("modified_by")
    #             else None
    #         ),
    #     )
