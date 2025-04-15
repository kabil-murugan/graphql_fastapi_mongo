"""Utility functions for GraphQL queries and MongoDB projections."""

from typing import Any, Callable, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId
from strawberry.types.nodes import SelectedField
from strawberry.utils.str_converters import to_snake_case


def _extract_subfields(selection: SelectedField) -> dict[str, Any]:
    """Extracts subfields from a GraphQL selection.

    Args:
        selection (SelectedField): The GraphQL selection to extract
        subfields from.

    Returns:
        dict[str, Any]: A dictionary representing the extracted subfields.
    """
    subfield: dict[str, Any] = {selection.name: []}
    for sub_selection in selection.selections:
        if isinstance(sub_selection, SelectedField):
            if sub_selection.selections:
                subfield[to_snake_case(selection.name)].append(
                    _extract_subfields(sub_selection)
                )
            else:
                subfield[to_snake_case(selection.name)].append(
                    to_snake_case(sub_selection.name)
                )
    return subfield


def extract_fields(info: strawberry.Info) -> list[Any]:
    """Extracts fields from the GraphQL query information.

    Args:
        info (strawberry.Info): The GraphQL query information.

    Returns:
        list[Any]: A list of extracted fields.
    """
    fields: list[Any] = []
    for field in info.selected_fields:
        for selection in field.selections:
            if isinstance(selection, SelectedField):
                if selection.selections:
                    subfield = _extract_subfields(selection)
                    fields.append(subfield)
                else:
                    fields.append(to_snake_case(selection.name))
    return fields


def build_projection(
    fields: list[Any], parent_key: str = ""
) -> dict[str, int]:
    """Builds a projection for MongoDB queries based on the provided fields.

    Args:
        fields (list[Any]): A list of fields to include in the projection.
        parent_key (str, optional): A parent key for nested fields.
        Defaults to "".

    Returns:
        dict[str, int]: A dictionary representing the projection.
    """
    projection = {"user_id": 1, "items.product_id": 1}
    for field in fields:
        if isinstance(field, str):
            full_key = f"{parent_key}.{field}" if parent_key else field
            projection[full_key] = 1
        elif isinstance(field, dict):
            for key, subfields in field.items():
                new_parent = f"{parent_key}.{key}" if parent_key else key
                projection.update(build_projection(subfields, new_parent))
    return projection


async def perform_resolving_action(
    info: Optional[strawberry.Info],
    resolver_function: Callable[..., Any],
    *args: Any,
) -> Any:
    """Perform a resolving action for a GraphQL field.

    Args:
        info (Optional[strawberry.Info]): GraphQL query information.
        resolver_function (Callable[..., Any]): The resolver function to call.

    Returns:
        Any: The result of the resolver function.
    """
    if info:
        fields = extract_fields(info)
        return await resolver_function(*args, fields=fields)
    return await resolver_function(*args)


def validate_id(id: str) -> bool:
    """Validate the format of an ID.

    Args:
        id (str): The ID to validate.

    Raises:
        ValueError: If the ID format is invalid.

    Returns:
        bool: True if the ID format is valid, False otherwise.
    """
    try:
        ObjectId(id)
        return True
    except InvalidId:
        raise ValueError(f"Invalid ID format: {id}. Check it and try again.")
