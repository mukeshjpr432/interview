# SOPHIA AI INTERVIEW COACH - AUTH SYSTEM SETUP (PowerShell)
# Run this script to set up AWS Cognito, DynamoDB, and Auth Infrastructure

param(
    [switch]$SkipValidation = $false,
    [string]$Profile = "default"
)

Write-Host "======================================================" -ForegroundColor Green
Write-Host "  SOPHIA AI - AUTHENTICATION SYSTEM SETUP" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""

# Color output
function Write-Success {
    param([string]$message)
    Write-Host "✓ $message" -ForegroundColor Green
}

function Write-Error {
    param([string]$message)
    Write-Host "❌ $message" -ForegroundColor Red
}

function Write-Info {
    param([string]$message)
    Write-Host $message -ForegroundColor Blue
}

function Write-Warning {
    param([string]$message)
    Write-Host "⚠ $message" -ForegroundColor Yellow
}

# Step 1: Check prerequisites
Write-Info "Step 1: Checking prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error "Python is required but not installed"
    exit 1
}

# Check AWS CLI
try {
    $awsVersion = aws --version 2>&1
    Write-Success "AWS CLI found: $awsVersion"
} catch {
    Write-Error "AWS CLI is required. Install from: https://aws.amazon.com/cli/"
    exit 1
}

Write-Host ""

# Step 2: Check AWS credentials
Write-Info "Step 2: Verifying AWS credentials..."

try {
    $accountId = aws sts get-caller-identity --query Account --output text --profile $Profile
    Write-Success "Connected to AWS Account: $accountId"
} catch {
    Write-Error "AWS credentials not configured"
    Write-Host "  Run: aws configure --profile $Profile"
    exit 1
}

Write-Host ""

# Step 3: Install Python dependencies
Write-Info "Step 3: Installing Python dependencies..."

python -m pip install -q boto3 botocore 2>$null

Write-Success "Dependencies installed"

Write-Host ""

# Step 4: Run setup script
Write-Info "Step 4: Creating Cognito infrastructure..."

python setup_cognito.py

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Some errors occurred during setup (see above)"
}

Write-Host ""

# Step 5: Load configuration
if (Test-Path "cognito_config.json") {
    Write-Info "Step 5: Loading configuration..."
    
    $config = Get-Content "cognito_config.json" | ConvertFrom-Json
    $userPoolId = $config.COGNITO_USER_POOL_ID
    $clientId = $config.COGNITO_CLIENT_ID
    
    Write-Success "Configuration loaded"
    Write-Host "  User Pool ID: $userPoolId"
    Write-Host "  Client ID: $clientId"
    Write-Host ""
    
    # Step 6: Create environment file
    Write-Info "Step 6: Creating environment files..."
    
    $envContent = @"
# Cognito Configuration
COGNITO_USER_POOL_ID=$userPoolId
COGNITO_CLIENT_ID=$clientId
COGNITO_REGION=us-east-1
API_ENDPOINT=https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com

# Frontend Configuration
REACT_APP_API_URL=https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com
REACT_APP_COGNITO_USER_POOL_ID=$userPoolId
REACT_APP_COGNITO_CLIENT_ID=$clientId
REACT_APP_COGNITO_REGION=us-east-1
"@
    
    $envContent | Out-File -FilePath ".env.auth" -Encoding UTF8
    Write-Success "Environment file created (.env.auth)"
    Write-Host ""
    
    # Step 7: Display next steps
    Write-Host ""
    Write-Host "======================================================" -ForegroundColor Green
    Write-Host "  SETUP COMPLETE! ✅" -ForegroundColor Green
    Write-Host "======================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Update src/auth_handlers.py with Cognito credentials" -ForegroundColor White
    Write-Host "   COGNITO_USER_POOL_ID = '$userPoolId'" -ForegroundColor Gray
    Write-Host "   COGNITO_CLIENT_ID = '$clientId'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Deploy Lambda functions:" -ForegroundColor White
    Write-Host "   `$env:COGNITO_USER_POOL_ID = '$userPoolId'" -ForegroundColor Gray
    Write-Host "   `$env:COGNITO_CLIENT_ID = '$clientId'" -ForegroundColor Gray
    Write-Host "   serverless deploy --stage prod" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Build and deploy frontend:" -ForegroundColor White
    Write-Host "   cd src\frontend" -ForegroundColor Gray
    Write-Host "   npm install" -ForegroundColor Gray
    Write-Host "   npm run build" -ForegroundColor Gray
    Write-Host "   npm run deploy" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Configure API Gateway Cognito Authorizer" -ForegroundColor White
    Write-Host ""
    Write-Host "Configuration saved to:" -ForegroundColor Cyan
    Write-Host "  - cognito_config.json" -ForegroundColor Gray
    Write-Host "  - .env.auth" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Available auth endpoints:" -ForegroundColor Cyan
    Write-Host "  - Signup: POST /auth/signup" -ForegroundColor Gray
    Write-Host "  - Login: POST /auth/login" -ForegroundColor Gray
    Write-Host "  - Profile: GET/PUT /profile" -ForegroundColor Gray
    Write-Host "  - History: GET /interview/history" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Documentation: AUTH_SYSTEM_GUIDE.md" -ForegroundColor Cyan
    Write-Host ""
    
} else {
    Write-Error "Configuration file not found. Setup may have failed."
    exit 1
}
