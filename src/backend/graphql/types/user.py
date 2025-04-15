"""Object Types for User."""

from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

from backend.graphql.resolvers.user import get_user_orders
from backend.utils.logger import get_logger
from backend.utils.utils import extract_fields

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
    async def orders(self, info: strawberry.Info):
        fields = extract_fields(info)
        return await get_user_orders(self, fields)
