"""
AWS Cognito Authentication Handlers for Sophia AI Interview Coach
Handles user signup, login, profile management, and authentication
"""

import json
import boto3
import hashlib
import secrets
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# AWS Clients
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Environment Variables
COGNITO_USER_POOL_ID = 'us-east-1_S8nbIWo7v'  # Replace with actual pool ID
COGNITO_CLIENT_ID = '18q1qj09bnngsu8fn3lsnso8cd'  # Replace with actual client ID
USERS_TABLE = 'sophia_users'
USER_PROFILES_TABLE = 'sophia_user_profiles'
INTERVIEW_HISTORY_TABLE = 'sophia_interview_history'


class AuthenticationHandler:
    """Handle user authentication with AWS Cognito"""
    
    @staticmethod
    def signup(email: str, password: str, full_name: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Register a new user with Cognito
        
        Args:
            email: User email address
            password: User password (must meet complexity requirements)
            full_name: User's full name
            
        Returns:
            Tuple of (success: bool, response: dict)
        """
        try:
            response = cognito_client.sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'false'},
                    {'Name': 'name', 'Value': full_name},
                    {'Name': 'given_name', 'Value': full_name.split()[0] if full_name else 'User'},
                ]
            )
            
            # Create user profile in DynamoDB
            ProfileManager.create_profile(
                user_id=response['UserSub'],
                email=email,
                full_name=full_name
            )
            
            return True, {
                'statusCode': 200,
                'body': {
                    'message': 'Signup successful. Please check your email for verification.',
                    'user_id': response['UserSub'],
                    'username': email
                }
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                return False, {
                    'statusCode': 400,
                    'body': {'error': 'Email already registered'}
                }
            elif error_code == 'InvalidPasswordException':
                return False, {
                    'statusCode': 400,
                    'body': {'error': 'Password does not meet requirements'}
                }
            else:
                return False, {
                    'statusCode': 500,
                    'body': {'error': str(e)}
                }
    
    @staticmethod
    def confirm_signup(email: str, confirmation_code: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Confirm user email with verification code
        
        Args:
            email: User email address
            confirmation_code: Code sent to email
            
        Returns:
            Tuple of (success: bool, response: dict)
        """
        try:
            cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            
            return True, {
                'statusCode': 200,
                'body': {'message': 'Email confirmed successfully'}
            }
            
        except ClientError as e:
            return False, {
                'statusCode': 400,
                'body': {'error': str(e)}
            }
    
    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Tuple of (success: bool, response with tokens)
        """
        try:
            response = cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            
            tokens = response['AuthenticationResult']
            
            # Decode token to get user ID
            user_id = AuthenticationHandler.get_user_from_token(tokens['IdToken'])
            
            return True, {
                'statusCode': 200,
                'body': {
                    'message': 'Login successful',
                    'access_token': tokens['AccessToken'],
                    'id_token': tokens['IdToken'],
                    'refresh_token': tokens['RefreshToken'],
                    'expires_in': tokens['ExpiresIn'],
                    'user_id': user_id
                }
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotConfirmedException':
                return False, {
                    'statusCode': 401,
                    'body': {'error': 'User not confirmed. Please check your email.'}
                }
            elif error_code == 'NotAuthorizedException':
                return False, {
                    'statusCode': 401,
                    'body': {'error': 'Invalid email or password'}
                }
            else:
                return False, {
                    'statusCode': 500,
                    'body': {'error': str(e)}
                }
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Refresh authentication tokens
        
        Args:
            refresh_token: User's refresh token
            
        Returns:
            Tuple of (success: bool, new tokens)
        """
        try:
            response = cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )
            
            tokens = response['AuthenticationResult']
            return True, {
                'statusCode': 200,
                'body': {
                    'access_token': tokens['AccessToken'],
                    'id_token': tokens['IdToken'],
                    'expires_in': tokens['ExpiresIn']
                }
            }
            
        except ClientError as e:
            return False, {
                'statusCode': 401,
                'body': {'error': 'Token refresh failed'}
            }
    
    @staticmethod
    def logout(access_token: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Sign out user (invalidate access token)
        
        Args:
            access_token: User's access token
            
        Returns:
            Tuple of (success: bool, response)
        """
        try:
            cognito_client.global_sign_out(AccessToken=access_token)
            return True, {
                'statusCode': 200,
                'body': {'message': 'Logout successful'}
            }
            
        except ClientError as e:
            return False, {
                'statusCode': 500,
                'body': {'error': str(e)}
            }
    
    @staticmethod
    def reset_password(email: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Initiate password reset for user
        
        Args:
            email: User email address
            
        Returns:
            Tuple of (success: bool, response)
        """
        try:
            cognito_client.forgot_password(
                ClientId=COGNITO_CLIENT_ID,
                Username=email
            )
            
            return True, {
                'statusCode': 200,
                'body': {'message': 'Reset code sent to email'}
            }
            
        except ClientError as e:
            return False, {
                'statusCode': 500,
                'body': {'error': str(e)}
            }
    
    @staticmethod
    def confirm_reset_password(email: str, code: str, new_password: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Confirm password reset with code
        
        Args:
            email: User email address
            code: Reset code from email
            new_password: New password
            
        Returns:
            Tuple of (success: bool, response)
        """
        try:
            cognito_client.confirm_forgot_password(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                ConfirmationCode=code,
                Password=new_password
            )
            
            return True, {
                'statusCode': 200,
                'body': {'message': 'Password reset successful'}
            }
            
        except ClientError as e:
            return False, {
                'statusCode': 500,
                'body': {'error': str(e)}
            }
    
    @staticmethod
    def verify_token(token: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            Tuple of (valid: bool, claims: dict)
        """
        try:
            # In production, use proper JWT verification
            # For now, decode without verification (not secure)
            import base64
            
            parts = token.split('.')
            if len(parts) != 3:
                return False, {}
            
            # Add padding if necessary
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4)
            
            decoded = base64.urlsafe_b64decode(payload)
            claims = json.loads(decoded)
            
            return True, claims
            
        except Exception as e:
            return False, {}
    
    @staticmethod
    def get_user_from_token(token: str) -> str:
        """Extract user ID from JWT token"""
        valid, claims = AuthenticationHandler.verify_token(token)
        if valid and 'sub' in claims:
            return claims['sub']
        return ''


class ProfileManager:
    """Manage user profiles and preferences"""
    
    @staticmethod
    def create_profile(user_id: str, email: str, full_name: str) -> bool:
        """Create new user profile"""
        try:
            table = dynamodb.Table(USER_PROFILES_TABLE)
            table.put_item(
                Item={
                    'user_id': user_id,
                    'email': email,
                    'full_name': full_name,
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat(),
                    'interviews_completed': 0,
                    'total_score': 0,
                    'preferred_categories': [],
                    'skills': [],
                    'experience_level': 'junior',
                    'notification_settings': {
                        'email_notifications': True,
                        'interview_reminders': True
                    }
                }
            )
            return True
        except ClientError as e:
            print(f"Error creating profile: {e}")
            return False
    
    @staticmethod
    def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        try:
            table = dynamodb.Table(USER_PROFILES_TABLE)
            response = table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting profile: {e}")
            return None
    
    @staticmethod
    def update_profile(user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user profile"""
        try:
            table = dynamodb.Table(USER_PROFILES_TABLE)
            
            # Build update expression
            update_expr = "SET updated_at = :now"
            expr_attr_values = {':now': datetime.utcnow().isoformat()}
            
            for key, value in updates.items():
                if key != 'user_id':  # Don't update partition key
                    update_expr += f", {key} = :{key}"
                    expr_attr_values[f":{key}"] = value
            
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_attr_values
            )
            return True
        except ClientError as e:
            print(f"Error updating profile: {e}")
            return False
    
    @staticmethod
    def get_user_stats(user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        profile = ProfileManager.get_profile(user_id)
        if not profile:
            return {}
        
        # Calculate stats from interview history
        history = InterviewHistoryManager.get_user_history(user_id)
        
        total_interviews = len(history)
        avg_score = sum(h.get('score', 0) for h in history) / total_interviews if history else 0
        
        return {
            'total_interviews': total_interviews,
            'average_score': round(avg_score, 2),
            'completed_categories': list(set(h.get('category', '') for h in history if h.get('category'))),
            'last_interview': history[0]['start_time'] if history else None,
            'experience_level': profile.get('experience_level', 'junior'),
            'skills': profile.get('skills', [])
        }


class InterviewHistoryManager:
    """Manage interview history and results"""
    
    @staticmethod
    def save_interview(
        user_id: str,
        interview_id: str,
        category: str,
        role: str,
        start_time: str,
        end_time: str,
        score: float,
        feedback: Dict[str, Any],
        transcript: Optional[str] = None
    ) -> bool:
        """Save interview to history"""
        try:
            table = dynamodb.Table(INTERVIEW_HISTORY_TABLE)
            table.put_item(
                Item={
                    'user_id': user_id,
                    'interview_id': interview_id,
                    'start_time': start_time,
                    'category': category,
                    'role': role,
                    'end_time': end_time,
                    'score': score,
                    'feedback': feedback,
                    'transcript': transcript or '',
                    'created_at': datetime.utcnow().isoformat()
                }
            )
            
            # Update user profile statistics
            profile = ProfileManager.get_profile(user_id)
            if profile:
                new_completed = profile.get('interviews_completed', 0) + 1
                new_total = profile.get('total_score', 0) + score
                
                ProfileManager.update_profile(user_id, {
                    'interviews_completed': new_completed,
                    'total_score': new_total,
                    'last_interview_time': end_time
                })
            
            return True
        except ClientError as e:
            print(f"Error saving interview: {e}")
            return False
    
    @staticmethod
    def get_user_history(user_id: str, limit: int = 50) -> list:
        """Get user interview history"""
        try:
            table = dynamodb.Table(INTERVIEW_HISTORY_TABLE)
            response = table.query(
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': user_id},
                ScanIndexForward=False,  # Latest first
                Limit=limit
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting history: {e}")
            return []
    
    @staticmethod
    def get_interview_details(user_id: str, interview_id: str) -> Optional[Dict[str, Any]]:
        """Get details of a specific interview"""
        try:
            table = dynamodb.Table(INTERVIEW_HISTORY_TABLE)
            
            # First get the interview from history
            history = InterviewHistoryManager.get_user_history(user_id)
            for interview in history:
                if interview['interview_id'] == interview_id:
                    return interview
            
            return None
        except ClientError as e:
            print(f"Error getting interview details: {e}")
            return None
    
    @staticmethod
    def delete_interview(user_id: str, interview_id: str) -> bool:
        """Delete interview from history"""
        try:
            table = dynamodb.Table(INTERVIEW_HISTORY_TABLE)
            
            # Get the interview first to find start_time
            history = InterviewHistoryManager.get_user_history(user_id)
            start_time = None
            for interview in history:
                if interview['interview_id'] == interview_id:
                    start_time = interview['start_time']
                    break
            
            if not start_time:
                return False
            
            table.delete_item(
                Key={
                    'user_id': user_id,
                    'start_time': start_time
                }
            )
            return True
        except ClientError as e:
            print(f"Error deleting interview: {e}")
            return False


def lambda_auth_handler(event, context):
    """Lambda handler for auth endpoints"""
    
    method = event['requestContext']['http']['method']
    path = event['rawPath']
    
    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}
    
    # Signup endpoint
    if method == 'POST' and path == '/auth/signup':
        success, response = AuthenticationHandler.signup(
            email=body.get('email'),
            password=body.get('password'),
            full_name=body.get('full_name')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Login endpoint
    elif method == 'POST' and path == '/auth/login':
        success, response = AuthenticationHandler.login(
            email=body.get('email'),
            password=body.get('password')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Confirm signup endpoint
    elif method == 'POST' and path == '/auth/confirm':
        success, response = AuthenticationHandler.confirm_signup(
            email=body.get('email'),
            confirmation_code=body.get('code')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Refresh token endpoint
    elif method == 'POST' and path == '/auth/refresh':
        success, response = AuthenticationHandler.refresh_token(
            refresh_token=body.get('refresh_token')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Logout endpoint
    elif method == 'POST' and path == '/auth/logout':
        token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
        success, response = AuthenticationHandler.logout(token)
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Password reset endpoints
    elif method == 'POST' and path == '/auth/forgot-password':
        success, response = AuthenticationHandler.reset_password(
            email=body.get('email')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    elif method == 'POST' and path == '/auth/reset-password':
        success, response = AuthenticationHandler.confirm_reset_password(
            email=body.get('email'),
            code=body.get('code'),
            new_password=body.get('new_password')
        )
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body']),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Get profile
    elif method == 'GET' and path.startswith('/profile'):
        token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
        user_id = AuthenticationHandler.get_user_from_token(token)
        
        if not user_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Unauthorized'}),
                'headers': {'Content-Type': 'application/json'}
            }
        
        profile = ProfileManager.get_profile(user_id)
        if profile:
            # Add user stats
            stats = ProfileManager.get_user_stats(user_id)
            profile['stats'] = stats
            
            return {
                'statusCode': 200,
                'body': json.dumps(profile),
                'headers': {'Content-Type': 'application/json'}
            }
        
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Profile not found'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Update profile
    elif method == 'PUT' and path.startswith('/profile'):
        token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
        user_id = AuthenticationHandler.get_user_from_token(token)
        
        if not user_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Unauthorized'}),
                'headers': {'Content-Type': 'application/json'}
            }
        
        success = ProfileManager.update_profile(user_id, body)
        
        if success:
            profile = ProfileManager.get_profile(user_id)
            return {
                'statusCode': 200,
                'body': json.dumps(profile),
                'headers': {'Content-Type': 'application/json'}
            }
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Update failed'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Get interview history
    elif method == 'GET' and path == '/interview/history':
        token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
        user_id = AuthenticationHandler.get_user_from_token(token)
        
        if not user_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Unauthorized'}),
                'headers': {'Content-Type': 'application/json'}
            }
        
        history = InterviewHistoryManager.get_user_history(user_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'interviews': history,
                'count': len(history)
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Endpoint not found'}),
            'headers': {'Content-Type': 'application/json'}
        }
