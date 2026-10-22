from sqlalchemy.orm import Session

from database import engine
from models import Product


def main():
    with Session(engine) as session:
        laptop = session.get(Product, 1)

        if laptop is None:
            raise RuntimeError("Laptop product not found")

        original_stock = laptop.stock

        print("1. Original stock:", original_stock)

        try:
            laptop.stock -= 2

            # Sends UPDATE to PostgreSQL,
            # but does NOT commit it.
            session.flush()

            print("2. Stock after flush:", laptop.stock)

        finally:
            # Undo this transaction even if an error occurs.
            session.rollback()
            print("3. Transaction rolled back")

    # Read through a new database session.
    with Session(engine) as session:
        laptop = session.get(Product, 1)

        print("4. Stock after rollback:", laptop.stock)

        assert laptop.stock == original_stock

    print("PASS: Uncommitted stock change was undone")


if __name__ == "__main__":
    main()