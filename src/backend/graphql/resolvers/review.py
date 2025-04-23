"""Resolvers for Review related GraphQL queries."""

from typing import TYPE_CHECKING, Any, Optional

import strawberry
from beanie import PydanticObjectId
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.test_result import Review
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
    validate_id,
)

if TYPE_CHECKING:
    from backend.graphql.types.filter import LogicalFilterInput

logger = get_logger(__name__)


async def get_reviews(
    fields: list[Any], filters: Optional["LogicalFilterInput"] = None
) -> list[Review]:
    """Fetch all reviews with specified fields.

    Args:
        fields (list[Any]): List of fields to include in the projection.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        list[Review]: List of Review objects with the specified fields.
    """
    logger.info(f"Fetching all reviews with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]

    if filters:
        (
            user_filters,
            product_filters,
            review_filters,
        ) = extract_filters_by_prefixes(filters, ["user.", "product."])
        review_filter_query = build_query_from_filters(review_filters)
        aggregation_pipeline = [
            {"$match": review_filter_query},
        ]
        if product_filters:
            aggregation_pipeline = build_filter_aggregation_pipeline(
                ("products", "product_id", "_id", "products"),
                product_filters,
                aggregation_pipeline,
            )
        if user_filters:
            aggregation_pipeline = build_filter_aggregation_pipeline(
                ("users", "user_id", "_id", "users"),
                user_filters,
                aggregation_pipeline,
            )

    logger.info(f"Aggregation pipeline: {aggregation_pipeline}")
    reviews = await Review.find_all().aggregate(aggregation_pipeline).to_list()
    logger.info(f"Reviews fetched: {reviews}")
    return [Review.model_validate(review) for review in reviews]


async def get_review_by_id(id: strawberry.ID, fields: list[Any]) -> Review:
    """Fetch a review by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the order to fetch.
        fields (list[Any]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid or the review is not found.

    Returns:
        Review: The Review object with the specified ID and fields.
    """
    logger.info(f"Fetching review with ID: {id} and fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [
        {"$project": projection},
    ]
    try:
        review = (
            await Review.find({"_id": ObjectId(id)})
            .aggregate(aggregation_pipeline)
            .to_list()
        )
    except InvalidId:
        raise ValueError(f"Invalid ID format: {id}. Check it and try again.")
    if review:
        return Review.model_validate(review[0])
    raise ValueError(f"Review with ID {id} not found.")


async def create_review(
    product_id: str, user_id: str, rating: int, comment: Optional[str]
) -> Review:
    """Create a new review."""
    logger.info(f"Creating review for user {user_id}")
    if validate_id(user_id) and validate_id(product_id):
        review = Review(
            user_id=PydanticObjectId(ObjectId(user_id)),
            product_id=PydanticObjectId(ObjectId(product_id)),
            rating=rating,
            comment=comment,
        )
        await review.insert()
        return review
    raise


# async def update_order(
#     id: strawberry.ID,
#     user_id: Optional[str] = None,
#     items: Optional[list[OrderItemInput]] = None,
#     status: Optional[OrderStatus] = None,
# ) -> Order:
#     """Update an existing order.

#     Args:
#         id (strawberry.ID): The ID of the order to update.
#         user_id (Optional[str], optional): The new user ID. Defaults to None.
#         items (Optional[list[OrderItemInput]], optional): The new items inthe
#         order. Defaults to None.
#         status (Optional[OrderStatus], optional): The new status of theorder.
#         Defaults to None.

#     Returns:
#         Order: The updated Order object.
#     """
#     logger.info(f"Updating order with ID: {id}")
#     if validate_id(id):
#         order = await get_order_by_id(
#             id, ["user_id", {"items": ["product_id", "quantity"]}, "status"]
#         )
#         if user_id:
#             order.user_id = PydanticObjectId(ObjectId(user_id))
#         if items:
#             order.items = [OrderItem.model_validate(item) for item in items]
#         if status:
#             order.status = OrderStatusModel(status.value)
#         await order.save()
#         return order
#     raise


# async def delete_order(id: strawberry.ID) -> Order:
#     """Delete an existing order.

#     Args:
#         id (strawberry.ID): The ID of the order to delete.

#     Returns:
#         Order: The deleted Order object.
#     """
#     logger.info(f"Deleting order with ID: {id}")
#     if validate_id(id):
#         order = await get_order_by_id(
#             id, ["user_id", {"items": ["quantity", "product_id"]}, "status"]
#         )
#         await order.delete()
#         return order
#     raise
