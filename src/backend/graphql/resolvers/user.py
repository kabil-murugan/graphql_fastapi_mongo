"""Resolvers for user-related GraphQL queries."""

from typing import TYPE_CHECKING, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.order import Order
from backend.models.user import User
from backend.utils.utils import build_projection

if TYPE_CHECKING:
    from backend.graphql.types.user import User as UserType

from backend.utils.logger import get_logger

logger = get_logger(__name__)


async def get_users(fields: list) -> list[User]:
    """Fetch all users with specified fields.

    Args:
        fields (list): fields to include in the projection.

    Returns:
        list[User]: List of User objects with the specified fields.
    """
    logger.info(f"Fetching all users with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    users = await User.find_all().aggregate(aggregation_pipeline).to_list()
    return [User.model_validate(user) for user in users]


async def get_user_by_id(
    id: strawberry.ID, fields: list[str]
) -> Optional[User]:
    """Fetch a user by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the user to fetch.
        fields (list[str]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid.

    Returns:
        Optional[User]: The User object with the specified ID and fields,
        or None if not found.
    """
    logger.info(f"Fetching user with ID: {id} and fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    try:
        users = (
            await User.find({"_id": ObjectId(id)})
            .aggregate(aggregation_pipeline)
            .to_list()
        )
    except InvalidId:
        raise ValueError(f"Invalid ID format: {id}. Check it and try again.")
    if users:
        return User.model_validate(users[0])
    return None


async def get_user_orders(user: "UserType", fields: list) -> list[Order]:
    """Fetch all orders for a user with specified fields.

    Args:
        user (UserType): The user object for which to fetch orders.
        fields (list): fields to include in the projection.

    Returns:
        list[Order]: List of Order objects with the specified fields.
    """
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    orders = (
        await Order.find(Order.user_id == str(user.id))
        .aggregate(aggregation_pipeline)
        .to_list()
    )
    return [Order.model_validate(order) for order in orders]
