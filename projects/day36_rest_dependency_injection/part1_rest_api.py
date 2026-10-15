from fastapi import (
    FastAPI,
    HTTPException,
    status,
)

from pydantic import (
    BaseModel,
    Field,
)


app = FastAPI(
    title="Day 36 Product REST API",
    version="1.0.0",
)

# Defining the Model
class ProductCreate(
    BaseModel
):
    name: str

    price: float = Field(
        gt=0
    )

    stock: int = Field(
        ge=0
    )

# Patch Product Model
class ProductUpdate(
    BaseModel
):
    name: str | None = None

    price: float | None = Field(
        default=None,
        gt=0,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )


# Product Resposne Model
class Product(
    ProductCreate
):
    id: int


#Temp Database
products = {}

next_id = 1

#Health Check Endpoint
@app.get(
    "/health"
)
async def health():

    return {
        "status": "ok"
    }


# Create Product Endpoint
@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
):
    global next_id

    new_product = {
        "id": next_id,
        **product.model_dump(),
    }

    products[
        next_id
    ] = new_product

    next_id += 1

    return new_product

# Get Product Endpoint
@app.get(
    "/products",
    response_model=list[Product],
)
async def get_products():

    return list(
        products.values()
    )

# Read One Product Endpoint
@app.get(
    "/products/{product_id}",
    response_model=Product,
)
async def get_product(
    product_id: int,
):

    product = products.get(
        product_id
    )

    if product is None:

        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail="Product not found",
        )

    return product


# Put Product Endpoint
@app.put(
    "/products/{product_id}",
    response_model=Product,
)
async def replace_product(
    product_id: int,
    product: ProductCreate,
):

    if product_id not in products:

        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail="Product not found",
        )

    updated_product = {
        "id": product_id,
        **product.model_dump(),
    }

    products[
        product_id
    ] = updated_product

    return updated_product


# Patch Product Endpoint
@app.patch(
    "/products/{product_id}",
    response_model=Product,
)
async def update_product(
    product_id: int,
    product: ProductUpdate,
):

    existing_product = products.get(
        product_id
    )

    if existing_product is None:

        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail="Product not found",
        )

    update_data = (
        product.model_dump(
            exclude_unset=True
        )
    )

    existing_product.update(
        update_data
    )

    return existing_product


# Delete Product Endpoint
@app.delete(
    "/products/{product_id}",
    status_code=(
        status.HTTP_204_NO_CONTENT
    ),
)
async def delete_product(
    product_id: int,
):

    if product_id not in products:

        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail="Product not found",
        )

    del products[
        product_id
    ]