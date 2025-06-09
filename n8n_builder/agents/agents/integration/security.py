import jwt
import hashlib
import time
import re
from typing import Dict, Any, Optional, List, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class SecurityError(Exception):
    """Base class for security-related errors."""
    pass

class AuthenticationError(SecurityError):
    """Raised when authentication fails."""
    pass

class AuthorizationError(SecurityError):
    """Raised when authorization fails."""
    pass

class ValidationError(SecurityError):
    """Raised when validation fails."""
    pass

class RateLimitError(SecurityError):
    """Raised when rate limit is exceeded."""
    pass

class PermissionLevel(Enum):
    """Permission levels for users."""
    READ = 1
    WRITE = 2
    ADMIN = 3

@dataclass
class User:
    """User information and permissions."""
    user_id: str
    username: str
    email: str
    permission_level: PermissionLevel
    roles: Set[str]
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: datetime = datetime.now()

@dataclass
class Session:
    """Session information."""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_valid: bool = True

class SecurityManager:
    """Manages security, authentication, and validation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.secret_key = config.get('secret_key', 'your-secret-key')
        self.token_expiry = config.get('token_expiry', 3600)  # 1 hour
        self.rate_limits = config.get('rate_limits', {
            'default': {'requests': 100, 'period': 60},  # 100 requests per minute
            'workflow': {'requests': 10, 'period': 60},  # 10 workflow requests per minute
            'api': {'requests': 1000, 'period': 60}      # 1000 API requests per minute
        })
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.rate_limiters: Dict[str, Dict[str, List[float]]] = {}
        
        # Initialize rate limiters
        for limit_type in self.rate_limits:
            self.rate_limiters[limit_type] = {}
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self, user_id: str, session_id: str) -> str:
        """Generate a JWT token."""
        payload = {
            'user_id': user_id,
            'session_id': session_id,
            'exp': int(time.time()) + self.token_expiry
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def _verify_token(self, token: str) -> Dict[str, Any]:
        """Verify a JWT token."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    def _check_rate_limit(self, client_id: str, limit_type: str = 'default') -> bool:
        """Check if a client has exceeded their rate limit."""
        if limit_type not in self.rate_limits:
            limit_type = 'default'
        
        limit = self.rate_limits[limit_type]
        now = time.time()
        
        # Initialize rate limiter for client if not exists
        if client_id not in self.rate_limiters[limit_type]:
            self.rate_limiters[limit_type][client_id] = []
        
        # Remove old requests
        self.rate_limiters[limit_type][client_id] = [
            t for t in self.rate_limiters[limit_type][client_id]
            if now - t < limit['period']
        ]
        
        # Check if limit exceeded
        if len(self.rate_limiters[limit_type][client_id]) >= limit['requests']:
            return False
        
        # Add new request
        self.rate_limiters[limit_type][client_id].append(now)
        return True
    
    def _validate_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate input data against a schema."""
        for field, rules in schema.items():
            if field not in data:
                if rules.get('required', False):
                    return False, f"Missing required field: {field}"
                continue
            
            value = data[field]
            
            # Type validation
            if 'type' in rules and not isinstance(value, rules['type']):
                return False, f"Invalid type for field {field}"
            
            # Pattern validation
            if 'pattern' in rules and not re.match(rules['pattern'], str(value)):
                return False, f"Invalid format for field {field}"
            
            # Range validation
            if 'min' in rules and value < rules['min']:
                return False, f"Value too small for field {field}"
            if 'max' in rules and value > rules['max']:
                return False, f"Value too large for field {field}"
            
            # Length validation
            if 'min_length' in rules and len(str(value)) < rules['min_length']:
                return False, f"Value too short for field {field}"
            if 'max_length' in rules and len(str(value)) > rules['max_length']:
                return False, f"Value too long for field {field}"
        
        return True, None
    
    async def authenticate(self, username: str, password: str, 
                          ip_address: str, user_agent: str) -> Tuple[str, str]:
        """Authenticate a user and create a session."""
        # Find user
        user = next((u for u in self.users.values() if u.username == username), None)
        if not user or not user.is_active:
            raise AuthenticationError("Invalid username or password")
        
        # Verify password
        if self._hash_password(password) != self._hash_password(user.password):
            raise AuthenticationError("Invalid username or password")
        
        # Create session
        session_id = f"session_{int(time.time())}"
        session = Session(
            session_id=session_id,
            user_id=user.user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self.token_expiry),
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.sessions[session_id] = session
        
        # Update user
        user.last_login = datetime.now()
        
        # Generate token
        token = self._generate_token(user.user_id, session_id)
        
        return token, session_id
    
    async def validate_token(self, token: str) -> User:
        """Validate a token and return the associated user."""
        # Verify token
        payload = self._verify_token(token)
        
        # Get session
        session = self.sessions.get(payload['session_id'])
        if not session or not session.is_valid:
            raise AuthenticationError("Invalid session")
        
        # Check expiration
        if datetime.now() > session.expires_at:
            session.is_valid = False
            raise AuthenticationError("Session expired")
        
        # Get user
        user = self.users.get(payload['user_id'])
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        return user
    
    async def check_permission(self, user: User, required_level: PermissionLevel) -> bool:
        """Check if a user has the required permission level."""
        return user.permission_level.value >= required_level.value
    
    async def validate_workflow_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate workflow data."""
        schema = {
            'workflow_id': {'type': str, 'required': True, 'pattern': r'^[a-zA-Z0-9_-]+$'},
            'name': {'type': str, 'required': True, 'min_length': 1, 'max_length': 100},
            'description': {'type': str, 'required': False, 'max_length': 500},
            'nodes': {'type': list, 'required': True, 'min_length': 1},
            'edges': {'type': list, 'required': True}
        }
        return self._validate_input(data, schema)
    
    async def validate_agent_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate agent data."""
        schema = {
            'agent_id': {'type': str, 'required': True, 'pattern': r'^[a-zA-Z0-9_-]+$'},
            'type': {'type': str, 'required': True},
            'config': {'type': dict, 'required': True}
        }
        return self._validate_input(data, schema)
    
    async def check_rate_limit(self, client_id: str, limit_type: str = 'default'):
        """Check if a client has exceeded their rate limit."""
        if not self._check_rate_limit(client_id, limit_type):
            raise RateLimitError(f"Rate limit exceeded for {limit_type}")
    
    async def invalidate_session(self, session_id: str):
        """Invalidate a session."""
        if session_id in self.sessions:
            self.sessions[session_id].is_valid = False
    
    async def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        now = datetime.now()
        expired = [
            session_id for session_id, session in self.sessions.items()
            if now > session.expires_at
        ]
        for session_id in expired:
            del self.sessions[session_id] 