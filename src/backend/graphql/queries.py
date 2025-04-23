"""Queries for the GraphQL API."""

from typing import Optional

import strawberry

from backend.graphql.resolvers.test import get_tests
from backend.graphql.resolvers.test_plan import get_test_plans
from backend.graphql.resolvers.test_result import get_test_results
from backend.graphql.types.common import LogicalFilterInput
from backend.graphql.types.test import Test
from backend.graphql.types.test_plan import TestPlan
from backend.graphql.types.test_result import TestResult
from backend.utils.logger import get_logger
from backend.utils.utils import perform_resolving_action

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
        return await perform_resolving_action(info, get_tests, filters=filters)

    @strawberry.field(graphql_type=list[TestPlan])
    async def test_plans(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[TestPlan]:
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

    @strawberry.field(graphql_type=list[TestResult])
    async def test_results(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[TestResult]:
        """Get all test results.
        This function is used to resolve the test results query.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[TestResult]: List of TestResult objects.
        """
        return await perform_resolving_action(
            info, get_test_results, filters=filters
        )
