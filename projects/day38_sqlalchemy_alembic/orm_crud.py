from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from database import engine
from models import Product


def main():
    practice_id = None

    try:
        # ---------------------------------------
        # CREATE: INSERT a new product
        # ---------------------------------------
        with Session(engine) as session:
            product = Product(
                name=f"ORM Practice {uuid4().hex[:8]}",
                price=Decimal("299.00"),
                stock=5,
            )

            session.add(product)

            # Executes INSERT, generating the ID
            # without committing yet.
            session.flush()

            practice_id = product.id

            print("\n1. CREATE")
            print("New product ID:", practice_id)

            session.commit()
            print("INSERT committed successfully")

        # ---------------------------------------
        # READ: Retrieve product by primary key
        # ---------------------------------------
        with Session(engine) as session:
            product = session.get(Product, practice_id)

            print("\n2. READ")
            print(product)

        # ---------------------------------------
        # UPDATE: Change product stock
        # ---------------------------------------
        with Session(engine) as session:
            product = session.get(Product, practice_id)

            product.stock = 8

            # SQLAlchemy detects the changed value.
            session.commit()

            print("\n3. UPDATE")
            print("Stock updated and committed")

        # ---------------------------------------
        # VERIFY: Open a fresh session
        # ---------------------------------------
        with Session(engine) as session:
            product = session.get(Product, practice_id)

            print("\n4. VERIFY UPDATE")
            print(product)

    finally:
        # ---------------------------------------
        # DELETE: Clean up only our test product
        # ---------------------------------------
        if practice_id is not None:
            with Session(engine) as session:
                product = session.get(Product, practice_id)

                if product is not None:
                    session.delete(product)
                    session.commit()
                    print("\n5. DELETE")
                    print("Practice product deleted")

            # -----------------------------------
            # VERIFY: Product no longer exists
            # -----------------------------------
            with Session(engine) as session:
                deleted = session.get(Product, practice_id)

                print("\n6. VERIFY DELETE")
                print("Product after deletion:", deleted)


if __name__ == "__main__":
    main()