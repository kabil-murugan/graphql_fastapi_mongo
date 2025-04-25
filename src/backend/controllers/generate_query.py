"""Generate query endpoint."""

from fastapi import APIRouter, HTTPException

from backend.models.llm_query_model import QueryRequest, QueryResponse
from backend.graphql.schema import graphql_schema
from backend.services.generate_query import (
    generate_graphql_query,
)

router: APIRouter = APIRouter()


@router.post("/generate_query", response_model=QueryResponse)
async def generate_query(request: QueryRequest):
    """Generate and execute a GraphQL query from a natural language query."""
    try:
        graphql_query = await generate_graphql_query(
            request.natural_language_query, graphql_schema.as_str()
        )

        # result = await validate_and_execute_query(
        #     graphql_query, graphql_schema
        # )

        return QueryResponse(graphql_query=graphql_query, result={})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
