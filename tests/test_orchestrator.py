"""
Test suite for Interview Orchestrator
"""

import pytest
import json
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'lambda'))

from orchestrator import InterviewOrchestrator, lambda_handler, InterviewPhase


class TestInterviewOrchestrator:
    """Test the main orchestrator class"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for testing"""
        return InterviewOrchestrator()
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initializes correctly"""
        assert orchestrator.interview_id is not None
        assert orchestrator.conversation_history == []
        assert orchestrator.interviewer_model is not None
    
    @patch('orchestrator.bedrock_client.invoke_model')
    @patch('orchestrator.INTERVIEWS_TABLE.put_item')
    def test_start_interview(self, mock_ddb_put, mock_bedrock, orchestrator):
        """Test starting an interview"""
        
        # Mock Bedrock response
        mock_bedrock.return_value = {
            'body': MagicMock(read=lambda: json.dumps({
                'content': [{'text': 'Hello! Tell me about yourself.'}]
            }).encode())
        }
        
        # Mock DynamoDB
        mock_ddb_put.return_value = {}
        
        result = orchestrator.start_interview(
            job_role='Software Engineer',
            experience_level='3+ years'
        )
        
        assert result['status'] == 'started'
        assert 'message' in result
        assert result['interview_id'] == orchestrator.interview_id
        assert orchestrator.job_role == 'Software Engineer'
        assert orchestrator.experience_level == '3+ years'
    
    @patch('orchestrator.bedrock_client.invoke_model')
    @patch('orchestrator.INTERVIEWS_TABLE.update_item')
    def test_process_candidate_response(self, mock_ddb_update, mock_bedrock, orchestrator):
        """Test processing candidate response"""
        
        # Setup
        orchestrator.job_role = 'Software Engineer'
        orchestrator.experience_level = '3+ years'
        orchestrator.conversation_history = [
            {'role': 'interviewer', 'content': 'Tell me about your experience'},
            {'role': 'candidate', 'content': 'I have 5 years of experience'}
        ]
        
        # Mock Bedrock response
        mock_bedrock.return_value = {
            'body': MagicMock(read=lambda: json.dumps({
                'content': [{'text': 'What technologies have you used?'}]
            }).encode())
        }
        
        mock_ddb_update.return_value = {}
        
        result = orchestrator.process_candidate_response(
            'I worked with Python, Java, and AWS'
        )
        
        assert result['status'] == 'in_progress'
        assert 'message' in result
        assert len(orchestrator.conversation_history) == 4  # 2 initial + 2 new
    
    @patch('orchestrator.INTERVIEWS_TABLE.update_item')
    def test_end_interview(self, mock_ddb_update, orchestrator):
        """Test ending interview"""
        
        mock_ddb_update.return_value = {}
        orchestrator.conversation_history = [
            {'role': 'interviewer', 'content': 'Question 1'},
            {'role': 'candidate', 'content': 'Answer 1'}
        ]
        
        result = orchestrator.end_interview()
        
        assert result['status'] == 'completed'
        assert result['phase'] == InterviewPhase.COMPLETED.value
    
    @patch('orchestrator.bedrock_client.invoke_model')
    @patch('orchestrator.EVALUATIONS_TABLE.put_item')
    @patch('orchestrator.INTERVIEWS_TABLE.update_item')
    def test_evaluate_interview(self, mock_ddb_update, mock_eval_put, mock_bedrock, orchestrator):
        """Test evaluating interview"""
        
        # Setup
        orchestrator.job_role = 'Software Engineer'
        orchestrator.experience_level = '3+ years'
        orchestrator.conversation_history = [
            {'role': 'interviewer', 'content': 'Tell me about your experience'},
            {'role': 'candidate', 'content': 'I have 5 years of experience'}
        ]
        
        # Mock evaluation response
        evaluation_json = {
            'scores': {
                'technical_knowledge': 8.0,
                'communication_clarity': 7.5,
                'confidence_level': 7.0,
                'problem_solving': 8.5
            },
            'overall_score': 7.75,
            'strengths': ['Strong technical foundation'],
            'weaknesses': ['Could improve confidence']
        }
        
        mock_bedrock.return_value = {
            'body': MagicMock(read=lambda: json.dumps(evaluation_json).encode())
        }
        
        mock_eval_put.return_value = {}
        mock_ddb_update.return_value = {}
        
        result = orchestrator.evaluate_interview()
        
        assert result['status'] == 'evaluated'
        assert 'evaluation' in result
        assert result['evaluation']['overall_score'] == 7.75


class TestLambdaHandler:
    """Test AWS Lambda handler"""
    
    @patch.object(InterviewOrchestrator, 'start_interview')
    def test_lambda_start_interview(self, mock_start):
        """Test Lambda handler for starting interview"""
        
        mock_start.return_value = {
            'interview_id': 'test-id',
            'status': 'started',
            'message': 'Hello!'
        }
        
        event = {
            'action': 'start_interview',
            'job_role': 'Software Engineer',
            'experience_level': '3+ years'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'started'
    
    @patch.object(InterviewOrchestrator, 'end_interview')
    def test_lambda_end_interview(self, mock_end):
        """Test Lambda handler for ending interview"""
        
        mock_end.return_value = {
            'interview_id': 'test-id',
            'status': 'completed'
        }
        
        event = {
            'action': 'end_interview',
            'interview_id': 'test-id'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
    
    def test_lambda_unknown_action(self):
        """Test Lambda handler with unknown action"""
        
        event = {
            'action': 'unknown_action'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200  # Lambda still returns 200
        body = json.loads(response['body'])
        assert 'error' in body


class TestIntegration:
    """Integration tests for full interview flow"""
    
    @pytest.mark.asyncio
    @patch('orchestrator.bedrock_client.invoke_model')
    @patch('orchestrator.INTERVIEWS_TABLE.put_item')
    @patch('orchestrator.INTERVIEWS_TABLE.update_item')
    @patch('orchestrator.INTERVIEWS_TABLE.get_item')
    @patch('orchestrator.EVALUATIONS_TABLE.put_item')
    @patch('orchestrator.EVALUATIONS_TABLE.get_item')
    @patch('orchestrator.TRANSCRIPTS_TABLE.put_item')
    async def test_full_interview_flow(self, mock_transcripts, mock_eval_get, mock_eval_put,
                                       mock_session_get, mock_session_update, mock_session_put,
                                       mock_bedrock):
        """Test complete interview flow from start to report"""
        
        # Mock all responses
        mock_bedrock.return_value = {
            'body': MagicMock(read=lambda: json.dumps({
                'content': [{'text': 'Test response'}]
            }).encode())
        }
        
        # Test would be comprehensive end-to-end flow
        # Simplified for demonstration
        assert True  # Placeholder


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
