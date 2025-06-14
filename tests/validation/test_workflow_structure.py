"""Unit tests for the WorkflowStructureValidator."""

import pytest
from n8n_builder.validation.validators.workflow_structure import WorkflowStructureValidator
from n8n_builder.validation.error_codes import ValidationErrorCode, ValidationWarningCode

def test_validate_valid_workflow(workflow_structure_validator, basic_workflow):
    """Test validation of a valid workflow."""
    result = workflow_structure_validator.validate(basic_workflow)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 0
    assert result.metadata['node_count'] == 2
    assert result.metadata['connection_count'] == 1
    assert result.metadata['has_settings'] is True
    assert result.metadata['has_version'] is True

def test_validate_invalid_input_type(workflow_structure_validator):
    """Test validation with invalid input type."""
    result = workflow_structure_validator.validate("not a dict")
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.INVALID_WORKFLOW_STRUCTURE
    assert "must be a dictionary" in result.errors[0].message

def test_validate_missing_required_fields(workflow_structure_validator):
    """Test validation with missing required fields."""
    invalid_workflow = {
        "name": "Test Workflow",
        "nodes": []
    }
    
    result = workflow_structure_validator.validate(invalid_workflow)
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.MISSING_REQUIRED_FIELD
    assert "connections" in result.errors[0].message

def test_validate_invalid_field_types(workflow_structure_validator):
    """Test validation with invalid field types."""
    invalid_workflow = {
        "name": "Test Workflow",
        "nodes": "not a list",
        "connections": []
    }
    
    result = workflow_structure_validator.validate(invalid_workflow)
    
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == ValidationErrorCode.INVALID_FIELD_TYPE
    assert "nodes" in result.errors[0].message

def test_validate_empty_workflow(workflow_structure_validator):
    """Test validation of an empty workflow."""
    empty_workflow = {
        "name": "Empty Workflow",
        "nodes": [],
        "connections": []
    }
    
    result = workflow_structure_validator.validate(empty_workflow)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 2  # Empty workflow + missing optional fields
    assert result.warnings[0].code == ValidationWarningCode.EMPTY_WORKFLOW
    assert result.warnings[1].code == ValidationWarningCode.UNUSED_FIELD
    assert result.metadata['node_count'] == 0
    assert result.metadata['connection_count'] == 0

def test_validate_missing_optional_fields(workflow_structure_validator):
    """Test validation with missing optional fields."""
    minimal_workflow = {
        "name": "Minimal Workflow",
        "nodes": [],
        "connections": []
    }
    
    result = workflow_structure_validator.validate(minimal_workflow)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 2  # Empty workflow + missing optional fields
    assert result.metadata['has_settings'] is False
    assert result.metadata['has_version'] is False

def test_validate_workflow_with_settings(workflow_structure_validator):
    """Test validation of workflow with settings."""
    workflow_with_settings = {
        "name": "Workflow with Settings",
        "nodes": [],
        "connections": [],
        "settings": {
            "saveExecutionProgress": True,
            "timezone": "UTC"
        }
    }
    
    result = workflow_structure_validator.validate(workflow_with_settings)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert result.metadata['has_settings'] is True

def test_validate_workflow_with_version(workflow_structure_validator):
    """Test validation of workflow with version."""
    workflow_with_version = {
        "name": "Workflow with Version",
        "nodes": [],
        "connections": [],
        "version": 1
    }
    
    result = workflow_structure_validator.validate(workflow_with_version)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert result.metadata['has_version'] is True

def test_validate_workflow_with_extra_fields(workflow_structure_validator):
    """Test validation of workflow with extra fields."""
    workflow_with_extra = {
        "name": "Workflow with Extra Fields",
        "nodes": [],
        "connections": [],
        "extra_field": "value"
    }
    
    result = workflow_structure_validator.validate(workflow_with_extra)
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert len(result.warnings) == 3  # Empty workflow + missing optional fields + extra field
    assert result.warnings[0].code == ValidationWarningCode.EMPTY_WORKFLOW
    assert result.warnings[1].code == ValidationWarningCode.UNUSED_FIELD
    assert result.warnings[2].code == ValidationWarningCode.UNKNOWN_FIELD
    assert "extra_field" in result.warnings[2].message 