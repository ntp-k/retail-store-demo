from fastapi import APIRouter, Depends
from app.auth import verify_api_key

catalog_router = APIRouter(prefix="/catalog", dependencies=[Depends(verify_api_key)])

catalog = {
    "item001": {"name": "Laptop", "price": 1000},
    "item002": {"name": "Mouse", "price": 25}
}

@catalog_router.get("/")
def list_catalog():
    return {"catalog": catalog}
