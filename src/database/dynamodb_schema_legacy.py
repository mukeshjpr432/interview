"""
DynamoDB Schema and Table Creation
AWS Database structure for interview platform
"""

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='us-east-1')


def create_interviews_table():
    """
    Create table for storing interview sessions
    
    Attributes:
    - interview_id (PK): UUID of the interview
    - job_role: Position being interviewed for
    - experience_level: Candidate experience
    - start_time: ISO timestamp
    - end_time: ISO timestamp
    - phase: Current phase (init, in_progress, completed, evaluated, coached)
    - questions_count: Number of questions asked
    - conversation_history: Array of dialogue turns
    - candidate_id: Optional candidate reference
    """
    
    try:
        response = dynamodb.create_table(
            TableName='interview_sessions',
            KeySchema=[
                {'AttributeName': 'interview_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'interview_id', 'AttributeType': 'S'},
                {'AttributeName': 'start_time', 'AttributeType': 'S'},
                {'AttributeName': 'job_role', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
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
                {'Key': 'Application', 'Value': 'AIInterviewCoach'},
                {'Key': 'Environment', 'Value': 'production'}
            ]
        )
        print("Created interview_sessions table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("interview_sessions table already exists")
        else:
            raise


def create_evaluations_table():
    """
    Create table for storing evaluation results
    
    Attributes:
    - interview_id (PK): UUID of the interview
    - evaluation_result: JSON scores from Evaluator Agent
    - coaching_feedback: Text feedback from Coach Agent
    - job_role: Position evaluated
    - experience_level: Candidate level
    - overall_score: Aggregate score (0-10)
    - timestamp: ISO timestamp of evaluation
    - readiness_level: Ready / Almost Ready / Needs Improvement
    """
    
    try:
        response = dynamodb.create_table(
            TableName='evaluation_results',
            KeySchema=[
                {'AttributeName': 'interview_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'interview_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                {'AttributeName': 'overall_score', 'AttributeType': 'N'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'timestamp_index',
                    'KeySchema': [
                        {'AttributeName': 'timestamp', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'BillingMode': 'PAY_PER_REQUEST'
                },
                {
                    'IndexName': 'readiness_index',
                    'KeySchema': [
                        {'AttributeName': 'readiness_level', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'BillingMode': 'PAY_PER_REQUEST'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {'Key': 'Application', 'Value': 'AIInterviewCoach'},
                {'Key': 'Environment', 'Value': 'production'}
            ]
        )
        print("Created evaluation_results table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("evaluation_results table already exists")
        else:
            raise


def create_transcripts_table():
    """
    Create table for storing full interview transcripts
    
    Attributes:
    - interview_id (PK): UUID of the interview
    - transcript: Full dialogue text
    - role: Job role
    - experience_level: Candidate level
    - timestamp: ISO timestamp
    - duration_minutes: Interview length
    """
    
    try:
        response = dynamodb.create_table(
            TableName='interview_transcripts',
            KeySchema=[
                {'AttributeName': 'interview_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'interview_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {'Key': 'Application', 'Value': 'AIInterviewCoach'},
                {'Key': 'Environment', 'Value': 'production'}
            ]
        )
        print("Created interview_transcripts table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("interview_transcripts table already exists")
        else:
            raise


def create_candidate_profiles_table():
    """
    Create table for storing candidate profiles
    
    Attributes:
    - candidate_id (PK): UUID of candidate
    - email: Candidate email
    - name: Candidate name
    - resume_url: S3 URL to resume
    - interview_history: Array of interview IDs
    - total_interviews: Count of interviews
    - avg_score: Average score across interviews
    - created_at: Account creation timestamp
    - updated_at: Last update timestamp
    """
    
    try:
        response = dynamodb.create_table(
            TableName='candidate_profiles',
            KeySchema=[
                {'AttributeName': 'candidate_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'candidate_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email_index',
                    'KeySchema': [
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'BillingMode': 'PAY_PER_REQUEST'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {'Key': 'Application', 'Value': 'AIInterviewCoach'},
                {'Key': 'Environment', 'Value': 'production'}
            ]
        )
        print("Created candidate_profiles table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("candidate_profiles table already exists")
        else:
            raise


def create_all_tables():
    """Create all DynamoDB tables"""
    create_interviews_table()
    create_evaluations_table()
    create_transcripts_table()
    create_candidate_profiles_table()
    print("\n✅ All DynamoDB tables created successfully!")


if __name__ == "__main__":
    create_all_tables()
