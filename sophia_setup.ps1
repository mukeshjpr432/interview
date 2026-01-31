#!/usr/bin/env pwsh
<#
.SYNOPSIS
Interview Trends Fine-tuning Setup Script
Complete workflow to set up Bedrock agents with trend-based fine-tuning

.DESCRIPTION
Agents ko interview trends ke anusar configure aur fine-tune karna

.EXAMPLE
.\setup_trends.ps1
#>

param(
    [switch]$SkipAWS = $false,
    [switch]$Verbose = $false
)

# Colors for output
$Colors = @{
    Success = 'Green'
    Error   = 'Red'
    Warning = 'Yellow'
    Info    = 'Cyan'
}

function Write-Status {
    param(
        [string]$Message,
        [string]$Status = "Info"
    )
    $color = $Colors[$Status] ?? 'White'
    Write-Host "   " -NoNewline
    Write-Host $Message -ForegroundColor $color
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "============================================================"
    Write-Host "  $Title"
    Write-Host "============================================================"
    Write-Host ""
}

# Main execution
try {
    Write-Section "INTERVIEW TRENDS FINE-TUNING SETUP"
    
    # Step 1: Check Python
    Write-Host "[1/5] Checking Python Installation..." -ForegroundColor Cyan
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "✓ Python found: $pythonVersion" "Success"
    } else {
        Write-Status "✗ Python not found. Please install Python 3.8+" "Error"
        exit 1
    }
    
    # Step 2: Check virtual environment
    Write-Host "[2/5] Checking Virtual Environment..." -ForegroundColor Cyan
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
        Write-Status "✓ Virtual environment activated" "Success"
    } else {
        Write-Status "⚠ Virtual environment not found. Using system Python." "Warning"
    }
    
    # Step 3: Install dependencies
    Write-Host "[3/5] Installing Dependencies..." -ForegroundColor Cyan
    pip install boto3 python-dotenv -q
    if ($LASTEXITCODE -eq 0) {
        Write-Status "✓ Dependencies installed" "Success"
    } else {
        Write-Status "⚠ Could not install some packages" "Warning"
    }
    
    # Step 4: Generate trends data
    Write-Host "[4/5] Generating Interview Trends Data..." -ForegroundColor Cyan
    $pythonCmd = @"
from src.interview_trends_data import InterviewTrendsDataGenerator
import json

try:
    gen = InterviewTrendsDataGenerator()
    data = gen.generate_all_trends_data()
    
    total = sum(len(d) for d in data.values())
    print(f'   ✓ Generated {total} trend-based samples')
    
    for cat, items in data.items():
        print(f'      • {cat:20} : {len(items)} samples')
    
    exit(0)
except Exception as e:
    print(f'   ✗ Error: {e}')
    exit(1)
"@
    
    python -c $pythonCmd
    if ($LASTEXITCODE -eq 0) {
        Write-Status "✓ Trends data generated successfully" "Success"
    } else {
        Write-Status "✗ Failed to generate trends data" "Error"
        exit 1
    }
    
    # Step 5: Validate setup
    Write-Host "[5/5] Validating Setup..." -ForegroundColor Cyan
    
    $files = @{
        'src/interview_trends_data.py' = 'Interview Trends Generator'
        'src/agent_setup_trends.py' = 'Agent Setup Manager'
        'setup_trends_workflow.py' = 'Workflow Orchestrator'
        'INTERVIEW_TRENDS_SETUP.md' = 'Setup Documentation'
    }
    
    $allFilesExist = $true
    foreach ($file in $files.GetEnumerator()) {
        if (Test-Path $file.Key) {
            Write-Status "✓ $($file.Value)" "Success"
        } else {
            Write-Status "✗ $($file.Value) - NOT FOUND" "Error"
            $allFilesExist = $false
        }
    }
    
    if (-not $allFilesExist) {
        Write-Status "Some files are missing" "Warning"
        exit 1
    }
    
    # Optional: Create agents if AWS credentials are available
    if (-not $SkipAWS) {
        Write-Host "[OPTIONAL] Creating Bedrock Agents..." -ForegroundColor Cyan
        
        $pythonCmd = @"
try:
    from src.agent_setup_trends import InterviewTrendAgent
    
    agent_mgr = InterviewTrendAgent()
    setup_results = agent_mgr.setup_all_agents()
    
    agents = setup_results.get('agents', {})
    print(f'   ✓ Created {len(agents)}/3 agents')
    
    for agent_type in agents.keys():
        print(f'      • {agent_type.capitalize()} Agent')
    
except Exception as e:
    print(f'   Note: AWS setup requires credentials: {e}')
"@
        
        python -c $pythonCmd
    }
    
    # Success message
    Write-Section "✓ SETUP COMPLETE"
    
    Write-Host "Next Steps:" -ForegroundColor Green
    Write-Host "  1. Review INTERVIEW_TRENDS_SETUP.md for detailed guide"
    Write-Host "  2. Run: python setup_trends_workflow.py (with AWS credentials)"
    Write-Host "  3. Monitor fine-tuning jobs in AWS Console"
    Write-Host "  4. Start conducting trend-based interviews"
    Write-Host ""
    
    Write-Host "Key Features:" -ForegroundColor Cyan
    Write-Host "  ✓ 3 Bedrock Agents (Interviewer, Evaluator, Coach)"
    Write-Host "  ✓ 50+ Interview Trends Training Samples"
    Write-Host "  ✓ Fine-tuning Pipeline (4 roles)"
    Write-Host "  ✓ 28+ IT Role Support"
    Write-Host "  ✓ All 2026 Interview Trends Integrated"
    Write-Host ""
    
    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  📖 INTERVIEW_TRENDS_SETUP.md - Quick Start Guide"
    Write-Host "  📖 BEDROCK_AGENTIC_AI_GUIDE.md - Complete Implementation"
    Write-Host ""
    
    Write-Section "Ready to conduct trend-based interviews! 🚀"
    
}
catch {
    Write-Status "Unexpected error: $_" "Error"
    exit 1
}
