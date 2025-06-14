"""
Core validation service for N8N Builder.
Provides centralized validation logic and error handling.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type
import logging
from datetime import datetime

# Configure validation logger
validation_logger = logging.getLogger('n8n_builder.validation')

class ValidationMode(Enum):
    """Validation modes for different levels of strictness."""
    STRICT = "strict"  # All validations must pass
    LENIENT = "lenient"  # Some validations can be warnings
    DEBUG = "debug"  # Additional validation for debugging

class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"

@dataclass
class ValidationIssue:
    """Base class for validation issues (errors and warnings)."""
    code: Any  # Can be string or enum
    message: str
    severity: ValidationSeverity
    location: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        code_str = self.code.value if hasattr(self.code, 'value') else str(self.code)
        return f"[{self.severity.value}] {code_str}: {self.message}"

@dataclass
class ValidationError(ValidationIssue):
    """Validation error with error-specific properties."""
    severity: ValidationSeverity = ValidationSeverity.ERROR

@dataclass
class ValidationWarning(ValidationIssue):
    """Validation warning with warning-specific properties."""
    severity: ValidationSeverity = ValidationSeverity.WARNING

@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationWarning] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_time: float = 0.0

    def add_error(self, error: ValidationError) -> None:
        """Add an error to the result."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: ValidationWarning) -> None:
        """Add a warning to the result."""
        self.warnings.append(warning)

    def has_errors(self) -> bool:
        """Check if the result has any errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if the result has any warnings."""
        return len(self.warnings) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary."""
        return {
            'is_valid': self.is_valid,
            'errors': [str(error) for error in self.errors],
            'warnings': [str(warning) for warning in self.warnings],
            'metadata': self.metadata,
            'validation_time': self.validation_time
        }

class Validator:
    """Base class for all validators."""
    def __init__(self, mode: ValidationMode = ValidationMode.STRICT):
        self.mode = mode
        self.logger = validation_logger

    def validate(self, data: Any) -> ValidationResult:
        """Validate the given data."""
        raise NotImplementedError("Subclasses must implement validate()")

class ValidationChain:
    """Chain of validators to be executed in sequence."""
    def __init__(self, mode: ValidationMode = ValidationMode.STRICT):
        self.validators: List[Validator] = []
        self.mode = mode
        self.logger = validation_logger

    def add_validator(self, validator: Validator) -> None:
        """Add a validator to the chain."""
        self.validators.append(validator)

    def validate(self, data: Any) -> ValidationResult:
        """Execute all validators in the chain."""
        result = ValidationResult(is_valid=True)
        start_time = datetime.now()

        for validator in self.validators:
            try:
                validator_result = validator.validate(data)
                result.errors.extend(validator_result.errors)
                result.warnings.extend(validator_result.warnings)
                result.metadata.update(validator_result.metadata)
                
                if validator_result.has_errors():
                    result.is_valid = False
                    if self.mode == ValidationMode.STRICT:
                        break
            except Exception as e:
                self.logger.error(f"Validator {validator.__class__.__name__} failed: {str(e)}")
                result.add_error(ValidationError(
                    code="VALIDATOR_ERROR",
                    message=f"Validator failed: {str(e)}",
                    details={'validator': validator.__class__.__name__}
                ))
                result.is_valid = False
                if self.mode == ValidationMode.STRICT:
                    break

        result.validation_time = (datetime.now() - start_time).total_seconds()
        return result

class ValidationService:
    """Central service for workflow validation."""
    def __init__(self, mode: ValidationMode = ValidationMode.STRICT):
        self.mode = mode
        self.chain = ValidationChain(mode)
        self.logger = validation_logger
        self._setup_default_validators()

    def _setup_default_validators(self) -> None:
        """Set up the default validation chain."""
        # Add validators in the order they should be executed
        self.chain.add_validator(WorkflowStructureValidator())
        self.chain.add_validator(NodeValidator())
        self.chain.add_validator(ConnectionValidator())
        self.chain.add_validator(WorkflowLogicValidator())

    def validate_workflow(self, workflow: Dict[str, Any]) -> ValidationResult:
        """Validate a complete workflow."""
        self.logger.info(f"Validating workflow with {len(workflow.get('nodes', []))} nodes")
        return self.chain.validate(workflow)

    def validate_connections(self, workflow: Dict[str, Any]) -> ValidationResult:
        """Validate only the connections in a workflow."""
        self.logger.info("Validating workflow connections")
        return ConnectionValidator().validate(workflow)

    def validate_nodes(self, workflow: Dict[str, Any]) -> ValidationResult:
        """Validate only the nodes in a workflow."""
        self.logger.info(f"Validating {len(workflow.get('nodes', []))} nodes")
        return NodeValidator().validate(workflow)

# Placeholder for validator implementations
class WorkflowStructureValidator(Validator):
    """Validates the basic structure of a workflow."""
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Implementation will be added in Phase 2
        return result

class NodeValidator(Validator):
    """Validates individual nodes in a workflow."""
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Implementation will be added in Phase 2
        return result

class ConnectionValidator(Validator):
    """Validates connections between nodes."""
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Implementation will be added in Phase 2
        return result

class WorkflowLogicValidator(Validator):
    """Validates the logical flow of the workflow."""
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        # Implementation will be added in Phase 2
        return result 