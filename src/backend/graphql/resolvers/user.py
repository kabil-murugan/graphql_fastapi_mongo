"""Resolvers for user-related GraphQL queries."""

from typing import TYPE_CHECKING, Any, Optional

import strawberry
from bson import ObjectId
from strawberry.dataloader import DataLoader

from backend.models.order import Order
from backend.models.user import Profile, User
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
)

if TYPE_CHECKING:
    from backend.graphql.types.filter import LogicalFilterInput
    from backend.graphql.types.user import ProfileInput
    from backend.graphql.types.user import User as UserType


logger = get_logger(__name__)


async def get_users(
    fields: list[Any],
    user_loader: DataLoader,
    filters: Optional["LogicalFilterInput"] = None,
) -> list[User]:
    logger.info(f"Fetching all users with fields: {fields}")

    if filters:
        product_filters, order_filters, user_filters = (
            extract_filters_by_prefixes(
                filters, ["orders.items.product.", "orders."]
            )
        )
        user_filter_query = build_query_from_filters(user_filters)
        aggregation_pipeline = [
            {"$match": user_filter_query},
            {"$project": build_projection(fields)},
        ]
        if order_filters or product_filters:
            aggregation_pipeline = build_filter_aggregation_pipeline(
                ("orders", "_id", "user_id", "orders"),
                order_filters,
                aggregation_pipeline,
            )
            if product_filters:
                aggregation_pipeline = build_filter_aggregation_pipeline(
                    ("products", "orders.items.product_id", "_id", "products"),
                    product_filters,
                    aggregation_pipeline,
                )
    else:
        aggregation_pipeline = [
            {"$project": build_projection(fields)},
        ]

    users = await User.find_all().aggregate(aggregation_pipeline).to_list()
    user_loader.prime_many({str(user["_id"]): user for user in users})
    logger.info("Primed users in DataLoader")
    return [User.model_validate(user) for user in users]


async def get_user_by_id(
    id: strawberry.ID, fields: list[Any], user_loader: DataLoader
) -> User:
    user_data = await user_loader.load((str(id), fields))
    if not user_data:
        raise ValueError(f"User with ID {id} not found.")
    return User.model_validate(user_data)


async def get_user_orders(user: "UserType", fields: list[Any]) -> list[Order]:
    """Fetch all orders for a user with specified fields.

    Args:
        user (UserType): The user object for which to fetch orders.
        fields (list[Any]): fields to include in the projection.

    Returns:
        list[Order]: List of Order objects with the specified fields.
    """
    logger.info(
        f"Fetching orders for user ID: {user.id} with fields: {fields}"
    )
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    orders = (
        await Order.find(Order.user_id == ObjectId(user.id))
        .aggregate(aggregation_pipeline)
        .to_list()
    )
    return [Order.model_validate(order) for order in orders]


async def create_user(
    name: str,
    email: str,
    profile: Optional["ProfileInput"] = None,
) -> User:
    """Create a new user.

    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        profile (Optional[dict], optional): The profile of the user.
        Defaults to None.

    Returns:
        User: The created User object.
    """
    logger.info(f"Creating user with name: {name}, email: {email}")
    user = User(name=name, email=email, profile=profile)
    await user.insert()
    return user


async def update_user(
    user_loader: DataLoader,
    id: strawberry.ID,
    name: Optional[str] = None,
    email: Optional[str] = None,
    profile: Optional["ProfileInput"] = None,
) -> User:
    logger.info(f"Updating user with ID: {id}")
    user = await get_user_by_id(
        id, ["name", "email", {"profile": ["age", "location"]}], user_loader
    )
    if name:
        user.name = name
    if email:
        user.email = email
    if profile:
        user.profile = Profile(age=profile.age, location=profile.location)
    await user.save()
    return user


async def delete_user(user_loader: DataLoader, id: strawberry.ID) -> User:
    """Delete a user by ID.

    Args:
        id (strawberry.ID): The ID of the user to delete.

    Returns:
        User: The deleted User object.
    """
    logger.info(f"Deleting user with ID: {id}")
    user = await get_user_by_id(
        id, ["name", "email", {"profile": ["age", "location"]}], user_loader
    )
    await user.delete()
    return user
