// src/contexts/ChatContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';
import api from '../services/api';

// Create context
const ChatContext = createContext();

// Custom hook for using the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [products, setProducts] = useState([]);
  
  // Send message to API and handle response
  const sendMessage = useCallback(async (messageText) => {
    if (!messageText.trim()) return;
    
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      content: messageText,
      isUser: true,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    
    try {
      // Use the correct API endpoint and body format for your backend
      const response = await api.post('/chat/query', { message: messageText });
      
      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        content: response.data.message, // Access message directly from response.data
        isUser: false,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, botMessage]);
      
      // Update recommended products if any
      if (response.data.products && response.data.products.length > 0) {
        setProducts(response.data.products);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        content: error.response?.data?.detail || "I'm having trouble connecting. Please try again.",
        isUser: false,
        error: true,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  }, []);
  
  // Clear chat history
  const clearChat = useCallback(() => {
    setMessages([]);
    setProducts([]);
  }, []);
  
  // Context value
  const value = {
    messages,
    isTyping,
    products,
    sendMessage,
    clearChat
  };
  
  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};
