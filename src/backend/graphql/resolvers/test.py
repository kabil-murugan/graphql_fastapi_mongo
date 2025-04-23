"""Resolvers for test-related GraphQL queries."""

from typing import TYPE_CHECKING, Any, Optional

from backend.models.test import Test
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_projection,
    build_query_from_filters,
)

if TYPE_CHECKING:
    from backend.graphql.types.common import LogicalFilterInput

logger = get_logger(__name__)


async def get_tests(
    fields: list[Any], filters: Optional["LogicalFilterInput"] = None
) -> list[Test]:
    """Fetch all tests with specified fields and apply filter logic.

    Args:
        fields (list[Any]): Fields to include in the projection.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        list[Test]: List of Test objects with the specified fields.
    """
    logger.info(f"Fetching all tests with fields: {fields}")

    aggregation_pipeline = [{"$project": build_projection(fields)}]

    if filters:
        test_filter_query = build_query_from_filters(filters)
        aggregation_pipeline.append({"$match": test_filter_query})
    tests = await Test.find_all().aggregate(aggregation_pipeline).to_list()
    logger.info(f"Pipeline: {aggregation_pipeline}")
    return [Test.model_validate(test) for test in tests]
