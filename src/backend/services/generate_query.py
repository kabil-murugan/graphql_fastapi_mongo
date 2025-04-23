"""Generate and validate GraphQL query with dynamic few-shot prompting."""

from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import RichPromptTemplate
import strawberry
from backend.utils.logger import get_logger
from backend.db.example_nodes import EXAMPLE_NODES

logger = get_logger(__name__)

Settings.llm = OpenAI(model="gpt-4.1")


index = VectorStoreIndex(nodes=EXAMPLE_NODES)
retriever = index.as_retriever(similarity_top_k=2)


PROMPT_TEMPLATE_STR = """
You are a GraphQL expert. You are an assistant that converts natural language
queries into GraphQL queries. You must strictly follow the provided
GraphQL schema and generate queries based on it.

Here is the GraphQL schema you should use:
<schema>
{{ schema }}
</schema>

Here are some examples of how you should convert natural language to GraphQL:
<examples>
{{ examples }}
</examples>

Now it's your turn.

Query: {{ query_str }}
GraphQL:
"""


def get_examples_fn(**kwargs):
    """Retrieve relevant examples based on the input query."""
    query = kwargs["query_str"]
    examples = retriever.retrieve(query)
    return "\n\n".join(node.text for node in examples)


prompt_template = RichPromptTemplate(
    PROMPT_TEMPLATE_STR,
    function_mappings={"examples": get_examples_fn},
)


async def generate_graphql_query(
    natural_language_query: str, schema: str
) -> str:
    """Generate a GraphQL query using dynamic few-shot prompting."""
    prompt = prompt_template.format(
        query_str=natural_language_query,
        schema=schema,
    )

    llm = Settings.llm
    response = await llm.acomplete(prompt)
    return response.text.strip()


async def validate_and_execute_query(
    graphql_query: str, schema: strawberry.Schema
):
    """Validate and execute the GraphQL query."""
    result = await schema.execute(graphql_query)
    if result.errors:
        raise ValueError(f"GraphQL execution errors: {result.errors}")
    return result.data
