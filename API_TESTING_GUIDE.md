# 🧪 SOPHIA AI - API TESTING GUIDE

**Status**: ✅ **ENDPOINTS LIVE & READY FOR TESTING**

---

## 🌐 BASE URL

```
https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com
```

**Region**: us-east-1  
**Stage**: dev  
**Status**: ✅ ACTIVE NOW

---

## 📋 AVAILABLE ENDPOINTS

### 🔐 Authentication Endpoints (7)

#### 1. User Signup
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "Password@123",
  "full_name": "John Doe"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "message": "User created. Check email to verify.",
  "user_id": "us-east-1_S8nbIWo7v_abc123xyz"
}
```

**cURL Example**:
```bash
curl -X POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password@123",
    "full_name": "John Doe"
  }'
```

**PowerShell Example**:
```powershell
$payload = @{
    email = "user@example.com"
    password = "Password@123"
    full_name = "John Doe"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup" `
    -Method POST `
    -ContentType "application/json" `
    -Body $payload
```

---

#### 2. User Login
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/login
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "Password@123"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "refresh_token_value",
    "expires_in": 3600,
    "token_type": "Bearer"
  }
}
```

**cURL Example**:
```bash
curl -X POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password@123"
  }'
```

---

#### 3. Confirm Email
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/confirm
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Note**: Code sent to email during signup

---

#### 4. Refresh Token
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/refresh
```

**Request Body**:
```json
{
  "refresh_token": "refresh_token_from_login"
}
```

**Response**: New access token

---

#### 5. Logout
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/logout
```

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "access_token": "token_from_login"
}
```

---

#### 6. Forgot Password
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/forgot-password
```

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response**: Reset code sent to email

---

#### 7. Reset Password
```
POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/reset-password
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "code": "reset_code_from_email",
  "new_password": "NewPassword@123"
}
```

---

### 👤 Profile Endpoints (2)

#### 1. Get Profile
```
GET https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/profile
```

**Headers**:
```
Authorization: Bearer <access_token>
```

**Success Response (200)**:
```json
{
  "success": true,
  "profile": {
    "user_id": "abc123",
    "email": "user@example.com",
    "full_name": "John Doe",
    "experience_level": "junior",
    "interviews_completed": 5,
    "total_score": 450,
    "average_score": 90
  }
}
```

**cURL Example**:
```bash
curl -X GET https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/profile \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json"
```

---

#### 2. Update Profile
```
PUT https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/profile
```

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "full_name": "John Smith",
  "experience_level": "mid",
  "phone_number": "+1234567890",
  "preferred_categories": ["Web Development", "Databases"]
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "profile": { ... }
}
```

---

### 📊 Interview History Endpoint (1)

#### Get Interview History
```
GET https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/interview/history
```

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters (Optional)**:
```
?limit=10        - Number of records (default: 50)
?category=Web    - Filter by category
?min_score=80    - Filter by minimum score
```

**Success Response (200)**:
```json
{
  "success": true,
  "interviews": [
    {
      "interview_id": "int_123",
      "category": "Web Development",
      "role": "Frontend Developer",
      "score": 92,
      "date": "2026-01-31T10:30:00Z",
      "duration": 1800,
      "feedback": "Excellent performance...",
      "completed": true
    }
  ],
  "total": 5,
  "statistics": {
    "average_score": 88,
    "highest_score": 95,
    "lowest_score": 78
  }
}
```

---

## 🧪 QUICK TEST EXAMPLES

### Test 1: Sign Up
```bash
curl -X POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass@123",
    "full_name": "John Doe"
  }'
```

### Test 2: Login (After Email Verification)
```bash
curl -X POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass@123"
  }'
```

### Test 3: Get Profile (Use token from login)
```bash
curl -X GET https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

### Test 4: Update Profile
```bash
curl -X PUT https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith",
    "experience_level": "mid"
  }'
```

### Test 5: Get Interview History
```bash
curl -X GET https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/interview/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🛠️ POSTMAN SETUP

### 1. Create New Request
- **URL**: `https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup`
- **Method**: POST
- **Content-Type**: application/json

### 2. Headers
```
Content-Type: application/json
```

### 3. Body (raw JSON)
```json
{
  "email": "test@example.com",
  "password": "Test@1234",
  "full_name": "Test User"
}
```

### 4. Send Request
Click "Send" to test

### 5. For Protected Endpoints
- Get access token from login response
- Go to "Headers" tab
- Add: `Authorization: Bearer <token>`
- Send request

---

## 📱 MOBILE/APP TESTING

### JavaScript/Fetch
```javascript
const signup = async () => {
  const response = await fetch(
    'https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'user@example.com',
        password: 'Password@123',
        full_name: 'John Doe'
      })
    }
  );
  return response.json();
};
```

### Python Requests
```python
import requests
import json

url = "https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup"
payload = {
    "email": "user@example.com",
    "password": "Password@123",
    "full_name": "John Doe"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Node.js Axios
```javascript
const axios = require('axios');

const signup = async () => {
  try {
    const response = await axios.post(
      'https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup',
      {
        email: 'user@example.com',
        password: 'Password@123',
        full_name: 'John Doe'
      }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

---

## ✅ EXPECTED BEHAVIORS

### Signup Success (200)
✅ User created  
✅ Verification email sent  
✅ User ID returned  

### Signup Failure (400)
❌ Email already exists  
❌ Password too weak  
❌ Invalid email format  

### Login Success (200)
✅ Tokens returned  
✅ Valid JWT token  
✅ Refresh token provided  

### Login Failure (401)
❌ Invalid credentials  
❌ Email not verified  
❌ Account locked  

### Profile Get Success (200)
✅ User data returned  
✅ Statistics calculated  

### Profile Get Failure (401)
❌ Invalid token  
❌ Token expired  

---

## 🔍 ERROR CODES

| Code | Message | Meaning |
|------|---------|---------|
| 200 | OK | Success |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Email already exists |
| 500 | Server Error | Lambda error |

---

## 🚀 DEPLOYMENT STATUS

| Component | Status | URL |
|-----------|--------|-----|
| API Gateway | ✅ LIVE | https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com |
| Cognito | ✅ ACTIVE | us-east-1_S8nbIWo7v |
| DynamoDB | ✅ READY | sophia_users, profiles, history |
| Lambda | ✅ DEPLOYED | ai-interview-coach-dev-authHandler |

---

## 📊 TESTING CHECKLIST

- [ ] Test signup endpoint
- [ ] Verify email sent
- [ ] Confirm email with code
- [ ] Test login endpoint
- [ ] Get access token
- [ ] Test profile GET
- [ ] Test profile PUT
- [ ] Test interview history
- [ ] Test token refresh
- [ ] Test logout
- [ ] Test error cases

---

## 🎯 NEXT STEPS

1. **Test Signup**
   - Use endpoint above
   - Check your email for verification code
   - Note the user_id

2. **Verify Email**
   - Use code from email
   - Call confirm endpoint

3. **Login**
   - Use credentials from signup
   - Save access_token

4. **Get Profile**
   - Use access_token in header
   - View your profile data

5. **Update Profile**
   - Modify profile fields
   - Verify changes saved

6. **Interview History**
   - Get all interviews
   - Check statistics

---

**API Status**: ✅ **READY FOR TESTING**  
**Date**: January 31, 2026  
**Region**: us-east-1  
**Endpoint**: https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com  

🎉 **Start testing your authentication system!** 🎉
