from fastapi import FastAPI
from app.routers import users, farmers, products

app = FastAPI(title="Farm Markets API")

app.include_router(users.router)
app.include_router(farmers.router)
app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Farm Markets API"}
