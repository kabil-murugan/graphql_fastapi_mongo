"""Generate and validate GraphQL query."""

from llama_index.llms.openai import OpenAI
import strawberry
from backend.utils.logger import get_logger



PROMPT_TEMPLATE = """
You are an assistant that converts natural language queries into GraphQL 
queries. \n Here is the GraphQL schema:

{schema}

Now, convert the following natural language query into a valid GraphQL query:

"{query}"
"""


def generate_graphql_query(natural_language_query: str, schema: str) -> str:
    """Generate a GraphQL query from a natural language query."""
    prompt = PROMPT_TEMPLATE.format(
        schema=schema, query=natural_language_query
    )
    llm = OpenAI(model="gpt-4.1")
    response = llm.complete(prompt)
    logger.info(f"")
    return response.text.strip()


async def validate_and_execute_query(
    graphql_query: str, schema: strawberry.Schema
):
    """Validate and execute the GraphQL query."""
    result = await schema.execute(graphql_query)
    if result.errors:
        raise ValueError(f"GraphQL execution errors: {result.errors}")
    return result.data
