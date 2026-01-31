"""
API Specification for AI Interview Coach
Complete REST API documentation
"""

# ===========================================
# AI INTERVIEW COACH - API SPECIFICATION
# ===========================================

## Base URL
```
https://api.aiinterviewcoach.com/v1
# or locally:
http://localhost:3000/v1
```

## Authentication
```
Authorization: Bearer {api_key}
```

---

## 1. START INTERVIEW

**Endpoint**: `POST /interview/start`

**Description**: Initialize a new interview session

**Request Body**:
```json
{
  "job_role": "Software Engineer",
  "experience_level": "3+ years",
  "interview_type": "mixed",  // Optional: "technical", "hr", "behavioral", "mixed"
  "candidate_id": "uuid",      // Optional: for returning candidates
  "name": "John Doe",          // Optional
  "email": "john@example.com"  // Optional
}
```

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "phase": "init",
  "message": "Hello! Welcome to your mock interview for the Software Engineer position. I'm excited to learn more about your experience and skills. Before we dive in, could you tell me a bit about your background?",
  "question_number": 1,
  "timestamp": "2024-01-31T14:30:00Z"
}
```

**Error Responses**:
```json
// 400 Bad Request
{
  "error": "Invalid job_role",
  "valid_roles": ["Software Engineer", "Data Analyst", "Product Manager", ...]
}

// 429 Too Many Requests
{
  "error": "Rate limit exceeded",
  "retry_after_seconds": 60
}

// 500 Internal Server Error
{
  "error": "Failed to initialize interview",
  "request_id": "req_123"
}
```

---

## 2. SEND CANDIDATE RESPONSE

**Endpoint**: `POST /interview/{interview_id}/response`

**Description**: Submit candidate response to interview question

**Path Parameters**:
- `interview_id` (required): UUID of the interview session

**Request Body**:
```json
{
  "response": "I have 5 years of experience in full-stack development...",
  "response_type": "text",    // "text" or "audio"
  "audio_file_s3": "s3://bucket/path/to/audio.wav",  // Only if audio
  "duration_ms": 45000        // Optional: duration of response
}
```

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "phase": "in_progress",
  "message": "That's great! Now, let me dig a bit deeper. Can you explain how you would design a system to handle 1 million concurrent users?",
  "question_number": 3,
  "progress": {
    "questions_asked": 3,
    "estimated_total": 12,
    "progress_percent": 25
  },
  "timestamp": "2024-01-31T14:35:00Z"
}
```

**Error Responses**:
```json
// 404 Not Found
{
  "error": "Interview not found",
  "interview_id": "550e8400-e29b-41d4-a716-446655440000"
}

// 400 Bad Request
{
  "error": "Interview already ended",
  "status": "completed"
}

// 413 Payload Too Large
{
  "error": "Response too long (max 2000 characters)"
}
```

---

## 3. END INTERVIEW

**Endpoint**: `POST /interview/{interview_id}/end`

**Description**: Conclude the interview and start evaluation

**Path Parameters**:
- `interview_id` (required): UUID of the interview

**Request Body**:
```json
{
  "reason": "completed",  // "completed", "candidate_request", "timeout"
  "notes": "Optional notes from interviewer"
}
```

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "phase": "evaluating",
  "message": "Interview completed! Your responses are being evaluated. Please wait for detailed feedback...",
  "total_questions": 12,
  "duration_minutes": 45,
  "evaluation_status": "in_progress",
  "estimated_completion_seconds": 30,
  "timestamp": "2024-01-31T15:15:00Z"
}
```

---

## 4. GET INTERVIEW REPORT

**Endpoint**: `GET /interview/{interview_id}/report`

**Description**: Retrieve complete interview report with scores and feedback

**Path Parameters**:
- `interview_id` (required): UUID of the interview

**Query Parameters**:
- `include_transcript` (optional): Include full transcript (boolean)
- `include_feedback` (optional): Include coaching feedback (boolean)
- `format` (optional): Response format - "json" or "pdf"

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_role": "Software Engineer",
  "experience_level": "3+ years",
  "interview_summary": {
    "start_time": "2024-01-31T14:30:00Z",
    "end_time": "2024-01-31T15:15:00Z",
    "duration_minutes": 45,
    "total_questions": 12,
    "status": "completed"
  },
  "performance_scores": {
    "overall_score": 7.6,
    "technical_knowledge": 8.0,
    "communication_clarity": 7.0,
    "confidence_level": 6.5,
    "problem_solving": 7.8
  },
  "readiness_assessment": {
    "readiness_level": "Almost Ready",
    "confidence_percentage": 75,
    "main_strength": "Strong technical foundation",
    "main_concern": "Needs more confidence in interviews"
  },
  "strengths": [
    {
      "title": "Strong system design thinking",
      "description": "Demonstrated clear understanding of scalable architecture",
      "examples": [
        "Correctly identified CAP theorem in distributed systems",
        "Proposed well-structured database schema"
      ]
    }
  ],
  "improvement_areas": [
    {
      "title": "Confidence in unfamiliar domains",
      "description": "Shows hesitation when facing new topics",
      "priority": "high",
      "suggestions": [
        "Practice explaining concepts out loud",
        "Mock interview drills 3x per week"
      ]
    }
  ],
  "coaching_feedback": "You have a solid technical foundation with excellent system design skills...",
  "preparation_roadmap": {
    "duration_days": 14,
    "week_1": [
      {
        "day": 1,
        "focus": "System design patterns",
        "resources": ["System Design Primer", "YouTube link"]
      }
    ],
    "week_2": [
      {
        "day": 8,
        "focus": "Mock interviews",
        "resources": ["Pramp", "Interviewing.io"]
      }
    ]
  },
  "next_steps": [
    "Schedule another mock interview",
    "Review system design concepts",
    "Practice confidence-building exercises"
  ],
  "transcript": "[optional full interview transcript]"
}
```

**Error Response**:
```json
// 404 Not Found
{
  "error": "Interview not found or still evaluating",
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "evaluating",
  "estimated_ready_seconds": 25
}
```

---

## 5. GET INTERVIEW STATUS

**Endpoint**: `GET /interview/{interview_id}/status`

**Description**: Check current interview status

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",  // "in_progress", "completed", "evaluating", "ready"
  "phase": "in_progress",
  "current_question_number": 5,
  "total_questions_estimate": 12,
  "progress_percent": 42,
  "elapsed_minutes": 20,
  "time_remaining_estimate_minutes": 25,
  "last_question_at": "2024-01-31T14:50:00Z"
}
```

---

## 6. VOICE INTERVIEW - TRANSCRIBE

**Endpoint**: `POST /interview/{interview_id}/voice/transcribe`

**Description**: Convert candidate audio response to text

**Request Body**:
```json
{
  "audio_file_s3": "s3://interview-coach-voice/responses/abc123.wav",
  "language": "en-US"  // Optional
}
```

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "text": "I have 5 years of experience in full-stack development...",
  "confidence": 0.95,
  "duration_seconds": 45,
  "timestamp": "2024-01-31T14:50:00Z"
}
```

---

## 7. VOICE INTERVIEW - SYNTHESIZE

**Endpoint**: `POST /interview/{interview_id}/voice/synthesize`

**Description**: Convert AI question to speech

**Request Body**:
```json
{
  "text": "Tell me about your experience with system design.",
  "voice_id": "Joanna",  // "Joanna", "Matthew", "Salli", "Joey"
  "rate": "100"          // Words per minute: 80-360
}
```

**Response** (200 OK):
```json
{
  "interview_id": "550e8400-e29b-41d4-a716-446655440000",
  "audio_url": "s3://interview-coach-voice/questions/joanna_1706703000.mp3",
  "duration_ms": 4500,
  "voice_id": "Joanna",
  "timestamp": "2024-01-31T14:50:00Z"
}
```

---

## 8. GET CANDIDATE INTERVIEW HISTORY

**Endpoint**: `GET /candidate/{candidate_id}/interviews`

**Description**: Retrieve interview history for a candidate

**Query Parameters**:
- `limit` (optional): Number of interviews (default: 10, max: 50)
- `offset` (optional): Pagination offset
- `role` (optional): Filter by job role

**Response** (200 OK):
```json
{
  "candidate_id": "cand_123",
  "total_interviews": 3,
  "interviews": [
    {
      "interview_id": "550e8400-e29b-41d4-a716-446655440000",
      "job_role": "Software Engineer",
      "experience_level": "3+ years",
      "date": "2024-01-31T14:30:00Z",
      "score": 7.6,
      "readiness": "Almost Ready",
      "duration_minutes": 45
    },
    {
      "interview_id": "550e8400-e29b-41d4-a716-446655440001",
      "job_role": "Software Engineer",
      "experience_level": "3+ years",
      "date": "2024-01-30T10:00:00Z",
      "score": 6.8,
      "readiness": "Needs Improvement",
      "duration_minutes": 42
    }
  ],
  "trends": {
    "avg_score": 7.2,
    "improvement_percent": 11,
    "most_common_weakness": "Confidence"
  }
}
```

---

## 9. GET ANALYTICS (Admin Only)

**Endpoint**: `GET /admin/analytics`

**Description**: Platform-wide analytics

**Query Parameters**:
- `time_range`: "24h", "7d", "30d", "all" (required)
- `role`: Filter by job role

**Response** (200 OK):
```json
{
  "time_range": "24h",
  "total_interviews": 1245,
  "avg_score_overall": 7.3,
  "score_by_role": {
    "Software Engineer": 7.5,
    "Data Analyst": 7.1,
    "Product Manager": 7.2
  },
  "readiness_distribution": {
    "Ready": 25,
    "Almost Ready": 45,
    "Needs Improvement": 30
  },
  "most_common_weakness": "Confidence in unfamiliar domains",
  "avg_interview_duration_minutes": 43
}
```

---

## Error Codes Reference

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing/invalid API key |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Interview already ended |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Bedrock API down |

---

## Rate Limiting

- **Free Plan**: 5 interviews/day
- **Pro Plan**: 50 interviews/day  
- **Enterprise**: Unlimited

Response headers:
```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1706703600
```

---

## Webhooks (Optional)

```
POST /webhook/interview_completed
{
  "event": "interview.completed",
  "interview_id": "...",
  "candidate_id": "...",
  "score": 7.6,
  "timestamp": "2024-01-31T15:15:00Z"
}
```

---

## Example cURL Commands

### Start Interview
```bash
curl -X POST https://api.aiinterviewcoach.com/v1/interview/start \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_role": "Software Engineer",
    "experience_level": "3+ years"
  }'
```

### Send Response
```bash
curl -X POST https://api.aiinterviewcoach.com/v1/interview/{id}/response \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "response": "I have 5 years of experience...",
    "response_type": "text"
  }'
```

### Get Report
```bash
curl -X GET 'https://api.aiinterviewcoach.com/v1/interview/{id}/report?include_transcript=true' \\
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

**Last Updated**: January 2025
**API Version**: 1.0
**Status**: Production Ready
