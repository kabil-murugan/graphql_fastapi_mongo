"""Populate fake data into MongoDB for testing purposes."""

import asyncio
from faker import Faker
from bson import ObjectId
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient


client: AsyncIOMotorClient = AsyncIOMotorClient(
    "mongodb://kabil1012:kabilm2003@localhost:27017"
)
db = client["test_database"]

fake = Faker()


async def seed_users():
    users = []
    for _ in range(10000):
        users.append(
            {
                "_id": ObjectId(),
                "name": fake.name(),
                "email": fake.email(),
                "profile": {
                    "age": fake.random_int(min=18, max=80),
                    "location": fake.country(),
                },
                "review_ids": [],
            }
        )
    await db.users.insert_many(users)
    print("Seeded 10,000 users.")
    return [user["_id"] for user in users]


async def seed_products():
    products = []
    for _ in range(10000):
        products.append(
            {
                "_id": ObjectId(),
                "name": fake.word(),
                "price": fake.random_int(min=10, max=1000),
                "review_ids": [],
            }
        )
    await db.products.insert_many(products)
    print("Seeded 10,000 products.")
    return [product["_id"] for product in products]


async def seed_reviews(user_ids, product_ids):
    reviews = []
    for _ in range(10000):
        reviews.append(
            {
                "_id": ObjectId(),
                "product_id": fake.random_element(product_ids),
                "user_id": fake.random_element(user_ids),
                "rating": fake.random_int(min=1, max=5),
                "comment": fake.text(max_nb_chars=200),
                "created_at": datetime.now(timezone.utc),
            }
        )
    await db.reviews.insert_many(reviews)
    print("Seeded 10,000 reviews.")
    return reviews


async def seed_orders(user_ids, product_ids):
    orders = []
    for _ in range(10000):
        orders.append(
            {
                "_id": ObjectId(),
                "user_id": fake.random_element(user_ids),
                "items": [
                    {
                        "product_id": fake.random_element(product_ids),
                        "quantity": fake.random_int(min=1, max=5),
                    }
                ],
                "status": fake.random_element(
                    ["PENDING", "ORDERED", "SHIPPED", "DELIVERED", "CANCELLED"]
                ),
                "created_at": datetime.now(timezone.utc),
            }
        )
    await db.orders.insert_many(orders)
    print("Seeded 10,000 orders.")
    return orders


async def update_interconnections(reviews, user_ids, product_ids):
    # Update products with review IDs
    for review in reviews:
        await db.products.update_one(
            {"_id": review["product_id"]},
            {"$push": {"review_ids": review["_id"]}},
        )
    print("Updated products with review IDs.")

    # Update users with review IDs
    for review in reviews:
        await db.users.update_one(
            {"_id": review["user_id"]},
            {"$push": {"review_ids": review["_id"]}},
        )
    print("Updated users with review IDs.")


async def main():
    user_ids = await seed_users()
    product_ids = await seed_products()

    reviews = await seed_reviews(user_ids, product_ids)
    await seed_orders(user_ids, product_ids)

    await update_interconnections(reviews, user_ids, product_ids)

    print("Database seeding completed.")


if __name__ == "__main__":
    asyncio.run(main())
