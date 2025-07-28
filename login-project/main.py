from fastapi import FastAPI
from contextlib import asynccontextmanager
from login import router as auth_router
import logging

# Set up logger
logger = logging.getLogger("auth_app")
logger.setLevel(logging.INFO)

# File Handler
file_handler = logging.FileHandler("user.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI application started")
    yield
    logger.info("FastAPI application stopped")

app = FastAPI(lifespan=lifespan)

# Register Auth Router
app.include_router(auth_router)
