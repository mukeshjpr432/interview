@echo off
REM Quick Start Script for AI Interview Coach (Windows)
REM Run this script to set up local development environment

echo.
echo ========================================
echo 🚀 AI Interview Coach - Quick Start Setup
echo ========================================
echo.

REM Check Python version
echo [1/6] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
python --version
echo ✓ Python found
echo.

REM Install Python dependencies
echo [2/6] Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependencies installed
echo.

REM Create .env file
echo [3/6] Creating .env file...
if not exist .env (
    (
        echo AWS_REGION=us-east-1
        echo BEDROCK_INTERVIEWER_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
        echo BEDROCK_EVALUATOR_MODEL=anthropic.claude-3-opus-20240229-v1:0
        echo BEDROCK_COACH_MODEL=anthropic.claude-3-opus-20240229-v1:0
        echo STAGE=dev
    ) > .env
    echo ✓ .env file created
) else (
    echo ⚠ .env file already exists (skipping)
)
echo.

REM Check AWS CLI
echo [4/6] Checking AWS CLI...
aws --version >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS CLI not found. Please install it:
    echo    https://aws.amazon.com/cli/
    echo.
    echo Then run: aws configure
    pause
    exit /b 1
)
echo ✓ AWS CLI found
echo.

REM Install Serverless Framework
echo [5/6] Installing Serverless Framework...
npm install -g serverless >nul 2>&1
echo ✓ Serverless Framework installed
echo.

REM Summary
echo [6/6] Setup complete!
echo.
echo ========================================
echo ✅ All done!
echo ========================================
echo.
echo 📚 Next Steps:
echo.
echo 1️⃣  Configure AWS credentials:
echo    aws configure
echo.
echo 2️⃣  Review the project:
echo    - Read: README.md
echo    - Check: src\agents\ (AI prompts)
echo    - Review: src\lambda\orchestrator.py
echo.
echo 3️⃣  Create DynamoDB tables locally:
echo    docker run -p 8000:8000 amazon/dynamodb-local
echo    (in another terminal)
echo    python src\database\dynamodb_schema.py
echo.
echo 4️⃣  Start local development:
echo    serverless offline start
echo.
echo 5️⃣  Test endpoints:
echo    curl -X POST http://localhost:3000/dev/interview/start ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"job_role\": \"Software Engineer\", \"experience_level\": \"3+ years\"}"
echo.
echo 6️⃣  Deploy to AWS:
echo    serverless deploy --stage prod
echo.
echo ========================================
echo 📖 Documentation:
echo ========================================
echo.
echo - README.md                  ^> Project overview
echo - PROJECT_SUMMARY.md         ^> What's included
echo - docs\API_SPECIFICATION.md  ^> All API endpoints
echo - docs\DEPLOYMENT_GUIDE.md   ^> AWS deployment steps
echo.
echo ========================================
echo 💬 Feedback?
echo ========================================
echo.
echo Check: src\agents\*.md (AI system prompts)
echo Code: src\lambda\orchestrator.py (main logic)
echo.
echo Happy coding! 🎉
echo.
pause
