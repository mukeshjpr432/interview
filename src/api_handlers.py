"""
Enhanced API endpoints for Bedrock Agentic AI Interview System
Includes support for IT categories and agent-based interviews
"""

from typing import Dict, Any, Optional
import json


def get_api_endpoints():
    """
    Define all API endpoints for agentic AI system
    
    Returns:
        Dictionary of API configurations
    """
    
    endpoints = {
        # Category Management
        "list_categories": {
            "path": "/categories",
            "method": "GET",
            "description": "List all IT interview categories"
        },
        
        "get_category": {
            "path": "/categories/{category_id}",
            "method": "GET",
            "description": "Get specific IT category details"
        },
        
        "list_roles": {
            "path": "/categories/{category_id}/roles",
            "method": "GET",
            "description": "List roles within a category"
        },
        
        # Agentic AI Interview Endpoints
        "start_agent_interview": {
            "path": "/agent/interview/start",
            "method": "POST",
            "description": "Start interview with Bedrock Agent",
            "body": {
                "type": "object",
                "properties": {
                    "candidate_id": {"type": "string"},
                    "category_id": {"type": "string", "example": "backend_dev"},
                    "role_id": {"type": "string", "example": "python_backend"},
                    "difficulty_level": {
                        "type": "string",
                        "enum": ["junior", "mid", "senior"]
                    },
                    "enable_trace": {"type": "boolean", "default": True}
                },
                "required": ["candidate_id", "category_id", "role_id", "difficulty_level"]
            }
        },
        
        "agent_question": {
            "path": "/agent/interview/{interview_id}/question",
            "method": "POST",
            "description": "Get next question from interviewer agent",
            "body": {
                "type": "object",
                "properties": {
                    "candidate_response": {"type": "string"},
                    "force_new_topic": {"type": "boolean"}
                },
                "required": ["candidate_response"]
            }
        },
        
        "agent_evaluation": {
            "path": "/agent/interview/{interview_id}/evaluate",
            "method": "POST",
            "description": "Get evaluation from evaluator agent",
            "body": {
                "type": "object",
                "properties": {
                    "response_text": {"type": "string"},
                    "question_context": {"type": "string"}
                },
                "required": ["response_text"]
            }
        },
        
        "agent_coaching": {
            "path": "/agent/interview/{interview_id}/coaching",
            "method": "POST",
            "description": "Get coaching feedback from coach agent",
            "body": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "evaluation_score": {"type": "number"},
                    "focus_area": {"type": "string"}
                },
                "required": ["topic", "evaluation_score"]
            }
        },
        
        "end_interview": {
            "path": "/agent/interview/{interview_id}/end",
            "method": "POST",
            "description": "End interview and get final report"
        },
        
        "interview_report": {
            "path": "/agent/interview/{interview_id}/report",
            "method": "GET",
            "description": "Get comprehensive interview report"
        },
        
        # Agent Management
        "get_agent_status": {
            "path": "/agents/status",
            "method": "GET",
            "description": "Get status of all interview agents"
        },
        
        "create_custom_agent": {
            "path": "/agents/create",
            "method": "POST",
            "description": "Create custom agent for specific role",
            "body": {
                "type": "object",
                "properties": {
                    "role_id": {"type": "string"},
                    "custom_prompts": {"type": "object"},
                    "enable_fine_tuning": {"type": "boolean"}
                },
                "required": ["role_id"]
            }
        },
        
        # Fine-tuning Management
        "create_fine_tuning_job": {
            "path": "/fine-tuning/create",
            "method": "POST",
            "description": "Create fine-tuning job for specific category",
            "body": {
                "type": "object",
                "properties": {
                    "model_id": {"type": "string"},
                    "category_id": {"type": "string"},
                    "training_data_uri": {"type": "string", "format": "uri"},
                    "hyperparameters": {"type": "object"}
                },
                "required": ["model_id", "category_id", "training_data_uri"]
            }
        },
        
        "get_fine_tuning_status": {
            "path": "/fine-tuning/{job_id}/status",
            "method": "GET",
            "description": "Get fine-tuning job status"
        },
        
        "list_custom_models": {
            "path": "/fine-tuning/models",
            "method": "GET",
            "description": "List all custom fine-tuned models"
        },
        
        # Analytics & Metrics
        "get_agent_metrics": {
            "path": "/metrics/agents",
            "method": "GET",
            "description": "Get agent performance metrics",
            "query_params": {
                "category_id": "optional",
                "time_period": "optional (24h, 7d, 30d)",
                "metric_type": "optional (accuracy, response_time, etc)"
            }
        },
        
        "get_interview_analytics": {
            "path": "/analytics/interviews",
            "method": "GET",
            "description": "Get interview analytics by category",
            "query_params": {
                "category_id": "optional",
                "role_id": "optional",
                "date_range": "optional"
            }
        },
        
        # Voice Integration
        "transcribe_audio": {
            "path": "/interview/{interview_id}/voice/transcribe",
            "method": "POST",
            "description": "Transcribe audio to text",
            "body": {
                "type": "object",
                "properties": {
                    "audio_uri": {"type": "string", "format": "uri"},
                    "language": {"type": "string", "default": "en-US"}
                },
                "required": ["audio_uri"]
            }
        },
        
        "synthesize_speech": {
            "path": "/interview/{interview_id}/voice/synthesize",
            "method": "POST",
            "description": "Synthesize text to speech",
            "body": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "voice_id": {"type": "string", "default": "Joanna"},
                    "language": {"type": "string", "default": "en-US"}
                },
                "required": ["text"]
            }
        }
    }
    
    return endpoints


def get_response_schemas():
    """Define response schemas for all endpoints"""
    
    schemas = {
        "AgentQuestion": {
            "type": "object",
            "properties": {
                "question_id": {"type": "string"},
                "question": {"type": "string"},
                "difficulty": {"type": "string"},
                "category": {"type": "string"},
                "context": {"type": "string"},
                "audio_url": {"type": "string"},
                "expected_duration": {"type": "integer"}
            }
        },
        
        "Evaluation": {
            "type": "object",
            "properties": {
                "evaluation_id": {"type": "string"},
                "score": {"type": "number", "minimum": 0, "maximum": 100},
                "technical_score": {"type": "number"},
                "communication_score": {"type": "number"},
                "problem_solving_score": {"type": "number"},
                "feedback": {"type": "string"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "improvements": {"type": "array", "items": {"type": "string"}}
            }
        },
        
        "CoachingFeedback": {
            "type": "object",
            "properties": {
                "suggestion": {"type": "string"},
                "resources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "type": {"type": "string"}
                        }
                    }
                },
                "practice_areas": {"type": "array", "items": {"type": "string"}},
                "estimated_improvement_time": {"type": "string"}
            }
        },
        
        "InterviewReport": {
            "type": "object",
            "properties": {
                "interview_id": {"type": "string"},
                "candidate_id": {"type": "string"},
                "category": {"type": "string"},
                "role": {"type": "string"},
                "difficulty_level": {"type": "string"},
                "overall_score": {"type": "number"},
                "questions_asked": {"type": "integer"},
                "average_response_time": {"type": "number"},
                "evaluations": {"type": "array"},
                "coaching_feedback": {"type": "array"},
                "recommendations": {"type": "array"},
                "next_steps": {"type": "array"},
                "interview_duration": {"type": "integer"},
                "completed_at": {"type": "string", "format": "date-time"}
            }
        }
    }
    
    return schemas


# Serverless Framework HTTP API configuration
http_api_config = {
    "description": "Bedrock Agentic AI Interview Coach API",
    "version": "2.0.0",
    "basePath": "/api",
    "schemes": ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    
    "securityDefinitions": {
        "api_key": {
            "type": "apiKey",
            "name": "x-api-key",
            "in": "header"
        },
        "oauth2": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "https://auth.example.com/oauth/authorize"
        }
    },
    
    "security": [
        {"api_key": []},
        {"oauth2": ["read", "write"]}
    ],
    
    "x-amazon-apigateway-cors": {
        "allowedOrigins": ["*"],
        "allowedHeaders": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"],
        "allowedMethods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "maxAge": 300
    }
}
