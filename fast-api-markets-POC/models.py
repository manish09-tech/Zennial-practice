from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    customer_id: str
    
class AddCartRequest(BaseModel):
    customer_id: str
    product: int
    
class RemoveCartRequest(BaseModel):
    customer_id: str
    product: int
