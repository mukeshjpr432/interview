"""
Real-Time Voice & Video Interview Handler
Female AI Agent (Sophia) with streaming audio/video
"""

import boto3
import json
import asyncio
from typing import Dict, Any, AsyncGenerator
import numpy as np
from datetime import datetime

# AWS Services
transcribe_client = boto3.client('transcribe', region_name='us-east-1')
polly_client = boto3.client('polly', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

# Configuration
AGENT_CONFIG = {
    'name': 'Sophia',
    'voice_id': 'Joanna',  # Female voice
    'engine': 'neural',
    'rate': '95',
    'pitch': '+10%',
    'style': 'conversational'
}

VOICE_S3_BUCKET = 'interview-coach-voice-storage'


class FemaleAgentVoiceHandler:
    """Handles real-time voice interaction with female AI agent (Sophia)"""
    
    def __init__(self, interview_id: str):
        self.interview_id = interview_id
        self.agent_name = AGENT_CONFIG['name']
        self.voice_id = AGENT_CONFIG['voice_id']
        self.current_transcription = ""
        self.is_listening = False
        self.is_speaking = False
    
    async def speak_question(self, question_text: str) -> Dict[str, Any]:
        """
        Female agent (Sophia) speaks the interview question
        Returns audio stream for real-time playback
        
        Args:
            question_text: The interview question to ask
            
        Returns:
            Audio stream and metadata
        """
        
        print(f"🎤 Sophia is about to speak: {question_text[:50]}...")
        self.is_speaking = True
        
        try:
            # Create engaging introduction from Sophia
            full_speech = f"Let me ask you this. {question_text}"
            
            response = polly_client.synthesize_speech(
                Text=full_speech,
                OutputFormat='pcm',  # For streaming
                VoiceId=self.voice_id,
                Engine=AGENT_CONFIG['engine'],
                Rate=AGENT_CONFIG['rate'],
                LanguageCode='en-US',
                SpeechMarkTypes=['word', 'sentence']
            )
            
            audio_stream = response['AudioStream'].read()
            
            result = {
                'status': 'speaking',
                'agent': self.agent_name,
                'message': full_speech,
                'audio_data': audio_stream,
                'duration_ms': len(audio_stream) // 32,  # Approximate
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.is_speaking = False
            return result
            
        except Exception as e:
            self.is_speaking = False
            return {
                'status': 'error',
                'error': str(e),
                'agent': self.agent_name
            }
    
    async def listen_to_candidate(self, audio_chunk: bytes) -> AsyncGenerator:
        """
        Real-time listening and transcription
        Streams partial results back to UI
        
        Args:
            audio_chunk: Raw audio data from candidate
            
        Yields:
            Streaming transcription updates
        """
        
        print("👂 Sophia is listening to candidate response...")
        self.is_listening = True
        
        try:
            # Setup for real-time transcription
            # Using AWS Transcribe streaming
            
            async for partial_result in self._transcribe_streaming(audio_chunk):
                # Yield result immediately for UI update
                yield {
                    'status': 'listening',
                    'partial_text': partial_result,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat()
                }
                self.current_transcription = partial_result
            
            self.is_listening = False
            
        except Exception as e:
            self.is_listening = False
            yield {
                'status': 'error',
                'error': str(e),
                'agent': self.agent_name
            }
    
    async def _transcribe_streaming(self, audio_chunk: bytes) -> AsyncGenerator[str, None]:
        """
        Stream transcription with partial results
        
        Args:
            audio_chunk: Audio data to transcribe
            
        Yields:
            Partial transcription strings in real-time
        """
        
        try:
            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=f"sophia_{self.interview_id}_{int(__import__('time').time())}",
                Media={'MediaFileUri': f"s3://{VOICE_S3_BUCKET}/{self.interview_id}/audio.wav"},
                MediaFormat='wav',
                LanguageCode='en-US',
                Settings={
                    'ShowAlternatives': False,
                    'VocabularyFilterMethod': 'mask'
                }
            )
            
            # Poll for results
            job_name = response['TranscriptionJob']['TranscriptionJobName']
            
            while True:
                job = transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                
                if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                    transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    transcript_obj = s3_client.get_object(
                        Bucket=VOICE_S3_BUCKET,
                        Key=transcript_uri.split(f"{VOICE_S3_BUCKET}/")[1]
                    )
                    transcript_data = json.loads(transcript_obj['Body'].read())
                    yield transcript_data['results']['transcripts'][0]['transcript']
                    break
                elif job['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                    raise Exception(job.get('TranscriptionJob', {}).get('FailureReason', 'Unknown error'))
                
                await asyncio.sleep(1)
                
        except Exception as e:
            raise e
    
    async def get_agent_feedback(self, response: str) -> Dict[str, Any]:
        """
        Get Sophia's feedback on candidate response
        
        Args:
            response: Candidate's transcribed response
            
        Returns:
            Feedback with Polly audio
        """
        
        try:
            # Generate feedback based on response length/quality
            if len(response) < 20:
                feedback = "That's a start! Could you expand a bit more on that?"
            elif len(response) > 500:
                feedback = "Wow, that's comprehensive! Let me dig a bit deeper..."
            else:
                feedback = "Great! That's a solid answer. Let me follow up..."
            
            # Sophia speaks the feedback
            feedback_audio = polly_client.synthesize_speech(
                Text=feedback,
                OutputFormat='mp3',
                VoiceId=self.voice_id,
                Engine=AGENT_CONFIG['engine'],
                Rate=AGENT_CONFIG['rate'],
                LanguageCode='en-US'
            )
            
            return {
                'status': 'feedback',
                'agent': self.agent_name,
                'feedback_text': feedback,
                'audio': feedback_audio['AudioStream'].read(),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        
        status = 'idle'
        if self.is_speaking:
            status = 'speaking'
        elif self.is_listening:
            status = 'listening'
        
        return {
            'agent_name': self.agent_name,
            'status': status,
            'is_speaking': self.is_speaking,
            'is_listening': self.is_listening,
            'last_transcription': self.current_transcription,
            'voice_id': self.voice_id
        }


async def websocket_handler(websocket, path):
    """
    WebSocket handler for real-time voice interaction
    Allows bidirectional audio streaming
    """
    
    print(f"🎤 New voice interview connection from {websocket.remote_address}")
    
    interview_id = "interview_123"  # From URL/auth
    handler = FemaleAgentVoiceHandler(interview_id)
    
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            
            # Agent speaks question
            if action == 'speak_question':
                question = data.get('question')
                result = await handler.speak_question(question)
                await websocket.send(json.dumps(result))
            
            # Listen to candidate (stream)
            elif action == 'listen':
                audio_chunk = data.get('audio_chunk')
                async for transcript_update in handler.listen_to_candidate(audio_chunk):
                    await websocket.send(json.dumps(transcript_update))
            
            # Get feedback
            elif action == 'get_feedback':
                response = data.get('response')
                feedback = await handler.get_agent_feedback(response)
                await websocket.send(json.dumps(feedback))
            
            # Get status
            elif action == 'get_status':
                status = handler.get_agent_status()
                await websocket.send(json.dumps(status))
    
    except Exception as e:
        print(f"❌ WebSocket error: {str(e)}")
        await websocket.send(json.dumps({
            'status': 'error',
            'error': str(e)
        }))


def lambda_websocket_handler(event, context):
    """
    AWS Lambda handler for WebSocket connections
    Handles voice/video interview streams
    """
    
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')
    
    print(f"🔗 WebSocket {route_key} connection: {connection_id}")
    
    if route_key == '$connect':
        return {'statusCode': 200, 'body': 'Connected'}
    
    elif route_key == '$disconnect':
        return {'statusCode': 200, 'body': 'Disconnected'}
    
    elif route_key == 'default':
        # Handle incoming messages
        body = json.loads(event.get('body', '{}'))
        interview_id = body.get('interview_id')
        handler = FemaleAgentVoiceHandler(interview_id)
        
        action = body.get('action')
        if action == 'speak_question':
            result = handler.speak_question(body.get('question'))
            return {'statusCode': 200, 'body': json.dumps(result)}
        
        elif action == 'get_status':
            status = handler.get_agent_status()
            return {'statusCode': 200, 'body': json.dumps(status)}
        
        return {'statusCode': 400, 'body': 'Invalid action'}
    
    return {'statusCode': 400, 'body': 'Unknown route'}


if __name__ == "__main__":
    # Test
    handler = FemaleAgentVoiceHandler("test_interview_123")
    
    # Test speaking
    import asyncio
    result = asyncio.run(handler.speak_question(
        "Tell me about a challenging project you worked on and how you solved it."
    ))
    print(f"✅ Agent spoke: {result['status']}")
    
    # Get agent status
    status = handler.get_agent_status()
    print(f"👩‍💼 Agent Status: {status}")
