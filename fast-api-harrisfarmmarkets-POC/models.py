from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: int


class ProductUpdate(BaseModel):
    name: str
    price: int


class AddToCartRequest(BaseModel):
    product_id : int
    quantity: int


class UpdateCartRequest(BaseModel):
    quantity: int