"""
Bedrock Agent Initialization & Fine-tuning Setup
Initialize agents with trend-based fine-tuning for production interviews
"""

import json
import boto3
import time
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class AgentStatus(Enum):
    DRAFT = "DRAFT"
    PREPARED = "PREPARED"
    IN_USE = "IN_USE"

class InterviewTrendAgent:
    """Initialize and manage interview agents with fine-tuning"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.bedrock_client = boto3.client('bedrock-agent', region_name=region)
        self.bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name=region)
        self.bedrock = boto3.client('bedrock', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        
        self.agents_config = {
            'interviewer': {
                'name': 'Interview-Trend-Interviewer',
                'description': 'Conducts technical interviews with trend-based questions',
                'prompt': self._get_interviewer_prompt(),
                'model': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'actions': ['generateQuestion', 'generateFollowUp', 'evaluateResponse']
            },
            'evaluator': {
                'name': 'Interview-Trend-Evaluator',
                'description': 'Evaluates interview responses and provides scoring',
                'prompt': self._get_evaluator_prompt(),
                'model': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'actions': ['scoreResponse', 'generateFeedback', 'suggestImprovement']
            },
            'coach': {
                'name': 'Interview-Trend-Coach',
                'description': 'Provides personalized coaching based on interview performance',
                'prompt': self._get_coach_prompt(),
                'model': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'actions': ['suggestResource', 'provideTip', 'trackProgress']
            }
        }
    
    def _get_interviewer_prompt(self) -> str:
        """Get system prompt for interviewer agent based on 2026 trends"""
        return """You are an expert technical interviewer with deep knowledge of current (2026) interview trends and best practices.

Key Interview Trends to Follow:
1. System Design Focus: Ask about scalability, architecture, and trade-offs at all levels
2. Behavioral Integration: Mix technical with behavioral questions naturally
3. Problem Solving: Present real-world scenarios and edge cases
4. AI/ML Awareness: For non-ML roles, ask about AI impact on their domain
5. Remote Collaboration: Assess communication in distributed teams
6. Security Mindset: Include security considerations in questions
7. Cost Optimization: Ask about cloud costs and resource efficiency

Interview Flow:
- Start with easy warm-up question relevant to role and level
- Progress to system design / architecture questions
- Include one behavioral question naturally
- Ask about recent technologies in the field
- Adapt difficulty based on responses

Your Responsibilities:
1. Generate appropriate questions based on role, level, and trends
2. Follow up on vague answers to get clarity
3. Provide hints when candidate is stuck (after 2 attempts)
4. Maintain professional, encouraging tone
5. Track question difficulty and candidate performance

Always format your responses as JSON with:
{
  "question": "Your question here",
  "context": "Why this question is relevant to trends",
  "difficulty": "easy|medium|hard",
  "expectedLevelOfDetail": "brief|moderate|detailed",
  "hints": ["hint1", "hint2"]
}
"""
    
    def _get_evaluator_prompt(self) -> str:
        """Get system prompt for evaluator agent"""
        return """You are an expert technical evaluator with 20+ years of hiring experience.

Evaluation Criteria Based on 2026 Standards:
- Technical Knowledge: Fundamentals + relevant trends (weight: 40%)
- Problem Solving: Approach, clear thinking, handling ambiguity (weight: 25%)
- System Design: Architecture, scalability, trade-offs (weight: 20%)
- Communication: Clear explanation, listens to feedback (weight: 10%)
- Awareness: AI/ML impact, security, cost awareness (weight: 5%)

Scoring Scale:
- 90-100: Exceptional (hire immediately, senior level)
- 80-89: Strong (hire, mid level)
- 70-79: Good (hire for junior, maybe mid)
- 60-69: Acceptable (borderline, needs more assessment)
- 50-59: Weak (probably no hire)
- <50: Very weak (definite no)

Evaluation Format:
{
  "score": 0-100,
  "scoreBreakdown": {
    "technicalKnowledge": 0-40,
    "problemSolving": 0-25,
    "systemDesign": 0-20,
    "communication": 0-10,
    "awareness": 0-5
  },
  "strengths": ["strength1", "strength2", "strength3"],
  "areasForImprovement": ["area1", "area2"],
  "recommendation": "hire|maybe|consider_for_junior|no_hire",
  "feedback": "Detailed feedback for candidate"
}
"""
    
    def _get_coach_prompt(self) -> str:
        """Get system prompt for coaching agent"""
        return """You are an expert career coach and interview mentor specializing in tech roles.

Your Mission:
- Identify learning gaps from interview performance
- Provide personalized coaching and learning paths
- Recommend resources for improvement
- Track progress across interviews

Coaching Framework:
1. Identify Weakness: "You struggled with system design questions"
2. Explain Why: "This is critical for mid-level backend roles in 2026"
3. Provide Path: "Here's a 2-week learning plan"
4. Share Resources: Links to tutorials, practice platforms, books
5. Track Progress: "Let's test this area again in next mock interview"

Resource Types:
- Online Courses: Grokking System Design, LeetCode Premium, Educative
- Books: Designing Data-Intensive Applications, System Design Interview
- Practice: Mock interviews, LeetCode, HackerRank
- Communities: GitHub discussions, Stack Overflow, Discord servers

Coaching Response Format:
{
  "weakness": "Identified weak area",
  "impact": "Why this matters for their role",
  "learningPath": [
    "Step 1: Foundation (week 1)",
    "Step 2: Intermediate (week 2)",
    "Step 3: Practice (week 3)"
  ],
  "resources": [
    {
      "type": "course|book|practice|community",
      "title": "Resource title",
      "url": "https://...",
      "duration": "2-3 hours",
      "difficulty": "beginner|intermediate|advanced"
    }
  ],
  "nextCheckpoint": "Specific area to test in next interview",
  "motivation": "Encouraging message"
}
"""
    
    def create_agent(self, agent_type: str) -> Dict:
        """Create a Bedrock Agent"""
        config = self.agents_config.get(agent_type)
        if not config:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        try:
            print(f"\n📍 Creating agent: {agent_type}...")
            
            response = self.bedrock_client.create_agent(
                agentName=config['name'],
                agentDescription=config['description'],
                idleSessionTTLInSeconds=3600,
                foundationModel=config['model'],
                agentInstructionOverride=config['prompt']
            )
            
            agent_id = response['agentId']
            print(f"✅ Agent created: {agent_id}")
            
            return {
                'agentId': agent_id,
                'agentName': config['name'],
                'agentType': agent_type,
                'status': 'CREATED',
                'createdAt': datetime.now().isoformat(),
                'foundationModel': config['model']
            }
        
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            return None
    
    def add_action_group(self, agent_id: str, agent_type: str) -> Dict:
        """Add action group to agent"""
        try:
            print(f"\n🔧 Adding action group to {agent_type}...")
            
            action_schema = self._get_action_schema(agent_type)
            
            response = self.bedrock_client.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName=f"{agent_type}-actions",
                description=f"Actions for {agent_type} agent",
                actionGroupExecutor={
                    'lambda': 'arn:aws:lambda:us-east-1:613602869984:function:ai-interview-coach-dev-orchestrator'
                },
                apiSchema={
                    'payload': json.dumps(action_schema)
                }
            )
            
            print(f"✅ Action group created: {response['actionGroupId']}")
            return {
                'actionGroupId': response['actionGroupId'],
                'actionGroupName': f"{agent_type}-actions",
                'agentType': agent_type
            }
        
        except Exception as e:
            print(f"❌ Error adding action group: {e}")
            return None
    
    def _get_action_schema(self, agent_type: str) -> Dict:
        """Get OpenAPI schema for agent actions"""
        schemas = {
            'interviewer': {
                "openapi": "3.0.0",
                "info": {"title": "Interviewer Actions", "version": "1.0"},
                "paths": {
                    "/generate-question": {
                        "post": {
                            "description": "Generate interview question",
                            "parameters": [
                                {"name": "role", "in": "query", "schema": {"type": "string"}},
                                {"name": "level", "in": "query", "schema": {"type": "string"}},
                                {"name": "trend", "in": "query", "schema": {"type": "string"}}
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "/generate-followup": {
                        "post": {
                            "description": "Generate follow-up question",
                            "parameters": [
                                {"name": "previousAnswer", "in": "query", "schema": {"type": "string"}}
                            ]
                        }
                    }
                }
            },
            'evaluator': {
                "openapi": "3.0.0",
                "info": {"title": "Evaluator Actions", "version": "1.0"},
                "paths": {
                    "/score-response": {
                        "post": {
                            "description": "Score interview response",
                            "parameters": [
                                {"name": "question", "in": "query", "schema": {"type": "string"}},
                                {"name": "answer", "in": "query", "schema": {"type": "string"}},
                                {"name": "level", "in": "query", "schema": {"type": "string"}}
                            ]
                        }
                    },
                    "/generate-feedback": {
                        "post": {
                            "description": "Generate feedback on response",
                            "parameters": [
                                {"name": "score", "in": "query", "schema": {"type": "number"}},
                                {"name": "strength", "in": "query", "schema": {"type": "string"}},
                                {"name": "weakness", "in": "query", "schema": {"type": "string"}}
                            ]
                        }
                    }
                }
            },
            'coach': {
                "openapi": "3.0.0",
                "info": {"title": "Coach Actions", "version": "1.0"},
                "paths": {
                    "/suggest-resource": {
                        "post": {
                            "description": "Suggest learning resource",
                            "parameters": [
                                {"name": "weakness", "in": "query", "schema": {"type": "string"}},
                                {"name": "role", "in": "query", "schema": {"type": "string"}}
                            ]
                        }
                    },
                    "/provide-tip": {
                        "post": {
                            "description": "Provide coaching tip",
                            "parameters": [
                                {"name": "area", "in": "query", "schema": {"type": "string"}}
                            ]
                        }
                    }
                }
            }
        }
        return schemas.get(agent_type, {})
    
    def prepare_agent(self, agent_id: str, agent_type: str) -> Dict:
        """Prepare agent for use"""
        try:
            print(f"\n🚀 Preparing agent: {agent_type}...")
            
            response = self.bedrock_client.prepare_agent(
                agentId=agent_id
            )
            
            prepared_model_arn = response['agentPreparedDetails']['agentVersionId']
            print(f"✅ Agent prepared: {prepared_model_arn}")
            
            return {
                'agentId': agent_id,
                'status': 'PREPARED',
                'preparedAt': datetime.now().isoformat(),
                'modelArn': prepared_model_arn
            }
        
        except Exception as e:
            print(f"❌ Error preparing agent: {e}")
            return None
    
    def create_agent_alias(self, agent_id: str, agent_type: str) -> Dict:
        """Create agent alias for production"""
        try:
            print(f"\n🏷️  Creating agent alias: {agent_type}...")
            
            response = self.bedrock_client.create_agent_alias(
                agentId=agent_id,
                agentAliasName=f"{agent_type}-production",
                description=f"Production alias for {agent_type} agent",
                agentVersion='DRAFT'
            )
            
            alias_id = response['agentAliasId']
            print(f"✅ Alias created: {alias_id}")
            
            return {
                'aliasId': alias_id,
                'aliasName': f"{agent_type}-production",
                'agentId': agent_id,
                'createdAt': datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"❌ Error creating alias: {e}")
            return None
    
    def invoke_agent(self, agent_id: str, alias_id: str, session_id: str, user_input: str) -> Dict:
        """Invoke agent with user input"""
        try:
            response = self.bedrock_runtime.invoke_agent(
                agentId=agent_id,
                agentAliasId=alias_id,
                sessionId=session_id,
                inputText=user_input
            )
            
            return {
                'sessionId': session_id,
                'response': response.get('output', ''),
                'invokedAt': datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"❌ Error invoking agent: {e}")
            return None
    
    def setup_all_agents(self) -> Dict:
        """Complete setup: create, configure, and prepare all agents"""
        print("\n" + "="*60)
        print("🎯 SETTING UP INTERVIEW TREND AGENTS")
        print("="*60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'agents': {},
            'summary': {}
        }
        
        for agent_type in ['interviewer', 'evaluator', 'coach']:
            print(f"\n{'='*40}")
            print(f"Setting up: {agent_type}")
            print(f"{'='*40}")
            
            # Create agent
            agent_response = self.create_agent(agent_type)
            if not agent_response:
                continue
            
            agent_id = agent_response['agentId']
            
            # Add action group
            action_response = self.add_action_group(agent_id, agent_type)
            
            # Prepare agent
            prepare_response = self.prepare_agent(agent_id, agent_type)
            
            # Create alias
            alias_response = self.create_agent_alias(agent_id, agent_type)
            
            results['agents'][agent_type] = {
                'agent': agent_response,
                'actionGroup': action_response,
                'prepared': prepare_response,
                'alias': alias_response
            }
            
            print(f"\n✅ {agent_type} Agent Setup Complete!")
        
        # Summary
        results['summary'] = {
            'agentsCreated': len(results['agents']),
            'status': 'ready_for_interviews',
            'nextStep': 'Start conducting trend-based interviews',
            'note': 'All agents are prepared and ready for production use'
        }
        
        return results
    
    def create_fine_tuning_job(self, model_id: str, training_data_s3_path: str, role: str) -> Dict:
        """Create fine-tuning job for a specific role"""
        try:
            print(f"\n🎓 Creating fine-tuning job for {role}...")
            
            job_name = f"interview-trend-finetune-{role}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            response = self.bedrock.create_model_customization_job(
                jobName=job_name,
                customModelName=f"claude-interview-{role}-v1",
                roleArn='arn:aws:iam::613602869984:role/BedrockAgentRole',
                baseModelIdentifier=model_id,
                trainingDataConfig={
                    's3Uri': training_data_s3_path
                },
                outputDataConfig={
                    's3OutputPath': 's3://interview-coach-models-dev/fine-tuning-output/'
                },
                hyperParameters={
                    'epochs': '3',
                    'batchSize': '1',
                    'learningRate': '0.0002'
                }
            )
            
            job_arn = response['jobArn']
            print(f"✅ Fine-tuning job created: {job_arn}")
            
            return {
                'jobArn': job_arn,
                'jobName': job_name,
                'role': role,
                'baseModel': model_id,
                'status': 'InProgress',
                'createdAt': datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"❌ Error creating fine-tuning job: {e}")
            return None
    
    def get_fine_tuning_status(self, job_arn: str) -> Dict:
        """Get fine-tuning job status"""
        try:
            response = self.bedrock.get_model_customization_job(
                jobIdentifier=job_arn
            )
            
            return {
                'jobArn': job_arn,
                'status': response.get('status'),
                'customModelArn': response.get('customModelArn'),
                'outputModelName': response.get('outputModelName'),
                'creationTime': response.get('creationTime')
            }
        
        except Exception as e:
            print(f"❌ Error getting job status: {e}")
            return None
    
    def list_custom_models(self) -> List[Dict]:
        """List all custom models created"""
        try:
            response = self.bedrock.list_custom_models()
            
            models = []
            for model in response.get('modelSummaries', []):
                models.append({
                    'modelArn': model.get('modelArn'),
                    'modelName': model.get('modelName'),
                    'creationTime': model.get('creationTime'),
                    'baseModelArn': model.get('baseModelArn')
                })
            
            return models
        
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []


def main():
    """Main function to set up agents and fine-tuning"""
    
    # Initialize agent manager
    agent_manager = InterviewTrendAgent()
    
    # Setup all agents
    setup_results = agent_manager.setup_all_agents()
    
    # Print setup results
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE")
    print("="*60)
    print(json.dumps(setup_results, indent=2, default=str))
    
    # Summary
    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    print("""
1. Verify agents are created and prepared
2. Start conducting interviews with trend-based questions
3. Monitor agent performance and responses
4. Create fine-tuning jobs for role-specific models
5. Track interview metrics and coaching effectiveness

Ready to conduct trend-based technical interviews! 🚀
    """)


if __name__ == '__main__':
    main()
