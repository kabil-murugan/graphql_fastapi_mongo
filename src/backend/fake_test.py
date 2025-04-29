from datetime import datetime
from backend.models.test import (
    Test,
    TestType,
    TestStep,
    TestEnvironment,
    TestLog,
)
from backend.db.init_db import init_db

from beanie import PydanticObjectId
from backend.models.test_plan import (
    TestPlan,
    TestPlanValue,
)


from backend.models.test_result import (
    TestResult,
    TestResultValue,
    SampleOffset,
)
from backend.models.common import TestStatus, ParamGroupType, User

import asyncio


async def insert_test_document():
    """Insert a document into the tests collection."""
    await init_db()
    test_document = Test(
        name="Sample Test",
        description="This is a sample test document.",
        test_type=TestType.FUNCTIONAL,
        status=TestStatus.PENDING,
        steps=[
            TestStep(
                step_name="Step 1",
                description="Verify login functionality",
                expected_result="Login successful",
                actual_result=None,
                status=TestStatus.PENDING,
                executed_at=None,
            )
        ],
        environment=TestEnvironment(
            environment_name="Staging",
            os="Windows 10",
            browser="Chrome",
            version="91.0",
            hardware="Intel i7",
        ),
        logs=[
            TestLog(
                timestamp=datetime.utcnow(),
                message="Test created",
                level="INFO",
            )
        ],
        start_time=None,
        end_time=None,
        duration=None,
        version=1,
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        created_by=User(name="Admin", email="admin@example.com"),
        modified_by=User(name="Admin", email="admin@example.com"),
    )

    # Save the document to the database
    await test_document.insert()
    print("Test document inserted successfully.")


async def insert_test_plan_document():
    """Insert a document into the test_plans collection."""
    await init_db()
    test_plan_document = TestPlan(
        name="Sample Test Plan",
        schema_test_plan_condition="Condition for the test plan",
        test_id=PydanticObjectId(
            "680f97aca1449f50466fd209"
        ),  # Replace with a valid test ID
        test_planning_notes="These are the planning notes for the test plan.",
        test_planned_values=[
            TestPlanValue(
                test_plan_group_id=PydanticObjectId(
                    "644a1f4e5f9b2567e8a1c456"
                ),  # Replace with a valid group ID
                test_plan_group_type=ParamGroupType.TYPE_A,
                test_plan_group_name="Group A",
                test_plan_name="Plan A",
                test_plan_value=42.5,
                unit="ms",
            ),
            TestPlanValue(
                test_plan_group_id=PydanticObjectId(
                    "644a1f4e5f9b2567e8a1c789"
                ),  # Replace with a valid group ID
                test_plan_group_type=ParamGroupType.TYPE_B,
                test_plan_group_name="Group B",
                test_plan_name="Plan B",
                test_plan_value="High",
                unit=None,
            ),
        ],
        created_by=User(name="Admin", email="admin@example.com"),
        modified_by=User(name="Admin", email="admin@example.com"),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        version=1,
    )

    await test_plan_document.insert()
    print("Test plan document inserted successfully.")


async def insert_test_result_document():
    """Insert a document into the test_results collection."""
    await init_db()
    test_result_document = TestResult(
        name="Sample Test Result",
        test_id=PydanticObjectId(
            "680f97aca1449f50466fd209"
        ),  # Replace with a valid test ID
        test_plan_id=PydanticObjectId(
            "680f9ad1ce756c388e417cd4"
        ),  # Replace with a valid test plan ID
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow(),
        test_result_values=[
            TestResultValue(
                test_result_group_id=PydanticObjectId(
                    "644a1f4e5f9b2567e8a1c789"
                ),  # Replace with a valid group ID
                test_result_group_type=ParamGroupType.TYPE_A,
                test_result_group_name="Group A",
                test_result_name="Result A",
                test_result_value=95.5,
                unit="ms",
            ),
            TestResultValue(
                test_result_group_id=PydanticObjectId(
                    "644a1f4e5f9b2567e8a1c987"
                ),  # Replace with a valid group ID
                test_result_group_type=ParamGroupType.TYPE_B,
                test_result_group_name="Group B",
                test_result_name="Result B",
                test_result_value="Pass",
                unit=None,
            ),
        ],
        test_plan_time=datetime.utcnow(),
        start_position=0.0,
        end_position=100.0,
        status=TestStatus.COMPLETED,
        sensor_offsets=[
            SampleOffset(
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                start_pos=0.0,
                end_pos=50.0,
            )
        ],
        equipment_offsets=[
            SampleOffset(
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                start_pos=50.0,
                end_pos=100.0,
            )
        ],
        version=1,
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        created_by=User(name="Admin", email="admin@example.com"),
        modified_by=User(name="Admin", email="admin@example.com"),
    )

    # Save the document to the database
    await test_result_document.insert()
    print("Test result document inserted successfully.")


asyncio.run(insert_test_result_document())
