"""An endpoint for fetching test results for Performance comparison."""

from fastapi import APIRouter

from backend.models.test_result import TestResult, TestResultOutput

router: APIRouter = APIRouter()


@router.get("/test-results")
async def get_test_results_endpoint():
    """
    FastAPI endpoint to fetch test results.
    This replicates the functionality of the GraphQL query.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "tests",
                "localField": "test_id",
                "foreignField": "_id",
                "as": "test",
            }
        },
        {"$unwind": {"path": "$test"}},
        {
            "$lookup": {
                "from": "test_plans",
                "localField": "test_plan_id",
                "foreignField": "_id",
                "as": "test_plan",
            }
        },
        {"$unwind": {"path": "$test_plan"}},
        {
            "$project": {
                "test_id": 1,
                "test_plan_id": 1,
                "test._id": 1,
                "test_plan._id": 1,
                "id": 1,
                "name": 1,
                "status": 1,
                "test_plan.id": 1,
                "test_plan.name": 1,
                "test_plan.test_planned_values.test_plan_name": 1,
                "sensor_offsets.id": 1,
                "sensor_offsets.start_pos": 1,
                "equipment_offsets.id": 1,
                "equipment_offsets.start_pos": 1,
                "equipment_offsets.end_pos": 1,
                "created_by.name": 1,
                "created_by.email": 1,
                "modified_by.name": 1,
                "modified_by.email": 1,
            }
        },
    ]
    test_results = await TestResult.find_all().aggregate(pipeline).to_list()
    # print(f"Test Result Values: {test_results[0]}")
    return [TestResultOutput.model_validate(test) for test in test_results]
