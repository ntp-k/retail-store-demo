from fastapi import APIRouter, Depends
from app.auth import verify_api_key

cart_router = APIRouter(prefix="/cart", dependencies=[Depends(verify_api_key)])
cart = {}

@cart_router.post("/add")
def add_to_cart(item_id: str, quantity: int):
    cart[item_id] = cart.get(item_id, 0) + quantity
    return {"message": "Item added", "cart": cart}

@cart_router.get("/")
def view_cart():
    return {"cart": cart}
