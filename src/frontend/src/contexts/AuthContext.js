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

// Cognito configuration (for future use with AWS SDK)
// const COGNITO_CONFIG = {
//   region: process.env.REACT_APP_COGNITO_REGION || 'us-east-1',
//   userPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID || 'us-east-1_S8nbIWo7v',
//   clientId: process.env.REACT_APP_COGNITO_CLIENT_ID || '18q1qj09bnngsu8fn3lsnso8cd'
// };

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
      // Validate input
      if (!email || !password || !fullName) {
        throw new Error('Please fill in all fields');
      }

      // Check if user already exists in localStorage
      const existingUsers = JSON.parse(localStorage.getItem('sophia_users') || '[]');
      if (existingUsers.find(u => u.email === email)) {
        throw new Error('User with this email already exists');
      }

      // Create new user
      const newUser = {
        email,
        password, // Note: In production, password should be hashed on backend
        fullName,
        userId: `user_${Date.now()}`,
        createdAt: new Date().toISOString(),
        verified: false
      };

      // Store user
      existingUsers.push(newUser);
      localStorage.setItem('sophia_users', JSON.stringify(existingUsers));
      
      // Auto-login user
      const tokens = {
        access_token: `token_${newUser.userId}`,
        id_token: `id_${newUser.userId}`,
        refresh_token: `refresh_${newUser.userId}`,
        expires_in: 3600,
        email: email,
        user_id: newUser.userId
      };
      
      setTokens(tokens);
      setUser({ email, user_id: newUser.userId, fullName });
      localStorage.setItem('sophia_tokens', JSON.stringify(tokens));
      configureAxios(tokens.access_token);
      
      return { success: true, data: newUser };
    } catch (err) {
      const errorMsg = err.message || 'Signup failed';
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
      // Get users from localStorage
      const users = JSON.parse(localStorage.getItem('sophia_users') || '[]');
      const user = users.find(u => u.email === email && u.password === password);
      
      if (!user) {
        throw new Error('Invalid email or password');
      }

      // Create tokens
      const newTokens = {
        access_token: `token_${user.userId}`,
        id_token: `id_${user.userId}`,
        refresh_token: `refresh_${user.userId}`,
        expires_in: 3600,
        email: email,
        user_id: user.userId
      };
      
      setTokens(newTokens);
      setUser({ email, user_id: user.userId, fullName: user.fullName });
      localStorage.setItem('sophia_tokens', JSON.stringify(newTokens));
      configureAxios(newTokens.access_token);
      
      return { success: true, data: { email, user_id: user.userId } };
    } catch (err) {
      const errorMsg = err.message || 'Login failed';
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
