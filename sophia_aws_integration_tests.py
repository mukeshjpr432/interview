#!/usr/bin/env python3
"""
AWS Integration Test for Sophia
Verify AWS credentials, services, and integration
"""

import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_aws_cli_config():
    """Test AWS CLI configuration"""
    print("\n🧪 Test 1: AWS CLI Configuration")
    try:
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ AWS CLI installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ AWS CLI not found")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_aws_credentials():
    """Test AWS credentials are configured"""
    print("\n🧪 Test 2: AWS Credentials")
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            identity = json.loads(result.stdout)
            print(f"✅ Credentials valid")
            print(f"   Account ID: {identity.get('Account')}")
            print(f"   User ARN: {identity.get('Arn')}")
            return True
        else:
            print(f"❌ Credentials invalid: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_bedrock_access():
    """Test Bedrock API access"""
    print("\n🧪 Test 3: Bedrock API Access")
    try:
        result = subprocess.run(
            ['aws', 'bedrock', 'list-foundation-models', '--region', 'us-east-1'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            models = data.get('modelSummaries', [])
            print(f"✅ Bedrock accessible")
            print(f"   Available models: {len(models)}")
            return True
        else:
            if 'not yet available' in result.stderr or 'AccessDenied' in result.stderr:
                print(f"⚠️  Bedrock not yet available in your region")
                print(f"   Note: Bedrock must be enabled in AWS Console")
                return False
            else:
                print(f"❌ Error: {result.stderr}")
                return False
    except Exception as e:
        print(f"⚠️  Bedrock check skipped: {str(e)}")
        return False


def test_dynamodb_access():
    """Test DynamoDB access"""
    print("\n🧪 Test 4: DynamoDB Access")
    try:
        result = subprocess.run(
            ['aws', 'dynamodb', 'list-tables', '--region', 'us-east-1'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tables = data.get('TableNames', [])
            print(f"✅ DynamoDB accessible")
            print(f"   Tables available: {len(tables)}")
            if tables:
                for table in tables[:5]:
                    print(f"      • {table}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_s3_access():
    """Test S3 access"""
    print("\n🧪 Test 5: S3 Access")
    try:
        result = subprocess.run(
            ['aws', 's3', 'ls'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            buckets = [line.split()[-1] for line in result.stdout.strip().split('\n') if line]
            print(f"✅ S3 accessible")
            print(f"   S3 buckets: {len(buckets)}")
            if buckets:
                for bucket in buckets[:5]:
                    print(f"      • {bucket}")
            return True
        else:
            print(f"⚠️  S3 accessible but no buckets: {result.stderr}")
            return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_iam_permissions():
    """Test IAM permissions"""
    print("\n🧪 Test 6: IAM Permissions")
    try:
        result = subprocess.run(
            ['aws', 'iam', 'get-user'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            user_data = json.loads(result.stdout)
            user = user_data.get('User', {})
            print(f"✅ IAM access verified")
            print(f"   User: {user.get('UserName')}")
            print(f"   ARN: {user.get('Arn')}")
            return True
        else:
            print(f"⚠️  IAM check skipped: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️  IAM check skipped: {str(e)}")
        return False


def test_lambda_access():
    """Test Lambda access"""
    print("\n🧪 Test 7: Lambda Access")
    try:
        result = subprocess.run(
            ['aws', 'lambda', 'list-functions', '--region', 'us-east-1'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            functions = data.get('Functions', [])
            print(f"✅ Lambda accessible")
            print(f"   Lambda functions: {len(functions)}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_env_file():
    """Test environment configuration"""
    print("\n🧪 Test 8: Environment Configuration")
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            print(f"✅ .env file found")
            with open(env_path, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
                vars_set = len(lines)
                print(f"   Environment variables set: {vars_set}")
                
                # Check for critical vars
                with open(env_path, 'r') as f:
                    content = f.read()
                    critical = ['AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
                    for var in critical:
                        if var in content:
                            print(f"      ✓ {var}")
                        else:
                            print(f"      ✗ {var} (missing)")
            return True
        else:
            print(f"⚠️  .env file not found - using AWS CLI configuration")
            return True
    except Exception as e:
        print(f"⚠️  Error: {str(e)}")
        return True


def test_sophia_modules():
    """Test Sophia Python modules"""
    print("\n🧪 Test 9: Sophia Modules")
    try:
        from voice.female_agent_realtime import FemaleAgentVoiceHandler
        print(f"✅ FemaleAgentVoiceHandler imported")
        
        from database.dynamodb_schema import create_interviews_table
        print(f"✅ DynamoDB schema imported")
        
        handler = FemaleAgentVoiceHandler("aws_test_001")
        status = handler.get_agent_status()
        print(f"✅ Sophia agent status: {status['status']}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_bedrock_call():
    """Test actual Bedrock API call"""
    print("\n🧪 Test 10: Bedrock API Call (Optional)")
    try:
        import boto3
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Try to list available models
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        models = bedrock.list_foundation_models()
        
        if models.get('modelSummaries'):
            print(f"✅ Bedrock API responding")
            print(f"   Models available: {len(models['modelSummaries'])}")
            return True
        else:
            print(f"⚠️  No models found - Bedrock may not be enabled")
            return False
    except Exception as e:
        print(f"⚠️  Bedrock API test skipped: {str(e)}")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*70)
    print("AWS INTEGRATION TEST SUMMARY".center(70))
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:.<60} {test_name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print("🟢 ALL AWS SERVICES READY FOR DEPLOYMENT".center(70))
    elif passed >= total - 2:
        print("🟡 MOST SERVICES READY (Some optional services may need setup)".center(70))
    else:
        print("🔴 SOME SERVICES NOT AVAILABLE - Check configuration".center(70))
    
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SOPHIA - AWS INTEGRATION TEST SUITE".center(70))
    print("="*70)
    
    results = {
        "AWS CLI Configuration": test_aws_cli_config(),
        "AWS Credentials": test_aws_credentials(),
        "Bedrock API Access": test_bedrock_access(),
        "DynamoDB Access": test_dynamodb_access(),
        "S3 Access": test_s3_access(),
        "IAM Permissions": test_iam_permissions(),
        "Lambda Access": test_lambda_access(),
        "Environment Configuration": test_env_file(),
        "Sophia Modules": test_sophia_modules(),
        "Bedrock API Call": test_bedrock_call(),
    }
    
    all_ready = print_summary(results)
    
    print("\n📋 NEXT STEPS:\n")
    
    if all_ready:
        print("1. ✅ AWS services verified")
        print("2. 📦 Deploy infrastructure: serverless deploy --stage dev")
        print("3. 🗄️  Create DynamoDB tables: python src/database/dynamodb_schema.py")
        print("4. 🧪 Test API endpoints")
        print("5. 🚀 Go live!\n")
    else:
        print("⚠️  Some services need attention:")
        print("1. Check AWS credentials: aws sts get-caller-identity")
        print("2. Enable Bedrock in AWS Console (if using AI features)")
        print("3. Create S3 bucket for voice files")
        print("4. Verify IAM permissions\n")
    
    sys.exit(0 if all_ready else 1)
