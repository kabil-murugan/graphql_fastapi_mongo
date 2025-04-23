"""Example Nodes."""

from llama_index.core.schema import TextNode


EXAMPLE_NODES = [
    TextNode(
        text="""Query: Get all users whose profile age is between 10 and 40.
GraphQL: query {
  users(
    filters: {
      and_: [
        { filter: { field: "profile.age", operation: GTE, value: 10 } }
        { filter: { field: "profile.age", operation: LTE, value: 40 } }
      ]
    }
  ) {
    id
    name
    email
    profile {
      age
      location
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Give me all users who have pending orders with at least
one item priced above 200.
GraphQL: query {
  users(
    filters: {
      and_: [
        {
          filter: {
            field: "orders.status",
            operation: EQ,
            value: "PENDING"
          }
        }
        {
          filter: {
            field: "orders.items.product.price",
            operation: GT,
            value: 200
          }
        }
      ]
    }
  ) {
    id
    name
    email
    orders {
      id
      status
      items {
        product {
          id
          price
        }
      }
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all orders with their ID, status, items
(including product details and quantity), and user details.
GraphQL: query {
  orders {
    id
    status
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    user {
      id
      name
      email
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all orders where the quantity of any item is
greater than 300.
GraphQL: query {
  orders(
    filters: {
      filter: {
        field: "items.quantity",
        operation: GT,
        value: 300
      }
    }
  ) {
    id
    status
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    user {
      id
      name
      email
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all orders where the user's profile location
is "IND".
GraphQL: query {
  orders(
    filters: {
      filter: {
        field: "user.profile.location",
        operation: EQ,
        value: "IND"
      }
    }
  ) {
    id
    status
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    user {
      id
      name
      email
      profile {
        location
      }
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all orders where the user's profile location
is "IND", the status is "CANCELLED", and at least one item's product price is
greater than or equal to 300.
GraphQL: query {
  orders(
    filters: {
      and_: [
        {
          filter: {
            field: "user.profile.location",
            operation: EQ,
            value: "IND"
          }
        }
        {
          filter: {
            field: "status",
            operation: EQ,
            value: "CANCELLED"
          }
        }
        {
          filter: {
            field: "items.product.price",
            operation: GTE,
            value: 300
          }
        }
      ]
    }
  ) {
    id
    status
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    user {
      id
      name
      email
      profile {
        location
      }
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all orders where the status is either shipped or
delivered.
GraphQL: query {
  orders(
    filters: {
      or_: [
        { filter: { field: "status", operation: EQ, value: "SHIPPED" } }
        { filter: { field: "status", operation: EQ, value: "DELIVERED" } }
      ]
    }
  ) {
    id
    status
    items {
      product {
        id
        name
        price
      }
      quantity
    }
    user {
      id
      name
      email
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all products.
GraphQL: query {
  products {
    id
    name
    price
  }
}"""
    ),
    TextNode(
        text="""Query: Get all products with a price greater than 500
and less than 1000.
GraphQL: query {
  products(
    filters: {
      and_: [
        { filter: { field: "price", operation: GT, value: 500 } }
        { filter: { field: "price", operation: LT, value: 1000 } }
      ]
    }
  ) {
    id
    name
    price
    reviews {
      id
      rating
      comment
    }
  }
}"""
    ),
    TextNode(
        text="""Query: Get all products along with their reviews and the users
who wrote those reviews.
GraphQL: query {
  products {
    id
    name
    price
    reviews {
      id
      rating
      comment
      user {
        id
        name
        email
      }
    }
  }
}"""
    ),
]
