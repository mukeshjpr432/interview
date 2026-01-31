#!/usr/bin/env python3
"""
AWS Cognito Setup Script for Sophia AI Interview Coach
Creates user pool, app client, and supporting infrastructure
Run this ONCE to set up authentication infrastructure
"""

import boto3
import json
from botocore.exceptions import ClientError

# AWS Clients
cognito = boto3.client('cognito-idp', region_name='us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
ssm = boto3.client('ssm', region_name='us-east-1')

def create_cognito_user_pool():
    """Create AWS Cognito User Pool for Sophia"""
    
    print("Creating Cognito User Pool...")
    
    try:
        response = cognito.create_user_pool(
            PoolName='sophia-interview-coach-users',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': True
                }
            },
            LambdaConfig={},
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Mutable': True,
                    'Required': True
                },
                {
                    'Name': 'name',
                    'AttributeDataType': 'String',
                    'Mutable': True,
                    'Required': True
                },
                {
                    'Name': 'given_name',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'family_name',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'phone_number',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'profile',
                    'AttributeDataType': 'String',
                    'Mutable': True
                },
                {
                    'Name': 'updated_at',
                    'AttributeDataType': 'Number',
                    'Mutable': True
                }
            ],
            AutoVerifiedAttributes=['email'],
            EmailConfiguration={
                'EmailSendingAccount': 'COGNITO_DEFAULT'
            },
            AccountRecoverySetting={
                'RecoveryMechanisms': [
                    {
                        'Name': 'verified_email',
                        'Priority': 1
                    }
                ]
            },
            UserPoolTags={
                'Application': 'SophiaInterviewCoach',
                'Environment': 'Production',
                'Version': '2.0'
            }
        )
        
        user_pool_id = response['UserPool']['Id']
        print(f"✅ User Pool created: {user_pool_id}")
        
        return user_pool_id
        
    except ClientError as e:
        if 'already exists' in str(e):
            # Find existing pool
            print("User pool already exists, finding it...")
            response = cognito.list_user_pools(MaxResults=10)
            for pool in response['UserPools']:
                if pool['Name'] == 'sophia-interview-coach-users':
                    return pool['Id']
        print(f"❌ Error creating user pool: {e}")
        return None


def create_user_pool_client(user_pool_id: str):
    """Create Cognito App Client"""
    
    print("Creating Cognito App Client...")
    
    try:
        response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='sophia-web-app',
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH',
                'ALLOW_USER_SRP_AUTH'
            ],
            GenerateSecret=False,  # No secret for web/SPA
            AllowedOAuthFlows=[
                'code',
                'implicit'
            ],
            AllowedOAuthScopes=[
                'phone',
                'email',
                'openid',
                'profile'
            ],
            AllowedOAuthFlowsUserPoolClient=True,
            CallbackURLs=[
                'http://localhost:3000/callback',
                'https://yourdomain.com/callback'  # Replace with actual domain
            ],
            LogoutURLs=[
                'http://localhost:3000/logout',
                'https://yourdomain.com/logout'
            ],
            PreventUserExistenceErrors='ENABLED',
            EnableTokenRevocation=True
        )
        
        client_id = response['UserPoolClient']['ClientId']
        print(f"✅ App Client created: {client_id}")
        
        return client_id
        
    except ClientError as e:
        print(f"❌ Error creating app client: {e}")
        return None


def create_domain(user_pool_id: str):
    """Create Cognito domain for hosting UI"""
    
    print("Creating Cognito domain...")
    
    try:
        domain_name = f"sophia-interview-{user_pool_id[-8:].lower()}"
        
        response = cognito.create_user_pool_domain(
            Domain=domain_name,
            UserPoolId=user_pool_id
        )
        
        print(f"✅ Domain created: {domain_name}.auth.us-east-1.amazoncognito.com")
        return domain_name
        
    except ClientError as e:
        if 'already exists' in str(e):
            print(f"✅ Domain already exists")
            return domain_name
        print(f"❌ Error creating domain: {e}")
        return None


def create_dynamodb_user_tables():
    """Create DynamoDB tables for user data"""
    
    print("Creating DynamoDB tables for user data...")
    
    tables = [
        {
            'name': 'sophia_users',
            'schema': [
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
            ],
            'attributes': [
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'created_at', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            'gsi': [
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {'AttributeName': 'email', 'KeyType': 'HASH'},
                        {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                    ]
                }
            ]
        },
        {
            'name': 'sophia_user_profiles',
            'schema': [
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            'attributes': [
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'experience_level', 'AttributeType': 'S'}
            ],
            'gsi': [
                {
                    'IndexName': 'experience-index',
                    'KeySchema': [
                        {'AttributeName': 'experience_level', 'KeyType': 'HASH'}
                    ]
                }
            ]
        },
        {
            'name': 'sophia_interview_history',
            'schema': [
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
            ],
            'attributes': [
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'start_time', 'AttributeType': 'S'},
                {'AttributeName': 'category', 'AttributeType': 'S'},
                {'AttributeName': 'score', 'AttributeType': 'N'}
            ],
            'gsi': [
                {
                    'IndexName': 'category-index',
                    'KeySchema': [
                        {'AttributeName': 'category', 'KeyType': 'HASH'},
                        {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
                    ]
                },
                {
                    'IndexName': 'score-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'score', 'KeyType': 'RANGE'}
                    ]
                }
            ]
        }
    ]
    
    for table_config in tables:
        try:
            # Check if table exists
            dynamodb_client.describe_table(TableName=table_config['name'])
            print(f"✅ Table {table_config['name']} already exists")
        except ClientError:
            # Create table
            try:
                gsi_list = []
                if table_config['gsi']:
                    for gsi in table_config['gsi']:
                        gsi_list.append({
                            'IndexName': gsi['IndexName'],
                            'KeySchema': gsi['KeySchema'],
                            'Projection': {'ProjectionType': 'ALL'}
                        })
                
                dynamodb_client.create_table(
                    TableName=table_config['name'],
                    KeySchema=table_config['schema'],
                    AttributeDefinitions=table_config['attributes'],
                    GlobalSecondaryIndexes=gsi_list if gsi_list else [],
                    BillingMode='PAY_PER_REQUEST',
                    Tags=[
                        {'Key': 'Application', 'Value': 'SophiaInterviewCoach'},
                        {'Key': 'Purpose', 'Value': 'UserData'}
                    ]
                )
                
                print(f"✅ Table {table_config['name']} created")
            except ClientError as e:
                print(f"❌ Error creating {table_config['name']}: {e}")


def create_s3_bucket():
    """Create S3 bucket for frontend and user uploads"""
    
    print("Creating S3 bucket for frontend hosting...")
    
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'sophia-interview-coach-frontend'
    
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ S3 bucket created: {bucket_name}")
        
        # Enable versioning
        s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        # Enable public access for frontend
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            })
        )
        
        return bucket_name
        
    except ClientError as e:
        if 'BucketAlreadyOwnedByYou' in str(e):
            print(f"✅ S3 bucket already exists: {bucket_name}")
            return bucket_name
        print(f"❌ Error creating S3 bucket: {e}")
        return None


def save_config(user_pool_id: str, client_id: str):
    """Save configuration to SSM Parameter Store"""
    
    print("Saving configuration to SSM Parameter Store...")
    
    try:
        config = {
            'COGNITO_USER_POOL_ID': user_pool_id,
            'COGNITO_CLIENT_ID': client_id,
            'COGNITO_REGION': 'us-east-1',
            'API_ENDPOINT': 'https://9o8w0onxj8.execute-api.us-east-1.amazonaws.com'
        }
        
        for key, value in config.items():
            ssm.put_parameter(
                Name=f'/sophia-interview-coach/{key}',
                Value=value,
                Type='String',
                Overwrite=True
            )
        
        # Also save to local file
        with open('cognito_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration saved")
        return config
        
    except ClientError as e:
        print(f"⚠️ Error saving config: {e}")
        return config


def main():
    """Main setup function"""
    
    print("\n" + "="*70)
    print("  SOPHIA AI INTERVIEW COACH - COGNITO & AUTH SETUP")
    print("="*70 + "\n")
    
    # Step 1: Create user pool
    user_pool_id = create_cognito_user_pool()
    if not user_pool_id:
        print("❌ Failed to create user pool. Exiting.")
        return
    
    # Step 2: Create app client
    client_id = create_user_pool_client(user_pool_id)
    if not client_id:
        print("❌ Failed to create app client. Exiting.")
        return
    
    # Step 3: Create domain
    domain = create_domain(user_pool_id)
    
    # Step 4: Create DynamoDB tables
    create_dynamodb_user_tables()
    
    # Step 5: Create S3 bucket
    bucket = create_s3_bucket()
    
    # Step 6: Save configuration
    config = save_config(user_pool_id, client_id)
    
    print("\n" + "="*70)
    print("  SETUP COMPLETE! ✅")
    print("="*70)
    print("\nConfiguration:")
    print(f"  User Pool ID: {user_pool_id}")
    print(f"  Client ID: {client_id}")
    print(f"  Region: us-east-1")
    if domain:
        print(f"  Auth Domain: https://{domain}.auth.us-east-1.amazoncognito.com")
    if bucket:
        print(f"  Frontend S3: s3://{bucket}")
    
    print("\nNext Steps:")
    print("  1. Update src/auth_handlers.py with actual COGNITO_USER_POOL_ID and CLIENT_ID")
    print("  2. Deploy updated Lambda functions: serverless deploy --stage prod")
    print("  3. Build React frontend and deploy to S3 & Amplify")
    print("  4. Configure API Gateway CORS for frontend domain")
    print("\n")


if __name__ == '__main__':
    main()
