#!/bin/bash
# SOPHIA AI INTERVIEW COACH - AUTH SYSTEM QUICK SETUP
# Run this script to set up AWS Cognito, DynamoDB, and Auth Infrastructure

set -e

echo "======================================================"
echo "  SOPHIA AI - AUTHENTICATION SYSTEM SETUP"
echo "======================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is required but not installed"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# Step 1: Check AWS credentials
echo -e "${BLUE}Step 1: Verifying AWS credentials...${NC}"
if aws sts get-caller-identity &> /dev/null; then
    ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
    echo -e "${GREEN}✓ AWS Account: $ACCOUNT${NC}"
else
    echo -e "${YELLOW}⚠ AWS credentials not configured. Run:${NC}"
    echo "  aws configure"
    exit 1
fi
echo ""

# Step 2: Install Python dependencies
echo -e "${BLUE}Step 2: Installing Python dependencies...${NC}"
pip install -q boto3 botocore
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 3: Create Cognito infrastructure
echo -e "${BLUE}Step 3: Creating Cognito infrastructure...${NC}"
python3 setup_cognito.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Some errors occurred during setup${NC}"
    echo "  Check the output above for details"
fi

echo ""

# Step 4: Load configuration
if [ -f "cognito_config.json" ]; then
    echo -e "${BLUE}Step 4: Loading configuration...${NC}"
    
    COGNITO_USER_POOL_ID=$(python3 -c "import json; print(json.load(open('cognito_config.json'))['COGNITO_USER_POOL_ID'])")
    COGNITO_CLIENT_ID=$(python3 -c "import json; print(json.load(open('cognito_config.json'))['COGNITO_CLIENT_ID'])")
    
    echo -e "${GREEN}✓ Configuration loaded${NC}"
    echo "  User Pool ID: $COGNITO_USER_POOL_ID"
    echo "  Client ID: $COGNITO_CLIENT_ID"
    echo ""
    
    # Step 5: Update environment variables
    echo -e "${BLUE}Step 5: Updating environment variables...${NC}"
    
    # Create .env file
    cat > .env.auth << EOF
# Cognito Configuration
COGNITO_USER_POOL_ID=$COGNITO_USER_POOL_ID
COGNITO_CLIENT_ID=$COGNITO_CLIENT_ID
COGNITO_REGION=us-east-1
API_ENDPOINT=https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com

# Frontend Configuration
REACT_APP_API_URL=https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com
REACT_APP_COGNITO_USER_POOL_ID=$COGNITO_USER_POOL_ID
REACT_APP_COGNITO_CLIENT_ID=$COGNITO_CLIENT_ID
REACT_APP_COGNITO_REGION=us-east-1
EOF
    
    echo -e "${GREEN}✓ Environment file created (.env.auth)${NC}"
    echo ""
fi

# Step 6: Summary
echo -e "${GREEN}======================================================"
echo "  SETUP COMPLETE! ✅"
echo "======================================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Update src/auth_handlers.py with Cognito credentials"
echo "   COGNITO_USER_POOL_ID = '$COGNITO_USER_POOL_ID'"
echo "   COGNITO_CLIENT_ID = '$COGNITO_CLIENT_ID'"
echo ""
echo "2. Deploy Lambda functions:"
echo "   export COGNITO_USER_POOL_ID='$COGNITO_USER_POOL_ID'"
echo "   export COGNITO_CLIENT_ID='$COGNITO_CLIENT_ID'"
echo "   serverless deploy --stage prod"
echo ""
echo "3. Build and deploy frontend:"
echo "   cd src/frontend"
echo "   npm install"
echo "   npm run build"
echo "   npm run deploy"
echo ""
echo "4. Configure API Gateway Cognito Authorizer"
echo ""
echo "Configuration saved to: ${BLUE}cognito_config.json${NC}"
echo "Environment saved to: ${BLUE}.env.auth${NC}"
echo ""
echo "View auth endpoints:"
echo "  - Signup: POST /auth/signup"
echo "  - Login: POST /auth/login"
echo "  - Profile: GET/PUT /profile"
echo "  - History: GET /interview/history"
echo ""
