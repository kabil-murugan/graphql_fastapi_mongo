"""Resolvers for Order related GraphQL queries."""

from typing import Optional
import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.order import Order, OrderItem
from backend.models.order import OrderStatus as OrderStatusModel
from backend.graphql.types.order import OrderStatus, OrderItemInput
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection, validate_id

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


async def get_order_by_id(id: strawberry.ID, fields: list[str]) -> Order:
    """Fetch an order by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the order to fetch.
        fields (list[str]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid or the order is not found.

    Returns:
        Order: The Order object with the specified ID and fields.
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
    raise ValueError(f"Order with ID {id} not found.")


async def create_order(
    user_id: str, items: list[OrderItemInput], status: OrderStatus
) -> Order:
    """Create a new order.

    Args:
        user_id (str): The ID of the user placing the order.
        items (list[OrderItemInput]): List of items in the order.
        status (OrderStatus): The status of the order.

    Returns:
        Order: The created Order object.
    """
    logger.info(f"Creating order for user {user_id}")
    if validate_id(user_id) and all(
        [validate_id(item.product_id) for item in items]
    ):
        order = Order(user_id=user_id, items=items, status=status)
        await order.insert()
        return order
    raise


async def update_order(
    id: strawberry.ID,
    user_id: Optional[str] = None,
    items: Optional[list[OrderItemInput]] = None,
    status: Optional[OrderStatus] = None,
) -> Order:
    """Update an existing order.

    Args:
        id (strawberry.ID): The ID of the order to update.
        user_id (Optional[str], optional): The new user ID. Defaults to None.
        items (Optional[list[OrderItemInput]], optional): The new items in the
        order. Defaults to None.
        status (Optional[OrderStatus], optional): The new status of the order.
        Defaults to None.

    Returns:
        Order: The updated Order object.
    """
    logger.info(f"Updating order with ID: {id}")
    if validate_id(id):
        order = await get_order_by_id(
            id, ["user_id", "items.product_id", "items.quantity", "status"]
        )
        if user_id:
            order.user_id = user_id
        if items:
            order.items = [OrderItem.model_validate(item) for item in items]
        if status:
            order.status = status
        await order.save()
        return order
    raise
