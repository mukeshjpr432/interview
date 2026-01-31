# SOPHIA AI - COMPLETE DEPLOYMENT GUIDE
## User Authentication + Interview System in AWS

---

## Phase 1: Infrastructure Setup (30 minutes)

### Step 1: Prepare AWS Account

```bash
# 1. Ensure AWS CLI is configured
aws configure

# 2. Verify you have the right account
aws sts get-caller-identity

# 3. Check region is set to us-east-1
aws configure get region
```

### Step 2: Run Cognito Setup

**On Windows (PowerShell)**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_auth.ps1
```

**On Linux/Mac**:
```bash
bash setup_auth.sh
```

**What this does**:
- Creates Cognito User Pool
- Creates App Client  
- Creates Cognito Domain
- Creates DynamoDB tables (3 tables)
- Creates S3 bucket for frontend
- Generates configuration file

**Output**:
```
✓ Cognito User Pool ID: us-east-1_XXXXXXXXX
✓ Cognito Client ID: XXXXXXXXXXXXXXXXX
✓ DynamoDB Tables: Created (3)
✓ S3 Bucket: Created
✓ Configuration saved to: cognito_config.json
```

### Step 3: Update Credentials

Edit `src/auth_handlers.py` and update:

```python
COGNITO_USER_POOL_ID = 'us-east-1_XXXXXXXXX'  # From setup output
COGNITO_CLIENT_ID = 'XXXXXXXXXXXXXXXXX'       # From setup output
```

---

## Phase 2: Backend Deployment (15 minutes)

### Step 1: Install Dependencies

```bash
# Install serverless framework
npm install -g serverless

# Install Python dependencies
pip install -r requirements.txt

# Install serverless plugins
npm install
```

### Step 2: Deploy Lambda Functions

```bash
# Set environment variables
set COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
set COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXX

# Or on Linux/Mac
export COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
export COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXX

# Deploy to AWS
serverless deploy --stage prod
```

**Output will show**:
```
✓ Deploying ai-interview-coach to AWS
✓ endpoints:
  POST https://xxxxx.execute-api.us-east-1.amazonaws.com/auth/signup
  POST https://xxxxx.execute-api.us-east-1.amazonaws.com/auth/login
  GET  https://xxxxx.execute-api.us-east-1.amazonaws.com/profile
  ...
```

### Step 3: Test API Endpoints

```bash
# Test signup
curl -X POST https://xxxxx.execute-api.us-east-1.amazonaws.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'

# Test login
curl -X POST https://xxxxx.execute-api.us-east-1.amazonaws.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

---

## Phase 3: Frontend Deployment (30 minutes)

### Step 1: Install Frontend Dependencies

```bash
cd src/frontend
npm install
```

### Step 2: Configure Environment

Create `.env` file in `src/frontend`:

```bash
REACT_APP_API_URL=https://xxxxx.execute-api.us-east-1.amazonaws.com
REACT_APP_COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
REACT_APP_COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXX
REACT_APP_COGNITO_REGION=us-east-1
```

### Step 3: Build Frontend

```bash
npm run build

# Output
# > react-scripts build
# Creating an optimized production build...
# ✓ File sizes after gzip:
#   build/static/js/main.xxxxx.js  125 KB
# The build folder is ready to be deployed.
```

### Step 4: Deploy to AWS Amplify

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify
amplify init

# Choose settings:
# - Project name: sophia-interview-coach
# - Environment: prod
# - Default editor: Visual Studio Code
# - Profile: default

# Add hosting
amplify add hosting
# - Select: Amazon CloudFront and S3

# Deploy
amplify publish

# Output:
# ✓ Hosted URL: https://xxxxx.amplifyapp.com
```

### Step 5: Custom Domain (Optional)

```bash
# Add custom domain in Amplify console
# Domain: sophia.yourdomain.com
# Manage DNS settings in Route53 or your DNS provider
```

---

## Phase 4: API Gateway Configuration (10 minutes)

### Add Cognito Authorizer

1. Go to AWS API Gateway Console
2. Select your API
3. Click on "Authorizers"
4. Create authorizer:
   - **Name**: sophia-cognito-auth
   - **Type**: Cognito User Pool
   - **Cognito User Pool**: Select your pool
   - **Token Source**: Authorization

### Protect Endpoints

1. Select resource: `/profile`
2. Method: GET/PUT
3. Authorization: sophia-cognito-auth
4. Repeat for: `/interview/history`

---

## Phase 5: Testing & Verification (15 minutes)

### Test User Registration

```bash
# 1. Visit your frontend
https://xxxxx.amplifyapp.com

# 2. Click "Sign Up"
# 3. Fill in form:
#    Email: testuser@example.com
#    Password: TestPassword123!
#    Full Name: Test User
# 4. Click "Create Account"
# 5. Check email for verification code
# 6. Enter code in app
```

### Test User Login

```bash
# 1. Click "Sign In"
# 2. Enter credentials:
#    Email: testuser@example.com
#    Password: TestPassword123!
# 3. Click "Sign In"
# 4. View dashboard
```

### Test User Profile

```bash
# 1. Click on "Profile"
# 2. View user information
# 3. Click "Edit Profile"
# 4. Update experience level
# 5. Click "Save Changes"
# 6. Verify changes saved
```

### Test Interview History

```bash
# 1. Complete a mock interview
# 2. Click "Interview History"
# 3. View past interviews
# 4. Check scores and feedback
```

### Test Interview Flow

```bash
# 1. Click "Start Interview"
# 2. Select category and role
# 3. Complete interview
# 4. View evaluation results
# 5. Check profile updated with score
# 6. View in interview history
```

---

## Phase 6: Monitoring & Maintenance

### CloudWatch Monitoring

```bash
# View auth handler logs
aws logs tail /aws/lambda/ai-interview-coach-prod-authHandler --follow

# View orchestrator logs
aws logs tail /aws/lambda/ai-interview-coach-prod-orchestrator --follow

# View errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/ai-interview-coach-prod-authHandler \
  --filter-pattern "ERROR"
```

### DynamoDB Monitoring

```bash
# Check table metrics
aws dynamodb describe-table --table-name sophia_user_profiles \
  --query 'Table.{Name:TableName,Status:TableStatus,Size:TableSizeBytes}'

# View consumed capacity
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedWriteCapacityUnits \
  --dimensions Name=TableName,Value=sophia_user_profiles \
  --statistics Sum \
  --start-time 2026-01-31T00:00:00Z \
  --end-time 2026-02-01T00:00:00Z \
  --period 3600
```

### Cognito Monitoring

```bash
# Check user sign-up activity
aws cognito-idp describe-user-pool \
  --user-pool-id us-east-1_XXXXXXXXX \
  --query 'UserPool.EstimatedNumberOfUsers'

# List recent users
aws cognito-idp list-users \
  --user-pool-id us-east-1_XXXXXXXXX \
  --limit 10
```

---

## Troubleshooting

### Frontend Won't Load

```bash
# 1. Check build
npm run build

# 2. Check environment variables
echo "API_URL=$REACT_APP_API_URL"

# 3. Check Amplify deployment
amplify status

# 4. Check CloudFront distribution
aws cloudfront list-distributions
```

### Auth Endpoints Return 500 Error

```bash
# 1. Check Lambda logs
aws logs tail /aws/lambda/ai-interview-coach-prod-authHandler

# 2. Verify Cognito credentials
echo "Pool ID: $COGNITO_USER_POOL_ID"
echo "Client ID: $COGNITO_CLIENT_ID"

# 3. Test Cognito API directly
aws cognito-idp list-users --user-pool-id us-east-1_XXXXXXXXX
```

### Login Fails

```bash
# 1. Verify user exists in Cognito
aws cognito-idp admin-get-user \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com

# 2. Check user status
# Status should be: CONFIRMED

# 3. Reset password if needed
aws cognito-idp admin-set-user-password \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com \
  --password NewPassword123! \
  --permanent
```

### Cognito Setup Failed

```bash
# 1. Check Python version
python --version  # Should be 3.7+

# 2. Check boto3 installation
pip list | grep boto3

# 3. Check AWS credentials
aws sts get-caller-identity

# 4. Verify region
aws configure get region  # Should be us-east-1
```

---

## Estimated Costs (Monthly)

| Service | Usage | Cost |
|---------|-------|------|
| Cognito | 100 users | $0.00 (free tier) |
| DynamoDB | <25GB, <1M requests | $1.00 |
| Lambda | 1000 invocations | $0.20 |
| API Gateway | 100K requests | $3.50 |
| S3 / CloudFront | 1GB | $0.50 |
| **Total** | | **~$5.20** |

*Costs based on low-to-medium usage. Scale automatically with Amplify.*

---

## Production Checklist

### Security
- [ ] Cognito password policy enforced
- [ ] Email verification enabled
- [ ] MFA configured (optional)
- [ ] API Gateway authorizers configured
- [ ] CORS configured for frontend domain
- [ ] WAF rules enabled (optional)

### Infrastructure
- [ ] DynamoDB backups enabled
- [ ] CloudWatch alarms configured
- [ ] Auto-scaling enabled
- [ ] VPC endpoints configured (optional)
- [ ] KMS encryption enabled (optional)

### Monitoring
- [ ] CloudWatch log groups configured
- [ ] Application metrics dashboard created
- [ ] Error alerts configured
- [ ] Performance baselines established

### Deployment
- [ ] Frontend deployed to Amplify
- [ ] Custom domain configured
- [ ] SSL certificate installed
- [ ] CDN caching optimized
- [ ] Version control enabled

### Testing
- [ ] User registration tested
- [ ] Email verification tested
- [ ] Login flow tested
- [ ] Profile management tested
- [ ] Interview history tracked
- [ ] Interview flow integrated
- [ ] Error handling tested

### Documentation
- [ ] API documentation updated
- [ ] Setup guide completed
- [ ] Troubleshooting guide updated
- [ ] Team trained

---

## Next Steps

### Immediate (Today)
✅ Run setup_auth.ps1 / setup_auth.sh  
✅ Deploy Lambda functions  
✅ Deploy frontend to Amplify  
✅ Test auth flow  

### Short Term (This Week)
- [ ] Add email notifications
- [ ] Implement MFA
- [ ] Add social login (Google, GitHub)
- [ ] Create admin dashboard
- [ ] Set up monitoring alerts

### Medium Term (This Month)
- [ ] Implement analytics
- [ ] Add interview recommendations
- [ ] Build mobile app
- [ ] Create onboarding flow
- [ ] Add interview scheduling

### Long Term (Next Quarter)
- [ ] AI-powered coaching
- [ ] Advanced analytics
- [ ] Video interview support
- [ ] Integration with job boards
- [ ] Enterprise features

---

## Support & Documentation

### Key Documentation Files
- `AUTH_SYSTEM_GUIDE.md` - Complete auth system documentation
- `AUTH_SYSTEM_SUMMARY.md` - Quick reference
- `SOPHIA_API_SPECIFICATION.md` - Full API reference
- `SOPHIA_DEPLOYMENT_GUIDE.md` - Deployment instructions

### Getting Help

**Common Issues**:
1. See "Troubleshooting" section above
2. Check AWS CloudWatch logs
3. Verify Cognito user pool settings
4. Review AUTH_SYSTEM_GUIDE.md

**Need More Help**:
1. Check CloudWatch logs for error messages
2. Review serverless.yml configuration
3. Verify environment variables
4. Test API endpoints with curl/Postman

---

## Deployment Summary

**Time to Deploy**: 90 minutes (1.5 hours)

**Components Deployed**:
- ✅ AWS Cognito User Pool
- ✅ 3 DynamoDB Tables
- ✅ Lambda Auth Handler
- ✅ React Frontend
- ✅ AWS Amplify Hosting
- ✅ API Gateway Endpoints
- ✅ S3 Storage
- ✅ CloudFront Distribution

**Result**: 
Complete user authentication system for Sophia AI Interview Coach, ready for production use with 100+ concurrent users.

---

*Deployment Guide v1.0*  
*System: Sophia AI Interview Coach*  
*Date: January 31, 2026*  
*Status: Ready for Production*
