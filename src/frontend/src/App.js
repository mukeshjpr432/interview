import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import AuthPages from './pages/AuthPages';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <div className="app-container">
        <AuthPages />
      </div>
    </AuthProvider>
  );
}

export default App;
