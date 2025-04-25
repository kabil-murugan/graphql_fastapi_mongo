"""Object Types for Tests."""

from datetime import datetime
from enum import Enum
from typing import Optional

import strawberry

from backend.graphql.types.common import TestStatusEnum, User


@strawberry.enum
class TestTypeEnum(Enum):
    """Test Type Enum."""

    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    INTEGRATION = "INTEGRATION"
    REGRESSION = "REGRESSION"
    UNIT = "UNIT"


@strawberry.type
class TestStep:
    """Test Step Object Type."""

    id: Optional[strawberry.ID]
    step_name: Optional[str]
    description: Optional[str]
    expected_result: Optional[str]
    actual_result: Optional[str]
    status: Optional[TestStatusEnum]
    executed_at: Optional[datetime]


@strawberry.type
class TestEnvironment:
    """Test Environment Object Type."""

    environment_name: Optional[str]
    os: Optional[str]
    browser: Optional[str]
    version: Optional[str]
    hardware: Optional[str]


@strawberry.type
class TestLog:
    """Test Log Object Type."""

    timestamp: Optional[datetime]
    message: Optional[str]
    level: Optional[str]


@strawberry.type
class Test:
    """Test Object Type."""

    id: strawberry.ID
    name: Optional[str]
    description: Optional[str]
    test_type: Optional[TestTypeEnum]
    status: Optional[TestStatusEnum]
    steps: Optional[list[TestStep]]
    environment: Optional[TestEnvironment]
    logs: Optional[list[TestLog]]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    duration: Optional[float]
    version: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    created_by: Optional[User]
    modified_by: Optional[User]
