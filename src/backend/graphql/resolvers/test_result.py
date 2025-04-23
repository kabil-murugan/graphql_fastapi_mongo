"""Resolvers for test result-related GraphQL queries."""

from typing import Any, Optional

from backend.graphql.types.filter import LogicalFilterInput
from backend.models.test_result import TestResult
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
)

logger = get_logger(__name__)


async def get_test_results(
    fields: list[Any],
    filters: Optional["LogicalFilterInput"] = None,
) -> list[dict[str, Any]]:
    """Fetch all test results with specified fields.

    Args:
        fields (list[Any]): List of fields to include in the projection.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        list[TestResult]: List of TestResult objects with the specified fields.
    """
    logger.info(f"Fetching all test results with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]

    if filters:
        (
            test_filters,
            test_plan_filters,
            test_result_filters,
        ) = extract_filters_by_prefixes(filters, ["test.", "test_plan.", ""])
        test_result_filter_query = build_query_from_filters(
            test_result_filters
        )
        aggregation_pipeline.append({"$match": test_result_filter_query})
    else:
        test_filters, test_plan_filters, test_result_filters = (
            None,
            None,
            None,
        )

    if test_filters or any(
        filter.startswith("test.") for filter in projection
    ):
        aggregation_pipeline = build_filter_aggregation_pipeline(
            ("tests", "test_id", "_id", "tests"),
            test_filters,
            aggregation_pipeline,
        )

    if test_plan_filters or any(
        filter.startswith("test_plan.") for filter in projection
    ):
        aggregation_pipeline = build_filter_aggregation_pipeline(
            ("test_plans", "test_plan_id", "_id", "test_plans"),
            test_plan_filters,
            aggregation_pipeline,
        )

    logger.info(f"Aggregation pipeline: {aggregation_pipeline}")
    test_results = (
        await TestResult.find_all().aggregate(aggregation_pipeline).to_list()
    )
    return test_results
