"""Object Types for Orders."""

from enum import Enum
from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

from backend.graphql.resolvers.product import get_product
from backend.graphql.resolvers.user import get_user
from backend.utils.utils import extract_fields

if TYPE_CHECKING:
    from backend.graphql.types.product import Product
    from backend.graphql.types.user import User


@strawberry.enum
class OrderStatus(Enum):
    """Order Status Enum."""

    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@strawberry.type
class OrderItem:
    """Order Item Object Type."""

    product_id: strawberry.ID
    quantity: Optional[int]

    @strawberry.field(
        graphql_type=Optional[
            Annotated[
                "Product", strawberry.lazy("backend.graphql.types.product")
            ]
        ]
    )
    async def product(self, info: strawberry.Info):
        fields = extract_fields(info)
        return await get_product(self.product_id, fields)


@strawberry.type
class Order:
    """Order Object Type."""

    id: strawberry.ID
    user_id: strawberry.ID
    items: Optional[List["OrderItem"]]
    status: Optional["OrderStatus"]

    @strawberry.field(
        graphql_type=Optional[
            Annotated["User", strawberry.lazy("backend.graphql.types.user")]
        ]
    )
    async def user(self, info: strawberry.Info):
        fields = extract_fields(info)
        return await get_user(self.user_id, fields)
