from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[str] = None
    brand: Optional[str] = None
    rating: float = 0.0
    stock_quantity: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProductSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brand: Optional[str] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0
