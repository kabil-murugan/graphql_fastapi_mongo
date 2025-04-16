"""Object Types for Orders."""

from enum import Enum
from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

from backend.graphql.resolvers.product import get_product_by_id
from backend.graphql.resolvers.user import get_user_by_id
from backend.models.product import Product as ProductModel
from backend.models.user import User as UserModel
from backend.utils.utils import perform_resolving_action

if TYPE_CHECKING:
    from backend.graphql.types.product import Product
    from backend.graphql.types.user import User


@strawberry.enum
class OrderStatus(Enum):
    """Order Status Enum."""

    PENDING = "pending"
    ORDERED = "ordered"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@strawberry.type
class OrderItem:
    """Order Item Object Type."""

    product_id: strawberry.Private[strawberry.ID]
    quantity: Optional[int]

    @strawberry.field(
        graphql_type=Optional[
            Annotated[
                "Product", strawberry.lazy("backend.graphql.types.product")
            ]
        ]
    )
    async def product(self, info: strawberry.Info) -> Optional[ProductModel]:
        """Fetch product by ID.
        This function is used to resolve the product field in the OrderItem.

        Args:
            info (strawberry.Info): GraphQL info object.

        Returns:
            Optional[ProductModel]: ProductModel object or None.
        """
        return await perform_resolving_action(
            info, get_product_by_id, self.product_id
        )


@strawberry.type
class Order:
    """Order Object Type."""

    id: strawberry.ID
    user_id: strawberry.Private[strawberry.ID]
    items: Optional[List["OrderItem"]]
    status: Optional["OrderStatus"]

    @strawberry.field(
        graphql_type=Optional[
            Annotated["User", strawberry.lazy("backend.graphql.types.user")]
        ]
    )
    async def user(self, info: strawberry.Info) -> Optional[UserModel]:
        """Fetch user by ID.
        This function is used to resolve the user field in the Order object.

        Args:
            info (strawberry.Info): GraphQL info object.

        Returns:
            Optional[UserModel]: UserModel object or None.
        """
        return await perform_resolving_action(
            info, get_user_by_id, self.user_id
        )


@strawberry.input
class OrderItemInput:
    """Input type for Order Item."""

    product_id: str
    quantity: int
