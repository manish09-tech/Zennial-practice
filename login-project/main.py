from fastapi import FastAPI
from login import router as auth_router
from database import collection

app = FastAPI()

# make sure the email field is unique
collection.create_index("email", unique=True)

# Include authentication routes
app.include_router(auth_router)

