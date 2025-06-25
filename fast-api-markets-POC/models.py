from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    customer_id: str
    
class AddCartRequest(BaseModel):
    customer_id: str
    products:int
    
class RemoveCartRequest(BaseModel):
    customer_id: str
    products:int
