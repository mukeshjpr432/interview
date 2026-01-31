#!/bin/bash
# Quick Start Script for AI Interview Coach
# Run this script to set up local development environment

set -e

echo "🚀 AI Interview Coach - Quick Start Setup"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "${YELLOW}[1/6]${NC} Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Install Python dependencies
echo "${YELLOW}[2/6]${NC} Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Create .env file
echo "${YELLOW}[3/6]${NC} Creating .env file..."
if [ ! -f .env ]; then
    cat > .env << EOF
AWS_REGION=us-east-1
BEDROCK_INTERVIEWER_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_EVALUATOR_MODEL=anthropic.claude-3-opus-20240229-v1:0
BEDROCK_COACH_MODEL=anthropic.claude-3-opus-20240229-v1:0
STAGE=dev
EOF
    echo "${GREEN}✓ .env file created${NC}"
else
    echo "${YELLOW}⚠ .env file already exists (skipping)${NC}"
fi
echo ""

# Check AWS CLI
echo "${YELLOW}[4/6]${NC} Checking AWS CLI..."
if ! command -v aws &> /dev/null; then
    echo "${RED}❌ AWS CLI not found. Please install it:${NC}"
    echo "   https://aws.amazon.com/cli/"
    echo ""
    echo "Then run: aws configure"
    exit 1
fi
echo "${GREEN}✓ AWS CLI found${NC}"
echo ""

# Install Serverless Framework
echo "${YELLOW}[5/6]${NC} Installing Serverless Framework..."
npm install -g serverless > /dev/null 2>&1
echo "${GREEN}✓ Serverless Framework installed${NC}"
echo ""

# Summary
echo "${YELLOW}[6/6]${NC} Setup complete!"
echo ""
echo "${GREEN}✅ All done!${NC}"
echo ""
echo "=================================="
echo "📚 Next Steps:"
echo "=================================="
echo ""
echo "1️⃣  Configure AWS credentials:"
echo "    aws configure"
echo ""
echo "2️⃣  Review the project:"
echo "    - Read: README.md"
echo "    - Check: src/agents/ (AI prompts)"
echo "    - Review: src/lambda/orchestrator.py"
echo ""
echo "3️⃣  Create DynamoDB tables locally:"
echo "    docker run -p 8000:8000 amazon/dynamodb-local"
echo "    (in another terminal)"
echo "    python src/database/dynamodb_schema.py"
echo ""
echo "4️⃣  Start local development:"
echo "    serverless offline start"
echo ""
echo "5️⃣  Test endpoints:"
echo "    curl -X POST http://localhost:3000/dev/interview/start \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{\"job_role\": \"Software Engineer\", \"experience_level\": \"3+ years\"}'"
echo ""
echo "6️⃣  Deploy to AWS:"
echo "    serverless deploy --stage prod"
echo ""
echo "=================================="
echo "📖 Documentation:"
echo "=================================="
echo ""
echo "- README.md                  → Project overview"
echo "- PROJECT_SUMMARY.md         → What's included"
echo "- docs/API_SPECIFICATION.md  → All API endpoints"
echo "- docs/DEPLOYMENT_GUIDE.md   → AWS deployment steps"
echo ""
echo "=================================="
echo "💬 Feedback?"
echo "=================================="
echo ""
echo "Check: src/agents/*.md (AI system prompts)"
echo "Code: src/lambda/orchestrator.py (main logic)"
echo ""
echo "Happy coding! 🎉"
echo ""
