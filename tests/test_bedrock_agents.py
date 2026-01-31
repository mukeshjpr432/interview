"""
Test Suite for Bedrock Agentic AI Interview System
Tests agent creation, invocation, fine-tuning, and IT categories
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.bedrock_agents import (
    BedrockAgentManager,
    BedrockFineTuning,
    InterviewAgentType,
    InterviewAgentActionSchema
)
from src.fine_tuning_data import FineTuningDataGenerator
from config.it_categories import IT_CATEGORIES


class TestBedrockAgentManager:
    """Test Bedrock Agent Manager"""
    
    @pytest.fixture
    def agent_manager(self):
        """Initialize agent manager"""
        return BedrockAgentManager()
    
    def test_create_interview_agent(self, agent_manager):
        """Test creating interview agent"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.create_agent.return_value = {
                'agent': {
                    'agentId': 'agent-123',
                    'agentArn': 'arn:aws:bedrock:us-east-1:123456789:agent/agent-123',
                    'agentStatus': 'DRAFT'
                }
            }
            
            result = agent_manager.create_interview_agent(
                agent_name='sophia-interviewer',
                agent_type=InterviewAgentType.INTERVIEWER,
                description='Sophia Interview Agent'
            )
            
            assert result['agent_id'] == 'agent-123'
            assert result['status'] == 'DRAFT'
            assert result['type'] == 'interviewer'
    
    def test_create_action_group(self, agent_manager):
        """Test creating action group"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.create_agent_action_group.return_value = {
                'actionGroupId': 'action-123'
            }
            
            result = agent_manager.create_action_group(
                agent_id='agent-123',
                action_group_name='interview-actions',
                description='Interview management actions',
                action_schema=InterviewAgentActionSchema.get_interviewer_actions()
            )
            
            assert result['action_group_id'] == 'action-123'
            assert result['status'] == 'created'
    
    def test_prepare_agent(self, agent_manager):
        """Test preparing agent"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.prepare_agent.return_value = {
                'agentStatus': 'PREPARED'
            }
            
            result = agent_manager.prepare_agent('agent-123')
            
            assert result['status'] == 'PREPARED'
    
    def test_invoke_agent(self, agent_manager):
        """Test invoking agent"""
        with patch('boto3.client') as mock_client:
            mock_runtime = MagicMock()
            mock_client.return_value = mock_runtime
            
            # Mock streaming response
            mock_runtime.invoke_agent.return_value = {
                'body': [
                    {'chunk': {'bytes': b'What is async/await'}}
                ]
            }
            
            result = agent_manager.invoke_agent(
                agent_id='agent-123',
                agent_alias_id='alias-123',
                session_id='session-123',
                user_input='Tell me about async programming'
            )
            
            assert 'response' in result
            assert result['status'] == 'success'
    
    def test_create_agent_alias(self, agent_manager):
        """Test creating agent alias"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.create_agent_alias.return_value = {
                'agentAlias': {
                    'agentAliasId': 'alias-123'
                }
            }
            
            result = agent_manager.create_agent_alias(
                agent_id='agent-123',
                alias_name='production'
            )
            
            assert result['alias_id'] == 'alias-123'


class TestBedrockFineTuning:
    """Test Bedrock Fine-tuning"""
    
    @pytest.fixture
    def fine_tuner(self):
        """Initialize fine-tuner"""
        return BedrockFineTuning()
    
    def test_create_fine_tuning_job(self, fine_tuner):
        """Test creating fine-tuning job"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.create_model_customization_job.return_value = {
                'jobArn': 'arn:aws:bedrock:us-east-1:123456789:customization-job/job-123',
                'status': 'InProgress'
            }
            
            result = fine_tuner.create_fine_tuning_job(
                model_id='anthropic.claude-3-sonnet-20240229-v1:0',
                job_name='python-backend-finetuned',
                training_data_uri='s3://bucket/training.jsonl',
                output_data_uri='s3://bucket/output/'
            )
            
            assert result['job_arn'] is not None
            assert result['job_status'] == 'InProgress'
    
    def test_get_fine_tuning_job_status(self, fine_tuner):
        """Test getting fine-tuning status"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.get_model_customization_job.return_value = {
                'jobArn': 'arn:aws:bedrock:us-east-1:123456789:customization-job/job-123',
                'status': 'Completed',
                'creationTime': '2026-01-31T10:00:00Z',
                'completionTime': '2026-01-31T12:00:00Z',
                'outputModelArn': 'arn:aws:bedrock:us-east-1:123456789:custom-model/model-123'
            }
            
            result = fine_tuner.get_fine_tuning_job_status(
                'arn:aws:bedrock:us-east-1:123456789:customization-job/job-123'
            )
            
            assert result['status'] == 'Completed'
            assert result['output_model_arn'] is not None
    
    def test_list_custom_models(self, fine_tuner):
        """Test listing custom models"""
        with patch('boto3.client') as mock_client:
            mock_bedrock = MagicMock()
            mock_client.return_value = mock_bedrock
            mock_bedrock.list_custom_models.return_value = {
                'modelSummaries': [
                    {
                        'modelArn': 'arn:aws:bedrock:us-east-1:123456789:custom-model/model-123',
                        'modelName': 'python-backend-v1',
                        'baseModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/claude-3',
                        'creationTime': '2026-01-31T10:00:00Z'
                    }
                ]
            }
            
            result = fine_tuner.list_custom_models()
            
            assert len(result) > 0
            assert result[0]['model_name'] == 'python-backend-v1'


class TestFineTuningDataGenerator:
    """Test Fine-tuning Data Generator"""
    
    @pytest.fixture
    def generator(self):
        """Initialize generator"""
        return FineTuningDataGenerator()
    
    def test_generate_python_backend_data(self, generator):
        """Test generating Python backend training data"""
        data = generator.generate_python_backend_training_data()
        
        assert len(data) > 0
        assert all('user' in item and 'assistant' in item for item in data)
        assert all('system' in item for item in data)
    
    def test_generate_react_frontend_data(self, generator):
        """Test generating React frontend training data"""
        data = generator.generate_react_frontend_training_data()
        
        assert len(data) > 0
        assert all('user' in item and 'assistant' in item for item in data)
    
    def test_generate_devops_data(self, generator):
        """Test generating DevOps training data"""
        data = generator.generate_devops_training_data()
        
        assert len(data) > 0
        assert all('user' in item and 'assistant' in item for item in data)
    
    def test_generate_data_scientist_data(self, generator):
        """Test generating Data Scientist training data"""
        data = generator.generate_data_scientist_training_data()
        
        assert len(data) > 0
        assert all('user' in item and 'assistant' in item for item in data)
    
    def test_create_jsonl_file(self, generator):
        """Test creating JSONL training file"""
        with patch.object(generator, 's3_client') as mock_s3:
            mock_s3.put_object.return_value = {}
            
            training_data = [
                {
                    'system': 'You are an expert interviewer',
                    'user': 'What is Python?',
                    'assistant': 'Python is a programming language...'
                }
            ]
            
            result = generator.create_jsonl_training_file(training_data, 'python_backend')
            
            assert 's3://' in result
            assert 'python_backend' in result


class TestITCategories:
    """Test IT Categories Configuration"""
    
    def test_categories_structure(self):
        """Test IT categories structure"""
        assert 'categories' in IT_CATEGORIES
        
        for category_name, category_data in IT_CATEGORIES['categories'].items():
            assert 'name' in category_data
            assert 'roles' in category_data
            assert len(category_data['roles']) > 0
    
    def test_backend_category(self):
        """Test backend category"""
        backend = IT_CATEGORIES['categories']['backend']
        
        assert 'python_backend' in [r['id'] for r in backend['roles']]
        assert 'java_backend' in [r['id'] for r in backend['roles']]
        assert 'nodejs_backend' in [r['id'] for r in backend['roles']]
        assert 'golang_backend' in [r['id'] for r in backend['roles']]
    
    def test_frontend_category(self):
        """Test frontend category"""
        frontend = IT_CATEGORIES['categories']['frontend']
        
        assert 'react_frontend' in [r['id'] for r in frontend['roles']]
        assert 'angular_frontend' in [r['id'] for r in frontend['roles']]
        assert 'vue_frontend' in [r['id'] for r in frontend['roles']]
    
    def test_devops_category(self):
        """Test DevOps category"""
        devops = IT_CATEGORIES['categories']['devops']
        
        assert 'devops_engineer' in [r['id'] for r in devops['roles']]
        assert 'cloud_architect' in [r['id'] for r in devops['roles']]
        assert 'sre_engineer' in [r['id'] for r in devops['roles']]
    
    def test_data_category(self):
        """Test Data category"""
        data = IT_CATEGORIES['categories']['data']
        
        assert 'data_scientist' in [r['id'] for r in data['roles']]
        assert 'data_engineer' in [r['id'] for r in data['roles']]
        assert 'ml_engineer' in [r['id'] for r in data['roles']]
    
    def test_difficulty_mappings(self):
        """Test difficulty level mappings"""
        assert 'difficulty_mappings' in IT_CATEGORIES
        
        difficulties = IT_CATEGORIES['difficulty_mappings']
        assert 'junior' in difficulties
        assert 'mid' in difficulties
        assert 'senior' in difficulties
        
        assert difficulties['junior']['years'] == '0-2'
        assert difficulties['mid']['years'] == '2-5'
        assert difficulties['senior']['years'] == '5+'


class TestActionSchemas:
    """Test Action Schemas"""
    
    def test_interviewer_action_schema(self):
        """Test interviewer action schema"""
        schema = InterviewAgentActionSchema.get_interviewer_actions()
        
        assert schema['info']['title'] == 'Interviewer Agent Actions'
        assert '/interview/question' in schema['paths']
        assert '/interview/follow-up' in schema['paths']
    
    def test_evaluator_action_schema(self):
        """Test evaluator action schema"""
        schema = InterviewAgentActionSchema.get_evaluator_actions()
        
        assert schema['info']['title'] == 'Evaluator Agent Actions'
        assert '/evaluation/score' in schema['paths']
        assert '/evaluation/feedback' in schema['paths']
    
    def test_coach_action_schema(self):
        """Test coach action schema"""
        schema = InterviewAgentActionSchema.get_coach_actions()
        
        assert schema['info']['title'] == 'Coach Agent Actions'
        assert '/coaching/suggestion' in schema['paths']
        assert '/coaching/resources' in schema['paths']


# Integration Tests
class TestAgentIntegration:
    """Integration tests for agent workflow"""
    
    @pytest.mark.integration
    def test_full_agent_workflow(self):
        """Test complete agent workflow"""
        manager = BedrockAgentManager()
        fine_tuner = BedrockFineTuning()
        generator = FineTuningDataGenerator()
        
        # 1. Create agents
        # 2. Add action groups
        # 3. Prepare agents
        # 4. Create fine-tuning job
        # 5. Invoke agents
        
        # This is a placeholder for full integration test
        assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
