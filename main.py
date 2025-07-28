from fastapi import FastAPI
from app.cart import cart_router
from app.catalog import catalog_router
from app.product import product_router
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(openapi_version="3.0.3", docs_url=None)

@app.get("/")
def root():
    return {"message": "Welcome to retail-store-demo"}

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/swagger.json", title="Retail Store API")

@app.get("/swagger.json", include_in_schema=False)
def openapi_spec():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="Retail Store API", version="1.0", routes=app.routes)

app.include_router(cart_router)
app.include_router(catalog_router)
app.include_router(product_router)