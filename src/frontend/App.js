import React, { useState } from 'react';
import AuthContext from './contexts/AuthContext';
import AuthPages from './pages/AuthPages';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentPage, setCurrentPage] = useState('login');

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, currentPage, setCurrentPage }}>
      <div className="app-container">
        <AuthPages />
      </div>
    </AuthContext.Provider>
  );
}

export default App;
