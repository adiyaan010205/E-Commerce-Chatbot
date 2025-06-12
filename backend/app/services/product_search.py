from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from ..models.product import Product

class ProductSearchService:
    def __init__(self, db: Session):
        self.db = db

    def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Product]:
        """Search products with various filters"""
        
        db_query = self.db.query(Product).filter(Product.is_active == True)
        
        # Text search
        if query:
            db_query = db_query.filter(
                or_(
                    Product.title.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                    Product.category.ilike(f"%{query}%"),
                    Product.brand.ilike(f"%{query}%")
                )
            )
        
        # Category filter
        if category:
            db_query = db_query.filter(Product.category.ilike(f"%{category}%"))
        
        # Price range filters
        if min_price is not None:
            db_query = db_query.filter(Product.price >= min_price)
        
        if max_price is not None:
            db_query = db_query.filter(Product.price <= max_price)
        
        # Brand filter
        if brand:
            db_query = db_query.filter(Product.brand.ilike(f"%{brand}%"))
        
        # Order by relevance (rating, then by newest)
        db_query = db_query.order_by(Product.rating.desc(), Product.created_at.desc())
        
        return db_query.offset(offset).limit(limit).all()

    def get_categories(self) -> List[str]:
        """Get all unique product categories"""
        categories = self.db.query(Product.category).distinct().all()
        return [cat[0] for cat in categories if cat[0]]

    def get_brands(self) -> List[str]:
        """Get all unique product brands"""
        brands = self.db.query(Product.brand).distinct().all()
        return [brand[0] for brand in brands if brand[0]]

    def get_popular_products(self, limit: int = 10) -> List[Product]:
        """Get popular products based on rating"""
        return self.db.query(Product)\
            .filter(Product.is_active == True)\
            .order_by(Product.rating.desc())\
            .limit(limit).all()

    def get_products_by_category(self, category: str, limit: int = 10) -> List[Product]:
        """Get products by specific category"""
        return self.db.query(Product)\
            .filter(and_(
                Product.is_active == True,
                Product.category.ilike(f"%{category}%")
            ))\
            .order_by(Product.rating.desc())\
            .limit(limit).all()
