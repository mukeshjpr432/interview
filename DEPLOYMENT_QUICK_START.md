# 🚀 SOPHIA - QUICK DEPLOYMENT GUIDE

## ⚡ 5-Minute Quick Start

### Step 1: Setup Environment (1 min)
```bash
cd c:\AI_Project\interview

# Create .env file
cat > .env << EOF
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Bedrock
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# DynamoDB
DYNAMODB_REGION=us-east-1
INTERVIEW_TABLE=interview_sessions
EVALUATION_TABLE=evaluation_results
TRANSCRIPT_TABLE=interview_transcripts
PROFILE_TABLE=candidate_profiles

# Voice
POLLY_VOICE_ID=Joanna
TRANSCRIBE_REGION=us-east-1
S3_BUCKET=interview-coach-voice

# API
API_PORT=3000
API_STAGE=dev
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
ENABLE_CLOUDWATCH=true
EOF
```

### Step 2: Install Dependencies (1 min)
```bash
# Already done, but if needed:
pip install -r requirements.txt

# For serverless deployment:
npm install -g serverless
npm install
```

### Step 3: Configure AWS (1 min)
```bash
# Install AWS CLI if needed
pip install awscli

# Configure AWS credentials
aws configure
# Enter your AWS Access Key
# Enter your AWS Secret Key
# Region: us-east-1
# Output: json
```

### Step 4: Deploy to AWS (2 min)
```bash
# Using Serverless Framework
serverless deploy --stage dev

# Or deploy specific functions
serverless deploy function -f orchestrator --stage dev
serverless deploy function -f voiceHandler --stage dev
```

### Step 5: Test It!
```bash
# Get API endpoint from deployment output
API_URL=$(serverless info --stage dev | grep "POST" | head -1)

# Start interview
curl -X POST $API_URL/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "job_role": "Software Engineer",
    "experience_level": "mid",
    "candidate_name": "John Doe"
  }'
```

---

## 📋 DETAILED DEPLOYMENT STEPS

### Prerequisites Checklist

```
☑ AWS Account with appropriate permissions
☑ AWS CLI installed and configured
☑ Python 3.13+
☑ Node.js 18+
☑ Serverless Framework installed
☑ Git installed
☑ Text editor or IDE
```

### 1. AWS Setup

#### 1.1 Create IAM User
```bash
# Using AWS Console or CLI:
aws iam create-user --user-name sophia-deploy

# Attach policies
aws iam attach-user-policy \
  --user-name sophia-deploy \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

#### 1.2 Create Access Keys
```bash
aws iam create-access-key --user-name sophia-deploy
# Save: Access Key ID and Secret Access Key
```

#### 1.3 Configure AWS CLI
```bash
aws configure
# Paste Access Key ID
# Paste Secret Access Key  
# Region: us-east-1
# Output: json
```

### 2. Environment Configuration

#### 2.1 Create Environment File
```bash
# Copy template
cp .env.example .env

# Edit with your values
# AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
# AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

#### 2.2 Create S3 Bucket (for voice files)
```bash
aws s3 mb s3://interview-coach-voice-$(date +%s) \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket interview-coach-voice-xxx \
  --versioning-configuration Status=Enabled
```

### 3. Deploy Lambda Functions

#### 3.1 Package Code
```bash
# Using Serverless Framework
serverless package --stage dev
```

#### 3.2 Deploy All Services
```bash
# Full deployment
serverless deploy --stage dev

# Or deploy individually:
serverless deploy function -f orchestrator --stage dev
serverless deploy function -f voiceHandler --stage dev
```

#### 3.3 Create DynamoDB Tables
```bash
python src/database/dynamodb_schema.py
```

### 4. Verify Deployment

#### 4.1 Check Lambda Functions
```bash
aws lambda list-functions --region us-east-1 | grep sophia
```

#### 4.2 Check DynamoDB Tables
```bash
aws dynamodb list-tables --region us-east-1 | grep interview
```

#### 4.3 Check API Gateway
```bash
aws apigateway get-rest-apis --region us-east-1
```

### 5. Test API Endpoints

#### 5.1 Start Interview
```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "job_role": "Software Engineer",
    "experience_level": "mid",
    "candidate_id": "candidate_001"
  }'

# Response:
# {
#   "interview_id": "int_12345678",
#   "status": "started",
#   "first_question": "Tell me about yourself..."
# }
```

#### 5.2 Submit Response
```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/interview/int_12345678/respond \
  -H "Content-Type: application/json" \
  -d '{
    "response": "I am a software engineer with 5 years of experience..."
  }'
```

#### 5.3 End Interview
```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/interview/int_12345678/end
```

#### 5.4 Get Results
```bash
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/interview/int_12345678/results
```

---

## 🎯 DEPLOYMENT CHECKLIST

### Pre-Deployment
```
☑ AWS Account setup complete
☑ IAM user created with permissions
☑ Access keys generated
☑ AWS CLI configured
☑ .env file created with credentials
☑ All code files reviewed
☑ Tests pass locally (100%)
☑ Git repository initialized
```

### Deployment
```
☑ S3 bucket created for voice files
☑ Lambda functions packaged
☑ Infrastructure deployed with Serverless
☑ DynamoDB tables created
☑ API Gateway endpoints configured
☑ CloudWatch logging enabled
☑ IAM roles and policies set
☑ Environment variables deployed
```

### Post-Deployment
```
☑ API endpoints responding
☑ DynamoDB tables accessible
☑ Lambda functions executable
☑ CloudWatch logs visible
☑ Integration tests passing
☑ Load testing completed
☑ Security scan passed
☑ Documentation updated
```

### Monitoring Setup
```
☑ CloudWatch alarms created
☑ Error notifications configured
☑ Performance metrics dashboards created
☑ Cost monitoring enabled
☑ Log aggregation configured
☑ Health check endpoints verified
```

---

## 💡 COMMON ISSUES & SOLUTIONS

### Issue 1: Access Denied Error
```
Error: AccessDenied on DynamoDB
Solution:
1. Check AWS credentials in .env
2. Verify IAM user has DynamoDB permissions
3. Ensure region is correct (us-east-1)
```

### Issue 2: Bedrock Model Not Found
```
Error: Model not found or access denied
Solution:
1. Verify Bedrock access is enabled in AWS Console
2. Check region supports the model
3. Request model access if needed
4. Update BEDROCK_MODEL_ID in .env
```

### Issue 3: Lambda Timeout
```
Error: Task timed out after 30.00 seconds
Solution:
1. Increase timeout in serverless.yml
2. Optimize code for performance
3. Check for slow API calls
4. Enable Lambda layers for dependencies
```

### Issue 4: S3 Bucket Not Found
```
Error: NoSuchBucket
Solution:
1. Create bucket: aws s3 mb s3://your-bucket
2. Update S3_BUCKET in .env
3. Verify bucket region matches AWS_REGION
```

---

## 📊 DEPLOYMENT VERIFICATION

After deployment, verify with:

```bash
# 1. Test Lambda invocation
aws lambda invoke \
  --function-name sophia-orchestrator-dev \
  --region us-east-1 \
  response.json

# 2. Check DynamoDB connectivity
aws dynamodb describe-table \
  --table-name interview_sessions \
  --region us-east-1

# 3. List created API resources
aws apigateway get-resources \
  --rest-api-id your-api-id \
  --region us-east-1

# 4. View Lambda logs
aws logs tail /aws/lambda/sophia-orchestrator-dev \
  --follow --region us-east-1
```

---

## 🔄 UPDATES & REDEPLOYMENT

### For Code Updates:
```bash
# 1. Update code files
git add .
git commit -m "Updated Sophia AI agent"

# 2. Redeploy
serverless deploy --stage dev

# 3. Verify deployment
serverless info --stage dev
```

### For Configuration Changes:
```bash
# 1. Update .env
nano .env

# 2. Redeploy with new environment
serverless deploy --stage dev --update-env
```

### For Database Migrations:
```bash
# 1. Backup existing data
aws dynamodb create-backup \
  --table-name interview_sessions \
  --backup-name interview_sessions_backup_$(date +%s)

# 2. Run migration script
python scripts/migrate_db.py

# 3. Verify data
python scripts/validate_db.py
```

---

## 📈 SCALING FOR PRODUCTION

### Stage: Development ✅
```bash
serverless deploy --stage dev
# Low traffic, testing environment
```

### Stage: Staging
```bash
# Prepare for production testing
serverless deploy --stage staging

# Run load tests
locust -f tests/locustfile.py

# Monitor performance
cloudwatch-monitor.sh
```

### Stage: Production
```bash
# Full production deployment
serverless deploy --stage prod

# Enable auto-scaling
aws application-autoscaling register-scalable-target \
  --service-namespace dynamodb \
  --resource-id table/interview_sessions \
  --scalable-dimension dynamodb:table:WriteCapacityUnits \
  --min-capacity 100 \
  --max-capacity 40000

# Set scaling policy
aws application-autoscaling put-scaling-policy \
  --policy-name sophia-scaling \
  --policy-type TargetTrackingScaling
```

---

## 🎯 SUCCESS INDICATORS

You'll know deployment is successful when:

✅ API endpoints return 200 OK
✅ DynamoDB tables show items created
✅ CloudWatch logs show execution traces
✅ Lambda invocations complete in < 5 seconds
✅ Transcription works with audio files
✅ Bedrock API calls return valid responses
✅ Frontend loads without errors
✅ Voice audio plays correctly

---

## 📞 SUPPORT

If you encounter issues:

1. **Check CloudWatch Logs**
   ```bash
   aws logs tail /aws/lambda/sophia-orchestrator-dev --follow
   ```

2. **Review API Gateway Logs**
   ```bash
   aws apigateway get-account
   ```

3. **Test Bedrock Connectivity**
   ```bash
   python test_bedrock_connection.py
   ```

4. **Validate DynamoDB Access**
   ```bash
   python test_dynamodb_connection.py
   ```

---

**Deployment Guide Created**: January 31, 2026  
**Status**: Ready for Production  
**Estimated Deployment Time**: 15-30 minutes

Good luck deploying Sophia! 🚀
