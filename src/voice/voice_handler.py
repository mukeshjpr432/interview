"""
Voice Interview Handler
AWS Transcribe (STT) + Polly (TTS) integration for voice interviews
"""

import boto3
import json
from typing import Dict, Any, Tuple

transcribe_client = boto3.client('transcribe', region_name='us-east-1')
polly_client = boto3.client('polly', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

VOICE_S3_BUCKET = 'interview-coach-voice-storage'


class VoiceInterviewHandler:
    """Handles voice input/output for interviews"""
    
    def __init__(self, interview_id: str):
        self.interview_id = interview_id
        self.transcription_jobs = {}
    
    def transcribe_audio(self, audio_file_s3_path: str, language: str = 'en-US') -> Dict[str, Any]:
        """
        Convert audio to text using AWS Transcribe
        
        Args:
            audio_file_s3_path: S3 path to audio file (e.g., s3://bucket/audio.wav)
            language: Language code (default: en-US)
            
        Returns:
            Transcription result with text and confidence scores
        """
        
        job_name = f"interview_{self.interview_id}_transcribe"
        
        try:
            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': audio_file_s3_path},
                MediaFormat='wav',  # or 'mp3', 'mp4', 'flac'
                LanguageCode=language,
                OutputBucketName=VOICE_S3_BUCKET,
                OutputKey=f"{self.interview_id}/transcripts/",
                Settings={
                    'ShowAlternatives': False,
                    'MaxSpeakerLabels': 2,
                    'ShowSpeakerLabels': True
                }
            )
            
            self.transcription_jobs[job_name] = response
            
            return {
                'status': 'processing',
                'job_name': job_name,
                'message': 'Transcription started. Please wait...'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_transcription_result(self, job_name: str) -> Dict[str, Any]:
        """
        Get transcription result once job is complete
        
        Args:
            job_name: AWS Transcribe job name
            
        Returns:
            Transcribed text and metadata
        """
        
        try:
            response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            
            job = response['TranscriptionJob']
            
            if job['TranscriptionJobStatus'] == 'COMPLETED':
                transcript_uri = job['Transcript']['TranscriptFileUri']
                
                # Download transcript from S3
                s3_key = transcript_uri.replace(f"s3://{VOICE_S3_BUCKET}/", "")
                transcript_obj = s3_client.get_object(
                    Bucket=VOICE_S3_BUCKET,
                    Key=s3_key
                )
                
                transcript_data = json.loads(transcript_obj['Body'].read())
                
                return {
                    'status': 'completed',
                    'text': transcript_data['results']['transcripts'][0]['transcript'],
                    'confidence': transcript_data['results']['transcripts'][0].get('confidence', 1.0),
                    'items': transcript_data['results']['items']
                }
                
            elif job['TranscriptionJobStatus'] == 'FAILED':
                return {
                    'status': 'failed',
                    'error': job.get('FailureReason', 'Unknown error')
                }
            else:
                return {
                    'status': 'in_progress',
                    'message': f'Job status: {job["TranscriptionJobStatus"]}'
                }
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def synthesize_speech(self, text: str, voice_id: str = 'Joanna') -> Dict[str, Any]:
        """
        Convert text to speech using AWS Polly
        Interviewer voice for generating questions
        
        Args:
            text: Text to convert to speech
            voice_id: Polly voice (Joanna, Matthew, etc.)
            
        Returns:
            Audio file S3 URL and metadata
        """
        
        try:
            response = polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',  # or 'ogg_vorbis', 'pcm'
                VoiceId=voice_id,
                Engine='neural',  # For more natural speech
                Rate='100',  # Words per minute (80-360)
                SpeechMarkTypes=['sentence', 'word'],
                LanguageCode='en-US'
            )
            
            # Save to S3
            audio_key = f"{self.interview_id}/questions/{voice_id}_{int(__import__('time').time())}.mp3"
            
            s3_client.put_object(
                Bucket=VOICE_S3_BUCKET,
                Key=audio_key,
                Body=response['AudioStream'].read(),
                ContentType='audio/mpeg'
            )
            
            audio_url = f"s3://{VOICE_S3_BUCKET}/{audio_key}"
            
            return {
                'status': 'success',
                'audio_url': audio_url,
                'text': text,
                'voice_id': voice_id,
                'duration_ms': response.get('RequestCharacters', len(text)) * 50  # Approximate
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def process_voice_response(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process candidate voice response
        1. Upload audio to S3
        2. Transcribe using AWS Transcribe
        3. Return transcribed text
        
        Args:
            audio_file_path: Local path to audio file
            
        Returns:
            Transcribed response text
        """
        
        try:
            # Upload to S3
            s3_key = f"{self.interview_id}/responses/{audio_file_path.split('/')[-1]}"
            
            with open(audio_file_path, 'rb') as audio:
                s3_client.upload_fileobj(
                    audio,
                    VOICE_S3_BUCKET,
                    s3_key
                )
            
            audio_s3_path = f"s3://{VOICE_S3_BUCKET}/{s3_key}"
            
            # Transcribe
            transcription = self.transcribe_audio(audio_s3_path)
            
            return {
                'status': 'processing',
                'job_name': transcription['job_name'],
                'message': 'Processing your response...'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def generate_voice_interview_prompt(self) -> str:
        """System prompt for voice interview"""
        
        return """
You are an Interviewer Agent for voice-based interviews running on AWS Bedrock.

VOICE INTERACTION RULES:
1. Questions should be concise (under 200 words)
2. Speak naturally with appropriate pauses
3. Use conversational language (not written English)
4. Wait for candidate response after each question
5. Use follow-up probes if answer is incomplete

VOICE-SPECIFIC GUIDANCE:
- Ask one question at a time
- Allow 30-60 seconds thinking time
- Acknowledge if candidate needs clarification
- Maintain warm, encouraging tone through speech
- Avoid complex jargon in voice (unlike text)

INTERVIEW FLOW:
1. Greet warmly
2. Ask for job role & experience
3. Ask 10-12 questions over ~45 minutes
4. Provide closing remarks

Continue the interview based on the speech-to-text transcript provided.
"""


def lambda_voice_handler(event, context):
    """
    AWS Lambda handler for voice interview
    
    Event:
    {
        "action": "transcribe_response" | "synthesize_question" | "start_voice_interview",
        "interview_id": "uuid",
        "audio_file_s3": "s3://bucket/path/to/audio.wav (for transcribe)",
        "text": "Question text (for synthesize)",
        "voice_id": "Joanna (for synthesize)"
    }
    """
    
    try:
        action = event.get('action')
        interview_id = event.get('interview_id')
        
        handler = VoiceInterviewHandler(interview_id)
        
        if action == 'transcribe_response':
            audio_file = event.get('audio_file_s3')
            result = handler.get_transcription_result(audio_file)
            
        elif action == 'synthesize_question':
            text = event.get('text')
            voice_id = event.get('voice_id', 'Joanna')
            result = handler.synthesize_speech(text, voice_id)
            
        elif action == 'process_voice_response':
            audio_file_path = event.get('audio_file_path')
            result = handler.process_voice_response(audio_file_path)
            
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
    # Test synthesize
    handler = VoiceInterviewHandler("test_interview_123")
    result = handler.synthesize_speech(
        "Tell me about your experience with system design. What's the most complex system you've designed?"
    )
    print(json.dumps(result, indent=2))
