"""Queries for the GraphQL API."""

from typing import Optional

import strawberry

from backend.graphql.resolvers.order import get_order_by_id, get_orders
from backend.graphql.resolvers.product import get_product_by_id, get_products
from backend.graphql.resolvers.review import get_reviews
from backend.graphql.resolvers.user import get_user_by_id, get_users
from backend.graphql.types.filter import LogicalFilterInput
from backend.graphql.types.order import Order
from backend.graphql.types.product import Product
from backend.graphql.types.review import Review
from backend.graphql.types.user import User
from backend.models.order import Order as OrderModel
from backend.models.product import Product as ProductModel
from backend.models.review import Review as ReviewModel
from backend.models.user import User as UserModel
from backend.utils.logger import get_logger
from backend.utils.utils import perform_resolving_action

logger = get_logger(__name__)


@strawberry.type
class Query:
    """Query class for the GraphQL API."""

    @strawberry.field(graphql_type=list[User])
    async def users(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[UserModel]:
        """Get all users.
        This function is used to resolve the users query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[UserModel]: List of UserModel objects.
        """
        return await perform_resolving_action(info, get_users, filters=filters)

    @strawberry.field(graphql_type=list[Order])
    async def orders(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[OrderModel]:
        """Get all orders.
        This function is used to resolve the orders query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[OrderModel]: List of OrderModel objects.
        """
        return await perform_resolving_action(
            info, get_orders, filters=filters
        )

    @strawberry.field(graphql_type=list[Product])
    async def products(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[ProductModel]:
        """Get all products.
        This function is used to resolve the products query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[ProductModel]: List of ProductModel objects.
        """
        return await perform_resolving_action(
            info, get_products, filters=filters
        )

    @strawberry.field(graphql_type=list[Review])
    async def reviews(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[ReviewModel]:
        """Get all reviews.
        This function is used to resolve the reviews query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            filters (Optional[LogicalFilterInput]): Filters to apply.

        Returns:
            list[ReviewModel]: List of ReviewModel objects.
        """
        return await perform_resolving_action(
            info, get_reviews, filters=filters
        )

    @strawberry.field(graphql_type=User)
    async def user(
        self,
        info: strawberry.Info,
        id: strawberry.ID,
    ) -> UserModel:
        """Get a user by ID.
        This function is used to resolve the user query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            id (strawberry.ID): ID of the user to retrieve.

        Returns:
            UserModel: UserModel object.
        """
        return await perform_resolving_action(info, get_user_by_id, id)

    @strawberry.field(graphql_type=Order)
    async def order(
        self, info: strawberry.Info, id: strawberry.ID
    ) -> OrderModel:
        """Get an order by ID.

        Args:
            info (strawberry.Info): GraphQL info object.
            id (strawberry.ID): ID of the order to retrieve.

        Returns:
            OrderModel: OrderModel object.
        """
        return await perform_resolving_action(info, get_order_by_id, id)

    @strawberry.field(graphql_type=Product)
    async def product(
        self, info: strawberry.Info, id: strawberry.ID
    ) -> ProductModel:
        """Get a product by ID.
        This function is used to resolve the product query in the GraphQL API.

        Args:
            info (strawberry.Info): GraphQL info object.
            id (strawberry.ID): ID of the product to retrieve.

        Returns:
            ProductModel: ProductModel object.
        """
        return await perform_resolving_action(info, get_product_by_id, id)
