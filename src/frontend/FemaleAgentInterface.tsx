/**
 * Female AI Agent Interface Component (React)
 * Sophia - Real-time voice & video interview interaction
 */

import React, { useState, useEffect, useRef } from 'react';
import './FemaleAgentInterface.css';

interface AgentStatus {
  agent_name: string;
  status: 'idle' | 'speaking' | 'listening';
  is_speaking: boolean;
  is_listening: boolean;
  last_transcription: string;
}

const FemaleAgentInterface: React.FC = () => {
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({
    agent_name: 'Sophia',
    status: 'idle',
    is_speaking: false,
    is_listening: false,
    last_transcription: ''
  });

  const [transcript, setTranscript] = useState<string>('');
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<string>('');
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = new WebSocket('wss://your-api-endpoint/voice');
    
    ws.onopen = () => {
      console.log('🔗 Connected to Sophia');
      wsRef.current = ws;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.status === 'listening' && data.partial_text) {
        setTranscript(data.partial_text);
      } else if (data.status === 'feedback') {
        setFeedback(data.feedback_text);
        playAudio(data.audio);
      }
    };

    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
    };

    return () => {
      ws.close();
    };
  }, []);

  // Start recording candidate's voice
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      audioContextRef.current = audioContext;
      
      const analyser = audioContext.createAnalyser();
      analyserRef.current = analyser;
      
      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({
            action: 'listen',
            audio_chunk: event.data
          }));
        }
      };

      mediaRecorder.start(100); // Send every 100ms
      setIsRecording(true);
    } catch (error) {
      console.error('❌ Microphone access error:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Play audio response
  const playAudio = (audioData: ArrayBuffer) => {
    const audioContext = audioContextRef.current || new AudioContext();
    audioContext.decodeAudioData(audioData, (buffer) => {
      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);
      source.start(0);
    });
  };

  // Sophia speaks question
  const sophiaAskQuestion = (question: string) => {
    setCurrentQuestion(question);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        action: 'speak_question',
        question: question
      }));
    }
  };

  return (
    <div className="sophia-interview-container">
      
      {/* Header */}
      <div className="sophia-header">
        <h1>👩‍💼 Sophia - Your Interview Coach</h1>
        <p>Real-time voice interview practice</p>
      </div>

      {/* Main Interview Area */}
      <div className="sophia-main">
        
        {/* Agent Video/Avatar Section */}
        <div className="sophia-agent-section">
          {/* Avatar Placeholder */}
          <div className={`sophia-avatar ${agentStatus.status}`}>
            <div className="avatar-container">
              {/* Show animated avatar or waveform */}
              {agentStatus.is_speaking ? (
                <div className="speaking-indicator">
                  <SpeakingWaveform />
                  <p>Sophia is speaking...</p>
                </div>
              ) : agentStatus.is_listening ? (
                <div className="listening-indicator">
                  <ListeningWaveform />
                  <p>Sophia is listening...</p>
                </div>
              ) : (
                <div className="idle-indicator">
                  <p>👩‍💼 Sophia</p>
                  <p>Ready for your response</p>
                </div>
              )}
            </div>
          </div>

          {/* Status Badge */}
          <div className="sophia-status-badge">
            <span className={`status-dot ${agentStatus.status}`}></span>
            <span className="status-text">
              {agentStatus.status === 'speaking' && '🎤 Speaking'}
              {agentStatus.status === 'listening' && '👂 Listening'}
              {agentStatus.status === 'idle' && '✓ Ready'}
            </span>
          </div>
        </div>

        {/* Chat/Transcript Section */}
        <div className="sophia-chat-section">
          
          {/* Current Question */}
          {currentQuestion && (
            <div className="message agent-message">
              <p className="agent-name">Sophia:</p>
              <p className="message-text">"{currentQuestion}"</p>
            </div>
          )}

          {/* Candidate Transcript */}
          {transcript && (
            <div className="message candidate-message">
              <p className="candidate-name">You:</p>
              <p className="message-text">{transcript}</p>
              {isRecording && <span className="recording-dot"></span>}
            </div>
          )}

          {/* Feedback */}
          {feedback && (
            <div className="feedback-message">
              <p className="feedback-icon">✨</p>
              <p className="feedback-text">{feedback}</p>
            </div>
          )}
        </div>
      </div>

      {/* Controls */}
      <div className="sophia-controls">
        <button 
          className={`record-button ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
        >
          {isRecording ? (
            <>
              <span className="recording-light"></span>
              Stop Recording
            </>
          ) : (
            <>
              🎤 Start Answering
            </>
          )}
        </button>

        <button 
          className="next-question-button"
          onClick={() => sophiaAskQuestion("Tell me about a challenging project you worked on.")}
        >
          Next Question
        </button>

        <button className="help-button">
          ❓ Need Help?
        </button>
      </div>

      {/* Progress */}
      <div className="sophia-progress">
        <p>Question 1 of 12</p>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: '8%' }}></div>
        </div>
      </div>
    </div>
  );
};

// Waveform Components
const SpeakingWaveform: React.FC = () => (
  <div className="waveform speaking">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="bar" style={{
        animationDelay: `${i * 0.1}s`
      }}></div>
    ))}
  </div>
);

const ListeningWaveform: React.FC = () => (
  <div className="waveform listening">
    {[...Array(5)].map((_, i) => (
      <div key={i} className="bar" style={{
        animationDelay: `${i * 0.1}s`
      }}></div>
    ))}
  </div>
);

export default FemaleAgentInterface;
