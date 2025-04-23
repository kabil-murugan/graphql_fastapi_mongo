"""Resolvers for product-related GraphQL queries."""

from typing import Any, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId

from backend.graphql.types.filter import LogicalFilterInput
from backend.models.test import Product
from backend.models.test_result import Review
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
)

logger = get_logger(__name__)


async def get_products(
    fields: list[Any], filters: Optional["LogicalFilterInput"] = None
) -> list[Product]:
    """Fetch all products with specified fields.

    Args:
        fields (list[Any]): List of fields to include in the projection.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        list[Product]: List of Product objects with the specified fields.
    """
    logger.info(f"Fetching all products with fields: {fields}")
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]

    (review_filters, product_filters) = extract_filters_by_prefixes(
        filters, ["reviews."]
    )
    product_filter_query = build_query_from_filters(product_filters)
    aggregation_pipeline = [
        {"$match": product_filter_query},
    ]
    if review_filters:
        aggregation_pipeline = build_filter_aggregation_pipeline(
            ("reviews", "review_ids", "_id", "reviews"),
            review_filters,
            aggregation_pipeline,
        )
    logger.info(f"Aggregation pipeline: {aggregation_pipeline}")
    products = (
        await Product.find_all().aggregate(aggregation_pipeline).to_list()
    )
    logger.info(f"Products fetched: {products}")
    return [Product.model_validate(product) for product in products]


async def get_product_by_id(id: strawberry.ID, fields: list[Any]) -> Product:
    """Fetch a product by ID with specified fields.

    Args:
        id (strawberry.ID): The ID of the product to fetch.
        fields (list[Any]): List of fields to include in the projection.

    Raises:
        ValueError: If the ID format is invalid or the product is not found.

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
    raise ValueError(f"Product with ID {id} not found.")


async def get_product_reviews(
    product_id: strawberry.ID, fields: list[Any]
) -> list[Review]:
    """Fetch all reviews for a product with specified fields."""
    logger.info(
        f"Fetching reviews for product: {product_id} with fields: {fields}"
    )
    projection = build_projection(fields)
    aggregation_pipeline = [{"$project": projection}]
    reviews = (
        await Review.find({"_id": ObjectId(product_id)})
        .aggregate(aggregation_pipeline)
        .to_list()
    )
    return [Review.model_validate(review) for review in reviews]


async def create_product(name: str, price: float) -> Product:
    """Create a new product.

    Args:
        name (str): The name of the product.
        price (float): The price of the product.

    Returns:
        Product: The created Product object.
    """
    logger.info(f"Creating product with name: {name}, price: {price}")
    product = Product(name=name, price=price)
    await product.insert()
    return product


async def update_product(
    id: strawberry.ID, name: str, price: float
) -> Product:
    """Update an existing product.

    Args:
        id (strawberry.ID): The ID of the product to update.
        name (str): The new name of the product.
        price (float): The new price of the product.

    Returns:
        Product: The updated Product object.
    """
    logger.info(f"Updating product with ID: {id}")
    product = await get_product_by_id(id, ["name", "price"])
    if name:
        product.name = name
    if price:
        product.price = price
    await product.save()
    return product


async def delete_product(id: strawberry.ID) -> Product:
    """Delete an existing product.

    Args:
        id (strawberry.ID): The ID of the product to delete.

    Returns:
        Product: The deleted Product object.
    """
    logger.info(f"Deleting product with ID: {id}")
    product = await get_product_by_id(id, ["name", "price"])
    await product.delete()
    return product
