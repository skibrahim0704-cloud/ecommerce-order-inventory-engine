from fastapi import APIRouter, HTTPException
from mongodb.product_crud import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# CREATE PRODUCT
@router.post("/")
def add_product(product: dict):
    return create_product(product)


# GET ALL PRODUCTS
@router.get("/")
def read_products():
    return get_products()


# GET ONE PRODUCT
@router.get("/{product_id}")
def read_product(product_id: str):
    product = get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# UPDATE PRODUCT
@router.put("/{product_id}")
def edit_product(product_id: str, product: dict):
    updated = update_product(product_id, product)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product updated successfully"
    }


# DELETE PRODUCT
@router.delete("/{product_id}")
def remove_product(product_id: str):
    deleted = delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }
