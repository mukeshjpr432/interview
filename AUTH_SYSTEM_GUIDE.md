# SOPHIA AI INTERVIEW COACH - COMPLETE AUTHENTICATION SYSTEM

## Overview

Sophia now has a complete, production-ready authentication system featuring:

- **AWS Cognito User Pool**: Secure user authentication
- **User Profiles**: Persistent user data storage
- **Interview History**: Track all interviews and performance
- **AWS Amplify**: Frontend hosting and deployment
- **S3 Static Hosting**: Frontend assets
- **API Gateway**: Protected endpoints with Cognito integration
- **DynamoDB**: User data, profiles, and history
- **Lambda Functions**: Secure auth handlers

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SOPHIA AI ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (React)                                             │
│  ├── AWS Amplify Hosting                                      │
│  ├── S3 Static Website                                        │
│  └── CloudFront CDN                                           │
│         │                                                     │
│         ▼                                                     │
│  AWS Cognito User Pool (Authentication)                       │
│  ├── User Registration                                        │
│  ├── Email Verification                                       │
│  ├── Password Management                                      │
│  └── JWT Tokens                                               │
│         │                                                     │
│         ▼                                                     │
│  API Gateway (REST API)                                       │
│  ├── /auth/* (Login, Signup, etc)                             │
│  ├── /profile (User Profile)                                  │
│  ├── /interview/history (History)                             │
│  ├── /interview/* (Interview APIs)                            │
│  └── Authorization: Cognito Authorizer                        │
│         │                                                     │
│         ▼                                                     │
│  Lambda Functions                                             │
│  ├── authHandler (Authentication)                             │
│  ├── orchestrator (Interview Logic)                           │
│  └── voiceHandler (Voice Processing)                          │
│         │                                                     │
│         ▼                                                     │
│  AWS Services                                                 │
│  ├── DynamoDB (User Data)                                     │
│  │   ├── sophia_users                                         │
│  │   ├── sophia_user_profiles                                 │
│  │   └── sophia_interview_history                             │
│  ├── Bedrock (AI Models)                                      │
│  ├── S3 (Voice/Training Data)                                 │
│  └── CloudWatch (Logging)                                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## AWS Resources Required

### 1. Cognito User Pool
- **Name**: sophia-interview-coach-users
- **Purpose**: User authentication and management
- **Features**:
  - Email-based signup/login
  - Password complexity: Min 8 chars, uppercase, lowercase, number, special char
  - Email verification
  - Password reset
  - MFA ready

### 2. DynamoDB Tables

#### sophia_users
```yaml
Primary Key:
  - user_id (HASH)
  - created_at (RANGE)

Global Secondary Indexes:
  - email-index: email (HASH), created_at (RANGE)

Attributes:
  - user_id: string (Cognito User ID)
  - email: string
  - created_at: string (ISO timestamp)
  - password_hash: string
  - status: string (active/suspended)
```

#### sophia_user_profiles
```yaml
Primary Key:
  - user_id (HASH)

Attributes:
  - user_id: string
  - email: string
  - full_name: string
  - experience_level: string (junior/mid/senior/lead)
  - interviews_completed: number
  - total_score: number
  - preferred_categories: list
  - skills: list
  - notification_settings: map
  - created_at: string
  - updated_at: string
```

#### sophia_interview_history
```yaml
Primary Key:
  - user_id (HASH)
  - start_time (RANGE)

Global Secondary Indexes:
  - category-index: category (HASH), start_time (RANGE)
  - score-index: user_id (HASH), score (RANGE)

Attributes:
  - user_id: string
  - interview_id: string
  - category: string
  - role: string
  - start_time: string
  - end_time: string
  - score: number (0-100)
  - feedback: map
  - transcript: string
  - created_at: string
```

### 3. S3 Bucket
- **Name**: sophia-interview-coach-frontend
- **Purpose**: Frontend hosting
- **Features**:
  - Static website hosting
  - Versioning enabled
  - CORS configured
  - CloudFront distribution

### 4. AWS Amplify
- **Framework**: React
- **Build**: npm run build
- **Deploy**: Auto-deploy on git push
- **Environment**: Production

## Authentication Flow

### Signup Flow

```
1. User enters: Email, Password, Full Name
2. Frontend validation
3. POST /auth/signup
   ├── Cognito: SignUp
   ├── Create user profile in DynamoDB
   └── Return user_id
4. Send verification email
5. User confirms email with code
6. POST /auth/confirm
   └── Cognito: ConfirmSignUp
7. User can now login
```

### Login Flow

```
1. User enters: Email, Password
2. POST /auth/login
   ├── Cognito: InitiateAuth (USER_PASSWORD_AUTH)
   ├── Validate credentials
   └── Return JWT tokens
3. Frontend stores tokens
4. Configure Authorization header: "Bearer {access_token}"
5. User authenticated ✓
```

### Token Refresh Flow

```
1. Access token expires
2. POST /auth/refresh
   ├── Cognito: InitiateAuth (REFRESH_TOKEN_AUTH)
   └── Return new access/id tokens
3. Frontend updates tokens
4. User session continues
```

### Logout Flow

```
1. User clicks logout
2. POST /auth/logout
   ├── Cognito: GlobalSignOut
   └── Invalidate tokens
3. Clear localStorage
4. Redirect to login
```

## API Endpoints

### Authentication Endpoints

#### POST /auth/signup
**Description**: Register new user

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response**:
```json
{
  "message": "Signup successful. Check email.",
  "user_id": "us-east-1:12345678-1234-1234-1234-123456789012",
  "username": "user@example.com"
}
```

#### POST /auth/login
**Description**: Authenticate user

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response**:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGc...",
  "id_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600,
  "user_id": "us-east-1:12345678-1234-1234-1234-123456789012"
}
```

#### POST /auth/confirm
**Description**: Confirm email with verification code

**Request**:
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response**:
```json
{
  "message": "Email confirmed successfully"
}
```

#### POST /auth/refresh
**Description**: Refresh JWT tokens

**Request**:
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response**:
```json
{
  "access_token": "eyJhbGc...",
  "id_token": "eyJhbGc...",
  "expires_in": 3600
}
```

#### POST /auth/logout
**Description**: Logout user and invalidate tokens

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response**:
```json
{
  "message": "Logout successful"
}
```

#### POST /auth/forgot-password
**Description**: Request password reset

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response**:
```json
{
  "message": "Reset code sent to email"
}
```

#### POST /auth/reset-password
**Description**: Confirm password reset

**Request**:
```json
{
  "email": "user@example.com",
  "code": "123456",
  "new_password": "NewPassword123!"
}
```

**Response**:
```json
{
  "message": "Password reset successful"
}
```

### User Profile Endpoints

#### GET /profile
**Description**: Get user profile

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response**:
```json
{
  "user_id": "us-east-1:...",
  "email": "user@example.com",
  "full_name": "John Doe",
  "experience_level": "mid",
  "interviews_completed": 5,
  "total_score": 425,
  "stats": {
    "total_interviews": 5,
    "average_score": 85,
    "completed_categories": ["backend_dev", "frontend_dev"],
    "last_interview": "2026-01-31T10:30:00Z",
    "skills": ["Python", "JavaScript", "React"]
  }
}
```

#### PUT /profile
**Description**: Update user profile

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "full_name": "John Doe",
  "experience_level": "senior",
  "skills": ["Python", "JavaScript", "React", "AWS"],
  "notification_settings": {
    "email_notifications": true,
    "interview_reminders": true
  }
}
```

**Response**:
```json
{
  "user_id": "...",
  "email": "user@example.com",
  "full_name": "John Doe",
  "updated_at": "2026-01-31T15:45:00Z"
}
```

### Interview History Endpoints

#### GET /interview/history
**Description**: Get user's interview history

**Headers**:
```
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `limit`: Number of results (default: 50)

**Response**:
```json
{
  "interviews": [
    {
      "interview_id": "int-123456",
      "user_id": "us-east-1:...",
      "category": "backend_dev",
      "role": "python_backend",
      "start_time": "2026-01-31T10:00:00Z",
      "end_time": "2026-01-31T10:30:00Z",
      "score": 85,
      "feedback": {
        "strengths": ["Problem solving", "Communication"],
        "improvements": ["System design", "Testing"],
        "summary": "Good overall performance"
      }
    }
  ],
  "count": 1
}
```

## Setup Instructions

### Step 1: Create Cognito Infrastructure

```bash
# Run setup script
python setup_cognito.py

# This will create:
# - Cognito User Pool
# - App Client
# - Auth Domain
# - DynamoDB Tables
# - S3 Bucket
# - Configuration file (cognito_config.json)
```

### Step 2: Update Configuration

Update `src/auth_handlers.py` with actual values:
```python
COGNITO_USER_POOL_ID = 'us-east-1_XXXXXXXXX'  # From setup output
COGNITO_CLIENT_ID = 'XXXXXXXXX'  # From setup output
```

### Step 3: Deploy Lambda Functions

```bash
# Update serverless.yml environment variables
export COGNITO_USER_POOL_ID='us-east-1_XXXXXXXXX'
export COGNITO_CLIENT_ID='XXXXXXXXX'

# Deploy to AWS
serverless deploy --stage prod
```

### Step 4: Configure API Gateway

1. Go to API Gateway Console
2. Select your API
3. Add Cognito Authorizer:
   - Name: `sophia-cognito-auth`
   - Provider: Your Cognito User Pool
   - Token Source: `Authorization`
4. Attach to /profile and /interview/history routes

### Step 5: Build Frontend

```bash
# Install dependencies
cd src/frontend
npm install

# Build production version
npm run build

# Deploy to Amplify
amplify init
amplify push
```

### Step 6: Deploy to Amplify

```bash
# Configure Amplify
amplify configure

# Initialize Amplify in project
amplify init

# Add hosting
amplify add hosting

# Deploy
amplify push

# Publish frontend
amplify publish
```

## Frontend Integration

### Using AuthContext

```javascript
import { useAuth } from './contexts/AuthContext';

function LoginComponent() {
  const { login, loading, error } = useAuth();

  const handleLogin = async (email, password) => {
    const result = await login(email, password);
    if (result.success) {
      // Navigate to dashboard
    }
  };

  return (
    // JSX here
  );
}
```

### Protected Routes

```javascript
import { useAuth } from './contexts/AuthContext';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return children;
}

// Usage
<ProtectedRoute>
  <InterviewDashboard />
</ProtectedRoute>
```

## Security Features

### Password Security
- Minimum 8 characters
- Requires uppercase, lowercase, number, special character
- Encrypted storage in Cognito
- Never transmitted in plain text

### Token Security
- JWT tokens with 1-hour expiration
- Refresh tokens for extended sessions
- Tokens stored in localStorage (consider httpOnly cookies for higher security)
- Token revocation on logout

### Data Protection
- DynamoDB encryption at rest
- TLS 1.2+ for all API calls
- CORS configured for your domain
- API Gateway request validation

### API Security
- Cognito Authorizer on protected endpoints
- Input validation on all endpoints
- Rate limiting via API Gateway
- CloudWatch monitoring and alerting

## Monitoring & Logs

### CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/ai-interview-coach-prod-authHandler --follow

# Query auth errors
aws logs describe-log-groups | grep sophia
aws logs filter-log-events --log-group-name /aws/lambda/ai-interview-coach-prod-authHandler --filter-pattern "ERROR"
```

### Metrics to Monitor
- Auth success/failure rate
- API response times
- DynamoDB throttling
- Cognito sign-up failures
- Token refresh rate

## Troubleshooting

### User Can't Verify Email
1. Check Cognito email settings
2. Verify email is not marked as spam
3. Resend verification code
4. Check email configuration in user pool

### Login Fails with "NotAuthorizedException"
1. Verify email and password are correct
2. Check user status in Cognito (not disabled/suspended)
3. Verify user confirmed email
4. Check Cognito sign-in settings

### "Invalid token" Error
1. Token may have expired - refresh token
2. Verify token format in Authorization header
3. Check API Gateway Cognito Authorizer configuration
4. Verify Cognito User Pool ID matches

### Profile Update Fails
1. Verify user is authenticated (valid token)
2. Check DynamoDB table permissions
3. Verify table name in environment variables
4. Check CloudWatch logs for specific error

## Next Steps

1. **Add MFA**: Enable multi-factor authentication
2. **Social Login**: Add Google/GitHub OAuth
3. **Admin Dashboard**: Monitor users and interviews
4. **Email Notifications**: Send interview reminders
5. **Analytics**: Track user engagement and performance
6. **Advanced Security**: Implement WAF rules

## Support

For issues or questions:
1. Check CloudWatch logs: `/aws/lambda/ai-interview-coach-prod-*`
2. Review Cognito user pool settings
3. Verify IAM permissions
4. Check API Gateway CORS configuration
5. Review DynamoDB access patterns
