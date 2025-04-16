"""Mutations for the GraphQL API."""

from typing import Optional

import strawberry

from backend.graphql.resolvers.order import (
    create_order,
    delete_order,
    update_order,
)
from backend.graphql.resolvers.product import (
    create_product,
    delete_product,
    update_product,
)
from backend.graphql.resolvers.user import (
    create_user,
    delete_user,
    update_user,
)
from backend.graphql.types.order import Order, OrderItemInput, OrderStatus
from backend.graphql.types.product import Product
from backend.graphql.types.user import ProfileInput, User
from backend.models.order import Order as OrderModel
from backend.models.product import Product as ProductModel
from backend.models.user import User as UserModel
from backend.utils.utils import perform_resolving_action


@strawberry.type
class Mutation:
    """Mutation class for the GraphQL API."""

    @strawberry.mutation(graphql_type=User)
    async def create_user(
        self, name: str, email: str, profile: Optional[ProfileInput] = None
    ) -> UserModel:
        """Create a new user.

        Args:
            name (str): The name of the user.
            email (str): The email of the user.
            profile (Optional[ProfileInput], optional): Profile of the user.
            Defaults to None.

        Returns:
            UserModel: UserModel object.
        """
        return await perform_resolving_action(
            None, create_user, name, email, profile
        )

    @strawberry.mutation(graphql_type=User)
    async def update_user(
        self,
        id: strawberry.ID,
        name: Optional[str] = None,
        email: Optional[str] = None,
        profile: Optional[ProfileInput] = None,
    ) -> UserModel:
        """Update an existing user.

        Args:
            id (strawberry.ID): The ID of the user to update.
            name (Optional[str], optional): The new name of the user.
            Defaults to None.
            email (Optional[str], optional): The new email of the user.
            Defaults to None.
            profile (Optional[ProfileInput], optional): The new profile of the
            user. Defaults to None.

        Returns:
            UserModel: Updated UserModel object.
        """
        return await perform_resolving_action(
            None, update_user, id, name, email, profile
        )

    @strawberry.mutation(graphql_type=User)
    async def delete_user(self, id: strawberry.ID) -> UserModel:
        """Delete an existing user.

        Args:
            id (strawberry.ID): The ID of the user to delete.

        Returns:
            UserModel: Deleted UserModel object.
        """
        return await perform_resolving_action(None, delete_user, id)

    @strawberry.mutation(graphql_type=Product)
    async def create_product(
        self,
        name: str,
        price: float,
    ) -> ProductModel:
        """Create a new product.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.

        Returns:
            ProductModel: Created ProductModel object.
        """
        return await perform_resolving_action(
            None, create_product, name, price
        )

    @strawberry.mutation(graphql_type=Product)
    async def update_product(
        self,
        id: strawberry.ID,
        name: Optional[str] = None,
        price: Optional[float] = None,
    ) -> ProductModel:
        """Update an existing product.

        Args:
            id (strawberry.ID): The ID of the product to update.
            name (Optional[str], optional): The new name of the product.
            Defaults to None.
            price (Optional[float], optional): The new price of the product.
            Defaults to None.

        Returns:
            ProductModel: Updated ProductModel object.
        """
        return await perform_resolving_action(
            None, update_product, id, name, price
        )

    @strawberry.mutation(graphql_type=Product)
    async def delete_product(self, id: strawberry.ID) -> ProductModel:
        """Delete an existing product.

        Args:
            id (strawberry.ID): The ID of the product to delete.

        Returns:
            ProductModel: Deleted ProductModel object.
        """
        return await perform_resolving_action(None, delete_product, id)

    @strawberry.mutation(graphql_type=Order)
    async def create_order(
        self,
        user_id: str,
        items: list[OrderItemInput],
        status: OrderStatus,
    ) -> OrderModel:
        """Create a new order.

        Args:
            user_id (str): The ID of the user placing the order.
            items (list[OrderItemInput]): List of items in the order.
            status (OrderStatus): The status of the order.

        Returns:
            OrderModel: Created OrderModel object.
        """
        return await perform_resolving_action(
            None, create_order, user_id, items, status
        )

    @strawberry.mutation(graphql_type=Order)
    async def update_order(
        self,
        id: strawberry.ID,
        user_id: Optional[str] = None,
        items: Optional[list[OrderItemInput]] = None,
        status: Optional[OrderStatus] = None,
    ) -> OrderModel:
        """Update an existing order.

        Args:
            id (strawberry.ID): The ID of the order to update.
            user_id (Optional[str], optional): The new user ID.
            Defaults to None.
            items (Optional[list[OrderItemInput]], optional): The new items in
            the order. Defaults to None.
            status (Optional[OrderStatus], optional): The new status of the
            order. Defaults to None.

        Returns:
            OrderModel: Updated OrderModel object.
        """
        return await perform_resolving_action(
            None, update_order, id, user_id, items, status
        )

    @strawberry.mutation(graphql_type=Order)
    async def delete_order(self, id: strawberry.ID) -> OrderModel:
        """Delete an existing order.

        Args:
            id (strawberry.ID): The ID of the order to delete.

        Returns:
            OrderModel: Deleted OrderModel object.
        """
        return await perform_resolving_action(None, delete_order, id)
