"""Unit tests for the NodeValidator."""

import pytest
from n8n_builder.validation.validators.node import NodeValidator
from n8n_builder.validation.error_codes import ValidationErrorCode, ValidationWarningCode

def test_validate_valid_node(node_validator, basic_workflow):
    """Test validation of a valid node."""
    node = basic_workflow['nodes'][0]
    result = node_validator.validate(node, [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 0
    assert result.metadata['node_type'] == 'n8n-nodes-base.httpRequest'
    assert result.metadata['node_id'] == '1'
    assert result.metadata['has_parameters'] is True

def test_validate_invalid_input_type(node_validator):
    """Test validation with invalid input type."""
    result = node_validator.validate("not a dict", [])
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.INVALID_NODE_STRUCTURE
    assert "must be a dictionary" in result.errors[0].message

def test_validate_missing_required_fields(node_validator):
    """Test validation with missing required fields."""
    invalid_node = {
        "name": "Test Node"
    }
    
    result = node_validator.validate(invalid_node, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have errors for missing id and type

def test_validate_invalid_field_types(node_validator):
    """Test validation with invalid field types."""
    invalid_node = {
        "id": 123,  # Should be string
        "type": "n8n-nodes-base.webhook",
        "parameters": "not a dict"  # Should be dict
    }
    
    result = node_validator.validate(invalid_node, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have errors for invalid types

def test_validate_duplicate_node_ids(node_validator):
    """Test validation of nodes with duplicate IDs."""
    nodes = [
        {"id": "1", "type": "n8n-nodes-base.webhook"},
        {"id": "1", "type": "n8n-nodes-base.function"}  # Duplicate ID
    ]
    
    result = node_validator.validate(nodes)
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.DUPLICATE_NODE_ID

def test_validate_node_with_parameters(node_validator):
    """Test validation of node with parameters."""
    node_with_params = {
        "id": "test-node",
        "type": "n8n-nodes-base.function",
        "parameters": {
            "functionCode": "return $input.all();"
        }
    }
    
    result = node_validator.validate(node_with_params, [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert result.metadata['has_parameters'] is True

def test_validate_node_without_parameters(node_validator):
    """Test validation of node without parameters."""
    node_without_params = {
        "id": "test-node",
        "type": "n8n-nodes-base.webhook"
    }
    
    result = node_validator.validate(node_without_params, [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 1  # Warning for missing parameters
    assert result.warnings[0].code == ValidationWarningCode.MISSING_PARAMETERS

def test_validate_node_with_extra_fields(node_validator):
    """Test validation of node with extra fields."""
    node_with_extra = {
        "id": "test-node",
        "type": "n8n-nodes-base.webhook",
        "extra_field": "value"
    }
    
    result = node_validator.validate(node_with_extra, [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) >= 1  # Warning for extra field and missing parameters

def test_validate_node_with_position(node_validator):
    """Test validation of node with position."""
    node_with_position = {
        "id": "test-node",
        "type": "n8n-nodes-base.webhook",
        "position": [100, 200]
    }
    
    result = node_validator.validate(node_with_position, [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert result.metadata['has_position'] is True

def test_validate_node_with_invalid_position(node_validator):
    """Test validation of node with invalid position."""
    node_with_invalid_position = {
        "id": "test-node",
        "type": "n8n-nodes-base.webhook",
        "position": {"x": 100, "y": 200}  # Should be list, not dict
    }
    
    result = node_validator.validate(node_with_invalid_position, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for invalid position type 