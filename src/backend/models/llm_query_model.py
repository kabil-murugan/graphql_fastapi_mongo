"""Models for generate query endpoint."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    natural_language_query: str


class QueryResponse(BaseModel):
    graphql_query: str
    result: dict
