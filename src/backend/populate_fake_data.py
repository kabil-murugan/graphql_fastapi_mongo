"""Populate fake data into MongoDB for testing purposes."""

import asyncio
from faker import Faker
from bson import ObjectId
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = AsyncIOMotorClient(
    "mongodb://kabilm10:kabilm1012@localhost:27017"
)
db = client["PI_test_database"]

fake = Faker()


async def seed_tests():
    """Seed the Test collection."""
    tests = []
    for _ in range(500):
        tests.append(
            {
                "name": fake.word(),
                "description": fake.text(max_nb_chars=200),
                "test_type": fake.random_element(
                    [
                        "FUNCTIONAL",
                        "PERFORMANCE",
                        "INTEGRATION",
                        "REGRESSION",
                        "UNIT",
                    ]
                ),
                "status": fake.random_element(
                    [
                        "PENDING",
                        "IN_PROGRESS",
                        "COMPLETED",
                        "FAILED",
                        "CANCELLED",
                    ]
                ),
                "steps": [
                    {
                        "id": ObjectId(),
                        "step_name": fake.sentence(),
                        "description": fake.text(max_nb_chars=100),
                        "expected_result": fake.sentence(),
                        "actual_result": None,
                        "status": fake.random_element(
                            [
                                "PENDING",
                                "IN_PROGRESS",
                                "COMPLETED",
                                "FAILED",
                                "CANCELLED",
                            ]
                        ),
                        "executed_at": datetime.now(timezone.utc),
                    }
                ],
                "environment": {
                    "environment_name": fake.word(),
                    "os": fake.random_element(["Windows", "Linux", "macOS"]),
                    "browser": fake.random_element(
                        ["Chrome", "Firefox", "Safari"]
                    ),
                    "version": fake.random_element(["91.0", "92.0", "93.0"]),
                    "hardware": fake.word(),
                },
                "logs": [
                    {
                        "timestamp": datetime.now(timezone.utc),
                        "message": fake.sentence(),
                        "level": fake.random_element(
                            ["INFO", "WARNING", "ERROR"]
                        ),
                    }
                ],
                "start_time": datetime.now(timezone.utc),
                "end_time": datetime.now(timezone.utc),
                "duration": fake.random_int(min=1, max=100),
                "version": 1,
                "created_at": datetime.now(timezone.utc),
                "modified_at": datetime.now(timezone.utc),
                "created_by": {"name": fake.name(), "email": fake.email()},
                "modified_by": {"name": fake.name(), "email": fake.email()},
            }
        )
    await db.tests.insert_many(tests)
    print("Seeded 500 tests.")

    # Fetch all test IDs after insertion
    test_ids = await db.tests.find({}, {"_id": 1}).to_list(length=None)
    return [ObjectId(test["_id"]) for test in test_ids]


async def seed_test_plans(test_ids):
    """Seed the TestPlan collection."""
    test_plans = []
    for _ in range(500):
        test_planned_values = []
        for _ in range(1500):
            test_planned_values.append(
                {
                    "id": ObjectId(),
                    "test_plan_group_id": ObjectId(),
                    "test_plan_group_type": fake.random_element(
                        ["TYPE_A", "TYPE_B", "TYPE_C"]
                    ),
                    "test_plan_group_name": fake.word(),
                    "test_plan_name": fake.word(),
                    "test_plan_value": fake.random_element(
                        [
                            fake.random_int(min=1, max=100),
                            fake.random_digit(),
                        ]
                    ),
                    "unit": fake.word(),
                }
            )

        test_plans.append(
            {
                "name": fake.word(),
                "schema_test_plan_condition": fake.sentence(),
                "test_id": fake.random_element(test_ids),
                "test_planning_notes": fake.text(max_nb_chars=200),
                "test_planned_values": test_planned_values,
                "created_by": {"name": fake.name(), "email": fake.email()},
                "modified_by": {"name": fake.name(), "email": fake.email()},
                "created_at": datetime.now(timezone.utc),
                "modified_at": datetime.now(timezone.utc),
                "version": 1,
            }
        )
    await db.test_plans.insert_many(test_plans)
    print("Seeded 500 test plans.")

    # Fetch all test plan IDs after insertion
    test_plan_ids = await db.test_plans.find({}, {"_id": 1}).to_list(
        length=None
    )
    return [ObjectId(test_plan["_id"]) for test_plan in test_plan_ids]


async def seed_test_results(test_ids, test_plan_ids):
    """Seed the TestResult collection."""
    test_results = []
    for _ in range(500):
        test_result_values = []
        for _ in range(2500):
            test_result_values.append(
                {
                    "id": ObjectId(),
                    "test_result_group_id": ObjectId(),
                    "test_result_group_type": fake.random_element(
                        ["TYPE_A", "TYPE_B", "TYPE_C"]
                    ),
                    "test_result_group_name": fake.word(),
                    "test_result_name": fake.word(),
                    "test_result_value": fake.random_element(
                        [
                            fake.random_int(min=1, max=100),
                            fake.random_digit(),
                        ]
                    ),
                    "unit": fake.word(),
                }
            )

        test_results.append(
            {
                "name": fake.word(),
                "test_id": fake.random_element(test_ids),
                "test_plan_id": fake.random_element(test_plan_ids),
                "start_time": datetime.now(timezone.utc),
                "end_time": datetime.now(timezone.utc),
                "test_result_values": test_result_values,
                "test_plan_time": datetime.now(timezone.utc),
                "start_position": fake.random_digit(),
                "end_position": fake.random_digit(),
                "status": fake.random_element(
                    [
                        "PENDING",
                        "IN_PROGRESS",
                        "COMPLETED",
                        "FAILED",
                        "CANCELLED",
                    ]
                ),
                "sensor_offsets": [
                    {
                        "id": ObjectId(),
                        "start_time": datetime.now(timezone.utc),
                        "end_time": datetime.now(timezone.utc),
                        "start_pos": fake.random_digit(),
                        "end_pos": fake.random_digit(),
                    }
                ],
                "equipment_offsets": [
                    {
                        "id": ObjectId(),
                        "start_time": datetime.now(timezone.utc),
                        "end_time": datetime.now(timezone.utc),
                        "start_pos": fake.random_digit(),
                        "end_pos": fake.random_digit(),
                    }
                ],
                "version": 1,
                "created_at": datetime.now(timezone.utc),
                "modified_at": datetime.now(timezone.utc),
                "created_by": {"name": fake.name(), "email": fake.email()},
                "modified_by": {"name": fake.name(), "email": fake.email()},
            }
        )
    await db.test_results.insert_many(test_results)
    print("Seeded 500 test results.")


async def main():
    test_ids = await seed_tests()
    print(f"Test IDs: {test_ids[0]}")
    test_plan_ids = await seed_test_plans(test_ids)
    print(f"Test Plan IDs: {test_plan_ids[0]}")
    await seed_test_results(test_ids, test_plan_ids)
    print("Database seeding completed.")


if __name__ == "__main__":
    asyncio.run(main())
