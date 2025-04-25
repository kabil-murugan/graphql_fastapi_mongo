"""Filter Types."""

from enum import Enum
from typing import NewType, Optional, Union

import strawberry

VALUE = strawberry.scalar(
    NewType("VALUE", Union[str, int, float]),
    serialize=lambda v: v,
    parse_value=lambda v: v,
    description="A value that can be a string, int, or float.",
)


@strawberry.type
class User:
    """User Object Type."""

    name: Optional[str]
    email: Optional[str]


@strawberry.enum
class TestStatusEnum(Enum):
    """Enum for Test Status."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@strawberry.enum
class ParamGroupTypeEnum(Enum):
    """Enum for Test Plan Group Type."""

    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"


@strawberry.type
class TestData:
    """Test Data."""

    id: Optional[strawberry.ID]
    name: Optional[str]


@strawberry.enum
class FilterOperator(Enum):
    """Filter Operator Enum."""

    EQ = "$eq"
    GT = "$gt"
    GTE = "$gte"
    LT = "$lt"
    LTE = "$lte"
    NEQ = "$ne"


@strawberry.input
class FilterInput:
    """Filter Input Type."""

    field: str
    operation: FilterOperator
    value: VALUE  # type: ignore


@strawberry.input
class LogicalFilterInput:
    """Logical Filter Input Type."""

    and_: Optional[list["LogicalFilterInput"]] = None
    or_: Optional[list["LogicalFilterInput"]] = None
    not_: Optional["LogicalFilterInput"] = None
    filter: Optional[FilterInput] = None
