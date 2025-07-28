from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
from app.auth import verify_api_key

product_router = APIRouter(prefix="/products", dependencies=[Depends(verify_api_key)])

# In-memory product storage
products = {}

class Product(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int

class ProductResponse(Product):
    id: str

@product_router.get("/", response_model=list[ProductResponse])
def list_products():
    return [{"id": pid, **data} for pid, data in products.items()]

@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **product}

@product_router.post("/", response_model=ProductResponse)
def create_product(product: Product):
    product_id = str(uuid4())
    products[product_id] = product.dict()
    return {"id": product_id, **product.dict()}

@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = product.dict()
    return {"id": product_id, **product.dict()}

@product_router.delete("/{product_id}")
def delete_product(product_id: str):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return {"message": f"Product {product_id} deleted"}
