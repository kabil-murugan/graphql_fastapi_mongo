"""Performance Testing."""

import requests  # type: ignore
import time

# Server URL
BASE_URL = "http://127.0.0.1:8000"

# GraphQL Query
GRAPHQL_QUERY = """
query {
  testResults {
    id
    name
    status
    testPlan {
      id
      name
      testPlannedValues{
        testPlanName
      }
    }
    sensorOffsets {
      id
      startPos
    }
    equipmentOffsets {
      id
      startPos
      endPos
    }
    createdBy {
      name
      email
    }
    modifiedBy {
      name
      email
    }
  }
}
"""


def execute_graphql():
    """Execute the GraphQL endpoint."""
    url = f"{BASE_URL}/graphql"
    payload = {"query": GRAPHQL_QUERY}
    headers = {"Content-Type": "application/json"}

    start_time = time.perf_counter()
    response = requests.post(url, json=payload, headers=headers)
    process_time = time.perf_counter() - start_time

    print(f"GraphQL Response Time: {process_time:.4f} seconds")
    return response.json()


def execute_rest():
    """Execute the REST endpoint."""
    url = f"{BASE_URL}/test-results"

    start_time = time.perf_counter()
    response = requests.get(url)
    process_time = time.perf_counter() - start_time

    print(f"REST Response Time: {process_time:.4f} seconds")
    return response.json()


def main():
    """Main function to execute both endpoints."""
    print("Executing GraphQL Endpoint...")
    response = execute_graphql()
    print(response["data"]["testResults"][0])

    # print("\nExecuting REST Endpoint...")
    # rest_response = execute_rest()


if __name__ == "__main__":
    main()
