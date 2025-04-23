"""Schema for the GraphQL API."""

import strawberry
from strawberry.extensions.tracing import ApolloTracingExtension

from backend.graphql.queries import Query

graphql_schema = strawberry.Schema(
    query=Query,
    extensions=[
        ApolloTracingExtension,
    ],
)
