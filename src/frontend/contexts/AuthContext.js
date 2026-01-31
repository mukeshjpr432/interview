import React, { useState, useContext, createContext } from 'react';
import axios from 'axios';

/**
 * Auth Context for managing user authentication state
 * Provides user info, tokens, and auth methods throughout the app
 */
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(() => {
    // Load tokens from localStorage if available
    const saved = localStorage.getItem('sophia_tokens');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Configure axios to include auth token
  const configureAxios = (token) => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  if (tokens?.access_token) {
    configureAxios(tokens.access_token);
  }

  const signup = async (email, password, fullName) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/signup`, {
        email,
        password,
        full_name: fullName
      });
      
      setUser(response.data.body);
      return { success: true, data: response.data.body };
    } catch (err) {
      const errorMsg = err.response?.data?.body?.error || 'Signup failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const confirmSignup = async (email, code) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/confirm`, {
        email,
        code
      });
      return { success: true, data: response.data.body };
    } catch (err) {
      const errorMsg = err.response?.data?.body?.error || 'Confirmation failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password
      });
      
      const { access_token, id_token, refresh_token, user_id } = response.data.body;
      const newTokens = {
        access_token,
        id_token,
        refresh_token,
        expires_in: response.data.body.expires_in
      };
      
      setTokens(newTokens);
      setUser({ email, user_id });
      localStorage.setItem('sophia_tokens', JSON.stringify(newTokens));
      configureAxios(access_token);
      
      return { success: true, data: response.data.body };
    } catch (err) {
      const errorMsg = err.response?.data?.body?.error || 'Login failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      if (tokens?.access_token) {
        await axios.post(`${API_BASE_URL}/auth/logout`, {});
      }
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
      setTokens(null);
      localStorage.removeItem('sophia_tokens');
      configureAxios(null);
      setLoading(false);
    }
  };

  const refreshTokens = async () => {
    if (!tokens?.refresh_token) {
      return { success: false };
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
        refresh_token: tokens.refresh_token
      });
      
      const newTokens = {
        ...tokens,
        access_token: response.data.body.access_token,
        id_token: response.data.body.id_token,
        expires_in: response.data.body.expires_in
      };
      
      setTokens(newTokens);
      localStorage.setItem('sophia_tokens', JSON.stringify(newTokens));
      configureAxios(newTokens.access_token);
      
      return { success: true, tokens: newTokens };
    } catch (err) {
      // Clear tokens if refresh fails
      logout();
      return { success: false };
    }
  };

  const resetPassword = async (email) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/forgot-password`, {
        email
      });
      return { success: true, data: response.data.body };
    } catch (err) {
      const errorMsg = err.response?.data?.body?.error || 'Reset request failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const confirmResetPassword = async (email, code, newPassword) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/reset-password`, {
        email,
        code,
        new_password: newPassword
      });
      return { success: true, data: response.data.body };
    } catch (err) {
      const errorMsg = err.response?.data?.body?.error || 'Password reset failed';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const getProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/profile`);
      return { success: true, data: response.data };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to fetch profile';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (updates) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.put(`${API_BASE_URL}/profile`, updates);
      setUser(prev => ({ ...prev, ...response.data }));
      return { success: true, data: response.data };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to update profile';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const getInterviewHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/interview/history`);
      return { success: true, data: response.data };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to fetch history';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    tokens,
    loading,
    error,
    signup,
    confirmSignup,
    login,
    logout,
    refreshTokens,
    resetPassword,
    confirmResetPassword,
    getProfile,
    updateProfile,
    getInterviewHistory,
    isAuthenticated: !!tokens?.access_token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
