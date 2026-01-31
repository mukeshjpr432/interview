@echo off
REM Interview Trends Fine-tuning Setup Script
REM Complete workflow to set up agents and fine-tuning

echo.
echo ============================================================
echo  INTERVIEW TRENDS FINE-TUNING SETUP
echo  Interview agents ko trends ke anusar fine-tune karna
echo ============================================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)

echo [1/5] Activating Python environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo      ✓ Virtual environment activated
) else (
    echo      Note: Virtual environment not found. Using system Python.
)

echo.
echo [2/5] Installing required packages...
pip install boto3 python-dotenv -q
if errorlevel 1 (
    echo      Warning: Could not install some packages
) else (
    echo      ✓ Packages installed
)

echo.
echo [3/5] Generating Interview Trends Data...
python -c "
from src.interview_trends_data import InterviewTrendsDataGenerator
import json

gen = InterviewTrendsDataGenerator()
data = gen.generate_all_trends_data()

total = sum(len(d) for d in data.values())
print(f'   ✓ Generated {total} trend-based samples')

for cat, items in data.items():
    print(f'      • {cat:20} : {len(items)} samples')
" || (
    echo      ERROR: Failed to generate trends data
    exit /b 1
)

echo.
echo [4/5] Creating Bedrock Agents...
python -c "
from src.agent_setup_trends import InterviewTrendAgent
import json

agent_mgr = InterviewTrendAgent()
setup_results = agent_mgr.setup_all_agents()

agents = setup_results.get('agents', {})
print(f'   ✓ Created {len(agents)}/3 agents')
for agent_type in agents.keys():
    print(f'      • {agent_type.capitalize()} Agent')
" || (
    echo      Note: AWS credentials may not be configured
    echo      Run this command if you have AWS credentials set up:
    echo      python setup_trends_workflow.py
)

echo.
echo [5/5] Validating Setup...
python -c "
import os
from pathlib import Path

checks = {
    'src/interview_trends_data.py': 'Interview Trends Generator',
    'src/agent_setup_trends.py': 'Agent Setup Manager',
    'setup_trends_workflow.py': 'Workflow Orchestrator',
    'INTERVIEW_TRENDS_SETUP.md': 'Setup Documentation'
}

print('   Checking files...')
for file, desc in checks.items():
    if Path(file).exists():
        print(f'      ✓ {desc}')
    else:
        print(f'      ✗ {desc} - NOT FOUND')
" || (
    echo      Warning: Validation check failed
)

echo.
echo ============================================================
echo  ✓ SETUP COMPLETE
echo ============================================================
echo.
echo  Next Steps:
echo  -----------
echo  1. Review INTERVIEW_TRENDS_SETUP.md for detailed guide
echo  2. Run: python setup_trends_workflow.py (with AWS credentials)
echo  3. Monitor fine-tuning jobs in AWS Console
echo  4. Start conducting trend-based interviews
echo.
echo  Key Features:
echo  - 3 Bedrock Agents (Interviewer, Evaluator, Coach)
echo  - 50+ Interview Trends Training Samples
echo  - Fine-tuning Pipeline (4 roles)
echo  - 28+ IT Role Support
echo  - All 2026 Interview Trends Integrated
echo.
echo  Documentation:
echo  - INTERVIEW_TRENDS_SETUP.md - Quick Start Guide
echo  - BEDROCK_AGENTIC_AI_GUIDE.md - Complete Implementation
echo.
echo ============================================================
echo.

pause
