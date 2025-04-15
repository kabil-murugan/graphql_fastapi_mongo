"""Object type for Product."""

from typing import Optional

import strawberry


@strawberry.type
class Product:
    """Product Object Type."""

    id: strawberry.ID
    name: Optional[str]
    price: Optional[float]
