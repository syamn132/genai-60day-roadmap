from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Product

def main():

    with Session(engine) as session:

        print("\n1. ALL PRODUCTS")

        statement = (
            select(Product)
            .order_by(Product.id)
        )

        products = session.scalars(statement).all()

        for product in products:
            print(product)

        print("\n2. PRODUCTS PRICE > 1000")

        statement = (
            select(Product)
            .where(Product.price > 1000)
            .order_by(Product.price.desc())
        )

        expensive_products = session.scalars(
            statement
        ).all()

        for product in expensive_products:
            print(product.name, product.price)

        print("\n3. PRODUCT BY PRIMARY KEY")

        laptop = session.get(Product, 1)

        if laptop is not None:
            print(laptop)
        else:
            print("Product not found")


if __name__ == "__main__":
    main()