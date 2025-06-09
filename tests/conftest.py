import pytest
import asyncio
import json
from typing import Dict, Any, Generator
from datetime import datetime
from pathlib import Path

from n8n_builder.agents.integration.agent_integration_manager import AgentIntegrationManager, WorkflowPriority
from n8n_builder.agents.integration.monitoring import MonitoringManager, MetricType, HealthStatus
from n8n_builder.agents.integration.security import SecurityManager, PermissionLevel
from n8n_builder.agents.integration.error_recovery import ErrorRecoveryManager, CircuitState
from n8n_builder.agents.integration.ui_controller import AgentUIController
from n8n_builder.agents.integration.event_stream_manager import EventStreamManager
from n8n_builder.agents.integration.message_broker import MessageBroker
from n8n_builder.agents.integration.state_manager import StateManager

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Load test configuration."""
    config_path = Path(__file__).parent / "test_config.json"
    with open(config_path) as f:
        return json.load(f)

@pytest.fixture
async def message_broker():
    """Create a message broker instance for testing."""
    broker = MessageBroker()
    await broker.start()
    yield broker
    await broker.stop()

@pytest.fixture
async def state_manager(tmp_path):
    """Create a state manager instance for testing."""
    state_file = tmp_path / "test_state.json"
    manager = StateManager(str(state_file))
    yield manager
    await manager.close()

@pytest.fixture
async def event_stream_manager():
    """Create an event stream manager instance for testing."""
    manager = EventStreamManager()
    await manager.start()
    yield manager
    await manager.stop()

@pytest.fixture
async def ui_controller(event_stream_manager):
    """Create a UI controller instance for testing."""
    controller = AgentUIController(event_stream_manager)
    await controller.start()
    yield controller
    await controller.stop()

@pytest.fixture
async def security_manager(test_config):
    """Create a security manager instance for testing."""
    return SecurityManager(test_config.get('security', {}))

@pytest.fixture
async def error_recovery_manager(test_config):
    """Create an error recovery manager instance for testing."""
    return ErrorRecoveryManager(test_config.get('error_recovery', {}))

@pytest.fixture
async def monitoring_manager(test_config):
    """Create a monitoring manager instance for testing."""
    manager = MonitoringManager(test_config.get('monitoring', {}))
    await manager.start()
    yield manager
    await manager.stop()

@pytest.fixture
async def agent_integration_manager(
    test_config,
    message_broker,
    state_manager,
    event_stream_manager,
    ui_controller,
    security_manager,
    error_recovery_manager,
    monitoring_manager
):
    """Create an agent integration manager instance for testing."""
    manager = AgentIntegrationManager(test_config)
    await manager.start()
    yield manager
    await manager.stop()

@pytest.fixture
def sample_workflow_data() -> Dict[str, Any]:
    """Generate sample workflow data for testing."""
    return {
        'workflow_id': f'test_workflow_{datetime.now().timestamp()}',
        'name': 'Test Workflow',
        'description': 'A test workflow',
        'nodes': [
            {
                'id': 'node1',
                'type': 'start',
                'position': {'x': 0, 'y': 0}
            },
            {
                'id': 'node2',
                'type': 'process',
                'position': {'x': 100, 'y': 0}
            }
        ],
        'edges': [
            {
                'id': 'edge1',
                'source': 'node1',
                'target': 'node2'
            }
        ],
        'settings': {
            'timeout': 300,
            'retry_count': 3
        }
    }

@pytest.fixture
def sample_agent_config() -> Dict[str, Any]:
    """Generate sample agent configuration for testing."""
    return {
        'name': 'test_agent',
        'type': 'processor',
        'settings': {
            'max_concurrent_tasks': 5,
            'timeout': 60
        },
        'resources': {
            'cpu_limit': 50,
            'memory_limit': 512
        }
    }

@pytest.fixture
def mock_event():
    """Create a mock event for testing."""
    return {
        'event_type': 'test_event',
        'timestamp': datetime.now().isoformat(),
        'source': 'test_source',
        'data': {
            'key': 'value'
        }
    }

@pytest.fixture
def mock_metric():
    """Create a mock metric for testing."""
    return {
        'name': 'test_metric',
        'value': 42.0,
        'type': MetricType.GAUGE,
        'labels': {'test': 'true'},
        'timestamp': datetime.now()
    }

@pytest.fixture
def mock_health_check():
    """Create a mock health check for testing."""
    return {
        'name': 'test_service',
        'status': HealthStatus.HEALTHY,
        'message': 'Service is healthy',
        'timestamp': datetime.now(),
        'details': {'uptime': 3600}
    }

@pytest.fixture
def test_user():
    """Create a test user for authentication testing."""
    return {
        'user_id': 'test_user',
        'username': 'test',
        'permissions': [PermissionLevel.READ, PermissionLevel.WRITE],
        'email': 'test@example.com'
    }

@pytest.fixture
def test_token(security_manager, test_user):
    """Generate a test authentication token."""
    return security_manager.generate_token(test_user)

@pytest.fixture
def test_workflow_priority():
    """Get a test workflow priority."""
    return WorkflowPriority.NORMAL

@pytest.fixture
def test_circuit_state():
    """Get a test circuit breaker state."""
    return CircuitState.CLOSED 