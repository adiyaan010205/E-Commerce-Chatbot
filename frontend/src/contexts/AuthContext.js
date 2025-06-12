// src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

// Create context
const AuthContext = createContext();

// Custom hook for using the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoadingAuth] = useState(true);
  
  // Check if user is authenticated on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      const token = localStorage.getItem('token');

      if (token) {
        try {
          const response = await api.get('/auth/me');
          setUser(response.data);
        } catch (error) {
          console.error('Authentication check failed:', error);
          localStorage.removeItem('token');
        } 
      }
      
      setLoadingAuth(false);
    };
    
    checkAuthStatus();
  }, []);
  
  // Login function
  const login = async (email, password) => {
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);

      // Get user data
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);

      return { success: true, user: userResponse.data };
    } catch (error) {
      console.error('Login error:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };
  
  // Register function
  const register = async (userData) => {
    try {
      const response = await api.post('/auth/register', {
        email: userData.email,
        password: userData.password,
        first_name: userData.first_name,
        last_name: userData.last_name
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration error:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed. Please check your input and try again.' 
      };
    }
  };
  
  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };
  
  // Context value
  const value = {
    user,
    loading: setLoadingAuth,
    isAuthenticated: !!user,
    login,
    register,
    logout
  };
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
