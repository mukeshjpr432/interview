import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Sidebar.css';

export default function Sidebar({ currentPage, onPageChange, onLogout }) {
  const { user } = useAuth();
  const [isExpanded, setIsExpanded] = useState(true);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'interview', label: 'Start Interview', icon: '🎤' },
    { id: 'profile', label: 'My Profile', icon: '👤' },
    { id: 'history', label: 'Interview History', icon: '📜' }
  ];

  return (
    <div className={`sidebar ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🎓</span>
          {isExpanded && <span className="logo-text">Sophia AI</span>}
        </div>
        <button 
          className="toggle-btn" 
          onClick={() => setIsExpanded(!isExpanded)}
          title={isExpanded ? 'Collapse' : 'Expand'}
        >
          {isExpanded ? '◀' : '▶'}
        </button>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onPageChange(item.id)}
            title={!isExpanded ? item.label : ''}
          >
            <span className="nav-icon">{item.icon}</span>
            {isExpanded && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        {isExpanded && user && (
          <div className="user-info">
            <div className="user-avatar">
              {user.fullName?.charAt(0).toUpperCase() || '👤'}
            </div>
            <div className="user-details">
              <p className="user-name">{user.fullName || 'User'}</p>
              <p className="user-email">{user.email}</p>
            </div>
          </div>
        )}
        <button className="logout-btn" onClick={onLogout}>
          <span className="logout-icon">🚪</span>
          {isExpanded && <span>Logout</span>}
        </button>
      </div>
    </div>
  );
}
