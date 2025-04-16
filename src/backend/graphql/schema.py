"""Schema for the GraphQL API."""

import strawberry

from backend.graphql.mutations import Mutation
from backend.graphql.queries import Query

graphql_schema = strawberry.Schema(query=Query, mutation=Mutation)
