"""Resolvers for user-related GraphQL queries."""

from typing import TYPE_CHECKING, Any, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.order import Order
from backend.models.user import Profile, User
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection

if TYPE_CHECKING:
    from backend.graphql.types.user import ProfileInput
    from backend.graphql.types.user import User as UserType


logger = get_logger(__name__)


async def get_users(fields: list[Any]) -> list[User]:
    """Fetch all users with specified fields.

    Args:
        fields (list[Any]): fields to include in the projection.

    Returns:
        list[User]: List of User objects with the specified fields.
    """
    logger.info(f"Fetching all users with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    users = await User.find_all().aggregate(aggregation_pipeline).to_list()
    return [User.model_validate(user) for user in users]


async def get_user_by_id(id: strawberry.ID, fields: list[Any]) -> User:
    """Fetch a user by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the user to fetch.
        fields (list[Any]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid or the user is not found.

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
    raise ValueError(f"User with ID {id} not found.")


async def get_user_orders(user: "UserType", fields: list[Any]) -> list[Order]:
    """Fetch all orders for a user with specified fields.

    Args:
        user (UserType): The user object for which to fetch orders.
        fields (list[Any]): fields to include in the projection.

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
    id: strawberry.ID,
    name: Optional[str] = None,
    email: Optional[str] = None,
    profile: Optional["ProfileInput"] = None,
) -> User:
    """Update an existing user.

    Args:
        id (strawberry.ID): The ID of the user to update.
        name (Optional[str], optional): The name to update. Defaults to None.
        email (Optional[str], optional): The email to update. Defaults to None.
        profile (Optional[&quot;ProfileInput&quot;], optional): The profile of
        the user to update. Defaults to None.

    Returns:
        User: The updated User object.
    """
    logger.info(f"Updating user with ID: {id}")
    user = await get_user_by_id(
        id, ["name", "email", {"profile": ["age", "location"]}]
    )
    if name:
        user.name = name
    if email:
        user.email = email
    if profile:
        user.profile = Profile(age=profile.age, location=profile.location)
    await user.save()
    return user


async def delete_user(id: strawberry.ID) -> User:
    """Delete a user by ID.

    Args:
        id (strawberry.ID): The ID of the user to delete.

    Returns:
        User: The deleted User object.
    """
    logger.info(f"Deleting user with ID: {id}")
    user = await get_user_by_id(
        id, ["name", "email", {"profile": ["age", "location"]}]
    )
    await user.delete()
    return user
