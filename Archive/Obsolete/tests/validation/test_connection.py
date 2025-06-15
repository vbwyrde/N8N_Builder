"""Unit tests for the ConnectionValidator."""

import pytest
from n8n_builder.validation.validators.connection import ConnectionValidator
from n8n_builder.validation.error_codes import ValidationErrorCode, ValidationWarningCode

def test_validate_valid_connection(connection_validator, basic_workflow):
    """Test validation of a valid connection."""
    connection = basic_workflow['connections'][0]
    result = connection_validator.validate(connection, basic_workflow['nodes'], [])
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 0
    assert result.metadata['source_node'] == '1'
    assert result.metadata['target_node'] == '2'

def test_validate_invalid_input_type(connection_validator):
    """Test validation with invalid input type."""
    result = connection_validator.validate("not a dict", [], [])
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.INVALID_CONNECTION_STRUCTURE
    assert "must be a dictionary" in result.errors[0].message

def test_validate_missing_required_fields(connection_validator):
    """Test validation with missing required fields."""
    invalid_connection = {
        "source": "1"
    }
    
    result = connection_validator.validate(invalid_connection, [], [])
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.MISSING_REQUIRED_FIELD
    assert "target" in result.errors[0].message

def test_validate_invalid_field_types(connection_validator):
    """Test validation with invalid field types."""
    invalid_connection = {
        "source": 123,  # Should be string
        "target": "2",
        "sourceHandle": 456  # Should be string
    }
    
    result = connection_validator.validate(invalid_connection, [], [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have errors for invalid types

def test_validate_nonexistent_source_node(connection_validator):
    """Test validation of connection with nonexistent source node."""
    connection = {
        "source": "nonexistent",
        "target": "2"
    }
    nodes = [{"id": "2", "name": "Target Node"}]
    
    result = connection_validator.validate(connection, nodes, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for nonexistent source node

def test_validate_nonexistent_target_node(connection_validator):
    """Test validation of connection with nonexistent target node."""
    connection = {
        "source": "1",
        "target": "nonexistent"
    }
    nodes = [{"id": "1", "name": "Source Node"}]
    
    result = connection_validator.validate(connection, nodes, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for nonexistent target node

def test_validate_self_connection(connection_validator):
    """Test validation of connection to self."""
    connection = {
        "source": "1",
        "target": "1"
    }
    nodes = [{"id": "1", "name": "Test Node"}]
    
    result = connection_validator.validate(connection, nodes, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have error for self-connection

def test_validate_duplicate_connection(connection_validator):
    """Test validation of duplicate connections."""
    connection = {
        "source": "1",
        "target": "2",
        "sourceHandle": "output",
        "targetHandle": "input"
    }
    nodes = [
        {"id": "1", "name": "Source Node"},
        {"id": "2", "name": "Target Node"}
    ]
    existing_connections = [connection]
    
    result = connection_validator.validate(connection, nodes, existing_connections)
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.DUPLICATE_CONNECTION

def test_validate_connection_with_extra_fields(connection_validator):
    """Test validation of connection with extra fields."""
    connection_with_extra = {
        "source": "1",
        "target": "2",
        "extra_field": "value"
    }
    nodes = [
        {"id": "1", "name": "Source Node"},
        {"id": "2", "name": "Target Node"}
    ]
    
    result = connection_validator.validate(connection_with_extra, nodes, [])
    
    assert result.is_valid  # Extra fields should be warnings, not errors
    assert len(result.warnings) >= 1
    # Should have warning for extra field

def test_validate_connection_with_handles(connection_validator):
    """Test validation of connection with source and target handles."""
    connection_with_handles = {
        "source": "1",
        "target": "2",
        "sourceHandle": "output",
        "targetHandle": "input"
    }
    nodes = [
        {"id": "1", "name": "Source Node"},
        {"id": "2", "name": "Target Node"}
    ]
    
    result = connection_validator.validate(connection_with_handles, nodes, [])
    
    assert result.is_valid
    assert len(result.errors) == 0

def test_validate_connection_with_invalid_handles(connection_validator):
    """Test validation of connection with invalid handles."""
    connection_with_invalid_handles = {
        "source": "1",
        "target": "2",
        "sourceHandle": 123,  # Should be string
        "targetHandle": 456  # Should be string
    }
    nodes = [
        {"id": "1", "name": "Source Node"},
        {"id": "2", "name": "Target Node"}
    ]
    
    result = connection_validator.validate(connection_with_invalid_handles, nodes, [])
    
    assert not result.is_valid
    assert len(result.errors) >= 1
    # Should have errors for invalid handle types 