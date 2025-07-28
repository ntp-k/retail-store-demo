from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import verify_api_key
from typing import List

catalog_router = APIRouter(prefix="/catalog", dependencies=[Depends(verify_api_key)])

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str = ""

# In-memory "database"
products = {
    1: {"name": "Vacuum Cleaner", "price": 150.0, "description": "Powerful vacuum for home use"},
    2: {"name": "Microwave Oven", "price": 120.0, "description": "800W microwave oven"},
    3: {"name": "Coffee Maker", "price": 80.0, "description": "Automatic drip coffee maker"},
    4: {"name": "Blender", "price": 60.0, "description": "High-speed blender"},
    5: {"name": "Air Purifier", "price": 200.0, "description": "Removes dust and allergens"},
    6: {"name": "Toaster", "price": 40.0, "description": "2-slice toaster"},
    7: {"name": "Electric Kettle", "price": 30.0, "description": "Fast boiling kettle"},
    8: {"name": "Iron", "price": 50.0, "description": "Steam iron for clothes"},
    9: {"name": "Ceiling Fan", "price": 90.0, "description": "3-speed ceiling fan"},
    10: {"name": "Desk Lamp", "price": 25.0, "description": "LED desk lamp"},
}

# Helper to get next id
def next_product_id():
    return max(products.keys()) + 1 if products else 1

@catalog_router.get("/", response_model=List[Product])
def list_products():
    return [
        Product(id=pid, **data)
        for pid, data in products.items()
    ]

@catalog_router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(id=product_id, **product)

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str = ""

@catalog_router.post("/", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    pid = next_product_id()
    products[pid] = product.dict()
    return Product(id=pid, **products[pid])

@catalog_router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    products[product_id] = product.dict()
    return Product(id=product_id, **products[product_id])

@catalog_router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return
