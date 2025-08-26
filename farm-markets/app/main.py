from fastapi import FastAPI
from app.routers import users, farmers, buyers, products, orders

app = FastAPI(title="Farm Markets API")

# include routers
app.include_router(users.router)
app.include_router(farmers.router)
app.include_router(buyers.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Farm Markets API"}
