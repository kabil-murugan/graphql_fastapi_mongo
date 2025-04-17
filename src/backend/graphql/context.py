from asyncio import Future
from typing import Any, Callable, Hashable, Optional, Union

from bson import ObjectId
from strawberry.dataloader import AbstractCache

from backend.graphql.dataloader import CustomDataLoader
from backend.models.user import User as UserModel
from backend.models.order import Order as OrderModel
from backend.utils.logger import get_logger
from backend.utils.utils import build_projection, is_field_missing

logger = get_logger(__name__)


async def load_users(
    ids_with_fields: list[tuple[str, list[Any]]],
) -> list[dict[str, Any]]:
    logger.info(
        "Loading users with IDs: "
        f"{[user_id for user_id, _ in ids_with_fields]}"
        f"\nand fields: {[fields for _, fields in ids_with_fields]}"
    )
    users_data: list[dict[str, Any]] = []
    for user_id, fields in ids_with_fields:
        cached_user_future = user_cache.get(user_id)
        cached_user = (
            cached_user_future.result()
            if cached_user_future and cached_user_future.done()
            else {}
        )
        projection_fields = build_projection(fields)
        logger.info(f"Projection_fields: {projection_fields}")
        missing_projection_fields = {
            field: 1
            for field in projection_fields
            if is_field_missing(field, cached_user)
        }
        logger.info(f"Missing projection fields: {missing_projection_fields}")
        if missing_projection_fields:
            aggregation_pipeline = [{"$project": missing_projection_fields}]
            user_data = (
                await UserModel.find({"_id": ObjectId(user_id)})
                .aggregate(aggregation_pipeline)
                .to_list()
            )
            consolidated_user_data = {**cached_user, **user_data[0]}
            logger.info(f"Consolidated user data: {consolidated_user_data}")
        users_data.append(consolidated_user_data)

    return users_data


async def load_orders(
    ids_with_fields: list[tuple[str, list[Any]]],
) -> list[dict[str, Any]]:
    logger.info(
        "Loading orders with IDs: "
        f"{[order_id for order_id, _ in ids_with_fields]} "
        f"and fields: {[fields for _, fields in ids_with_fields]}"
    )
    orders_data: list[dict[str, Any]] = []
    for order_id, fields in ids_with_fields:
        cached_order_future = order_cache.get(order_id)
        cached_order = (
            cached_order_future.result()
            if cached_order_future and cached_order_future.done()
            else {}
        )
        projection_fields = build_projection(fields)
        logger.info(f"Projection_fields: {projection_fields}")
        missing_projection_fields = {
            field: 1
            for field in projection_fields
            if is_field_missing(field, cached_order)
        }
        logger.info(f"Missing projection fields: {missing_projection_fields}")
        if missing_projection_fields:
            aggregation_pipeline = [{"$project": missing_projection_fields}]
            order_data = (
                await OrderModel.find({"_id": ObjectId(order_id)})
                .aggregate(aggregation_pipeline)
                .to_list()
            )
            consolidated_order_data = {**cached_order, **order_data[0]}
            logger.info(f"Consolidated order data: {consolidated_order_data}")
        orders_data.append(consolidated_order_data)
    return orders_data


class CustomCache(AbstractCache[str, dict[str, Any]]):
    def __init__(
        self,
        cache_key_fn: Optional[
            Callable[[Union[str, tuple[str, list[Any]]]], Hashable]
        ] = None,
    ) -> None:
        self.cache_key_fn: Callable[[str], Hashable] = (
            cache_key_fn if cache_key_fn is not None else lambda x: x
        )
        self.cache: dict[Hashable, Future[dict[str, Any]]] = {}

    def get(self, key: str) -> Optional[Future[dict[str, Any]]]:
        return self.cache.get(self.cache_key_fn(key))

    def set(self, key: str, value: Future[dict[str, Any]]) -> None:
        self.cache[self.cache_key_fn(key)] = value

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[self.cache_key_fn(key)]

    def clear(self) -> None:
        self.cache.clear()


def cache_key_function(key: Union[str, tuple[str, list[Any]]]) -> str:
    """Generate a cache key for the user data loader."""
    if isinstance(key, str):
        return key
    user_id, _ = key
    return str(user_id)


user_cache = CustomCache(cache_key_fn=cache_key_function)
order_cache = CustomCache(cache_key_fn=cache_key_function)
product_cache = CustomCache(cache_key_fn=cache_key_function)


async def get_context() -> dict[str, CustomDataLoader]:
    """Get the context for the GraphQL API."""
    return {
        "user_loader": CustomDataLoader(
            load_fn=load_users,
            cache_map=user_cache,
        ),
    }
