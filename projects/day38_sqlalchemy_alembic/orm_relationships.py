from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import engine
from models import Customer, Order


def main():
    with Session(engine) as session:

        statement = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.product),
            )
            .order_by(Order.id)
        )

        orders = session.scalars(statement).all()

        print("\nORDER REPORT")
        print("-" * 60)

        for order in orders:
            total = order.product.price * order.quantity

            print("Customer:", order.customer.name)
            print("City:", order.customer.city)
            print("Product:", order.product.name)
            print("Quantity:", order.quantity)
            print("Order total:", total)
            print("-" * 60)

        print("\nCUSTOMER ORDER COUNTS")

        statement = (
            select(Customer)
            .options(selectinload(Customer.orders))
            .order_by(Customer.id)
        )

        customers = session.scalars(statement).all()

        for customer in customers:
            print(
                f"{customer.name}: "
                f"{len(customer.orders)} order(s)"
            )


if __name__ == "__main__":
    main()