"""Utility functions for GraphQL queries and MongoDB projections."""

from typing import Any, Callable, Optional

import strawberry
from bson import ObjectId
from bson.errors import InvalidId
from strawberry.types.nodes import SelectedField
from strawberry.utils.str_converters import to_snake_case

from backend.graphql.types.common import (
    FilterInput,
    LogicalFilterInput,
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def _extract_subfields(selection: SelectedField) -> dict[str, Any]:
    """Extracts subfields from a GraphQL selection.

    Args:
        selection (SelectedField): The GraphQL selection to extract
        subfields from.

    Returns:
        dict[str, Any]: A dictionary representing the extracted subfields.
    """
    key = to_snake_case(selection.name)
    subfield: dict[str, Any] = {key: []}
    for sub_selection in selection.selections:
        if isinstance(sub_selection, SelectedField):
            if key not in subfield:
                subfield[key] = []
            if sub_selection.selections:
                subfield[key].append(_extract_subfields(sub_selection))
            else:
                subfield[key].append(to_snake_case(sub_selection.name))
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
    projection = {
        "test_id": 1,
        "test_plan_id": 1,
        "test._id": 1,
        "test_plan._id": 1,
    }
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
    filters: Optional[LogicalFilterInput] = None,
) -> Any:
    """Perform a resolving action for a GraphQL field.

    Args:
        info (Optional[strawberry.Info]): GraphQL query information.
        resolver_function (Callable[..., Any]): The resolver function to call.
        filters (Optional[LogicalFilterInput], optional): Filters to apply.

    Returns:
        Any: The result of the resolver function.
    """
    if info:
        fields = extract_fields(info)
        if filters:
            return await resolver_function(
                *args, fields=fields, filters=filters
            )
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


def build_query_from_filters(
    filters: Optional["LogicalFilterInput"],
) -> dict[str, Any]:
    """Recursively build a MongoDB query from LogicalFilterInput.

    Args:
        filters (Optional[LogicalFilterInput]): Filters to apply.

    Returns:
        dict[str, Any]: MongoDB query.
    """
    if not filters:
        return {}

    query: dict[str, Any] = {}

    if filters.filter:
        field = filters.filter.field
        operation = filters.filter.operation
        value = filters.filter.value

        query[field] = {operation.value: value}

    if filters.and_:
        query["$and"] = [build_query_from_filters(f) for f in filters.and_]

    if filters.or_:
        query["$or"] = [build_query_from_filters(f) for f in filters.or_]

    return query


def extract_filters_by_prefixes(
    filters: Optional[LogicalFilterInput], prefixes: list[str]
) -> tuple[Optional[LogicalFilterInput], ...]:
    """
    Extracts filters based on a list of prefixes from the LogicalFilterInput.

    Args:
        filters (Optional[LogicalFilterInput]): The input filters.
        prefixes (list[str]): A list of prefixes to identify specific filters.

    Returns:
        tuple[Optional[LogicalFilterInput], ...]:
            - A tuple of extracted filters for each prefix in the
            order of the prefixes.
            - The last element in the tuple is the remaining filters.
    """
    if not filters:
        return tuple(None for _ in prefixes) + (None,)

    remaining_filters = LogicalFilterInput()
    prefixed_filters_list = [LogicalFilterInput() for _ in prefixes]

    def match_prefix(field: str) -> Optional[int]:
        for i, prefix in enumerate(prefixes):
            if field.startswith(prefix):
                return i
        return None

    if filters.filter:
        matched_index = match_prefix(filters.filter.field)
        if matched_index is not None:
            prefixed_filters_list[matched_index].filter = FilterInput(
                field=filters.filter.field[len(prefixes[matched_index]):],
                operation=filters.filter.operation,
                value=filters.filter.value,
            )
        else:
            remaining_filters.filter = filters.filter

    if filters.and_:
        remaining_and_filters = []
        prefixed_and_filters_list = [[] for _ in prefixes]  # type: ignore
        for sub_filter in filters.and_:
            sub_results = extract_filters_by_prefixes(sub_filter, prefixes)
            for i, pf in enumerate(sub_results[:-1]):
                if pf:
                    prefixed_and_filters_list[i].append(pf)
            if sub_results[-1]:
                remaining_and_filters.append(sub_results[-1])
        if remaining_and_filters:
            remaining_filters.and_ = remaining_and_filters
        for i, prefixed_and_filters in enumerate(prefixed_and_filters_list):
            if prefixed_and_filters:
                prefixed_filters_list[i].and_ = prefixed_and_filters

    if filters.or_:
        remaining_or_filters = []
        prefixed_or_filters_list = [[] for _ in prefixes]  # type: ignore
        for sub_filter in filters.or_:
            sub_results = extract_filters_by_prefixes(sub_filter, prefixes)
            for i, pf in enumerate(sub_results[:-1]):
                if pf:
                    prefixed_or_filters_list[i].append(pf)
            if sub_results[-1]:
                remaining_or_filters.append(sub_results[-1])
        if remaining_or_filters:
            remaining_filters.or_ = remaining_or_filters
        for i, prefixed_or_filters in enumerate(prefixed_or_filters_list):
            if prefixed_or_filters:
                prefixed_filters_list[i].or_ = prefixed_or_filters

    if filters.not_:
        sub_results = extract_filters_by_prefixes(filters.not_, prefixes)
        for i, pf in enumerate(sub_results[:-1]):
            if pf:
                prefixed_filters_list[i].not_ = pf
        if sub_results[-1]:
            remaining_filters.not_ = sub_results[-1]

    return tuple(
        pf if pf.filter or pf.and_ or pf.or_ or pf.not_ else None
        for pf in prefixed_filters_list
    ) + (
        (
            remaining_filters
            if remaining_filters.filter
            or remaining_filters.and_
            or remaining_filters.or_
            or remaining_filters.not_
            else None
        ),
    )


def build_filter_aggregation_pipeline(
    look_up_fields: tuple[str, str, str, str],
    filters: Optional["LogicalFilterInput"],
    aggregation_pipeline: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    from_collection, local_field, foreign_field, as_field = look_up_fields
    aggregation_pipeline.append(
        {
            "$lookup": {
                "from": from_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field,
            }
        },
    )
    if filters:
        secondary_filter_query = build_query_from_filters(filters)
        aggregation_pipeline[-1]["$lookup"]["pipeline"] = [
            {"$match": secondary_filter_query},
        ]
    aggregation_pipeline.append(
        {
            "$unwind": {
                "path": f"${as_field}",
            }
        }
    )
    return aggregation_pipeline
