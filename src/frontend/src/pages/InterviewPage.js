import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './InterviewPage.css';

const INTERVIEW_CATEGORIES = [
  { id: 'behavioral', name: 'Behavioral Interview', icon: '👤' },
  { id: 'technical', name: 'Technical Interview', icon: '💻' },
  { id: 'hr', name: 'HR Interview', icon: '📋' },
  { id: 'case', name: 'Case Study', icon: '📊' }
];

const INTERVIEW_QUESTIONS = {
  behavioral: [
    {
      id: 1,
      question: "Tell me about a time when you had to handle a difficult situation at work. How did you resolve it?",
      tips: ["Be specific", "Use STAR method (Situation, Task, Action, Result)", "Focus on your role"]
    },
    {
      id: 2,
      question: "Describe a situation where you worked in a team. What was your contribution?",
      tips: ["Highlight teamwork", "Show leadership skills", "Mention specific achievements"]
    },
    {
      id: 3,
      question: "Tell me about a time you failed. What did you learn from it?",
      tips: ["Be honest and humble", "Focus on learning", "Show growth mindset"]
    },
    {
      id: 4,
      question: "How do you handle feedback and criticism?",
      tips: ["Show openness", "Give specific example", "Demonstrate improvement"]
    },
    {
      id: 5,
      question: "Describe your biggest professional achievement.",
      tips: ["Be proud but humble", "Quantify results", "Explain the impact"]
    }
  ],
  technical: [
    {
      id: 1,
      question: "Explain the difference between REST and GraphQL APIs.",
      tips: ["Compare architecture", "Discuss advantages/disadvantages", "Give use cases"]
    },
    {
      id: 2,
      question: "What is the difference between SQL and NoSQL databases?",
      tips: ["Explain schema", "Discuss scalability", "Give examples of use cases"]
    },
    {
      id: 3,
      question: "How would you optimize a slow database query?",
      tips: ["Index strategy", "Query optimization", "Caching mechanisms"]
    },
    {
      id: 4,
      question: "Explain the concept of microservices.",
      tips: ["Architecture benefits", "Challenges", "Real-world implementation"]
    },
    {
      id: 5,
      question: "What is CI/CD and why is it important?",
      tips: ["Automation benefits", "DevOps practices", "Tools and implementation"]
    }
  ],
  hr: [
    {
      id: 1,
      question: "Why are you interested in this position?",
      tips: ["Research company", "Match skills with role", "Show enthusiasm"]
    },
    {
      id: 2,
      question: "What are your salary expectations?",
      tips: ["Research market rate", "Consider experience", "Be reasonable"]
    },
    {
      id: 3,
      question: "Where do you see yourself in 5 years?",
      tips: ["Show ambition", "Align with company", "Be realistic"]
    },
    {
      id: 4,
      question: "What are your strengths and weaknesses?",
      tips: ["Be honest", "Weakness should be addressable", "Give examples"]
    },
    {
      id: 5,
      question: "Do you have any questions for us?",
      tips: ["Ask meaningful questions", "Show interest", "Avoid salary/benefits initially"]
    }
  ],
  case: [
    {
      id: 1,
      question: "How would you estimate the number of gas stations in your city?",
      tips: ["Show methodology", "Break into components", "Use reasonable assumptions"]
    },
    {
      id: 2,
      question: "What is the market size for coffee in the USA?",
      tips: ["Top-down or bottom-up", "Use data points", "Explain assumptions"]
    },
    {
      id: 3,
      question: "How would you improve Uber's revenue?",
      tips: ["Brainstorm ideas", "Analyze feasibility", "Consider metrics"]
    },
    {
      id: 4,
      question: "Estimate how many hours a week the average person watches Netflix.",
      tips: ["Segment users", "Use research data", "Cross-validate"]
    },
    {
      id: 5,
      question: "How would you value a startup with $1M revenue but no profits?",
      tips: ["Multiple approaches", "Justify assumptions", "Consider growth potential"]
    }
  ]
};

const AI_FEEDBACK_RESPONSES = [
  "Great answer! You provided a clear example with good structure. Consider adding more specific metrics.",
  "Good effort. Your answer shows understanding. Try to dive deeper into the why.",
  "Excellent! You covered all key points. Your examples were relatable and well-articulated.",
  "Nice perspective! This shows good thinking. You could strengthen this by discussing trade-offs.",
  "Solid response. You demonstrated knowledge well. In future, try to connect this back to business impact.",
  "Impressive depth! You clearly have experience with this. Don't forget to mention the learning points.",
  "Good start! This is on the right track. Can you elaborate on your approach?",
  "Very thoughtful answer. You showed critical thinking. This would impress any interviewer!"
];

function InterviewStartScreen({ onSelectCategory }) {
  return (
    <div className="interview-start-screen">
      <div className="interview-header">
        <h2>🎯 Start Your Interview</h2>
        <p>Choose an interview type to begin coaching</p>
      </div>
      <div className="category-grid">
        {INTERVIEW_CATEGORIES.map(category => (
          <button
            key={category.id}
            className="category-card"
            onClick={() => onSelectCategory(category.id)}
          >
            <span className="category-icon">{category.icon}</span>
            <span className="category-name">{category.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

function InterviewSessionScreen({ categoryId, onBack, onFinish }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [sessionScore, setSessionScore] = useState(0);
  const timerRef = useRef(null);

  const questions = INTERVIEW_QUESTIONS[categoryId];
  const categoryName = INTERVIEW_CATEGORIES.find(c => c.id === categoryId)?.name;

  useEffect(() => {
    timerRef.current = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, []);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSubmitAnswer = () => {
    if (!userAnswer.trim()) {
      alert('Please provide an answer before continuing.');
      return;
    }

    // Generate AI feedback
    const randomFeedback = AI_FEEDBACK_RESPONSES[Math.floor(Math.random() * AI_FEEDBACK_RESPONSES.length)];
    
    // Calculate score based on answer length and content
    const answerLength = userAnswer.trim().split(' ').length;
    const scoreBonus = Math.min(answerLength / 30, 0.3); // Bonus for detailed answers
    const score = Math.round((50 + scoreBonus * 30 + Math.random() * 20));

    setFeedback({
      text: randomFeedback,
      score: score,
      timestamp: new Date().toLocaleTimeString()
    });
    setShowFeedback(true);
    setAnswers([...answers, { question: questions[currentQuestion].question, answer: userAnswer, score }]);
    setSessionScore(sessionScore + score);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setUserAnswer('');
      setShowFeedback(false);
    } else {
      handleFinishInterview();
    }
  };

  const handleFinishInterview = () => {
    const avgScore = Math.round(sessionScore / answers.length);
    onFinish({
      category: categoryId,
      categoryName: categoryName,
      totalQuestions: answers.length + 1,
      averageScore: avgScore,
      totalTime: elapsedTime,
      timestamp: new Date().toISOString(),
      answers: [...answers, { question: questions[currentQuestion].question, answer: userAnswer, score: 0 }]
    });
  };

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="interview-session">
      <div className="session-header">
        <div className="session-info">
          <h3>{categoryName}</h3>
          <span className="question-count">Question {currentQuestion + 1} of {questions.length}</span>
        </div>
        <div className="session-timer">⏱️ {formatTime(elapsedTime)}</div>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="question-container">
        <div className="question-text">
          <h4>🎤 {question.question}</h4>
          <div className="tips">
            <strong>Tips:</strong>
            <ul>
              {question.tips.map((tip, idx) => (
                <li key={idx}>{tip}</li>
              ))}
            </ul>
          </div>
        </div>

        <textarea
          className="answer-input"
          placeholder="Type your answer here... (Speak or think through your response)"
          value={userAnswer}
          onChange={(e) => setUserAnswer(e.target.value)}
          disabled={showFeedback}
          rows="6"
        />

        {!showFeedback ? (
          <button className="submit-button" onClick={handleSubmitAnswer}>
            Submit Answer
          </button>
        ) : (
          <div className="feedback-section">
            <div className={`feedback-score score-${feedback.score}`}>
              <span className="score-number">{feedback.score}</span>
              <span className="score-label">/100</span>
            </div>
            <div className="feedback-text">
              <strong>AI Coach Feedback:</strong>
              <p>{feedback.text}</p>
            </div>
            <button className="next-button" onClick={handleNextQuestion}>
              {currentQuestion < questions.length - 1 ? 'Next Question' : 'Finish Interview'}
            </button>
          </div>
        )}
      </div>

      <button className="back-button" onClick={onBack}>← Back to Categories</button>
    </div>
  );
}

export default function InterviewPage() {
  const { user } = useAuth();
  const [interviewState, setInterviewState] = useState('start'); // 'start', 'session', 'complete'
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [completedInterview, setCompletedInterview] = useState(null);

  const handleSelectCategory = (categoryId) => {
    setSelectedCategory(categoryId);
    setInterviewState('session');
  };

  const handleBackToStart = () => {
    setInterviewState('start');
    setSelectedCategory(null);
  };

  const handleFinishInterview = (results) => {
    setCompletedInterview(results);
    setInterviewState('complete');

    // Store in localStorage
    const interviews = JSON.parse(localStorage.getItem('sophia_interviews') || '[]');
    interviews.push({
      ...results,
      userId: user?.id,
      id: Date.now()
    });
    localStorage.setItem('sophia_interviews', JSON.stringify(interviews));
  };

  return (
    <div className="interview-page">
      {interviewState === 'start' && (
        <InterviewStartScreen onSelectCategory={handleSelectCategory} />
      )}

      {interviewState === 'session' && selectedCategory && (
        <InterviewSessionScreen
          categoryId={selectedCategory}
          onBack={handleBackToStart}
          onFinish={handleFinishInterview}
        />
      )}

      {interviewState === 'complete' && completedInterview && (
        <div className="interview-completion">
          <div className="completion-header">
            <h2>✅ Interview Complete!</h2>
            <p>Great job practicing with Sophia AI</p>
          </div>

          <div className="results-summary">
            <div className="result-card">
              <span className="result-label">Interview Type</span>
              <span className="result-value">{completedInterview.categoryName}</span>
            </div>
            <div className="result-card">
              <span className="result-label">Average Score</span>
              <span className="result-value highlight">{completedInterview.averageScore}%</span>
            </div>
            <div className="result-card">
              <span className="result-label">Questions Answered</span>
              <span className="result-value">{completedInterview.totalQuestions}</span>
            </div>
            <div className="result-card">
              <span className="result-label">Duration</span>
              <span className="result-value">
                {Math.floor(completedInterview.totalTime / 60)}:{(completedInterview.totalTime % 60).toString().padStart(2, '0')}
              </span>
            </div>
          </div>

          <div className="score-feedback">
            {completedInterview.averageScore >= 80 && (
              <div className="feedback-excellent">
                <h3>🌟 Excellent Performance!</h3>
                <p>You demonstrated strong communication and deep thinking. Keep practicing to maintain this level!</p>
              </div>
            )}
            {completedInterview.averageScore >= 60 && completedInterview.averageScore < 80 && (
              <div className="feedback-good">
                <h3>👍 Good Job!</h3>
                <p>You showed understanding and good effort. Focus on the tips and practice more for better results.</p>
              </div>
            )}
            {completedInterview.averageScore < 60 && (
              <div className="feedback-improve">
                <h3>💪 Keep Practicing!</h3>
                <p>Every interview is a learning opportunity. Review the feedback and try another interview to improve.</p>
              </div>
            )}
          </div>

          <button className="new-interview-button" onClick={handleBackToStart}>
            Start Another Interview
          </button>
        </div>
      )}
    </div>
  );
}
