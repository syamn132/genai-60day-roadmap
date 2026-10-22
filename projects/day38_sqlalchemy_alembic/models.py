# from datetime import datetime
# from decimal import Decimal

# from sqlalchemy import (
#     DateTime,
#     Identity,
#     Integer,
#     Numeric,
#     String,
#     text,
# )
# from sqlalchemy.orm import (
#     DeclarativeBase,
#     Mapped,
#     mapped_column,
# )

# class Base(DeclarativeBase):
#     pass

# class Product(Base):
#     __tablename__ = "products"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         Identity(always=True),
#         primary_key=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String(100),
#         nullable=False,
#     )

#     price: Mapped[Decimal] = mapped_column(
#         Numeric(12, 2),
#         nullable=False,
#     )

#     stock: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#         server_default=text("0"),
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP"),
#     )

#     def __repr__(self):
#         return (
#             f"Product(id={self.id}, "
#             f"name={self.name!r}, "
#             f"price={self.price}, "
#             f"stock={self.stock})"
#         )


# Updated models.py with additional classes for Customer and Order, including relationships and constraints.

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Text,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price > 0", name="products_price_check"),
        CheckConstraint("stock >= 0", name="products_stock_check"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="product"
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    def __repr__(self):
        return (
            f"Product(id={self.id}, "
            f"name={self.name!r}, "
            f"price={self.price}, "
            f"stock={self.stock})"
        )


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer"
    )


class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="orders_quantity_check"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="orders"
    )

    product: Mapped["Product"] = relationship(
        back_populates="orders"
    )