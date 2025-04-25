"""Example Nodes."""

from llama_index.core.schema import TextNode

EXAMPLE_NODES = [
    TextNode(
        text="""Query: Get all tests.
GraphQL: query {
  tests {
    id
    name
    testType
    status
  }
}"""
    ),
]
