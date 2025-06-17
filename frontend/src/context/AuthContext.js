import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'; // You might need to install this: npm install jwt-decode
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      try {
        const decodedUser = jwtDecode(token);
        setUser(decodedUser);
      } catch (e) {
        // Invalid token
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
      }
    }
  }, [token]);
  
  const login = async (email, password) => {
    const response = await api.post('/token', new URLSearchParams({
      username: email,
      password: password,
    }));
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    setToken(access_token);
    const decodedUser = jwtDecode(access_token);
    setUser(decodedUser);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;