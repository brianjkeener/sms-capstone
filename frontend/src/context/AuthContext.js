// This is the complete and final code for frontend/src/context/AuthContext.js

import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Holds basic token data (role, email)
  const [fullUserProfile, setFullUserProfile] = useState(null); // Holds full details from API
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(true); // Add a loading state

  useEffect(() => {
    const bootstrapAppData = async () => {
      if (token) {
        try {
          // 1. Decode token to get basic info immediately
          const decoded = jwtDecode(token);
          setUser(decoded);

          // 2. Fetch the full user profile from the /users/me endpoint
          const response = await api.get('/users/me');
          setFullUserProfile(response.data);
        } catch (e) {
          console.error("Token is invalid or fetching user failed", e);
          // If anything fails, logout the user
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
          setFullUserProfile(null);
        }
      }
      setLoading(false); // We are done loading whether we have a token or not
    };

    bootstrapAppData();
  }, [token]);

  const login = async (email, password) => {
    const response = await api.post('/token', new URLSearchParams({
      username: email,
      password: password,
    }));
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    setToken(access_token); // This will trigger the useEffect to fetch user details
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setFullUserProfile(null); // Clear the full profile on logout
  };

  // We pass down the loading state so other components can use it
  return (
    <AuthContext.Provider value={{ user, fullUserProfile, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;