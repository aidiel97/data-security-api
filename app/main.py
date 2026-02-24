from fastapi import FastAPI
from app.database.connection import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from app.routers import test
from app.routers import products
from app.routers import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="My Secure API",
    description="Learning FastAPI with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(test.router)
app.include_router(products.router)
app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}