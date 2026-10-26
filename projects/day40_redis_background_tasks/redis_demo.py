
import redis


client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)


def main():
    print("DAY 40 — REDIS BASICS")

    print("\n1. CONNECTION")
    print("Redis PING:", client.ping())

    key = "day40:demo:message"

    print("\n2. SET VALUE")

    client.set(
        key,
        "Hello from Python",
        ex=120,
    )

    print("Value stored")

    print("\n3. GET VALUE")
    print("Value:", client.get(key))

    print("\n4. CHECK TTL")
    print("Remaining seconds:", client.ttl(key))

    print("\n5. DELETE VALUE")
    print("Keys deleted:", client.delete(key))

    print("\n6. VERIFY DELETION")
    print("Value after deletion:", client.get(key))

    print("\nREDIS BASIC TEST COMPLETED")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()
