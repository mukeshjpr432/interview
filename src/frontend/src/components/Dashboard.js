import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Dashboard.css';

export default function Dashboard({ onStartInterview }) {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalInterviews: 0,
    averageScore: 0,
    bestScore: 0,
    totalTime: 0
  });

  useEffect(() => {
    // Calculate stats from localStorage
    const interviews = JSON.parse(localStorage.getItem('sophia_interviews') || '[]');
    if (interviews.length > 0) {
      const avgScore = Math.round(
        interviews.reduce((sum, i) => sum + i.averageScore, 0) / interviews.length
      );
      const bestScore = Math.max(...interviews.map(i => i.averageScore));
      const totalTime = interviews.reduce((sum, i) => sum + i.totalTime, 0);

      setStats({
        totalInterviews: interviews.length,
        averageScore: avgScore,
        bestScore: bestScore,
        totalTime: totalTime
      });
    }
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (hours > 0) return `${hours}h ${mins}m`;
    return `${mins}m`;
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.fullName || 'User'}! 👋</h1>
        <p>Continue your interview preparation journey</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <p className="stat-label">Interviews Completed</p>
            <p className="stat-value">{stats.totalInterviews}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <p className="stat-label">Average Score</p>
            <p className="stat-value">{stats.averageScore > 0 ? `${stats.averageScore}%` : '-'}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <div className="stat-content">
            <p className="stat-label">Best Score</p>
            <p className="stat-value">{stats.bestScore > 0 ? `${stats.bestScore}%` : '-'}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <p className="stat-label">Total Practice Time</p>
            <p className="stat-value">{stats.totalTime > 0 ? formatTime(stats.totalTime) : '-'}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-cta">
        <h2>Ready to Practice?</h2>
        <p>Choose an interview type and get personalized feedback from Sophia AI</p>
        <button className="cta-button" onClick={onStartInterview}>
          🎤 Start New Interview
        </button>
      </div>

      <div className="dashboard-features">
        <h3>Features</h3>
        <div className="features-grid">
          <div className="feature-item">
            <span className="feature-icon">👤</span>
            <h4>Behavioral Questions</h4>
            <p>Practice common behavioral interview questions with AI coaching</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">💻</span>
            <h4>Technical Challenges</h4>
            <p>Sharpen your technical skills with industry-standard questions</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📋</span>
            <h4>HR Interview Prep</h4>
            <p>Master HR and general interview questions with confidence</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <h4>Case Study Analysis</h4>
            <p>Work through real-world case studies with detailed feedback</p>
          </div>
        </div>
      </div>

      <div className="dashboard-tips">
        <h3>💡 Interview Tips</h3>
        <ul>
          <li><strong>STAR Method:</strong> Use Situation, Task, Action, Result for behavioral questions</li>
          <li><strong>Be Specific:</strong> Provide concrete examples from your experience</li>
          <li><strong>Research:</strong> Learn about the company and role beforehand</li>
          <li><strong>Practice:</strong> Regular practice builds confidence and fluency</li>
          <li><strong>Ask Questions:</strong> Show genuine interest by asking thoughtful questions</li>
          <li><strong>Follow Up:</strong> Send thank-you email after the interview</li>
        </ul>
      </div>
    </div>
  );
}
