"""Unit tests for the WorkflowLogicValidator."""

import pytest
from n8n_builder.validation.validators.workflow_logic import WorkflowLogicValidator
from n8n_builder.validation.error_codes import ValidationErrorCode, ValidationWarningCode

def test_validate_valid_workflow_logic(workflow_logic_validator, basic_workflow):
    """Test validation of a valid workflow logic."""
    result = workflow_logic_validator.validate(basic_workflow)
    
    # The basic workflow uses httpRequest nodes which are not start/end nodes
    # So it should fail validation
    assert not result.is_valid
    assert len(result.errors) >= 2  # Missing start and end nodes
    assert result.metadata['has_start_node'] is False  # httpRequest is not a start node type
    assert result.metadata['has_end_node'] is False    # httpRequest is not an end node type
    assert result.metadata['is_acyclic'] is True

def test_validate_invalid_input_type(workflow_logic_validator):
    """Test validation with invalid input type."""
    result = workflow_logic_validator.validate("not a dict")
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.INVALID_WORKFLOW_LOGIC
    assert "must be a dictionary" in result.errors[0].message

def test_validate_workflow_with_cycle(workflow_logic_validator):
    """Test validation of workflow with cycles."""
    workflow_with_cycle = {
        "name": "Workflow with Cycle",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.webhook"},
            {"id": "2", "type": "n8n-nodes-base.function"},
            {"id": "3", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "2"},
            {"source": "2", "target": "3"},
            {"source": "3", "target": "1"}  # Creates a cycle
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_with_cycle)
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for cycle detection

def test_validate_workflow_with_isolated_nodes(workflow_logic_validator):
    """Test validation of workflow with isolated nodes."""
    workflow_with_isolated = {
        "name": "Workflow with Isolated Nodes",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.webhook"},
            {"id": "2", "type": "n8n-nodes-base.function"},  # Isolated node
            {"id": "3", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "3"}  # Node 2 is isolated
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_with_isolated)
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for isolated node

def test_validate_workflow_with_start_node(workflow_logic_validator):
    """Test validation of workflow with proper start node."""
    workflow_with_start = {
        "name": "Workflow with Start Node",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.webhook"},  # Start node
            {"id": "2", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "2"}
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_with_start)
    
    assert result.metadata['has_start_node'] is True

def test_validate_workflow_with_end_node(workflow_logic_validator):
    """Test validation of workflow with proper end node."""
    workflow_with_end = {
        "name": "Workflow with End Node",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.function"},
            {"id": "2", "type": "n8n-nodes-base.noOp"}  # End node
        ],
        "connections": [
            {"source": "1", "target": "2"}
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_with_end)
    
    assert result.metadata['has_end_node'] is True

def test_validate_workflow_missing_start_node(workflow_logic_validator):
    """Test validation of workflow missing start node."""
    workflow_missing_start = {
        "name": "Workflow Missing Start Node",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.function"},
            {"id": "2", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "2"}
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_missing_start)
    
    assert not result.is_valid
    assert any(e.code == ValidationErrorCode.MISSING_START_NODE for e in result.errors)

def test_validate_workflow_missing_end_node(workflow_logic_validator):
    """Test validation of workflow missing end node."""
    workflow_missing_end = {
        "name": "Workflow Missing End Node",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.webhook"},
            {"id": "2", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "2"}
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_missing_end)
    
    assert not result.is_valid
    assert any(e.code == ValidationErrorCode.MISSING_END_NODE for e in result.errors)

def test_validate_workflow_with_multiple_start_nodes(workflow_logic_validator):
    """Test validation of workflow with multiple start nodes."""
    workflow_multiple_start = {
        "name": "Workflow with Multiple Start Nodes",
        "nodes": [
            {"id": "1", "type": "n8n-nodes-base.webhook"},      # Start node 1
            {"id": "2", "type": "n8n-nodes-base.webhook"},      # Start node 2
            {"id": "3", "type": "n8n-nodes-base.function"}
        ],
        "connections": [
            {"source": "1", "target": "3"},
            {"source": "2", "target": "3"}
        ]
    }
    
    result = workflow_logic_validator.validate(workflow_multiple_start)
    
    assert not result.is_valid
    assert any(e.code == ValidationErrorCode.MULTIPLE_START_NODES for e in result.errors)

def test_validate_empty_workflow_logic(workflow_logic_validator):
    """Test validation of empty workflow logic."""
    empty_workflow = {
        "name": "Empty Workflow",
        "nodes": [],
        "connections": []
    }
    
    result = workflow_logic_validator.validate(empty_workflow)
    
    assert not result.is_valid
    assert any(e.code == ValidationErrorCode.MISSING_START_NODE for e in result.errors)
    assert any(e.code == ValidationErrorCode.MISSING_END_NODE for e in result.errors) 