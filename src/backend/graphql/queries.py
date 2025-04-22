"""Queries for the GraphQL API."""

from typing import Optional

import strawberry

from backend.graphql.resolvers.order import get_order_by_id, get_orders
from backend.graphql.resolvers.product import get_product_by_id, get_products
from backend.graphql.resolvers.user import get_user_by_id, get_users
from backend.graphql.types.filter import LogicalFilterInput
from backend.graphql.types.order import Order, OrderItem, OrderStatus
from backend.graphql.types.product import Product
from backend.graphql.types.user import User, Profile
from backend.models.order import Order as OrderModel
from backend.models.product import Product as ProductModel
from backend.models.user import User as UserModel
from backend.utils.logger import get_logger
from backend.utils.utils import extract_fields, perform_resolving_action

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
        return await get_users(
            extract_fields(info), info.context["user_loader"], filters=filters
        )

    @strawberry.field(graphql_type=list[Order])
    async def orders(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[Order]:
        orders = await get_orders(
            extract_fields(info), info.context["order_loader"], filters=filters
        )
        return [
            Order(
                id=data.get("_id"),
                user_id=data.get("user_id"),
                items=(
                    [
                        OrderItem(
                            product_id=item.get("product_id"),
                            quantity=item.get("quantity"),
                            product=(
                                Product(
                                    id=product.get("_id"),
                                    name=product.get("name"),
                                    price=product.get("price"),
                                )
                                if (
                                    product := next(
                                        (
                                            p
                                            for p in data.get("products", [])
                                            if p["_id"]
                                            == item.get("product_id")
                                        ),
                                        None,
                                    )
                                )
                                else None
                            ),
                        )
                        for item in data.get("items", [])
                    ]
                    if data.get("items")
                    else None
                ),
                status=(
                    OrderStatus(data.get("status"))
                    if data.get("status")
                    else None
                ),
                user=(
                    User(
                        id=user.get("_id"),
                        name=user.get("name"),
                        email=user.get("email"),
                        profile=(
                            Profile(
                                age=user.get("profile", {}).get("age"),
                                location=user.get("profile", {}).get(
                                    "location"
                                ),
                            )
                            if user.get("profile")
                            else None
                        ),
                    )
                    if (user := next(iter(data.get("users", [])), None))
                    else None
                ),
            )
            for data in orders
        ]

    @strawberry.field(graphql_type=list[Product])
    async def products(
        self,
        info: strawberry.Info,
        filters: Optional[LogicalFilterInput] = None,
    ) -> list[ProductModel]:
        return await get_products(
            extract_fields(info),
            info.context["product_loader"],
            filters=filters,
        )

    @strawberry.field(graphql_type=User)
    async def user(
        self, info: strawberry.Info, id: strawberry.ID
    ) -> UserModel:
        fields = extract_fields(info)
        return await get_user_by_id(id, fields, info.context["user_loader"])

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
