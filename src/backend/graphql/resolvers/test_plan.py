"""Resolvers for user-related GraphQL queries."""

from typing import Any, Optional

from backend.graphql.types.common import LogicalFilterInput
from backend.models.test_plan import TestPlan, TestPlanOutput
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
)

logger = get_logger(__name__)


async def get_test_plans(
    fields: list[Any],
    filters: Optional["LogicalFilterInput"] = None,
) -> list[dict[str, Any]]:
    """Fetch all test plans with specified fields.

    Args:
        fields (list[Any]): List of fields to include in the projection.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        list[TestPlan]: List of TestPlan objects with the specified fields.
    """
    logger.info(f"Fetching all test plans with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = []

    if filters:
        test_filters, test_plan_filters = extract_filters_by_prefixes(
            filters, ["test."]
        )
        test_plan_filter_query = build_query_from_filters(test_plan_filters)
        aggregation_pipeline.append({"$match": test_plan_filter_query})
    else:
        test_filters, test_plan_filters = None, None

    if test_filters or any(f.startswith("test.") for f in projection):
        aggregation_pipeline = build_filter_aggregation_pipeline(
            ("tests", "test_id", "_id", "test"),
            test_filters,
            aggregation_pipeline,
        )
    # aggregation_pipeline.append({"$project": projection})

    logger.info(f"Aggregation pipeline: {aggregation_pipeline}")

    test_plans = (
        await TestPlan.find_all().aggregate(aggregation_pipeline).to_list()
    )
    if test_plans:
        logger.info(f"Test plans fetched: {test_plans[0]}")
    return [
        TestPlanOutput.model_validate(test_plan) for test_plan in test_plans
    ]
