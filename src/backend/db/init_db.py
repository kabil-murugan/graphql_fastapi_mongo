"""Database initialization module."""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from backend.core.config import settings
from backend.models.order import Order
from backend.models.product import Product
from backend.models.review import Review
from backend.models.user import User
from backend.utils.logger import get_logger

logger = get_logger(__name__)


async def init_db() -> AsyncIOMotorClient:
    """Initialize the database connection and models.

    Raises:
        ValueError: If the MongoDB connection string or
        database name is not set.

    Returns:
        AsyncIOMotorClient: The MongoDB client instance.
    """
    if settings.mongo_db and settings.mongo_url:
        client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_url)
        await init_beanie(
            database=client[settings.mongo_db],
            document_models=[User, Order, Product, Review],
        )
        logger.info("Database initialized successfully.")
        return client
    logger.error("MongoDB connection string or database name is not set.")
    raise ValueError("MongoDB connection string or database name is not set.")


async def close_db(client: AsyncIOMotorClient) -> None:
    """Close the database connection.

    Args:
        client (AsyncIOMotorClient): The MongoDB client instance to close.
    """
    client.close()
    logger.info("Database connection closed successfully.")
