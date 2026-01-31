import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Sidebar from '../components/Sidebar';
import Dashboard from '../components/Dashboard';
import InterviewPage from './InterviewPage';
import './AuthPages.css';

/**
 * Login Component
 * Handles user login with email and password
 */
export const LoginPage = ({ onSuccess, onSwitchToSignup }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [localError, setLocalError] = useState('');
  const { login, loading } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');

    if (!email || !password) {
      setLocalError('Please fill in all fields');
      return;
    }

    const result = await login(email, password);
    
    if (result.success) {
      onSuccess?.();
    } else {
      setLocalError(result.error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>Welcome to Sophia</h1>
        <p>AI Interview Coach</p>

        {localError && <div className="error-message">{localError}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-wrapper">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                required
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            className="auth-button primary"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="auth-footer">
          <button className="link-button">Forgot Password?</button>
          <p>
            Don't have an account?{' '}
            <button 
              className="link-button"
              onClick={onSwitchToSignup}
            >
              Sign Up
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

/**
 * Signup Component
 * Handles user registration
 */
export const SignupPage = ({ onSuccess, onSwitchToLogin }) => {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [localError, setLocalError] = useState('');
  const { signup, loading } = useAuth();

  const validatePassword = (pwd) => {
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(pwd);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');

    if (!email || !fullName || !password || !confirmPassword) {
      setLocalError('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      setLocalError('Passwords do not match');
      return;
    }

    if (!validatePassword(password)) {
      setLocalError(
        'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
      );
      return;
    }

    const result = await signup(email, password, fullName);
    
    if (result.success) {
      onSuccess?.();
    } else {
      setLocalError(result.error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>Join Sophia</h1>
        <p>Start your interview preparation</p>

        {localError && <div className="error-message">{localError}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="John Doe"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-wrapper">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                required
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            <small className="password-requirements">
              At least 8 characters, with uppercase, lowercase, number, and special character
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type={showPassword ? 'text' : 'password'}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              disabled={loading}
              required
            />
          </div>

          <button 
            type="submit" 
            className="auth-button primary"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <button 
              className="link-button"
              onClick={onSwitchToLogin}
            >
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

/**
 * Profile Component
 * Display and edit user profile
 */
export const ProfilePage = () => {
  const { getProfile, updateProfile, loading } = useAuth();
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  const loadProfile = React.useCallback(async () => {
    const result = await getProfile();
    if (result.success) {
      setProfile(result.data);
      setFormData(result.data);
    }
  }, [getProfile]);

  React.useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    const result = await updateProfile(formData);
    if (result.success) {
      setProfile(result.data);
      setIsEditing(false);
    }
  };

  if (!profile) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Your Profile</h1>
        <button 
          className="auth-button secondary"
          onClick={() => setIsEditing(!isEditing)}
        >
          {isEditing ? 'Cancel' : 'Edit Profile'}
        </button>
      </div>

      {isEditing ? (
        <form onSubmit={handleUpdate} className="profile-form">
          <div className="form-group">
            <label>Email</label>
            <input 
              type="email"
              value={formData.email}
              readOnly
              className="read-only"
            />
          </div>
          <div className="form-group">
            <label>Full Name</label>
            <input 
              type="text"
              value={formData.full_name || ''}
              onChange={(e) => setFormData({...formData, full_name: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Experience Level</label>
            <select 
              value={formData.experience_level || 'junior'}
              onChange={(e) => setFormData({...formData, experience_level: e.target.value})}
            >
              <option value="junior">Junior</option>
              <option value="mid">Mid-Level</option>
              <option value="senior">Senior</option>
              <option value="lead">Lead</option>
            </select>
          </div>
          <button type="submit" className="auth-button primary" disabled={loading}>
            {loading ? 'Saving...' : 'Save Changes'}
          </button>
        </form>
      ) : (
        <div className="profile-info">
          <div className="info-group">
            <label>Email</label>
            <p>{profile.email}</p>
          </div>
          <div className="info-group">
            <label>Full Name</label>
            <p>{profile.full_name}</p>
          </div>
          <div className="info-group">
            <label>Experience Level</label>
            <p className="badge">{profile.experience_level}</p>
          </div>
          <div className="info-group">
            <label>Interviews Completed</label>
            <p>{profile.interviews_completed || 0}</p>
          </div>
          <div className="info-group">
            <label>Average Score</label>
            <p>{profile.stats?.average_score || 0}/100</p>
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * Interview History Component
 * Display user's past interviews
 */
export const InterviewHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const { getInterviewHistory } = useAuth();

  const loadHistory = React.useCallback(async () => {
    setLoading(true);
    const result = await getInterviewHistory();
    if (result.success) {
      setHistory(result.data.interviews || []);
    }
    setLoading(false);
  }, [getInterviewHistory]);

  React.useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  if (history.length === 0) {
    return (
      <div className="empty-state">
        <h2>No interviews yet</h2>
        <p>Start your first interview to see your history here</p>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h1>Interview History</h1>
      
      <div className="history-stats">
        <div className="stat">
          <h3>{history.length}</h3>
          <p>Interviews Completed</p>
        </div>
        <div className="stat">
          <h3>{(history.reduce((sum, h) => sum + (h.score || 0), 0) / history.length).toFixed(1)}</h3>
          <p>Average Score</p>
        </div>
      </div>

      <div className="history-list">
        {history.map((interview) => (
          <div key={interview.interview_id} className="history-item">
            <div className="item-header">
              <h3>{interview.role}</h3>
              <span className="score">{interview.score}/100</span>
            </div>
            <p className="category">{interview.category}</p>
            <p className="date">{new Date(interview.start_time).toLocaleDateString()}</p>
            <p className="feedback">{interview.feedback?.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * Main AuthPages Component
 * Handles page navigation between all features with sidebar
 */
export default function AuthPages() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const { isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return (
      <div>
        {currentPage === 'login' ? (
          <LoginPage 
            onSuccess={() => setCurrentPage('dashboard')}
            onSwitchToSignup={() => setCurrentPage('signup')}
          />
        ) : (
          <SignupPage 
            onSuccess={() => setCurrentPage('login')}
            onSwitchToLogin={() => setCurrentPage('login')}
          />
        )}
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Sidebar 
        currentPage={currentPage} 
        onPageChange={setCurrentPage}
        onLogout={logout}
      />
      
      <main className="main-content">
        {currentPage === 'dashboard' && (
          <Dashboard onStartInterview={() => setCurrentPage('interview')} />
        )}
        {currentPage === 'interview' && <InterviewPage />}
        {currentPage === 'profile' && <ProfilePage />}
        {currentPage === 'history' && <InterviewHistoryPage />}
      </main>
    </div>
  );
}
