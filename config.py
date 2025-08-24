"""
Configuration settings for AWS Parameter Store Manager
"""
import os
import boto3
from typing import Optional, Dict, Any
from enum import Enum
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

class AuthMethod(Enum):
    """Supported AWS authentication methods"""
    ACCESS_KEY = "access_key"
    PROFILE = "profile"
    SSO = "sso"
    ROLE = "role"
    ENVIRONMENT = "environment"
    DEFAULT = "default"

class AWSConfig:
    """AWS Configuration management with support for multiple authentication methods"""
    
    def __init__(self):
        # Common settings
        self.region: str = 'us-east-1'
        self.kms_key_alias: str = 'alias/aws/ssm'
        self.auth_method: AuthMethod = AuthMethod.DEFAULT
        
        # Access key authentication
        self.access_key_id: Optional[str] = None
        self.secret_access_key: Optional[str] = None
        self.session_token: Optional[str] = None
        
        # Profile authentication
        self.profile_name: Optional[str] = None
        
        # SSO authentication
        self.sso_start_url: Optional[str] = None
        self.sso_region: Optional[str] = None
        self.sso_account_id: Optional[str] = None
        self.sso_role_name: Optional[str] = None
        
        # Role assumption
        self.role_arn: Optional[str] = None
        self.role_session_name: Optional[str] = None
        self.external_id: Optional[str] = None
        self.mfa_serial: Optional[str] = None
        self.mfa_token: Optional[str] = None
        
        # Current session
        self._session: Optional[boto3.Session] = None
    
    def set_access_key_auth(self, access_key_id: str, secret_access_key: str, 
                           session_token: str = None, region: str = 'us-east-1'):
        """Configure access key authentication"""
        self.auth_method = AuthMethod.ACCESS_KEY
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.region = region
        self._session = None  # Reset session
    
    def set_profile_auth(self, profile_name: str, region: str = 'us-east-1'):
        """Configure AWS profile authentication"""
        self.auth_method = AuthMethod.PROFILE
        self.profile_name = profile_name
        self.region = region
        self._session = None  # Reset session
    
    def set_sso_auth(self, sso_start_url: str, sso_region: str, sso_account_id: str, 
                     sso_role_name: str, region: str = 'us-east-1'):
        """Configure AWS SSO authentication"""
        self.auth_method = AuthMethod.SSO
        self.sso_start_url = sso_start_url
        self.sso_region = sso_region
        self.sso_account_id = sso_account_id
        self.sso_role_name = sso_role_name
        self.region = region
        self._session = None  # Reset session
    
    def set_role_auth(self, role_arn: str, role_session_name: str = None, 
                      external_id: str = None, mfa_serial: str = None, 
                      mfa_token: str = None, region: str = 'us-east-1'):
        """Configure IAM role assumption authentication"""
        self.auth_method = AuthMethod.ROLE
        self.role_arn = role_arn
        self.role_session_name = role_session_name or f"aws-parameter-store-{os.getpid()}"
        self.external_id = external_id
        self.mfa_serial = mfa_serial
        self.mfa_token = mfa_token
        self.region = region
        self._session = None  # Reset session
    
    def set_environment_auth(self, region: str = 'us-east-1'):
        """Configure environment variable authentication"""
        self.auth_method = AuthMethod.ENVIRONMENT
        self.region = region
        self._session = None  # Reset session
    
    def set_default_auth(self, region: str = 'us-east-1'):
        """Use default AWS credential chain"""
        self.auth_method = AuthMethod.DEFAULT
        self.region = region
        self._session = None  # Reset session
    
    def is_configured(self) -> bool:
        """Check if AWS credentials are configured"""
        if self.auth_method == AuthMethod.ACCESS_KEY:
            return bool(self.access_key_id and self.secret_access_key)
        elif self.auth_method == AuthMethod.PROFILE:
            return bool(self.profile_name)
        elif self.auth_method == AuthMethod.SSO:
            return bool(self.sso_start_url and self.sso_region and 
                       self.sso_account_id and self.sso_role_name)
        elif self.auth_method == AuthMethod.ROLE:
            return bool(self.role_arn)
        elif self.auth_method in [AuthMethod.ENVIRONMENT, AuthMethod.DEFAULT]:
            return True  # These will be validated during session creation
        return False
    
    def get_session(self) -> boto3.Session:
        """Get or create a boto3 session based on the configured authentication method"""
        if self._session is not None:
            return self._session
        
        try:
            if self.auth_method == AuthMethod.ACCESS_KEY:
                self._session = self._create_access_key_session()
            elif self.auth_method == AuthMethod.PROFILE:
                self._session = self._create_profile_session()
            elif self.auth_method == AuthMethod.SSO:
                self._session = self._create_sso_session()
            elif self.auth_method == AuthMethod.ROLE:
                self._session = self._create_role_session()
            elif self.auth_method == AuthMethod.ENVIRONMENT:
                self._session = self._create_environment_session()
            elif self.auth_method == AuthMethod.DEFAULT:
                self._session = self._create_default_session()
            else:
                raise ValueError(f"Unsupported authentication method: {self.auth_method}")
            
            return self._session
        
        except Exception as e:
            self._session = None
            raise e
    
    def _create_access_key_session(self) -> boto3.Session:
        """Create session using access key credentials"""
        session_config = {
            'aws_access_key_id': self.access_key_id,
            'aws_secret_access_key': self.secret_access_key,
            'region_name': self.region
        }
        if self.session_token:
            session_config['aws_session_token'] = self.session_token
        
        return boto3.Session(**session_config)
    
    def _create_profile_session(self) -> boto3.Session:
        """Create session using AWS profile"""
        return boto3.Session(profile_name=self.profile_name, region_name=self.region)
    
    def _create_sso_session(self) -> boto3.Session:
        """Create session using AWS SSO"""
        # For SSO, we need to create a session and then get credentials
        session = boto3.Session(region_name=self.region)
        
        # Try to get SSO credentials
        try:
            sso_client = session.client('sso')
            
            # This is a simplified approach - in practice, you might need to handle
            # the SSO login flow more comprehensively
            # For now, we'll assume the user has already authenticated via AWS CLI
            
            # Create a new session with SSO profile configuration
            # This typically requires the user to have configured SSO via AWS CLI
            return boto3.Session(region_name=self.region)
            
        except Exception as e:
            raise ValueError(f"SSO authentication failed. Please ensure you've configured SSO via AWS CLI: {str(e)}")
    
    def _create_role_session(self) -> boto3.Session:
        """Create session using role assumption"""
        # First, create a session with default credentials to assume the role
        base_session = boto3.Session(region_name=self.region)
        sts_client = base_session.client('sts')
        
        assume_role_params = {
            'RoleArn': self.role_arn,
            'RoleSessionName': self.role_session_name
        }
        
        if self.external_id:
            assume_role_params['ExternalId'] = self.external_id
        
        if self.mfa_serial and self.mfa_token:
            assume_role_params['SerialNumber'] = self.mfa_serial
            assume_role_params['TokenCode'] = self.mfa_token
        
        response = sts_client.assume_role(**assume_role_params)
        credentials = response['Credentials']
        
        return boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=self.region
        )
    
    def _create_environment_session(self) -> boto3.Session:
        """Create session using environment variables"""
        # boto3 will automatically use environment variables
        return boto3.Session(region_name=self.region)
    
    def _create_default_session(self) -> boto3.Session:
        """Create session using default credential chain"""
        return boto3.Session(region_name=self.region)
    
    def get_session_config(self) -> dict:
        """Get session configuration for boto3 (legacy method for backward compatibility)"""
        if self.auth_method == AuthMethod.ACCESS_KEY:
            config = {
                'aws_access_key_id': self.access_key_id,
                'aws_secret_access_key': self.secret_access_key,
                'region_name': self.region
            }
            if self.session_token:
                config['aws_session_token'] = self.session_token
            return config
        else:
            # For other methods, return region only as session creation is handled differently
            return {'region_name': self.region}
    
    def get_auth_info(self) -> Dict[str, Any]:
        """Get current authentication configuration info"""
        info = {
            'method': self.auth_method.value,
            'region': self.region
        }
        
        if self.auth_method == AuthMethod.ACCESS_KEY:
            info['access_key_id'] = self.access_key_id[:8] + '...' if self.access_key_id else None
            info['has_session_token'] = bool(self.session_token)
        elif self.auth_method == AuthMethod.PROFILE:
            info['profile_name'] = self.profile_name
        elif self.auth_method == AuthMethod.SSO:
            info['sso_start_url'] = self.sso_start_url
            info['sso_account_id'] = self.sso_account_id
            info['sso_role_name'] = self.sso_role_name
        elif self.auth_method == AuthMethod.ROLE:
            info['role_arn'] = self.role_arn
            info['role_session_name'] = self.role_session_name
        
        return info
    
    def reset(self):
        """Reset all configuration"""
        self.__init__()

# Global configuration instance
aws_config = AWSConfig()
