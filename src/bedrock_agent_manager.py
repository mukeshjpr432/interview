"""
AWS Bedrock Agentic AI Module
Manages Bedrock Agents, Action Groups, and Fine-tuning
"""

import boto3
import json
from typing import Dict, List, Any, Optional
from enum import Enum

bedrock_agent_client = boto3.client('bedrock-agent', region_name='us-east-1')
bedrock_runtime_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
bedrock_client = boto3.client('bedrock', region_name='us-east-1')


class InterviewAgentType(Enum):
    """Types of interview agents"""
    INTERVIEWER = "interviewer"
    EVALUATOR = "evaluator"
    COACH = "coach"


class BedrockAgentManager:
    """Manages Bedrock Agents for interview coaching"""
    
    def __init__(self):
        self.region = 'us-east-1'
        self.agent_ids = {}
        self.action_group_ids = {}
        
    def create_interview_agent(
        self,
        agent_name: str,
        agent_type: InterviewAgentType,
        description: str,
        foundation_model: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    ) -> Dict[str, Any]:
        """
        Create a new Bedrock Agent for interview
        
        Args:
            agent_name: Unique name for the agent
            agent_type: Type of agent (Interviewer, Evaluator, Coach)
            description: Agent description
            foundation_model: Base model to use
            
        Returns:
            Agent configuration
        """
        try:
            agent_response = bedrock_agent_client.create_agent(
                agentName=agent_name,
                description=description,
                foundationModel=foundation_model,
                agentResourceRoleArn=self._get_agent_role_arn(),
                idleSessionTTLInSeconds=900,  # 15 minutes
                customerEncryptionKeyArn=None,
                tags={
                    'interview_system': 'true',
                    'agent_type': agent_type.value,
                    'created_date': str(__import__('datetime').datetime.utcnow())
                }
            )
            
            self.agent_ids[agent_type.value] = agent_response['agent']['agentId']
            
            return {
                'agent_id': agent_response['agent']['agentId'],
                'agent_arn': agent_response['agent']['agentArn'],
                'status': agent_response['agent']['agentStatus'],
                'type': agent_type.value
            }
            
        except Exception as e:
            print(f"Error creating agent {agent_name}: {str(e)}")
            raise
    
    def create_action_group(
        self,
        agent_id: str,
        action_group_name: str,
        description: str,
        action_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create action group for agent
        
        Args:
            agent_id: ID of the agent
            action_group_name: Name of action group
            description: Description
            action_schema: Schema for actions
            
        Returns:
            Action group details
        """
        try:
            response = bedrock_agent_client.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=action_group_name,
                description=description,
                actionGroupExecutor={
                    'lambda': self._get_lambda_executor_arn()
                },
                actionGroupState='ENABLED',
                apiSchema={
                    'payload': json.dumps(action_schema)
                }
            )
            
            self.action_group_ids[action_group_name] = response['actionGroupId']
            
            return {
                'action_group_id': response['actionGroupId'],
                'status': 'created'
            }
            
        except Exception as e:
            print(f"Error creating action group {action_group_name}: {str(e)}")
            raise
    
    def prepare_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Prepare (validate and version) agent for use
        
        Args:
            agent_id: ID of the agent to prepare
            
        Returns:
            Preparation status
        """
        try:
            response = bedrock_agent_client.prepare_agent(agentId=agent_id)
            
            return {
                'agent_id': agent_id,
                'status': response['agentStatus'],
                'prepared_at': response.get('preparedAt', None)
            }
            
        except Exception as e:
            print(f"Error preparing agent {agent_id}: {str(e)}")
            raise
    
    def invoke_agent(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        user_input: str,
        enable_trace: bool = True
    ) -> Dict[str, Any]:
        """
        Invoke Bedrock Agent with user input
        
        Args:
            agent_id: Agent ID
            agent_alias_id: Agent Alias ID
            session_id: Session ID for conversation
            user_input: User input message
            enable_trace: Enable execution trace
            
        Returns:
            Agent response
        """
        try:
            response = bedrock_runtime_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=user_input,
                enableTrace=enable_trace
            )
            
            # Parse response
            response_text = ""
            for event in response['body']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        response_text += chunk['bytes'].decode('utf-8')
            
            return {
                'response': response_text,
                'session_id': session_id,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"Error invoking agent: {str(e)}")
            raise
    
    def create_agent_alias(self, agent_id: str, alias_name: str, description: str = "") -> Dict[str, Any]:
        """
        Create an alias for agent version
        
        Args:
            agent_id: Agent ID
            alias_name: Alias name
            description: Alias description
            
        Returns:
            Alias details
        """
        try:
            response = bedrock_agent_client.create_agent_alias(
                agentId=agent_id,
                agentAliasName=alias_name,
                description=description,
                routingConfiguration=[
                    {
                        'agentVersion': 'DRAFT'
                    }
                ]
            )
            
            return {
                'alias_id': response['agentAlias']['agentAliasId'],
                'agent_id': agent_id,
                'status': 'created'
            }
            
        except Exception as e:
            print(f"Error creating agent alias: {str(e)}")
            raise
    
    def _get_agent_role_arn(self) -> str:
        """Get or create IAM role for agent"""
        # This should be pre-created in AWS
        return "arn:aws:iam::613602869984:role/BedrockAgentRole"
    
    def _get_lambda_executor_arn(self) -> str:
        """Get Lambda function ARN for action execution"""
        # Return the Lambda orchestrator ARN
        return "arn:aws:lambda:us-east-1:613602869984:function:ai-interview-coach-dev-orchestrator"
    
    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """Get agent information"""
        try:
            response = bedrock_agent_client.get_agent(agentId=agent_id)
            return response['agent']
        except Exception as e:
            print(f"Error getting agent info: {str(e)}")
            raise


class BedrockFineTuning:
    """Manages fine-tuning for Bedrock models"""
    
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock', region_name='us-east-1')
        
    def create_fine_tuning_job(
        self,
        model_id: str,
        job_name: str,
        training_data_uri: str,
        output_data_uri: str,
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a fine-tuning job for a Bedrock model
        
        Args:
            model_id: Base model ID
            job_name: Name of the fine-tuning job
            training_data_uri: S3 URI for training data
            output_data_uri: S3 URI for output
            hyperparameters: Training hyperparameters
            
        Returns:
            Fine-tuning job details
        """
        if hyperparameters is None:
            hyperparameters = {
                'epochs': 3,
                'batch_size': 8,
                'learning_rate': 5e-5,
                'weight_decay': 0.01,
                'warmup_ratio': 0.06
            }
        
        try:
            response = self.bedrock_client.create_model_customization_job(
                jobName=job_name,
                customModelName=f"{job_name}-model",
                roleArn="arn:aws:iam::613602869984:role/BedrockFineTuningRole",
                baseModelIdentifier=model_id,
                trainingDataConfig={
                    's3Uri': training_data_uri
                },
                outputDataConfig={
                    's3OutputPath': output_data_uri
                },
                hyperParameters=hyperparameters,
                tags=[
                    {
                        'key': 'interview_system',
                        'value': 'true'
                    },
                    {
                        'key': 'fine_tuned',
                        'value': 'true'
                    }
                ]
            )
            
            return {
                'job_arn': response['jobArn'],
                'job_status': response['status'],
                'output_model_arn': response.get('outputModelArn', None)
            }
            
        except Exception as e:
            print(f"Error creating fine-tuning job: {str(e)}")
            raise
    
    def get_fine_tuning_job_status(self, job_arn: str) -> Dict[str, Any]:
        """Get status of fine-tuning job"""
        try:
            response = self.bedrock_client.get_model_customization_job(jobIdentifier=job_arn)
            
            return {
                'job_arn': response['jobArn'],
                'status': response['status'],
                'creation_time': str(response['creationTime']),
                'completion_time': str(response.get('completionTime', 'N/A')),
                'output_model_arn': response.get('outputModelArn', None),
                'failure_message': response.get('failureMessage', None)
            }
            
        except Exception as e:
            print(f"Error getting fine-tuning job status: {str(e)}")
            raise
    
    def list_custom_models(self) -> List[Dict[str, Any]]:
        """List all custom fine-tuned models"""
        try:
            response = self.bedrock_client.list_custom_models()
            
            return [
                {
                    'model_arn': model['modelArn'],
                    'model_name': model['modelName'],
                    'base_model_arn': model['baseModelArn'],
                    'creation_time': str(model['creationTime'])
                }
                for model in response.get('modelSummaries', [])
            ]
            
        except Exception as e:
            print(f"Error listing custom models: {str(e)}")
            raise


class InterviewAgentActionSchema:
    """Defines action schemas for interview agents"""
    
    @staticmethod
    def get_interviewer_actions() -> Dict[str, Any]:
        """Get action schema for interviewer agent"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Interviewer Agent Actions",
                "version": "1.0.0"
            },
            "paths": {
                "/interview/question": {
                    "post": {
                        "summary": "Generate interview question",
                        "description": "Generate next interview question based on candidate responses",
                        "operationId": "generateQuestion",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "interview_id": {"type": "string"},
                                            "role": {"type": "string"},
                                            "difficulty": {"type": "string"},
                                            "previous_answer": {"type": "string"},
                                            "topic": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/interview/follow-up": {
                    "post": {
                        "summary": "Generate follow-up question",
                        "description": "Generate follow-up based on candidate response",
                        "operationId": "generateFollowUp"
                    }
                }
            }
        }
    
    @staticmethod
    def get_evaluator_actions() -> Dict[str, Any]:
        """Get action schema for evaluator agent"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Evaluator Agent Actions",
                "version": "1.0.0"
            },
            "paths": {
                "/evaluation/score": {
                    "post": {
                        "summary": "Score response",
                        "description": "Score candidate response on technical and soft skills",
                        "operationId": "scoreResponse"
                    }
                },
                "/evaluation/feedback": {
                    "post": {
                        "summary": "Generate feedback",
                        "description": "Generate detailed feedback on answer",
                        "operationId": "generateFeedback"
                    }
                }
            }
        }
    
    @staticmethod
    def get_coach_actions() -> Dict[str, Any]:
        """Get action schema for coach agent"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Coach Agent Actions",
                "version": "1.0.0"
            },
            "paths": {
                "/coaching/suggestion": {
                    "post": {
                        "summary": "Coaching suggestion",
                        "description": "Provide coaching suggestion for improvement",
                        "operationId": "provideSuggestion"
                    }
                },
                "/coaching/resources": {
                    "post": {
                        "summary": "Learning resources",
                        "description": "Suggest resources for improvement",
                        "operationId": "suggestResources"
                    }
                }
            }
        }
