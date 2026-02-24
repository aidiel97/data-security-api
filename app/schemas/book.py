from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(..., ge=0)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True