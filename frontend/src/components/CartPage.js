import React, { useState } from 'react';
import { useCart } from '../contexts/CartContext';
import { useNavigate } from 'react-router-dom';

const CartPage = () => {
  const { cartItems, getCartTotal, removeFromCart, updateQuantity } = useCart();
  const navigate = useNavigate();
  const [notification, setNotification] = useState(null);

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => {
      setNotification(null);
    }, 3000); // Notification disappears after 3 seconds
  };

  const handleRemoveClick = async (productId) => {
    const result = await removeFromCart(productId);
    if (result.success) {
      showNotification('Item removed from cart', 'success');
    } else {
      showNotification(result.error || 'Failed to remove item', 'error');
    }
  };

  const handleUpdateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) return; // Prevent quantity from going below 1

    const result = await updateQuantity(productId, newQuantity);
    if (result.success) {
      showNotification('Cart updated successfully', 'success');
    } else {
      showNotification(result.error || 'Failed to update quantity', 'error');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 p-4 relative">
      {notification && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg text-white z-50 transition-opacity duration-300 ${notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'} opacity-100`}>
          {notification.message}
        </div>
      )}

      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 flex justify-between items-center shadow-sm mb-4">
        <h1 className="text-xl font-semibold text-gray-800">Your Shopping Cart</h1>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 text-sm bg-primary-500 text-white rounded hover:bg-primary-600 transition duration-150 ease-in-out"
        >
          Back to Chat
        </button>
      </div>

      {/* Cart Items */}
      <div className="flex-1 overflow-y-auto space-y-4">
        {cartItems.length === 0 ? (
          <p className="text-center text-gray-600">Your cart is empty.</p>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {cartItems.map((item) => (
              <div key={item.id} className="bg-white border border-gray-200 rounded-lg p-4 shadow-md flex items-center space-x-4 transition-all duration-300 ease-in-out transform hover:scale-[1.01]">
                <img src={item.image_url || 'https://via.placeholder.com/100'} alt={item.title} className="w-20 h-20 object-cover rounded-md" />
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900">{item.title}</h3>
                  <p className="text-sm text-gray-600">${item.price.toFixed(2)}</p>
                  <div className="flex items-center mt-2">
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      className="px-2 py-1 bg-gray-200 rounded-l hover:bg-gray-300 transition-all duration-150 ease-in-out"
                    >
                      -
                    </button>
                    <span className="px-3 py-1 border-t border-b border-gray-200 text-sm">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      className="px-2 py-1 bg-gray-200 rounded-r hover:bg-gray-300 transition-all duration-150 ease-in-out"
                    >
                      +
                    </button>
                    <button
                      onClick={() => handleRemoveClick(item.id)}
                      className="ml-4 text-danger-600 hover:text-danger-800 text-sm transition-colors duration-150 ease-in-out"
                    >
                      Remove
                    </button>
                  </div>
                </div>
                <span className="font-bold text-primary-600 text-lg">
                  ${(item.price * item.quantity).toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Cart Summary */}
      {cartItems.length > 0 && (
        <div className="bg-white border-t border-gray-200 p-4 shadow-md mt-4">
          <div className="flex justify-between items-center">
            <span className="text-lg font-semibold text-gray-800">Total:</span>
            <span className="text-xl font-bold text-primary-700">${getCartTotal().toFixed(2)}</span>
          </div>
          <button className="mt-4 w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 transition duration-150 ease-in-out">
            Proceed to Checkout
          </button>
        </div>
      )}
    </div>
  );
};

export default CartPage; 