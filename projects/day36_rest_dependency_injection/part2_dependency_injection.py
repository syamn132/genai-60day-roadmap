from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status,
)

from pydantic import BaseModel


app = FastAPI(
    title=(
        "Day 36 Dependency "
        "Injection API"
    ),
    version="1.0.0",
)


# --------------------------------------------------
# Models
# --------------------------------------------------

class Product(
    BaseModel
):

    id: int
    name: str
    price: float
    stock: int


class Pagination(
    BaseModel
):

    skip: int
    limit: int


# --------------------------------------------------
# Service
# --------------------------------------------------

class ProductService:

    def __init__(
        self,
    ):

        self._products = {
            1: {
                "id": 1,
                "name": "Laptop",
                "price": 65000,
                "stock": 10,
            },

            2: {
                "id": 2,
                "name": "Mouse",
                "price": 500,
                "stock": 25,
            },

            3: {
                "id": 3,
                "name": "Keyboard",
                "price": 1500,
                "stock": 15,
            },
        }


    def get_all(
        self,
        skip: int,
        limit: int,
    ):

        products = list(
            self._products.values()
        )

        return products[
            skip:
            skip + limit
        ]


    def get_by_id(
        self,
        product_id: int,
    ):

        return self._products.get(
            product_id
        )


# --------------------------------------------------
# Product service dependency
# --------------------------------------------------

product_service = ProductService()


def get_product_service(
) -> ProductService:

    print(
        "[DEPENDENCY] "
        "Providing ProductService"
    )

    return product_service


ProductServiceDep = Annotated[
    ProductService,
    Depends(
        get_product_service
    ),
]


# --------------------------------------------------
# Pagination dependency
# --------------------------------------------------

def get_pagination(
    skip: int = Query(
        default=0,
        ge=0,
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),

) -> Pagination:

    print(
        "[DEPENDENCY] "
        f"Pagination skip={skip}, "
        f"limit={limit}"
    )


    return Pagination(
        skip=skip,
        limit=limit,
    )


PaginationDep = Annotated[
    Pagination,
    Depends(
        get_pagination
    ),
]


# --------------------------------------------------
# Resource dependency with lifecycle
# --------------------------------------------------

class DemoResource:

    def __init__(
        self,
    ):

        self.connected = True


    def close(
        self,
    ):

        self.connected = False


def get_demo_resource():

    resource = DemoResource()


    print(
        "[DEPENDENCY] "
        "Opening resource"
    )


    try:

        yield resource


    finally:

        resource.close()

        print(
            "[DEPENDENCY] "
            "Closing resource"
        )


DemoResourceDep = Annotated[
    DemoResource,
    Depends(
        get_demo_resource
    ),
]


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get(
    "/health"
)
async def health():

    return {
        "status": "ok"
    }


# --------------------------------------------------
# List products
# --------------------------------------------------

@app.get(
    "/products",
    response_model=list[Product],
)
async def get_products(
    service: ProductServiceDep,
    pagination: PaginationDep,
):

    return service.get_all(
        skip=pagination.skip,
        limit=pagination.limit,
    )


# --------------------------------------------------
# Get product
# --------------------------------------------------

@app.get(
    "/products/{product_id}",
    response_model=Product,
)
async def get_product(
    product_id: int,
    service: ProductServiceDep,
):

    product = service.get_by_id(
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


# --------------------------------------------------
# Resource lifecycle demo
# --------------------------------------------------

@app.get(
    "/resource-demo"
)
async def resource_demo(
    resource: DemoResourceDep,
):

    print(
        "[ENDPOINT] "
        "Using resource"
    )


    return {
        "connected":
            resource.connected
    }