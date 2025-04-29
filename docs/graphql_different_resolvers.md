# GraphQL Endpoint Approaches and Time Comparison

## Approach 1: Custom Resolvers for Fields

- Each field in the GraphQL schema has its own resolver function.
- Resolvers are executed independently, leading to multiple database calls for nested fields.
- This approach is simple but can result in the **N+1 query problem**, where multiple redundant database queries are executed.

## Approach 2: Custom Resolvers with Data Loaders

- Similar to the first approach but uses **DataLoader** to batch and cache database requests.
- Tries to eliminate the **N+1 query problem** by reducing the number of database calls by grouping multiple requests into a single batch.
- Optimized for scenarios where the same data is requested multiple times in a single query.

## Approach 3: Top-Level Resolvers with MongoDB Lookup

- Uses a single top-level resolver with MongoDB's `$lookup` aggregation to fetch all nested fields in a single database call.
- Eliminates the **N+1 query problem** entirely by fetching all required data in one query.
- Highly efficient for complex queries with deeply nested fields but may require more complex aggregation pipelines.

---

## Time Comparison Table

GraphQL Complex Query:

```graphql
query {
  orders(filters: {
    and_: [
      { filter: { field: "items.product.price", operation: GTE, value: 100 } },
      { filter: { field: "items.product.price", operation: LTE, value: 1000 } },
    ]
  }) {
    id
    user {
      id
      name
      profile{
        age
      }
    }
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    status
  }
}
```

For the above query, the time is compared between these approaches in the below table:

| **Approach**                      | **Description**                              | **Average Query Time** |
|------------------------------------|----------------------------------------------|-------------------------|
| **Custom Resolvers for Fields**   | Multiple independent resolvers for fields.   | 40s -45 s                  |
| **Resolvers with Data Loaders**   | Batched and cached database requests.        | 35s -40 s                  |
| **Top-Level Resolvers with Lookup** | Single database call using MongoDB `$lookup`. | 5s -8 s                  |

---

### Observations

- **Custom Resolvers for Fields**: The slowest approach due to multiple database calls for nested fields.
- **Resolvers with Data Loaders**: Significant improvement by reducing redundant database calls.
- **Top-Level Resolvers with Lookup**: The fastest approach, as it minimizes database interactions by fetching all data in a single query.
