"""Resolvers for Order related GraphQL queries."""

from typing import Any, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId
from strawberry.dataloader import DataLoader
from backend.graphql.types.order import OrderItemInput, OrderStatus
from backend.models.order import Order, OrderItem
from backend.models.order import (
    OrderItem as OrderItemModel,
)
from backend.models.order import (
    OrderStatus as OrderStatusModel,
)
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection, validate_id

logger = get_logger(__name__)


async def get_orders(
    fields: list[Any], order_loader: DataLoader
) -> list[Order]:
    logger.info(f"Fetching all orders with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [
        {"$project": projection},
    ]
    orders = await Order.find_all().aggregate(aggregation_pipeline).to_list()
    order_loader.prime_many({str(order["_id"]): order for order in orders})
    logger.info("Primed orders in DataLoader")
    return [Order.model_validate(order) for order in orders]


async def get_order_by_id(
    id: strawberry.ID, fields: list[Any], order_loader: DataLoader
) -> Order:
    logger.info(f"Fetching order with ID: {id} and fields: {fields}")
    order_data = await order_loader.load((str(id), fields))
    logger.info(f"Fetched order data: {order_data}")
    if not order_data:
        raise ValueError(f"Order with ID {id} not found.")
    return Order.model_validate(order_data)


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
        items_db = [
            OrderItemModel(product_id=item.product_id, quantity=item.quantity)
            for item in items
        ]
        order = Order(user_id=user_id, items=items_db, status=status)
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
            id, ["user_id", {"items": ["product_id", "quantity"]}, "status"]
        )
        if user_id:
            order.user_id = user_id
        if items:
            order.items = [OrderItem.model_validate(item) for item in items]
        if status:
            order.status = OrderStatusModel(status.value)
        await order.save()
        return order
    raise


async def delete_order(id: strawberry.ID) -> Order:
    """Delete an existing order.

    Args:
        id (strawberry.ID): The ID of the order to delete.

    Returns:
        Order: The deleted Order object.
    """
    logger.info(f"Deleting order with ID: {id}")
    if validate_id(id):
        order = await get_order_by_id(
            id, ["user_id", {"items": ["quantity", "product_id"]}, "status"]
        )
        await order.delete()
        return order
    raise
