from sqlalchemy import text

from database import engine


def main():
    with engine.connect() as connection:

        # Check which database we connected to
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        print("Connected database:", database_name)

        # Count existing products
        product_count = connection.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar_one()

        print("Total products:", product_count)

        # Read the existing products
        result = connection.execute(
            text(
                """
                SELECT id, name, price, stock
                FROM products
                ORDER BY id
                """
            )
        )

        print("\nExisting products:")

        for row in result:
            print(
                f"ID={row.id}, "
                f"Name={row.name}, "
                f"Price={row.price}, "
                f"Stock={row.stock}"
            )


if __name__ == "__main__":
    try:
        main()
    finally:
        engine.dispose()