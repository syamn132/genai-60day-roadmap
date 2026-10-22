from fastapi import FastAPI, HTTPException, Query, status
from sqlalchemy import select

from dependencies import DBSession
from models import Product
from schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
)

app = FastAPI(
    title="Day 38 - SQLAlchemy Product API",
    version="1.0.0",
)

# ----------------------------------------
# HEALTH CHECK
# ----------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

# ----------------------------------------
# CREATE
# ----------------------------------------

@app.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    session: DBSession,
):
    product = Product(**data.model_dump())

    session.add(product)

    try:
        session.commit()
        session.refresh(product)
    except Exception:
        session.rollback()
        raise

    return product

# ----------------------------------------
# READ ALL
# ----------------------------------------

@app.get(
    "/products",
    response_model=list[ProductRead],
)
def list_products(
    session: DBSession,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    statement = (
        select(Product)
        .order_by(Product.id)
        .offset(skip)
        .limit(limit)
    )

    return session.scalars(statement).all()

# ----------------------------------------
# READ ONE
# ----------------------------------------

@app.get(
    "/products/{product_id}",
    response_model=ProductRead,
)
def get_product(
    product_id: int,
    session: DBSession,
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product

# ----------------------------------------
# PARTIAL UPDATE
# ----------------------------------------

@app.patch(
    "/products/{product_id}",
    response_model=ProductRead,
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    session: DBSession,
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    changes = data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )

        setattr(product, field, value)

    try:
        session.commit()
        session.refresh(product)
    except Exception:
        session.rollback()
        raise

    return product

# ----------------------------------------
# DELETE
# ----------------------------------------

@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    session: DBSession,
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # Day 38 practice safeguard.
    # Only temporary API-practice products can
    # be removed through this training endpoint.
    if not product.name.startswith("API Practice"):
        raise HTTPException(
            status_code=403,
            detail="Only API Practice products can be deleted",
        )

    session.delete(product)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return None