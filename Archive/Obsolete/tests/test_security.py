import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from n8n_builder.agents.integration.security import (
    SecurityManager,
    User,
    Token,
    Permission,
    SecurityError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    RateLimitError,
    PermissionLevel
)

pytestmark = pytest.mark.asyncio

class TestSecurityManager:
    """Test suite for SecurityManager."""
    
    async def test_initialization(self, security_manager):
        """Test proper initialization of the manager."""
        assert security_manager is not None
        assert security_manager.users is not None
        assert security_manager.tokens is not None
        assert security_manager.config is not None
    
    async def test_user_authentication(self, security_manager):
        """Test user authentication."""
        # Create a test user
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        security_manager.users[user.username] = user
        
        # Test successful authentication
        token = await security_manager.authenticate_user(
            "testuser",
            "testpass"
        )
        assert token is not None
        assert token.username == "testuser"
        
        # Test failed authentication
        with pytest.raises(Exception):
            await security_manager.authenticate_user(
                "testuser",
                "wrongpass"
            )
    
    async def test_token_validation(self, security_manager):
        """Test token validation."""
        # Create a test user and token
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        security_manager.users[user.username] = user
        
        token = await security_manager.authenticate_user(
            "testuser",
            "testpass"
        )
        
        # Test valid token
        validated_user = await security_manager.validate_token(token.token)
        assert validated_user is not None
        assert validated_user.username == "testuser"
        
        # Test invalid token
        with pytest.raises(Exception):
            await security_manager.validate_token("invalid_token")
    
    async def test_token_expiration(self, security_manager):
        """Test token expiration."""
        # Create a test user and token
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        security_manager.users[user.username] = user
        
        token = await security_manager.authenticate_user(
            "testuser",
            "testpass"
        )
        
        # Set token to expired
        token.expires_at = datetime.now() - timedelta(hours=1)
        
        # Test expired token
        with pytest.raises(Exception):
            await security_manager.validate_token(token.token)
    
    async def test_permission_checking(self, security_manager):
        """Test permission checking."""
        # Create a test user with specific permissions
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ, Permission.WRITE]
        )
        security_manager.users[user.username] = user
        
        # Test valid permissions
        assert await security_manager.check_permission(
            user,
            Permission.READ
        )
        assert await security_manager.check_permission(
            user,
            Permission.WRITE
        )
        
        # Test invalid permission
        assert not await security_manager.check_permission(
            user,
            Permission.ADMIN
        )
    
    async def test_rate_limiting(self, security_manager):
        """Test rate limiting."""
        # Create a test user
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        security_manager.users[user.username] = user
        
        # Test within rate limit
        for _ in range(5):
            assert await security_manager.check_rate_limit(user)
        
        # Test exceeding rate limit
        with pytest.raises(Exception):
            for _ in range(10):
                await security_manager.check_rate_limit(user)
    
    async def test_input_validation(self, security_manager):
        """Test input validation."""
        # Test valid input
        valid_input = {
            "name": "test",
            "value": 42,
            "list": [1, 2, 3]
        }
        assert await security_manager.validate_input(valid_input)
        
        # Test invalid input (script injection attempt)
        invalid_input = {
            "name": "<script>alert('xss')</script>",
            "value": "42; DROP TABLE users;"
        }
        assert not await security_manager.validate_input(invalid_input)
    
    async def test_user_management(self, security_manager):
        """Test user management functions."""
        # Create a test user
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        
        # Test user creation
        await security_manager.create_user(user)
        assert user.username in security_manager.users
        
        # Test user update
        user.permissions.append(Permission.WRITE)
        await security_manager.update_user(user)
        assert Permission.WRITE in security_manager.users[user.username].permissions
        
        # Test user deletion
        await security_manager.delete_user(user.username)
        assert user.username not in security_manager.users
    
    async def test_token_management(self, security_manager):
        """Test token management functions."""
        # Create a test user and token
        user = User(
            username="testuser",
            password="testpass",
            permissions=[Permission.READ]
        )
        security_manager.users[user.username] = user
        
        token = await security_manager.authenticate_user(
            "testuser",
            "testpass"
        )
        
        # Test token revocation
        await security_manager.revoke_token(token.token)
        with pytest.raises(Exception):
            await security_manager.validate_token(token.token)
        
        # Test token cleanup
        old_token = Token(
            token="old_token",
            username="testuser",
            created_at=datetime.now() - timedelta(days=2),
            expires_at=datetime.now() - timedelta(days=1)
        )
        security_manager.tokens[old_token.token] = old_token
        
        await security_manager.cleanup_expired_tokens()
        assert old_token.token not in security_manager.tokens
    
    async def test_security_logging(self, security_manager):
        """Test security logging."""
        # Test logging of various security events
        await security_manager.log_security_event(
            "test_event",
            {"user": "testuser", "action": "login"}
        )
        
        # Note: In a real test, we would verify the logs
        # This might require a custom logger or mock
        assert True  # Placeholder for actual assertion 