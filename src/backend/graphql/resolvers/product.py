"""Resolvers for product-related GraphQL queries."""

from typing import Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.models.product import Product
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection

logger = get_logger(__name__)


async def get_products(fields: list[str]) -> list[Product]:
    """Fetch all products with specified fields.

    Args:
        fields (list[str]): List of fields to include in the projection.

    Returns:
        list[Product]: List of Product objects with the specified fields.
    """
    logger.info(f"Fetching all products with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    products = (
        await Product.find_all().aggregate(aggregation_pipeline).to_list()
    )
    return [Product.model_validate(product) for product in products]


async def get_product_by_id(
    id: strawberry.ID, fields: list[str]
) -> Optional[Product]:
    """Fetch a product by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the product to fetch.
        fields (list[str]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid.

    Returns:
        Optional[Product]: The Product object with the specified ID and fields,
        or None if not found.
    """
    logger.info(f"Fetching product with ID: {id} and fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    try:
        products = (
            await Product.find({"_id": ObjectId(id)})
            .aggregate(aggregation_pipeline)
            .to_list()
        )
    except InvalidId:
        raise ValueError(f"Invalid ID format: {id}. Check it and try again.")
    if products:
        return Product.model_validate(products[0])
    return None
