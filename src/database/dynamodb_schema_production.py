"""
Enhanced DynamoDB Schema for Bedrock Agentic AI Interview System
Includes IT categories and fine-tuning tracking
"""

import boto3
from typing import Dict, Any
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def create_enhanced_tables():
    """Create or update DynamoDB tables for agentic AI system"""
    
    # 1. Interview Sessions with IT Categories
    interview_sessions_table = dynamodb.create_table(
        TableName='interview_sessions_v2',
        KeySchema=[
            {'AttributeName': 'interview_id', 'KeyType': 'HASH'},
            {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'interview_id', 'AttributeType': 'S'},
            {'AttributeName': 'start_time', 'AttributeType': 'S'},
            {'AttributeName': 'candidate_id', 'AttributeType': 'S'},
            {'AttributeName': 'job_category', 'AttributeType': 'S'},
            {'AttributeName': 'job_role', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'candidate_id_index',
                'KeySchema': [
                    {'AttributeName': 'candidate_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            },
            {
                'IndexName': 'job_category_index',
                'KeySchema': [
                    {'AttributeName': 'job_category', 'KeyType': 'HASH'},
                    {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            },
            {
                'IndexName': 'job_role_index',
                'KeySchema': [
                    {'AttributeName': 'job_role', 'KeyType': 'HASH'},
                    {'AttributeName': 'start_time', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'AIInterviewCoachAgentic'},
            {'Key': 'Version', 'Value': 'v2-agentic'}
        ]
    )
    
    # 2. Agent Sessions for tracking Bedrock Agent interactions
    agent_sessions_table = dynamodb.create_table(
        TableName='agent_sessions',
        KeySchema=[
            {'AttributeName': 'session_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'session_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            {'AttributeName': 'interview_id', 'AttributeType': 'S'},
            {'AttributeName': 'agent_type', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'interview_id_index',
                'KeySchema': [
                    {'AttributeName': 'interview_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            },
            {
                'IndexName': 'agent_type_index',
                'KeySchema': [
                    {'AttributeName': 'agent_type', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'BedrockAgents'},
            {'Key': 'Purpose', 'Value': 'AgentTracking'}
        ]
    )
    
    # 3. Agent Invocations with trace data
    agent_invocations_table = dynamodb.create_table(
        TableName='agent_invocations',
        KeySchema=[
            {'AttributeName': 'invocation_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'invocation_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            {'AttributeName': 'session_id', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'session_id_index',
                'KeySchema': [
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'AgentExecutionTrace'},
            {'Key': 'Purpose', 'Value': 'Debugging'}
        ]
    )
    
    # 4. Fine-tuning jobs tracking
    fine_tuning_jobs_table = dynamodb.create_table(
        TableName='fine_tuning_jobs',
        KeySchema=[
            {'AttributeName': 'job_id', 'KeyType': 'HASH'},
            {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'job_id', 'AttributeType': 'S'},
            {'AttributeName': 'created_at', 'AttributeType': 'S'},
            {'AttributeName': 'category', 'AttributeType': 'S'},
            {'AttributeName': 'status', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'category_index',
                'KeySchema': [
                    {'AttributeName': 'category', 'KeyType': 'HASH'},
                    {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            },
            {
                'IndexName': 'status_index',
                'KeySchema': [
                    {'AttributeName': 'status', 'KeyType': 'HASH'},
                    {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'FineTuningTracking'},
            {'Key': 'Purpose', 'Value': 'ModelCustomization'}
        ]
    )
    
    # 5. IT Categories and Role Mappings
    it_categories_table = dynamodb.create_table(
        TableName='it_categories',
        KeySchema=[
            {'AttributeName': 'category_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'category_id', 'AttributeType': 'S'},
            {'AttributeName': 'category_name', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'category_name_index',
                'KeySchema': [
                    {'AttributeName': 'category_name', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'InterviewCategories'},
            {'Key': 'Purpose', 'Value': 'RoleMapping'}
        ]
    )
    
    # 6. Agent Performance Metrics
    agent_metrics_table = dynamodb.create_table(
        TableName='agent_performance_metrics',
        KeySchema=[
            {'AttributeName': 'metric_id', 'KeyType': 'HASH'},
            {'AttributeName': 'recorded_at', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'metric_id', 'AttributeType': 'S'},
            {'AttributeName': 'recorded_at', 'AttributeType': 'S'},
            {'AttributeName': 'agent_id', 'AttributeType': 'S'},
            {'AttributeName': 'category', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'agent_id_index',
                'KeySchema': [
                    {'AttributeName': 'agent_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'recorded_at', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            },
            {
                'IndexName': 'category_index',
                'KeySchema': [
                    {'AttributeName': 'category', 'KeyType': 'HASH'},
                    {'AttributeName': 'recorded_at', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Application', 'Value': 'AgentMetrics'},
            {'Key': 'Purpose', 'Value': 'PerformanceMonitoring'}
        ]
    )
    
    return {
        'interview_sessions': interview_sessions_table,
        'agent_sessions': agent_sessions_table,
        'agent_invocations': agent_invocations_table,
        'fine_tuning_jobs': fine_tuning_jobs_table,
        'it_categories': it_categories_table,
        'agent_performance_metrics': agent_metrics_table
    }


def seed_it_categories():
    """Seed IT categories into DynamoDB"""
    
    categories_data = {
        'backend_dev': {
            'category_id': 'backend_dev',
            'category_name': 'Backend Development',
            'roles': ['python_backend', 'java_backend', 'nodejs_backend', 'golang_backend'],
            'description': 'Backend and API development',
            'agent_ids': []
        },
        'frontend_dev': {
            'category_id': 'frontend_dev',
            'category_name': 'Frontend Development',
            'roles': ['react_frontend', 'angular_frontend', 'vue_frontend'],
            'description': 'Frontend and UI development',
            'agent_ids': []
        },
        'devops': {
            'category_id': 'devops',
            'category_name': 'DevOps & Infrastructure',
            'roles': ['devops_engineer', 'cloud_architect', 'sre_engineer'],
            'description': 'Infrastructure and deployment',
            'agent_ids': []
        },
        'data': {
            'category_id': 'data',
            'category_name': 'Data & Analytics',
            'roles': ['data_scientist', 'data_engineer', 'ml_engineer'],
            'description': 'Data science and engineering',
            'agent_ids': []
        },
        'qa': {
            'category_id': 'qa',
            'category_name': 'Quality Assurance',
            'roles': ['qa_automation', 'qa_manual', 'performance_tester'],
            'description': 'Testing and quality assurance',
            'agent_ids': []
        }
    }
    
    table = dynamodb.Table('it_categories')
    
    for category_id, category_data in categories_data.items():
        table.put_item(Item=category_data)
        print(f"Seeded category: {category_id}")
    
    return categories_data


if __name__ == '__main__':
    # Create tables
    print("Creating enhanced DynamoDB tables...")
    tables = create_enhanced_tables()
    print("Tables created successfully!")
    
    # Seed categories
    print("\nSeeding IT categories...")
    seed_it_categories()
    print("Categories seeded!")
