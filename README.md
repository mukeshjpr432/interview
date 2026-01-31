# 🚀 AI Interview Coach - Enterprise Agentic System
## AWS Bedrock + Lambda + DynamoDB Architecture

### 🎯 Project Overview
A **production-grade AI interview coaching platform** using **AWS Bedrock** for autonomous agent-based interviews. Candidates practice with a realistic AI interviewer, get instant evaluation scores, and receive personalized coaching feedback.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React/Next.js)                │
│                  Interview, Dashboard, Reports              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              API GATEWAY (REST Endpoints)                    │
│     /interview/start, /interview/{id}/response, /report     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│        AWS LAMBDA - Interview Orchestrator                  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. Route to correct Agent                          │    │
│  │  2. Manage conversation flow                        │    │
│  │  3. Store/retrieve from DynamoDB                    │    │
│  │  4. Call Bedrock models                             │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌────────────┐ ┌──────────────┐
│ INTERVIEWER  │ │ EVALUATOR  │ │    COACH     │
│   AGENT      │ │   AGENT    │ │    AGENT     │
│ (Claude 3.5) │ │(Claude 3.5)│ │ (Claude 3.5) │
│              │ │            │ │              │
│ • Questions  │ │ • Scoring  │ │ • Feedback   │
│ • Adaptation │ │ • Analysis │ │ • Roadmap    │
│ • Flow       │ │ • JSON Out │ │ • Motivation │
└──────────────┘ └────────────┘ └──────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │    AWS BEDROCK SERVICE       │
        │   (Claude 3 Sonnet/Opus)     │
        └──────────────┬───────────────┘
                       │
        ┌──────────────┴──────────────────────────┐
        │                                          │
        ▼                                          ▼
┌──────────────────┐                   ┌──────────────────────┐
│  AWS DynamoDB    │                   │   AWS S3 (Voice)     │
│  Tables:         │                   │  • Audio uploads     │
│  • Sessions      │                   │  • Transcripts       │
│  • Evaluations   │                   │  • Reports           │
│  • Transcripts   │                   │                      │
│  • Profiles      │                   └──────────────────────┘
└──────────────────┘

        Optional:
        ┌──────────────┐    ┌─────────────┐
        │ Transcribe   │    │   Polly     │
        │ (STT)        │    │   (TTS)     │
        └──────────────┘    └─────────────┘
```

---

## 📁 Project Structure

```
ai-interview-coach/
├── src/
│   ├── agents/
│   │   ├── interviewer_agent_prompt.md      # Interviewer system prompt
│   │   ├── evaluator_agent_prompt.md        # Evaluator system prompt
│   │   └── coach_agent_prompt.md            # Coach system prompt
│   ├── lambda/
│   │   └── orchestrator.py                  # Main orchestrator function
│   ├── database/
│   │   └── dynamodb_schema.py               # DynamoDB table definitions
│   ├── voice/
│   │   └── voice_handler.py                 # STT/TTS integration
│   └── frontend/
│       ├── App.tsx                          # Main React component
│       ├── InterviewPage.tsx                # Interview interface
│       ├── DashboardSchema.json             # Dashboard data structure
│       └── styles.css
├── config/
│   └── aws_bedrock_config.json              # Bedrock configuration
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_SPECIFICATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── TESTING_GUIDE.md
├── tests/
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   └── test_voice.py
├── requirements.txt                         # Python dependencies
├── serverless.yml                           # Serverless Framework config
└── README.md
```

---

## 🤖 The Three Agents

### 1️⃣ **INTERVIEWER AGENT**
- **Role**: Conduct realistic interviews
- **Behavior**: Asks adaptive questions, adjusts difficulty, probes for depth
- **Output**: Next interview question
- **Model**: Claude 3 Sonnet (fast & intelligent)

```
Agentic Logic:
- IF answer is weak → Ask follow-up
- IF answer is strong → Increase difficulty
- IF nervous → Be supportive
- IF overconfident → Ask deeper questions
```

### 2️⃣ **EVALUATOR AGENT**
- **Role**: Score candidate performance
- **Behavior**: Analyzes responses objectively across 4 dimensions
- **Output**: JSON with structured scores
- **Model**: Claude 3 Opus (best reasoning)

**Scoring Dimensions**:
- Technical Knowledge (0-10)
- Communication Clarity (0-10)
- Confidence Level (0-10)
- Problem-Solving Ability (0-10)

### 3️⃣ **COACH AGENT**
- **Role**: Provide personalized coaching
- **Behavior**: Generates motivation + actionable improvement plan
- **Output**: Human-friendly feedback + 7-14 day roadmap
- **Model**: Claude 3 Opus (creative feedback)

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install AWS CLI
aws configure

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### 1. Deploy DynamoDB Tables
```bash
cd src/database
python dynamodb_schema.py
```

### 2. Deploy Lambda Function
```bash
serverless deploy
```

### 3. Test Interview Flow
```bash
python tests/test_orchestrator.py
```

---

## 📊 Interview Flow

```
START
  ↓
[1] Frontend: User selects job role + experience
  ↓
[2] Lambda: Calls Interviewer Agent
  ↓
[3] Bedrock: Returns greeting + first question
  ↓
[4] Candidate: Answers (text/voice)
  ↓
[5] Lambda: Stores response, calls Interviewer Agent
  ↓
[6] Bedrock: Returns next question (adaptive)
  ↓
[7] Repeat steps 4-6 for ~12 questions (45-60 mins)
  ↓
[8] Candidate: Says "Done" or timer expires
  ↓
[9] Lambda: Calls Evaluator Agent with full transcript
  ↓
[10] Bedrock: Returns JSON scores
  ↓
[11] Lambda: Calls Coach Agent with scores + transcript
  ↓
[12] Bedrock: Returns detailed feedback + roadmap
  ↓
[13] Frontend: Displays dashboard with all results
  ↓
END
```

---

## 💻 API Endpoints

### Start Interview
```bash
POST /interview/start
{
  "job_role": "Software Engineer",
  "experience_level": "3+ years"
}

Response:
{
  "interview_id": "uuid",
  "status": "started",
  "message": "[AI greeting + first question]"
}
```

### Send Response
```bash
POST /interview/{interview_id}/response
{
  "candidate_answer": "I have 5 years of experience..."
}

Response:
{
  "interview_id": "uuid",
  "status": "in_progress",
  "message": "[AI next question]",
  "questions_asked": 2
}
```

### End Interview
```bash
POST /interview/{interview_id}/end

Response:
{
  "interview_id": "uuid",
  "status": "completed",
  "phase": "completed"
}
```

### Get Report
```bash
GET /interview/{interview_id}/report

Response:
{
  "interview_id": "uuid",
  "overall_score": 7.6,
  "category_scores": {
    "technical": 8.0,
    "communication": 7.0,
    "confidence": 6.5,
    "problem_solving": 7.8
  },
  "readiness_status": "Almost Ready",
  "coaching_feedback": "[Detailed feedback]",
  "improvement_roadmap": "[7-14 day plan]"
}
```

---

## 🎤 Voice Interview (Optional)

### STT - Convert Audio to Text
```bash
POST /interview/{id}/voice/transcribe
{
  "audio_file_s3": "s3://bucket/audio.wav"
}
```

### TTS - Convert Question to Speech
```bash
POST /interview/{id}/voice/synthesize
{
  "text": "Tell me about your experience with system design",
  "voice_id": "Joanna"
}
```

---

## 📊 Dashboard JSON Output

See [DashboardSchema.json](src/frontend/DashboardSchema.json) for complete structure.

**Key fields**:
- Overall Score (0-10)
- Category Breakdown (Technical, Communication, Confidence, Problem-Solving)
- Readiness Status (Ready / Almost Ready / Needs Improvement)
- 3-4 Key Strengths
- 2-3 Improvement Areas
- 7-14 Day Preparation Roadmap

---

## 🔧 Configuration

Edit [aws_bedrock_config.json](config/aws_bedrock_config.json) to:
- Change model IDs
- Adjust temperature & max_tokens
- Configure DynamoDB tables
- Set S3 bucket names
- Enable/disable voice features

---

## 🧪 Testing

```bash
# Test orchestrator
python tests/test_orchestrator.py

# Test individual agents
python tests/test_agents.py

# Test voice handler
python tests/test_voice.py

# Load testing
python tests/test_load.py
```

---

## 💰 Cost Estimation

**Per Interview (~45 min)**:
- Bedrock API calls (3 agents): ~$0.10-0.15
- DynamoDB writes: ~$0.001
- S3 storage: ~$0.001
- Voice (optional): +$0.02-0.05

**Total per interview**: ~$0.12-0.20

---

## 🚀 Production Deployment

### Using Serverless Framework
```bash
serverless deploy --stage prod
```

### Using AWS SAM
```bash
sam build
sam deploy --guided
```

### Using Terraform
```bash
terraform plan
terraform apply
```

---

## 📈 Monitoring & Logs

### CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/interview-orchestrator --follow

# View error logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/interview-orchestrator \
  --filter-pattern "ERROR"
```

### Metrics
- Interview completion rate
- Average score by role
- Agent response time
- Error rate

---

## 🔐 Security

- ✅ AWS IAM authentication
- ✅ VPC endpoint for private access
- ✅ Encryption in transit (TLS)
- ✅ Encryption at rest (KMS)
- ✅ Input validation & sanitization
- ✅ Rate limiting on API Gateway
- ✅ CORS configuration

---

## 📚 Agents Deep Dive

### How Interviewer Agent Works

```
Current Interview State:
- Job Role: Software Engineer
- Experience: 3+ years
- Questions so far: 3
- Candidate answers: [...]

Decision Tree:
1. Analyze candidate's last answer
   - Technical accuracy?
   - Communication clarity?
   - Confidence level?
   
2. Based on analysis, decide:
   - Ask follow-up on same topic
   - Move to new topic
   - Increase difficulty
   - Simplify question
   
3. Generate contextual next question
4. Maintain conversational flow
```

### How Evaluator Agent Works

```
Input: Full interview transcript

Processing:
1. Extract all candidate responses
2. Score each response against 4 dimensions
3. Identify patterns (strengths/weaknesses)
4. Generate improvement areas

Output: Structured JSON
{
  "scores": {...},
  "strengths": [...],
  "weaknesses": [...],
  "improvement_areas": [...]
}
```

### How Coach Agent Works

```
Input: Evaluation scores + full transcript

Processing:
1. Interpret scores in human language
2. Identify highest-impact improvements
3. Create realistic 7-14 day roadmap
4. Suggest resources & practice areas
5. Provide motivational closing

Output: Personalized, actionable feedback
```

---

## 🎓 Features Explained

### ✅ Agentic AI (Autonomous Decision Making)
- Agents don't follow fixed scripts
- Real-time adaptation based on performance
- Natural conversation flow
- Thinks like real interviewer

### ✅ Multi-Agent System
- Separate concerns (Interview / Evaluate / Coach)
- Scalable architecture
- Easy to add more agents
- Each agent can be updated independently

### ✅ Voice Support
- Transcribe candidate speech to text
- Synthesize AI questions to speech
- Natural voice interaction
- Optional feature

### ✅ Comprehensive Feedback
- Objective scores
- Specific strengths
- Clear improvement areas
- Actionable 14-day plan

### ✅ Production Ready
- Error handling & retries
- Logging & monitoring
- Cost optimization
- Security best practices

---

## 📖 Documentation

- [API Specification](docs/API_SPECIFICATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Architecture Deep Dive](docs/ARCHITECTURE.md)
- [Testing Guide](docs/TESTING_GUIDE.md)

---

## 🤝 Contributing

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "Add feature"

# Push and create PR
git push origin feature/your-feature
```

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussion**: GitHub Discussions
- **Slack**: [Join Community](link)
- **Email**: support@aiinterviewcoach.com

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🎉 Key Differentiators

| Feature | This Project | Generic Interview Tool |
|---------|-------------|----------------------|
| Agentic AI | ✅ Autonomous | ❌ Scripted |
| Multi-Agent | ✅ 3 agents | ❌ Single model |
| Bedrock | ✅ AWS native | ❌ External APIs |
| Voice | ✅ Built-in STT/TTS | ❌ Text only |
| Evaluation | ✅ Structured JSON | ❌ Generic scores |
| Coaching | ✅ 14-day roadmap | ❌ Generic tips |
| Scalability | ✅ Serverless | ❌ Fixed capacity |

---

## 🚀 Next Steps

1. **Deploy DynamoDB tables**
   ```bash
   python src/database/dynamodb_schema.py
   ```

2. **Deploy Lambda function**
   ```bash
   serverless deploy
   ```

3. **Build React frontend**
   ```bash
   cd src/frontend
   npm install && npm start
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Monitor & optimize**
   - Check CloudWatch logs
   - Review costs
   - Gather user feedback

---

## 📊 Metrics to Track

- 📈 Total interviews conducted
- ⭐ Average score by role
- 📉 Improvement rate (compare interviews)
- ⏱️ Average interview duration
- 🎯 Readiness accuracy
- 💬 User satisfaction

---

## 🏆 Resume Impact

**This project demonstrates**:
- ✅ AI/ML expertise (Agentic AI, multi-agent systems)
- ✅ AWS cloud architecture (Lambda, Bedrock, DynamoDB, S3)
- ✅ System design thinking (scalable, modular, production-ready)
- ✅ Full-stack development (Backend API + Frontend + Voice)
- ✅ Product thinking (user value, roadmap, feedback)
- ✅ DevOps (deployment, monitoring, security)

---

**Built with ❤️ for interview preparation excellence**

Last updated: January 2025
