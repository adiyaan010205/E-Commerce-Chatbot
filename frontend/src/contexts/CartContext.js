// src/contexts/CartContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';
import api from '../services/api';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoadingCart] = useState(false); 

  // Add item to cart
  const addToCart = useCallback(async (product) => {
    try {
      setLoadingCart(true);
      const response = await api.post('/cart/add', {
        product_id: product.id,
        quantity: 1
      });
      
      setCartItems(prevItems => {
        const existingItem = prevItems.find(item => item.id === product.id);
        if (existingItem) {
          return prevItems.map(item =>
            item.id === product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          );
        }
        return [...prevItems, { ...product, quantity: 1 }];
      });
      
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Failed to add item to cart:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to add item to cart' 
      };
    } finally {
      setLoadingCart(false);
    }
  }, []);

  // Remove item from cart
  const removeFromCart = useCallback(async (productId) => {
    try {
      setLoadingCart(true);
      await api.delete(`/cart/remove/${productId}`);
      
      setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
      return { success: true };
    } catch (error) {
      console.error('Failed to remove item from cart:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to remove item from cart' 
      };
    } finally {
      setLoadingCart(false);
    }
  }, []);

  // Update item quantity
  const updateQuantity = useCallback(async (productId, quantity) => {
    try {
      setLoadingCart(true);
      await api.put(`/cart/update/${productId}?quantity=${quantity}`);
      
      setCartItems(prevItems =>
        prevItems.map(item =>
          item.id === productId
            ? { ...item, quantity }
            : item
        )
      );
      return { success: true };
    } catch (error) {
      console.error('Failed to update cart item:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to update cart item' 
      };
    } finally {
      setLoadingCart(false);
    }
  }, []);

  // Get cart total
  const getCartTotal = useCallback(() => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  }, [cartItems]);

  // Clear cart
  const clearCart = useCallback(async () => {
    try {
      setLoadingCart(true);
      await api.delete('/cart/clear');
      setCartItems([]);
      return { success: true };
    } catch (error) {
      console.error('Failed to clear cart:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to clear cart' 
      };
    } finally {
      setLoadingCart(false);
    }
  }, []);

  const value = {
    cartItems,
    loading: setLoadingCart,
    addToCart,
    removeFromCart,
    updateQuantity,
    getCartTotal,
    clearCart
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};