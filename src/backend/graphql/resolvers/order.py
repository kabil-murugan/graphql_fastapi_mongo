"""Resolvers for Order related GraphQL queries."""

from typing import Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.order import Order
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection

logger = get_logger(__name__)


async def get_orders(fields: list[str]) -> list[Order]:
    """Fetch all orders with specified fields.

    Args:
        fields (list[str]): List of fields to include in the projection.

    Returns:
        list[Order]: List of Order objects with the specified fields.
    """
    logger.info(f"Fetching all orders with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [
        {"$project": projection},
    ]
    orders = await Order.find_all().aggregate(aggregation_pipeline).to_list()
    return [Order.model_validate(order) for order in orders]


async def get_order_by_id(
    id: strawberry.ID, fields: list[str]
) -> Optional[Order]:
    """Fetch an order by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the order to fetch.
        fields (list[str]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid.

    Returns:
        Optional[Order]: The Order object with the specified ID and fields,
        or None if not found.
    """
    logger.info(f"Fetching order with ID: {id} and fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [
        {"$project": projection},
    ]
    try:
        order = (
            await Order.find({"_id": ObjectId(id)})
            .aggregate(aggregation_pipeline)
            .to_list()
        )
    except InvalidId:
        raise ValueError(f"Invalid ID format: {id}. Check it and try again.")
    if order:
        return Order.model_validate(order[0])
    return None
