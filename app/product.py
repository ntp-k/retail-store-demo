from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.auth import verify_api_key

product_router = APIRouter(prefix="/products", dependencies=[Depends(verify_api_key)])

class Product(BaseModel):
    id: int
    name: str
    description: str = ""
    price: float

# Demo product list (house items)
products = [
    Product(id=1, name="Chair", description="Wooden dining chair", price=49.99),
    Product(id=2, name="Table", description="Dining table for 4", price=199.99),
    Product(id=3, name="Sofa", description="3-seater sofa", price=499.99),
    Product(id=4, name="Lamp", description="Desk lamp with LED light", price=29.99),
    Product(id=5, name="Bookshelf", description="5-shelf wooden bookshelf", price=89.99),
    Product(id=6, name="Bed Frame", description="Queen size bed frame", price=299.99),
    Product(id=7, name="Wardrobe", description="2-door wardrobe", price=399.99),
    Product(id=8, name="Curtains", description="Set of 2 curtains", price=39.99),
    Product(id=9, name="Carpet", description="Living room carpet", price=59.99),
    Product(id=10, name="Coffee Table", description="Glass top coffee table", price=129.99),
]

def find_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return None

@product_router.get("/", response_model=List[Product])
def list_products():
    return products

@product_router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.post("/", response_model=Product, status_code=201)
def create_product(product: Product):
    if find_product(product.id):
        raise HTTPException(status_code=400, detail="Product ID already exists")
    products.append(product)
    return product

@product_router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, updated: Product):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = updated.name
    product.description = updated.description
    product.price = updated.price
    return product

@product_router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products.remove(product)
