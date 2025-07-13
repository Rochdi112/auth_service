# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Auth Service",
    version="1.0",
    lifespan=lifespan
)

# Inclusion des routes
app.include_router(router)
