"""
Workflow structure validation for workflows.
"""
from typing import Any, Dict, List, Optional, Set
from ..validation_service import Validator, ValidationResult, ValidationError, ValidationWarning, ValidationMode
from ..error_codes import ValidationErrorCode, ValidationWarningCode, format_error_message, format_warning_message

class WorkflowStructureValidator(Validator):
    """Validates the basic structure of a workflow."""
    
    REQUIRED_FIELDS = {
        'nodes': list,
        'connections': list
    }
    
    OPTIONAL_FIELDS = {
        'name': str,
        'settings': dict,
        'version': (int, float),
        'active': bool
    }

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate the basic structure of a workflow."""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(data, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_WORKFLOW_STRUCTURE,
                message=format_error_message(
                    ValidationErrorCode.INVALID_WORKFLOW_STRUCTURE.value,
                    details="Workflow must be a dictionary"
                )
            ))
            return result

        # Validate required fields
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in data:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.MISSING_REQUIRED_FIELD,
                    message=format_error_message(
                        ValidationErrorCode.MISSING_REQUIRED_FIELD.value,
                        field=field,
                        location="workflow"
                    )
                ))
            elif not isinstance(data[field], expected_type):
                result.add_error(ValidationError(
                    code=ValidationErrorCode.INVALID_FIELD_TYPE,
                    message=format_error_message(
                        ValidationErrorCode.INVALID_FIELD_TYPE.value,
                        field=field,
                        location="workflow",
                        expected_type=expected_type.__name__,
                        actual_type=type(data[field]).__name__
                    )
                ))

        # Validate optional fields if present
        for field, expected_type in self.OPTIONAL_FIELDS.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.INVALID_FIELD_TYPE,
                        message=format_error_message(
                            ValidationErrorCode.INVALID_FIELD_TYPE.value,
                            field=field,
                            location="workflow",
                            expected_type=expected_type.__name__ if isinstance(expected_type, type) else " or ".join(t.__name__ for t in expected_type),
                            actual_type=type(data[field]).__name__
                        )
                    ))

        # Check for empty workflow
        if result.is_valid:
            if not data.get('nodes') and not data.get('connections'):
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.EMPTY_WORKFLOW,
                    message=format_warning_message(
                        ValidationWarningCode.EMPTY_WORKFLOW.value,
                        details="Workflow has no nodes or connections"
                    )
                ))

        # Check for missing optional fields
        if result.is_valid and 'settings' not in data and 'version' not in data:
            result.add_warning(ValidationWarning(
                code=ValidationWarningCode.UNUSED_FIELD,
                message=format_warning_message(
                    ValidationWarningCode.UNUSED_FIELD.value,
                    field="settings and version",
                    location="workflow"
                )
            ))

        # Check for unknown fields
        known_fields = set(self.REQUIRED_FIELDS.keys()) | set(self.OPTIONAL_FIELDS.keys())
        for field in data:
            if field not in known_fields:
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.UNKNOWN_FIELD,
                    message=format_warning_message(
                        ValidationWarningCode.UNKNOWN_FIELD.value,
                        field=field,
                        location="workflow"
                    )
                ))

        # Add metadata
        result.metadata.update({
            'node_count': len(data.get('nodes', [])),
            'connection_count': len(data.get('connections', [])),
            'has_settings': 'settings' in data,
            'has_version': 'version' in data,
            'is_active': data.get('active', False)
        })

        return result 