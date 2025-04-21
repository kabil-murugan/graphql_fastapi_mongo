"""Object type for Product."""

from typing import Optional

import strawberry

from backend.graphql.types.review import Review
from backend.utils.utils import perform_resolving_action
from backend.graphql.resolvers.product import get_product_reviews


@strawberry.type
class Product:
    """Product Object Type."""

    id: strawberry.ID
    name: Optional[str]
    price: Optional[float]

    @strawberry.field
    async def reviews(self, info: strawberry.Info) -> Optional[list[Review]]:
        """Fetch reviews for this product."""
        return await perform_resolving_action(
            info, get_product_reviews, self.id
        )
