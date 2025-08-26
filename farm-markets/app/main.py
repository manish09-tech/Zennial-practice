from fastapi import FastAPI
from app.routers import users, farmers

app = FastAPI(title="Farm Markets API")

app.include_router(users.router)
app.include_router(farmers.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Farm Markets API"}
