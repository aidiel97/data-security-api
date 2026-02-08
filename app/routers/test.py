from fastapi import APIRouter, Depends
from app.database.connection import get_database

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/")
async def test_endpoint():
    return {"message": "Test router works!"}

@router.get("/db")
async def test_database():
    db = await get_database()
    # Insert test document
    result = await db.test_collection.insert_one({"test": "data"})
    return {"message": "Database works!", "id": str(result.inserted_id)}