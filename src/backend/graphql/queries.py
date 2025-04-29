"""Queries for the GraphQL API."""

import time
from typing import Optional

import strawberry

from backend.graphql.resolvers.test import get_tests
from backend.graphql.resolvers.test_plan import get_test_plans
from backend.graphql.resolvers.test_result import get_test_results
from backend.graphql.types.common import LogicalFilterInput
from backend.graphql.types.test import Test
from backend.graphql.types.test_plan import TestPlan
from backend.models.test_result import TestResultOutput
from backend.utils.logger import get_logger
from backend.utils.utils import perform_resolving_action, convert_object_ids
import json

logger = get_logger(__name__)


@strawberry.type
class Query:
    """Query class for the GraphQL API."""

    @strawberry.field(graphql_type=list[Test])
    async def tests(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[Test]:
        """Get all tests.
        This function is used to resolve the tests query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[Test]: List of Test objects.
        """
        tests = await perform_resolving_action(
            info, get_tests, filters=filters
        )
        return tests

    @strawberry.field(graphql_type=list[TestPlan])
    async def test_plans(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> strawberry.scalars.JSON:
        """Get all test plans.
        This function is used to resolve the test plans query.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[TestPlan]: List of TestPlan objects.
        """
        return await perform_resolving_action(
            info, get_test_plans, filters=filters
        )

    @strawberry.field()
    async def test_results(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[str]:
        """Get all test results.
        This function is used to resolve the test results query.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[TestResult]: List of TestResult objects.
        """
        start_time = time.perf_counter()
        test_results = await perform_resolving_action(
            info, get_test_results, filters=filters
        )
        logger.info(
            "Fetching and validation completed in "
            f"{time.perf_counter() - start_time} seconds"
        )
        logger.info(f"Test Results: {test_results[0]}")
        return [json.dumps(result) for result in test_results]
