"""Resolvers for product-related GraphQL queries."""

from typing import Any, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId
from strawberry.dataloader import DataLoader

from backend.graphql.types.filter import LogicalFilterInput
from backend.models.product import Product
from backend.utils.logger import get_logger
from backend.utils.utils import (
    build_filter_aggregation_pipeline,
    build_projection,
    build_query_from_filters,
    extract_filters_by_prefixes,
)

logger = get_logger(__name__)


async def get_products(
    fields: list[Any],
    product_loader: DataLoader,
    filters: Optional["LogicalFilterInput"] = None,
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
    # logger.info(f"Aggregation pipeline: {aggregation_pipeline}")
    products = (
        await Product.find_all().aggregate(aggregation_pipeline).to_list()
    )
    product_loader.prime_many(
        {str(product["_id"]): product for product in products}
    )
    logger.info("Primed products in DataLoader")
    return [Product.model_validate(product) for product in products]


async def get_product_by_id(
    id: strawberry.ID, fields: list[Any], product_loader: DataLoader
) -> Product:
    product_data = await product_loader.load((str(id), fields))
    if not product_data:
        raise ValueError(f"Product with ID {id} not found.")
    return Product.model_validate(product_data)


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
