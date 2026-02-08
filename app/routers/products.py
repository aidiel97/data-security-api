from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.database.connection import get_database
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/products", tags=["Products"])

# Helper function to convert MongoDB document to response
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "stock": product["stock"],
        "created_at": product["created_at"],
        "updated_at": product["updated_at"]
    }

# CREATE - Add new product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product with all the information:
    
    - **name**: Product name (required)
    - **description**: Product description (required)
    - **price**: Product price, must be greater than 0 (required)
    - **category**: Product category (required)
    - **stock**: Available stock, must be >= 0 (required)
    """
    db = await get_database()
    
    product_dict = product.dict()
    product_dict["created_at"] = datetime.utcnow()
    product_dict["updated_at"] = datetime.utcnow()
    
    result = await db.products.insert_one(product_dict)
    
    created_product = await db.products.find_one({"_id": result.inserted_id})
    
    return ProductResponse(**product_helper(created_product))

# READ - Get all products with optional filters
@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None
):
    """
    Get all products with optional filtering and pagination:
    
    - **skip**: Number of products to skip (for pagination)
    - **limit**: Maximum number of products to return
    - **category**: Filter by category
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **search**: Search in name and description
    """
    db = await get_database()
    
    # Build query filter
    query = {}
    
    if category:
        query["category"] = category
    
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Execute query with pagination
    cursor = db.products.find(query).skip(skip).limit(limit).sort("created_at", -1)
    products = await cursor.to_list(length=limit)
    
    return [ProductResponse(**product_helper(product)) for product in products]

# READ - Get single product by ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get a specific product by ID
    """
    db = await get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID format"
        )
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    return ProductResponse(**product_helper(product))

# READ - Get products by category
@router.get("/category/{category_name}", response_model=List[ProductResponse])
async def get_products_by_category(
    category_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get all products in a specific category
    """
    db = await get_database()
    
    cursor = db.products.find({"category": category_name}).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found in category: {category_name}"
        )
    
    return [ProductResponse(**product_helper(product)) for product in products]

# UPDATE - Update product
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    """
    Update a product. Only provided fields will be updated.
    """
    db = await get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID format"
        )
    
    # Check if product exists
    existing_product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    # Prepare update data (only include fields that were provided)
    update_data = {k: v for k, v in product_update.dict(exclude_unset=True).items()}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update the product
    await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    
    # Fetch and return updated product
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    return ProductResponse(**product_helper(updated_product))

# UPDATE - Partial update (PATCH)
@router.patch("/{product_id}", response_model=ProductResponse)
async def partial_update_product(product_id: str, product_update: ProductUpdate):
    """
    Partially update a product. Same as PUT but semantically different.
    """
    return await update_product(product_id, product_update)

# UPDATE - Update stock
@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_stock(product_id: str, stock: int = Query(..., ge=0)):
    """
    Update only the stock quantity of a product
    """
    db = await get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID format"
        )
    
    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"stock": stock, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    return ProductResponse(**product_helper(updated_product))

# DELETE - Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """
    Delete a product permanently
    """
    db = await get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID format"
        )
    
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    return None

# DELETE - Delete multiple products
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_products(product_ids: List[str]):
    """
    Delete multiple products at once
    """
    db = await get_database()
    
    # Validate all IDs
    valid_ids = []
    for pid in product_ids:
        if ObjectId.is_valid(pid):
            valid_ids.append(ObjectId(pid))
    
    if not valid_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid product IDs provided"
        )
    
    result = await db.products.delete_many({"_id": {"$in": valid_ids}})
    
    return {
        "message": f"Deleted {result.deleted_count} products",
        "deleted_count": result.deleted_count
    }

# Additional useful endpoints

# Get product count
@router.get("/stats/count")
async def get_product_count(category: Optional[str] = None):
    """
    Get total count of products, optionally filtered by category
    """
    db = await get_database()
    
    query = {"category": category} if category else {}
    count = await db.products.count_documents(query)
    
    return {"total_products": count, "category": category}

# Get all categories
@router.get("/stats/categories")
async def get_categories():
    """
    Get list of all unique categories
    """
    db = await get_database()
    
    categories = await db.products.distinct("category")
    
    return {"categories": categories, "total": len(categories)}

# Get price statistics
@router.get("/stats/price-range")
async def get_price_range(category: Optional[str] = None):
    """
    Get min, max, and average price, optionally by category
    """
    db = await get_database()
    
    match_stage = {"$match": {"category": category}} if category else {"$match": {}}
    
    pipeline = [
        match_stage,
        {
            "$group": {
                "_id": None,
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "avg_price": {"$avg": "$price"},
                "total_products": {"$sum": 1}
            }
        }
    ]
    
    result = await db.products.aggregate(pipeline).to_list(1)
    
    if not result:
        return {"message": "No products found"}
    
    return {
        "min_price": result[0]["min_price"],
        "max_price": result[0]["max_price"],
        "avg_price": round(result[0]["avg_price"], 2),
        "total_products": result[0]["total_products"],
        "category": category
    }