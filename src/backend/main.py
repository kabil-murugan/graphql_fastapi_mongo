"""Main entry point for the FastAPI application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from backend.db.init_db import close_db, init_db
from backend.graphql.schema import graphql_schema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Add startup and shutdown events to the FastAPI app."""
    client = await init_db()
    yield
    await close_db(client)


graphql_app = GraphQLRouter(schema=graphql_schema)


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
