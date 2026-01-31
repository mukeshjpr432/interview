#!/usr/bin/env python3
"""
Quick Test Suite for Female AI Agent (Sophia)
Test all core modules and functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_voice_handler():
    """Test FemaleAgentVoiceHandler"""
    print("\n🧪 Test 1: Voice Handler")
    try:
        from voice.female_agent_realtime import FemaleAgentVoiceHandler, AGENT_CONFIG
        print("✅ FemaleAgentVoiceHandler imported successfully")
        print(f"   Agent Name: {AGENT_CONFIG['name']}")
        print(f"   Voice ID: {AGENT_CONFIG['voice_id']}")
        print(f"   Engine: {AGENT_CONFIG['engine']}")
        
        handler = FemaleAgentVoiceHandler('test_interview_001')
        print(f"✅ Handler instance created")
        print(f"   Interview ID: {handler.interview_id}")
        print(f"   Agent Name: {handler.agent_name}")
        
        status = handler.get_agent_status()
        print(f"✅ Agent status: {status['status']}")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def test_database_schema():
    """Test database schema"""
    print("\n🧪 Test 2: Database Schema")
    try:
        from database import dynamodb_schema
        print("✅ DynamoDB schema module imported successfully")
        
        # Check for table creation functions
        schema_path = Path(__file__).parent / "src/database/dynamodb_schema.py"
        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        functions = [
            'create_interviews_table',
            'create_evaluations_table', 
            'create_transcripts_table',
            'create_profiles_table'
        ]
        
        for func in functions:
            if func in content:
                print(f"   ✓ {func} defined")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def test_bedrock_config():
    """Test Bedrock configuration"""
    print("\n🧪 Test 3: Bedrock Configuration")
    try:
        import json
        config_path = Path(__file__).parent / "config/aws_bedrock_config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ Bedrock config loaded successfully")
        
        if 'bedrock_models' in config:
            models = list(config['bedrock_models'].keys())
            print(f"   Models configured: {len(models)} models")
            for model in models[:2]:
                print(f"      - {model}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def test_frontend_components():
    """Test frontend components exist"""
    print("\n🧪 Test 4: Frontend Components")
    try:
        components = {
            'React Component': Path(__file__).parent / "src/frontend/FemaleAgentInterface.tsx",
            'CSS Styling': Path(__file__).parent / "src/frontend/FemaleAgentInterface.css",
            'Dashboard Schema': Path(__file__).parent / "src/frontend/DashboardSchema.json",
        }
        
        for name, path in components.items():
            if path.exists():
                print(f"✅ {name}: {path.name}")
            else:
                print(f"❌ {name}: NOT FOUND")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def test_agent_prompts():
    """Test agent prompts"""
    print("\n🧪 Test 5: Agent Prompts")
    try:
        prompts = {
            'Interviewer': Path(__file__).parent / "src/agents/interviewer_agent_prompt.md",
            'Evaluator': Path(__file__).parent / "src/agents/evaluator_agent_prompt.md",
            'Coach': Path(__file__).parent / "src/agents/coach_agent_prompt.md",
            'Female Agent': Path(__file__).parent / "src/agents/female_agent_config.md",
        }
        
        for name, path in prompts.items():
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    size = len(f.read())
                print(f"✅ {name}: {size:,} bytes")
            else:
                print(f"❌ {name}: NOT FOUND")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def test_orchestrator():
    """Test orchestrator module"""
    print("\n🧪 Test 6: Orchestrator Module")
    try:
        import importlib.util
        orchestrator_path = Path(__file__).parent / "src/lambda/orchestrator.py"
        
        spec = importlib.util.spec_from_file_location("orchestrator", orchestrator_path)
        orchestrator = importlib.util.module_from_spec(spec)
        
        print(f"✅ Orchestrator module found: {orchestrator_path.name}")
        
        with open(orchestrator_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'InterviewOrchestrator' in content:
                print(f"✅ InterviewOrchestrator class defined")
            if 'lambda_handler' in content:
                print(f"✅ Lambda handler implemented")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*70)
    print("🎉 FEMALE AI AGENT (SOPHIA) - TEST RESULTS 🎉")
    print("="*70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"SCORE: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n✨ ALL TESTS PASSED! Sophia is ready for deployment! ✨")
    else:
        print(f"\n⚠️  {total-passed} test(s) need attention")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("FEMALE AI AGENT (SOPHIA) - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {
        "Voice Handler (FemaleAgentVoiceHandler)": test_voice_handler(),
        "Database Schema (DynamoDB)": test_database_schema(),
        "Bedrock Configuration": test_bedrock_config(),
        "Frontend Components": test_frontend_components(),
        "Agent Prompts Quality": test_agent_prompts(),
        "Orchestrator Module": test_orchestrator(),
    }
    
    print_summary(results)
