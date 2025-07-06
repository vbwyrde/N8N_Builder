from typing import Dict, Any, Optional, List, Set
import asyncio
import logging
import hashlib
import jwt
from datetime import datetime, timedelta
from enum import Enum
from .event_types import Event, EventType, EventPriority

class PermissionLevel(Enum):
    """Permission levels for access control."""
    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3
    SUPER_ADMIN = 4

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

class SecurityManager:
    """Manages security-related functionality."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.secret_key = self.config.get('secret_key', 'default_secret_key')
        self.token_expiry = self.config.get('token_expiry', 3600)  # 1 hour
        self.allowed_origins = set(self.config.get('allowed_origins', ['*']))
        self.rate_limits = self.config.get('rate_limits', {})
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the security manager."""
        if self._running:
            return

        self._running = True
        self._tasks = [
            asyncio.create_task(self._cleanup_expired_tokens())
        ]
        self.logger.info("Security Manager started")

    async def stop(self):
        """Stop the security manager."""
        if not self._running:
            return

        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self.logger.info("Security Manager stopped")

    def generate_token(self, user_id: str, roles: List[str]) -> str:
        """Generate a JWT token for a user."""
        try:
            payload = {
                'user_id': user_id,
                'roles': roles,
                'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry)
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        except Exception as e:
            self.logger.error(f"Error generating token: {str(e)}")
            raise SecurityError("Failed to generate token")

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify a JWT token."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.hash_password(password) == hashed_password

    def check_permission(self, user_roles: List[str], required_roles: List[str]) -> bool:
        """Check if a user has the required roles."""
        return any(role in user_roles for role in required_roles)

    def validate_origin(self, origin: str) -> bool:
        """Validate if an origin is allowed."""
        return '*' in self.allowed_origins or origin in self.allowed_origins

    async def _cleanup_expired_tokens(self):
        """Clean up expired tokens."""
        while self._running:
            try:
                # This would typically clean up expired tokens from a database
                # For now, just sleep as this is a placeholder
                await asyncio.sleep(3600)  # Check every hour
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error cleaning up tokens: {str(e)}")
                await asyncio.sleep(60)  # Back off on error

    def create_security_event(self, event_type: str, data: Dict[str, Any]) -> Event:
        """Create a security-related event."""
        return Event(
            type=EventType.SECURITY_ALERT,
            data={
                "event_type": event_type,
                **data
            },
            priority=EventPriority.HIGH,
            source="security_manager"
        )

    async def check_rate_limit(self, user_id: str, action: str) -> bool:
        """Check if a user has exceeded their rate limit for an action."""
        # This would typically check against a rate limiting system
        # For now, return True as this is a placeholder
        return True 