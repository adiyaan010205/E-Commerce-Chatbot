from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.auth import get_current_user
from ..models.cart import CartItem
from ..models.user import User
from ..models.product import Product
from ..schemas.cart import CartItemCreate, CartItemResponse

router = APIRouter(tags=["cart"])

@router.post("/add", response_model=CartItemResponse)
async def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already exists in cart
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        # Update quantity if item exists
        cart_item.quantity += item.quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == product_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.put("/update/{product_id}")
async def update_cart_item(
    product_id: int,
    quantity: int = Query(..., ge=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == product_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/items", response_model=List[CartItemResponse])
async def get_cart_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return cart_items

@router.delete("/clear")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared successfully"} 