from fastapi import FastAPI
from models import ProductCreate
from services import product_service

app = FastAPI()

@app.post("/products")
def create_product(product: ProductCreate):
    pro_id= product_service.create_product(product)
    return {"id": pro_id, "message" : "product created"}

@app.get("/products")
def list_products():
    return product_service.get_all_products()

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return product_service.get_product_by_id(product_id)

@app.delete("/delete-product/{product_id}")
def del_product(product_id: int):
    product_service.delete_product(product_id)
    return {"message": "deleted"}