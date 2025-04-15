"""Object Types for User."""

from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

from backend.graphql.resolvers.user import get_user_orders
from backend.models.order import Order as OrderModel
from backend.utils.logger import get_logger
from backend.utils.utils import perform_resolving_action

if TYPE_CHECKING:
    from backend.graphql.types.order import Order


logger = get_logger(__name__)


@strawberry.type
class Profile:
    """Profile Object Type."""

    age: Optional[int]
    location: Optional[str] = None


@strawberry.type
class User:
    """User Object Type."""

    id: strawberry.ID
    name: Optional[str]
    email: Optional[str]
    profile: Optional[Profile]

    @strawberry.field(
        graphql_type=Optional[
            List[
                Annotated[
                    "Order", strawberry.lazy("backend.graphql.types.order")
                ]
            ]
        ]
    )
    async def orders(self, info: strawberry.Info) -> List[OrderModel]:
        """Fetch orders for a user.
        This function is used to resolve the orders field in the User.

        Args:
            info (strawberry.Info): GraphQL info object.

        Returns:
            List[OrderModel]: List of OrderModel objects.
        """
        return await perform_resolving_action(info, get_user_orders, self)
