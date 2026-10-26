
import json

import redis


client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)


# Simulated database for learning.
# This is NOT an actual PostgreSQL query.
DATABASE = {
    1: {
        "id": 1,
        "name": "Laptop",
        "price": 65000,
        "stock": 10,
    }
}


def fetch_from_database(product_id: int):
    print("[DATABASE] Fetching product")

    return DATABASE.get(product_id)


def get_product(product_id: int):
    cache_key = f"day40:product:{product_id}"

    cached = client.get(cache_key)

    if cached is not None:
        print("[CACHE HIT] Redis returned the product")
        return json.loads(cached)

    print("[CACHE MISS] Product not found in Redis")

    product = fetch_from_database(product_id)

    if product is not None:
        client.set(
            cache_key,
            json.dumps(product),
            ex=60,
        )

        print("[CACHE WRITE] Product stored for 60 seconds")

    return product


def main():
    key = "day40:product:1"

    # Make the demonstration repeatable.
    client.delete(key)

    print("\nFIRST REQUEST")
    first = get_product(1)
    print(first)

    print("\nSECOND REQUEST")
    second = get_product(1)
    print(second)

    assert first == second

    print("\nCACHE TTL")
    print(client.ttl(key))

    print("\nSIMULATE PRODUCT UPDATE")

    DATABASE[1]["stock"] = 15

    # Invalidate outdated cache.
    client.delete(key)

    print("\nREQUEST AFTER INVALIDATION")
    updated = get_product(1)
    print(updated)

    assert updated["stock"] == 15

    print("\nCACHE-ASIDE TEST COMPLETED")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()
