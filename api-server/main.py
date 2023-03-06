from fastapi import FastAPI
from dotenv import load_dotenv
import os

from .database.db import SessionLocal, engine
from .database import models

# Create tables if does not exists using models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()

@app.get("/")
async def root():
    return {"message": "Hello World!"}