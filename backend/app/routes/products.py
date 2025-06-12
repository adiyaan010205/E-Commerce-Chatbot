from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from ..core.database import get_db
from ..models.product import Product
from ..models.user import User
from ..schemas.product import ProductResponse, ProductSearch
from .auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    brand: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_active == True)
    
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    
    if search:
        query = query.filter(
            or_(
                Product.title.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/categories/", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return [category[0] for category in categories if category[0]]

@router.get("/brands/", response_model=List[str])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Product.brand).distinct().all()
    return [brand[0] for brand in brands if brand[0]]
