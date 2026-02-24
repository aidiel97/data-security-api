from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.database.connection import get_database
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/books", tags=["Books"])

# Helper function to convert MongoDB document to response
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "description": book["description"],
        "price": book["price"],
        "category": book["category"],
        "stock": book["stock"],
        "created_at": book["created_at"],
        "updated_at": book["updated_at"]
    }

# CREATE - Add new book
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    db = await get_database()
    
    book_dict = book.dict()
    book_dict["created_at"] = datetime.utcnow()
    book_dict["updated_at"] = datetime.utcnow()
    
    result = await db.books.insert_one(book_dict)
    
    created_book = await db.books.find_one({"_id": result.inserted_id})
    
    return BookResponse(**book_helper(created_book))

# READ - Get all products with optional filters
@router.get("/", response_model=List[BookResponse])
async def get_products():
    db = await get_database()
    
    # Execute query with pagination
    cursor = db.products.find().sort("created_at", -1)
    products = await cursor.to_list()
    
    return [BookResponse(**product_helper(product)) for product in products]