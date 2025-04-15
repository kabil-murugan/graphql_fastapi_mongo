"""Schema for the GraphQL API."""

import strawberry

from backend.graphql.queries import Query
from backend.graphql.mutations import Mutation


graphql_schema = strawberry.Schema(query=Query, mutation=Mutation)
