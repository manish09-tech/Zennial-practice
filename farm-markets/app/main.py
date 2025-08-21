from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="Farm Markets API")

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Farm Markets API"}
