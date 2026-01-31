"""
AWS Lambda Orchestrator Function with Bedrock Agentic AI
Coordinates Bedrock Agents: Interviewer, Evaluator, Coach
Manages interview flow, action groups, and multi-turn conversations
"""

import json
import boto3
import uuid
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

# AWS Services
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
bedrock_agent_client = boto3.client('bedrock-agent', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

# DynamoDB Tables
INTERVIEWS_TABLE = dynamodb.Table('interview_sessions')
EVALUATIONS_TABLE = dynamodb.Table('evaluation_results')
TRANSCRIPTS_TABLE = dynamodb.Table('interview_transcripts')
CANDIDATE_PROFILES = dynamodb.Table('candidate_profiles')


class InterviewPhase(Enum):
    """Interview phases"""
    INIT = "init"  # Collect role, experience level
    IN_PROGRESS = "in_progress"  # Ongoing interview
    COMPLETED = "completed"  # Interview finished
    EVALUATED = "evaluated"  # Evaluation done
    COACHED = "coached"  # Coaching feedback sent


class InterviewOrchestrator:
    """Main orchestrator class for interview workflow"""
    
    def __init__(self):
        self.interviewer_model = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.evaluator_model = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.coach_model = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.interview_id = str(uuid.uuid4())
        self.conversation_history = []
        
    def generate_interviewer_prompt(self) -> str:
        """Load Interviewer Agent system prompt"""
        with open('src/agents/interviewer_agent_prompt.md', 'r') as f:
            return f.read()
    
    def generate_evaluator_prompt(self) -> str:
        """Load Evaluator Agent system prompt"""
        with open('src/agents/evaluator_agent_prompt.md', 'r') as f:
            return f.read()
    
    def generate_coach_prompt(self) -> str:
        """Load Coach Agent system prompt"""
        with open('src/agents/coach_agent_prompt.md', 'r') as f:
            return f.read()
    
    def call_bedrock(self, model_id: str, system_prompt: str, user_message: str) -> str:
        """
        Call AWS Bedrock with specified model and prompt
        
        Args:
            model_id: Bedrock model ID (Claude, Llama, etc.)
            system_prompt: System instructions
            user_message: User input
            
        Returns:
            Model response text
        """
        try:
            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-06-01',
                    'max_tokens': 2000,
                    'system': system_prompt,
                    'messages': [
                        {
                            'role': 'user',
                            'content': user_message
                        }
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            print(f"Bedrock API Error: {str(e)}")
            raise
    
    def start_interview(self, job_role: str, experience_level: str) -> Dict[str, Any]:
        """
        Start a new interview session
        
        Args:
            job_role: Job position (Software Engineer, Data Analyst, PM, etc.)
            experience_level: Fresher / 1-3 yrs / 3+ yrs
            
        Returns:
            Greeting message from Interviewer Agent
        """
        self.job_role = job_role
        self.experience_level = experience_level
        
        # Store interview session in DynamoDB
        interview_session = {
            'interview_id': self.interview_id,
            'job_role': job_role,
            'experience_level': experience_level,
            'start_time': datetime.utcnow().isoformat(),
            'phase': InterviewPhase.INIT.value,
            'questions_count': 0,
            'conversation_history': []
        }
        
        INTERVIEWS_TABLE.put_item(Item=interview_session)
        
        # Get greeting from Interviewer Agent
        system_prompt = self.generate_interviewer_prompt()
        greeting_message = f"Start the interview for a {job_role} position. Candidate experience: {experience_level}."
        
        interviewer_response = self.call_bedrock(
            self.interviewer_model,
            system_prompt,
            greeting_message
        )
        
        # Store in conversation history
        self.conversation_history.append({
            'role': 'interviewer',
            'content': interviewer_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'interview_id': self.interview_id,
            'status': 'started',
            'message': interviewer_response,
            'phase': InterviewPhase.INIT.value
        }
    
    def process_candidate_response(self, candidate_answer: str) -> Dict[str, Any]:
        """
        Process candidate response and generate next question
        
        Args:
            candidate_answer: Candidate's response to interview question
            
        Returns:
            Next interview question from Interviewer Agent
        """
        # Store candidate response
        self.conversation_history.append({
            'role': 'candidate',
            'content': candidate_answer,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Build conversation context
        conversation_context = "\n".join([
            f"{turn['role'].upper()}: {turn['content']}" 
            for turn in self.conversation_history[-6:]  # Last 6 turns
        ])
        
        # Get next question from Interviewer Agent
        system_prompt = self.generate_interviewer_prompt()
        next_question_prompt = f"""
        Current interview context:
        Job Role: {self.job_role}
        Experience Level: {self.experience_level}
        
        Conversation so far:
        {conversation_context}
        
        Based on the candidate's response, generate the next appropriate question.
        """
        
        interviewer_response = self.call_bedrock(
            self.interviewer_model,
            system_prompt,
            next_question_prompt
        )
        
        # Store in conversation history
        self.conversation_history.append({
            'role': 'interviewer',
            'content': interviewer_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Update interview session
        interview_session = INTERVIEWS_TABLE.get_item(Key={'interview_id': self.interview_id})
        INTERVIEWS_TABLE.update_item(
            Key={'interview_id': self.interview_id},
            UpdateExpression='SET questions_count = questions_count + 1, #phase = :phase, conversation_history = :conv',
            ExpressionAttributeNames={'#phase': 'phase'},
            ExpressionAttributeValues={
                ':phase': InterviewPhase.IN_PROGRESS.value,
                ':conv': self.conversation_history
            }
        )
        
        return {
            'interview_id': self.interview_id,
            'status': 'in_progress',
            'message': interviewer_response,
            'questions_asked': len([t for t in self.conversation_history if t['role'] == 'interviewer']),
            'phase': InterviewPhase.IN_PROGRESS.value
        }
    
    def end_interview(self) -> Dict[str, Any]:
        """End interview and move to evaluation"""
        
        # Update interview status
        INTERVIEWS_TABLE.update_item(
            Key={'interview_id': self.interview_id},
            UpdateExpression='SET #phase = :phase, end_time = :end_time',
            ExpressionAttributeNames={'#phase': 'phase'},
            ExpressionAttributeValues={
                ':phase': InterviewPhase.COMPLETED.value,
                ':end_time': datetime.utcnow().isoformat()
            }
        )
        
        # Build full transcript
        transcript = "\n".join([
            f"{turn['role'].upper()}: {turn['content']}" 
            for turn in self.conversation_history
        ])
        
        # Store transcript
        TRANSCRIPTS_TABLE.put_item(Item={
            'interview_id': self.interview_id,
            'transcript': transcript,
            'role': self.job_role,
            'experience_level': self.experience_level,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'interview_id': self.interview_id,
            'status': 'completed',
            'message': 'Interview completed. Evaluation in progress...',
            'phase': InterviewPhase.COMPLETED.value
        }
    
    def evaluate_interview(self) -> Dict[str, Any]:
        """Evaluate interview using Evaluator Agent"""
        
        # Build full transcript
        transcript = "\n".join([
            f"{turn['role'].upper()}: {turn['content']}" 
            for turn in self.conversation_history
        ])
        
        # Call Evaluator Agent
        system_prompt = self.generate_evaluator_prompt()
        evaluation_prompt = f"""
        Evaluate this interview:
        
        Job Role: {self.job_role}
        Experience Level: {self.experience_level}
        
        Interview Transcript:
        {transcript}
        
        Return ONLY JSON evaluation (no additional text).
        """
        
        evaluation_json = self.call_bedrock(
            self.evaluator_model,
            system_prompt,
            evaluation_prompt
        )
        
        # Parse evaluation
        try:
            evaluation_result = json.loads(evaluation_json)
        except:
            # If JSON parsing fails, return structured error
            evaluation_result = {
                'error': 'Evaluation JSON parsing failed',
                'raw_response': evaluation_json
            }
        
        # Store evaluation in DynamoDB
        EVALUATIONS_TABLE.put_item(Item={
            'interview_id': self.interview_id,
            'evaluation_result': evaluation_result,
            'job_role': self.job_role,
            'experience_level': self.experience_level,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Update interview phase
        INTERVIEWS_TABLE.update_item(
            Key={'interview_id': self.interview_id},
            UpdateExpression='SET #phase = :phase',
            ExpressionAttributeNames={'#phase': 'phase'},
            ExpressionAttributeValues={':phase': InterviewPhase.EVALUATED.value}
        )
        
        return {
            'interview_id': self.interview_id,
            'status': 'evaluated',
            'evaluation': evaluation_result,
            'phase': InterviewPhase.EVALUATED.value
        }
    
    def generate_coaching_feedback(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized coaching feedback using Coach Agent"""
        
        # Build feedback prompt
        system_prompt = self.generate_coach_prompt()
        
        # Build transcript
        transcript = "\n".join([
            f"{turn['role'].upper()}: {turn['content']}" 
            for turn in self.conversation_history
        ])
        
        coaching_prompt = f"""
        Candidate Interview Summary:
        Role: {self.job_role}
        Experience: {self.experience_level}
        
        Evaluation Scores:
        {json.dumps(evaluation, indent=2)}
        
        Interview Transcript:
        {transcript}
        
        Generate personalized coaching feedback and 7-14 day preparation plan.
        """
        
        coaching_feedback = self.call_bedrock(
            self.coach_model,
            system_prompt,
            coaching_prompt
        )
        
        # Store coaching feedback in DynamoDB
        EVALUATIONS_TABLE.update_item(
            Key={'interview_id': self.interview_id},
            UpdateExpression='SET coaching_feedback = :feedback, #phase = :phase',
            ExpressionAttributeNames={'#phase': 'phase'},
            ExpressionAttributeValues={
                ':feedback': coaching_feedback,
                ':phase': InterviewPhase.COACHED.value
            }
        )
        
        return {
            'interview_id': self.interview_id,
            'status': 'coached',
            'coaching_feedback': coaching_feedback,
            'phase': InterviewPhase.COACHED.value
        }
    
    def get_final_report(self) -> Dict[str, Any]:
        """Generate final interview report with all components"""
        
        evaluation = EVALUATIONS_TABLE.get_item(Key={'interview_id': self.interview_id})['Item']
        interview = INTERVIEWS_TABLE.get_item(Key={'interview_id': self.interview_id})['Item']
        
        return {
            'interview_id': self.interview_id,
            'job_role': self.job_role,
            'experience_level': self.experience_level,
            'interview_duration': interview.get('questions_count', 0),
            'evaluation_scores': evaluation.get('evaluation_result'),
            'coaching_feedback': evaluation.get('coaching_feedback'),
            'start_time': interview.get('start_time'),
            'end_time': interview.get('end_time'),
            'status': 'complete'
        }


def lambda_handler(event, context):
    """
    AWS Lambda entry point
    
    Event structure:
    {
        "action": "start_interview" | "send_response" | "end_interview" | "evaluate" | "coach" | "get_report",
        "interview_id": "uuid (optional for existing interview)",
        "job_role": "string (required for start_interview)",
        "experience_level": "string (required for start_interview)",
        "candidate_answer": "string (required for send_response)"
    }
    """
    
    try:
        action = event.get('action')
        interview_id = event.get('interview_id')
        
        # Use existing orchestrator or create new
        orchestrator = InterviewOrchestrator()
        if interview_id:
            orchestrator.interview_id = interview_id
        
        if action == 'start_interview':
            job_role = event.get('job_role')
            experience_level = event.get('experience_level')
            result = orchestrator.start_interview(job_role, experience_level)
            
        elif action == 'send_response':
            candidate_answer = event.get('candidate_answer')
            result = orchestrator.process_candidate_response(candidate_answer)
            
        elif action == 'end_interview':
            result = orchestrator.end_interview()
            
        elif action == 'evaluate':
            result = orchestrator.evaluate_interview()
            
        elif action == 'coach':
            evaluation = event.get('evaluation')
            result = orchestrator.generate_coaching_feedback(evaluation)
            
        elif action == 'get_report':
            result = orchestrator.get_final_report()
            
        else:
            result = {'error': f'Unknown action: {action}'}
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


if __name__ == "__main__":
    # For local testing
    event = {
        "action": "start_interview",
        "job_role": "Software Engineer",
        "experience_level": "3+ years"
    }
    print(lambda_handler(event, None))
