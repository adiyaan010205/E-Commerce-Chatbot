// src/components/ChatInterface.js
import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../contexts/ChatContext';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const ChatInterface = () => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const [notification, setNotification] = useState(null);

  const { messages, isTyping, products, sendMessage, clearChat } = useChat();
  const { cartItems, addToCart, getCartTotal } = useCart();
  const { logout } = useAuth();

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => {
      setNotification(null);
    }, 3000); // Notification disappears after 3 seconds
  };
  
  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    await sendMessage(input);
    setInput('');
  };
  
  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat?')) {
      clearChat();
    }
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to log out?')) {
      logout();
    }
  };

  const handleAddToCart = async (product) => {
    const result = await addToCart(product);
    if (result.success) {
      showNotification('Product added to cart successfully!', 'success');
      console.log('Product added to cart successfully');
    } else {
      showNotification(result.error || 'Failed to add product to cart', 'error');
      console.error('Failed to add product to cart:', result.error);
    }
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-50 relative">
      {notification && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg text-white z-50 transition-opacity duration-300 ${notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'} opacity-100`}>
          {notification.message}
        </div>
      )}

      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 flex justify-between items-center shadow-sm">
        <h1 className="text-xl font-semibold text-gray-800">E-commerce Chatbot</h1>
        <div className="flex items-center space-x-4">
          <div className="relative cursor-pointer" onClick={() => navigate('/cart')}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            {cartItems.length > 0 && (
              <span className="absolute -top-2 -right-2 bg-primary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center animate-bounce-once">
                {cartItems.length}
              </span>
            )}
          </div>
          <button
            onClick={handleClearChat}
            className="px-3 py-1 text-sm text-danger-600 hover:bg-danger-50 rounded transition duration-150 ease-in-out"
          >
            Clear Chat
          </button>
          <button
            onClick={handleLogout}
            className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition duration-150 ease-in-out"
          >
            Logout
          </button>
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md p-3 rounded-lg shadow-md transition-all duration-300 ease-in-out transform ${msg.isUser ? 'bg-primary-500 text-white' : msg.error ? 'bg-danger-100 text-danger-800 border border-danger-200' : 'bg-gray-100 text-gray-800'}`}
            >
              <p>{msg.content}</p>
              <span className="block text-xs opacity-75 mt-1">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-lg shadow-sm">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Product Recommendations */}
      {products.length > 0 && (
        <div className="p-4 border-t border-gray-200 bg-white shadow-inner">
          <h2 className="text-lg font-medium mb-3 text-gray-800">Recommended Products</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {products.map((product) => (
              <div key={product.id} className="border border-gray-200 rounded-lg p-3 shadow-md transform transition-all duration-300 ease-in-out hover:scale-105">
                <h3 className="font-medium text-gray-900">{product.title}</h3>
                <p className="text-sm text-gray-600 mb-2">{product.category}</p>
                <div className="flex justify-between items-center mt-2">
                  <span className="font-bold text-primary-600">${product.price}</span>
                  <button 
                    onClick={() => handleAddToCart(product)}
                    className="bg-primary-500 text-white px-3 py-1 rounded text-sm hover:bg-primary-600 transition duration-150 ease-in-out"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Input Form */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm transition duration-150 ease-in-out"
            disabled={isTyping}
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="group relative flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition duration-150 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
