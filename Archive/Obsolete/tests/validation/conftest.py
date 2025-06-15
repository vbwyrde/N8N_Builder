"""
Test configuration for validation tests.
"""
import pytest
from n8n_builder.validation.validators.workflow_structure import WorkflowStructureValidator
from n8n_builder.validation.validators.node import NodeValidator
from n8n_builder.validation.validators.connection import ConnectionValidator
from n8n_builder.validation.validators.workflow_logic import WorkflowLogicValidator

@pytest.fixture
def workflow_structure_validator():
    """Create a WorkflowStructureValidator instance."""
    return WorkflowStructureValidator()

@pytest.fixture
def node_validator():
    """Create a NodeValidator instance."""
    return NodeValidator()

@pytest.fixture
def connection_validator():
    """Create a ConnectionValidator instance."""
    return ConnectionValidator()

@pytest.fixture
def workflow_logic_validator():
    """Create a WorkflowLogicValidator instance."""
    return WorkflowLogicValidator()

@pytest.fixture
def basic_workflow():
    """Create a basic valid workflow for testing."""
    return {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "Start Node",
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "url": "https://api.example.com",
                    "method": "GET"
                }
            },
            {
                "id": "2",
                "name": "End Node",
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "url": "https://api.example.com",
                    "method": "POST"
                }
            }
        ],
        "connections": [
            {
                "source": "1",
                "target": "2",
                "sourceHandle": "output",
                "targetHandle": "input"
            }
        ],
        "settings": {
            "saveExecutionProgress": True,
            "timezone": "UTC"
        },
        "version": 1
    } 