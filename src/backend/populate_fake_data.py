"""Populate fake data into MongoDB for testing purposes."""

import asyncio
from faker import Faker
from bson import ObjectId
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = AsyncIOMotorClient(
    "mongodb://kabil1012:kabilm2003@localhost:27017"
)
db = client["PI_test_database"]

fake = Faker()


async def seed_tests():
    """Seed the Test collection."""
    tests = []
    for _ in range(1000):
        tests.append(
            {
                "_id": ObjectId(),
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
                        "_id": ObjectId(),
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
    print("Seeded 1,000 tests.")
    return [test["_id"] for test in tests]


async def seed_test_plans(test_ids):
    """Seed the TestPlan collection."""
    test_plans = []
    for _ in range(1000):
        test_plans.append(
            {
                "_id": ObjectId(),
                "name": fake.word(),
                "schema_test_plan_condition": fake.sentence(),
                "test_id": fake.random_element(test_ids),
                "test_planning_notes": fake.text(max_nb_chars=200),
                "test_planned_values": [
                    {
                        "_id": ObjectId(),
                        "test_plan_Group_id": ObjectId(),
                        "test_plan_Group_type": fake.random_element(
                            ["TYPE_A", "TYPE_B", "TYPE_C"]
                        ),
                        "test_plan_Group_name": fake.word(),
                        "test_plan_Name": fake.word(),
                        "test_plan_Value": fake.random_element(
                            [
                                fake.random_int(min=1, max=100),
                                fake.random_digit(),
                            ]
                        ),
                        "unit": fake.word(),
                    }
                ],
                "created_by": {"name": fake.name(), "email": fake.email()},
                "modified_by": {"name": fake.name(), "email": fake.email()},
                "created_at": datetime.now(timezone.utc),
                "modified_at": datetime.now(timezone.utc),
                "version": 1,
            }
        )
    await db.test_plans.insert_many(test_plans)
    print("Seeded 1,000 test plans.")
    return [test_plan["_id"] for test_plan in test_plans]


async def seed_test_results(test_ids, test_plan_ids):
    """Seed the TestResult collection."""
    test_results = []
    for _ in range(1000):
        test_results.append(
            {
                "_id": ObjectId(),
                "name": fake.word(),
                "test_id": fake.random_element(test_ids),
                "test_plan_id": fake.random_element(test_plan_ids),
                "start_time": datetime.now(timezone.utc),
                "end_time": datetime.now(timezone.utc),
                "test_result_values": [
                    {
                        "_id": ObjectId(),
                        "test_result_Group_id": ObjectId(),
                        "test_result_Group_type": fake.random_element(
                            ["TYPE_A", "TYPE_B", "TYPE_C"]
                        ),
                        "test_result_Group_name": fake.word(),
                        "test_result_Name": fake.word(),
                        "test_result_Value": fake.random_element(
                            [
                                fake.random_int(min=1, max=100),
                                fake.random_digit(),
                            ]
                        ),
                        "unit": fake.word(),
                    }
                ],
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
                        "_id": ObjectId(),
                        "start_time": datetime.now(timezone.utc),
                        "end_time": datetime.now(timezone.utc),
                        "start_pos": fake.random_digit(),
                        "end_pos": fake.random_digit(),
                    }
                ],
                "equipment_offsets": [
                    {
                        "_id": ObjectId(),
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
    print("Seeded 1,000 test results.")


async def main():
    test_ids = await seed_tests()
    test_plan_ids = await seed_test_plans(test_ids)
    await seed_test_results(test_ids, test_plan_ids)
    print("Database seeding completed.")


if __name__ == "__main__":
    asyncio.run(main())
