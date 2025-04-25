"""Main entry point for the FastAPI application."""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter


from backend.db.init_db import close_db, init_db
from backend.controllers import generate_query
from backend.graphql.schema import graphql_schema
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Add startup and shutdown events to the FastAPI app."""
    client = await init_db()
    yield
    await close_db(client)


graphql_app = GraphQLRouter(schema=graphql_schema)


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(generate_query.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"Request: {request.method} {request.url}\n "
        f"Process Time: {process_time:.4f} seconds"
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
