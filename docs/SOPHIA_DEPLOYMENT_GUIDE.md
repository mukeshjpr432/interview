# Deployment Guide - AI Interview Coach

## Prerequisites

Before deploying, ensure you have:

- ✅ AWS Account with billing enabled
- ✅ AWS CLI configured (`aws configure`)
- ✅ Node.js 18+ installed
- ✅ Python 3.11+ installed
- ✅ Serverless Framework (`npm install -g serverless`)
- ✅ Docker (for local development)
- ✅ Git

---

## Step 1: Environment Setup

### 1.1 Clone Repository
```bash
git clone https://github.com/yourusername/ai-interview-coach.git
cd ai-interview-coach
```

### 1.2 Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node dependencies
npm install
```

### 1.3 Configure AWS Credentials
```bash
aws configure
# AWS Access Key ID: [Your key]
# AWS Secret Access Key: [Your secret]
# Default region: us-east-1
# Default output format: json
```

### 1.4 Set Environment Variables
```bash
# Create .env file
cat > .env << EOF
AWS_REGION=us-east-1
BEDROCK_INTERVIEWER_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_EVALUATOR_MODEL=anthropic.claude-3-opus-20240229-v1:0
BEDROCK_COACH_MODEL=anthropic.claude-3-opus-20240229-v1:0
STAGE=dev
EOF
```

---

## Step 2: Local Development

### 2.1 Start Local DynamoDB
```bash
docker pull amazon/dynamodb-local
docker run -p 8000:8000 amazon/dynamodb-local

# In another terminal, create tables
python src/database/dynamodb_schema.py
```

### 2.2 Run Locally with Serverless Offline
```bash
serverless offline start
# API will be available at http://localhost:3000
```

### 2.3 Test Endpoints
```bash
# Start interview
curl -X POST http://localhost:3000/dev/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "job_role": "Software Engineer",
    "experience_level": "3+ years"
  }'

# Run tests
pytest tests/ -v
```

---

## Step 3: Deploy to AWS

### 3.1 Deploy Development Environment
```bash
serverless deploy --stage dev
```

### 3.2 Deploy Staging Environment
```bash
serverless deploy --stage staging
```

### 3.3 Deploy Production Environment
```bash
serverless deploy --stage prod
```

**Output will show**:
```
Deploying ai-interview-coach to stage prod (us-east-1)
...
Service Information
service: ai-interview-coach
stage: prod
region: us-east-1
stack: ai-interview-coach-prod
endpoint: https://xxxxxx.execute-api.us-east-1.amazonaws.com/prod
functions:
  orchestrator: ai-interview-coach-prod-orchestrator
  voiceHandler: ai-interview-coach-prod-voiceHandler
```

---

## Step 4: Create DynamoDB Tables in AWS

```bash
# Create tables in production AWS account
python src/database/dynamodb_schema.py
```

Or use AWS Console:
1. Go to DynamoDB
2. Create tables manually as per `dynamodb_schema.py`

---

## Step 5: Configure IAM Permissions

### 5.1 Create Custom IAM Role (if not using Serverless defaults)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:*:table/interview*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::interview-coach-voice-storage/*"
    }
  ]
}
```

---

## Step 6: Enable AWS Services

### 6.1 Enable Bedrock
```bash
# Go to AWS Bedrock console
# https://console.aws.amazon.com/bedrock/

# Request access to models:
# - Claude 3 Sonnet
# - Claude 3 Opus
# - Llama 2 70B (optional)

# Takes 5-10 minutes to enable
```

### 6.2 Enable Transcribe & Polly (if using voice)
```bash
# Transcribe is automatically enabled
# Polly is automatically enabled
```

---

## Step 7: Deploy Frontend

### 7.1 Build Frontend
```bash
cd src/frontend
npm install
npm run build
```

### 7.2 Deploy to S3 + CloudFront
```bash
# Create S3 bucket for frontend
aws s3 mb s3://ai-interview-coach-frontend-prod

# Deploy
npm run deploy
```

Or use manual deployment:
```bash
# Build
npm run build

# Upload to S3
aws s3 sync build/ s3://ai-interview-coach-frontend-prod --delete

# Invalidate CloudFront (if using)
aws cloudfront create-invalidation \
  --distribution-id E1234EXAMPLE \
  --paths "/*"
```

---

## Step 8: Configure API Gateway & Domain

### 8.1 Create Custom Domain
```bash
serverless create_domain --stage prod
```

### 8.2 Map Domain
```bash
# Update Route53 or your DNS provider
# Point domain to API Gateway endpoint
```

---

## Step 9: Set Up Monitoring

### 9.1 Enable CloudWatch Logs
```bash
# Logs are automatically enabled

# View logs
aws logs tail /aws/lambda/ai-interview-coach-prod-orchestrator --follow
```

### 9.2 Create CloudWatch Alarms
```bash
# Error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name interview-error-rate \
  --alarm-description "Alert on high error rate" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

### 9.3 Enable X-Ray Tracing
```bash
# Uncomment in serverless.yml:
# provider:
#   tracing:
#     lambda: true
#     apiGateway: true

serverless deploy
```

---

## Step 10: Set Up CI/CD (GitHub Actions)

### 10.1 Create GitHub Secrets
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
BEDROCK_REGION
```

### 10.2 Create Workflow File
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Install dependencies
        run: npm install
      
      - name: Run tests
        run: pytest tests/ -v
      
      - name: Deploy to production
        run: serverless deploy --stage prod
```

---

## Step 11: Database Backup & Recovery

### 11.1 Enable DynamoDB Backups
```bash
# Enable point-in-time recovery
aws dynamodb update-continuous-backups \
  --table-name interview_sessions \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
  --region us-east-1
```

### 11.2 Create Manual Backup
```bash
aws dynamodb create-backup \
  --table-name interview_sessions \
  --backup-name interview-sessions-backup-$(date +%s)
```

---

## Step 12: Testing Deployment

### 12.1 Health Check
```bash
curl https://your-api-domain/prod/health
```

### 12.2 Integration Test
```bash
# Run full integration test
python tests/test_integration.py
```

### 12.3 Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 https://your-api-domain/prod/interview/status

# Using Locust
locust -f tests/locustfile.py
```

---

## Troubleshooting

### Issue: Bedrock Model Not Found
```bash
# Solution: Request access in Bedrock console
# Wait 5-10 minutes for activation
```

### Issue: DynamoDB Throttling
```bash
# Solution: Increase provisioned capacity or use on-demand billing
aws dynamodb update-table \
  --table-name interview_sessions \
  --billing-mode PAY_PER_REQUEST
```

### Issue: Lambda Timeout
```bash
# Increase timeout in serverless.yml
# functions:
#   orchestrator:
#     timeout: 600  # Increase from 300
```

### Issue: S3 Permission Denied
```bash
# Check bucket policy and IAM role
aws s3api get-bucket-policy --bucket interview-coach-voice-storage
```

---

## Scaling Considerations

### 12.1 Increase DynamoDB Capacity
```bash
# Switch to pay-per-request
aws dynamodb update-billing-mode \
  --table-name interview_sessions \
  --billing-mode PAY_PER_REQUEST
```

### 12.2 Enable API Gateway Caching
```yaml
# serverless.yml
functions:
  orchestrator:
    events:
      - httpApi:
          path: /interview/{id}/report
          method: GET
          caching:
            enabled: true
            ttlInSeconds: 3600
```

### 12.3 Use CloudFront for Static Assets
```bash
serverless plugin install -n serverless-cloudfront-invalidate
```

---

## Production Checklist

- [ ] AWS Account configured and ready
- [ ] Bedrock access requested and approved
- [ ] DynamoDB tables created
- [ ] Lambda functions deployed
- [ ] IAM roles configured correctly
- [ ] API Gateway endpoints working
- [ ] Frontend deployed to S3
- [ ] CloudFront distribution created
- [ ] Custom domain configured
- [ ] SSL certificate installed
- [ ] CloudWatch monitoring enabled
- [ ] Logging configured
- [ ] Backups enabled
- [ ] CI/CD pipeline set up
- [ ] Load testing passed
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Team trained on operations

---

## Rollback Procedures

### Quick Rollback
```bash
# Redeploy previous version
git checkout previous-commit
serverless deploy --stage prod
```

### Database Rollback
```bash
# Restore from DynamoDB backup
aws dynamodb restore-table-from-backup \
  --target-table-name interview_sessions_restored \
  --backup-arn arn:aws:dynamodb:us-east-1:123456789012:table/interview_sessions/backup/01234567890123-abcdefgh
```

---

## Support & Documentation

- **AWS Bedrock**: https://docs.aws.amazon.com/bedrock/
- **Lambda**: https://docs.aws.amazon.com/lambda/
- **DynamoDB**: https://docs.aws.amazon.com/dynamodb/
- **Serverless Framework**: https://www.serverless.com/framework/docs

---

**Last Updated**: January 2025
**Status**: Production Ready
