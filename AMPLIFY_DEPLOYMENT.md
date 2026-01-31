# Sophia AI Frontend - AWS Amplify Deployment

## Prerequisites
- AWS Account with Amplify enabled
- GitHub repository with frontend code
- AWS IAM user with Amplify and related permissions

## Deployment Steps

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial frontend setup"
git remote add origin https://github.com/YOUR_USERNAME/sophia-ai.git
git push -u origin main
```

### 2. Deploy via AWS Amplify Console

**Option A: Using AWS Console (Easiest)**
1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click "New App" > "Host Web App"
3. Select GitHub as the repository service
4. Authorize Amplify to access your GitHub
5. Select your repository and main branch
6. Click "Save and Deploy"

**Option B: Using AWS Amplify CLI**
```bash
npm install -g @aws-amplify/cli

amplify configure
amplify init
amplify add hosting
amplify publish
```

### 3. Configure Custom Domain

In AWS Amplify Console:
1. Go to App Settings > Domain Management
2. Click "Add Domain"
3. Enter your custom domain (e.g., `app.yourdomain.com`)
4. Amplify provides DNS records to add to your domain registrar
5. Add CNAME record to your domain provider
6. Amplify automatically handles SSL/TLS

### 4. Build Configuration

The `amplify.yml` file in the root directory contains:
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

### 5. Environment Variables

Add to Amplify Console under "Environment Variables":
```
REACT_APP_API_URL=https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com
REACT_APP_COGNITO_REGION=us-east-1
REACT_APP_COGNITO_USER_POOL_ID=us-east-1_S8nbIWo7v
REACT_APP_COGNITO_CLIENT_ID=18q1qj09bnngsu8fn3lsnso8cd
```

## Deployment Features

✅ **Automatic CI/CD**
- Automatic builds on every push to main branch
- Pull request previews for feature branches
- Rollback capability

✅ **Custom Domain**
- Use your own domain
- Free SSL/TLS certificate
- HTTPS enforcement

✅ **Performance**
- Global CDN (CloudFront)
- Image optimization
- Automatic minification

✅ **Security**
- CORS configuration
- CSRF protection
- Environment variable encryption

## After Deployment

### Test Endpoints
```bash
# From Amplify App URL
curl https://your-amplify-app.amplifyapp.com

# API Integration
curl -X POST https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test@123456","full_name":"Test User"}'
```

### Monitor Performance
- Amplify Console shows deployment history
- CloudFront metrics available
- Custom domain propagation time: 24-48 hours

## Troubleshooting

**Build Fails**
- Check Node version compatibility
- Ensure all dependencies in package.json
- Review build logs in Amplify Console

**CORS Errors**
- Verify API Gateway CORS headers
- Check allowed origins in AuthContext.js

**Domain Not Resolving**
- Wait 24-48 hours for DNS propagation
- Verify CNAME record in domain registrar

## Cost Estimation
- Amplify: ~$0.15/GB data transfer (free tier: 15GB/month)
- CloudFront CDN: Included
- SSL/TLS: Free
- **Monthly Cost: ~$2-5 for typical usage**

## Next Steps
1. Commit all frontend files to GitHub
2. Connect GitHub repository to Amplify
3. Configure custom domain (optional)
4. Monitor deployment in Amplify Console
5. Test endpoints from live URL
