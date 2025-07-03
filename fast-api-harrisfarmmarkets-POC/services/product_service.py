import database
from fastapi import HTTPException
from models import ProductCreate, ProductUpdate

def create_product(product: ProductCreate):
    product_id= database.product_id_counter
    database.products[product_id] = {"name" : product.name, "price" : product.price}
    database.product_id_counter+=1
    return product_id

def get_all_products():
    return database.products

def get_product_by_id(product_id: int):
    product = database.products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product

def delete_product(product_id: int):
    if product_id not in database.products:
        raise HTTPException(status_code=404, detail="Not found")
    del database.products[product_id]
    return product_id