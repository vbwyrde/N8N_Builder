"""
Configuration for the validation system.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from .validation_service import ValidationMode

@dataclass
class ValidationConfig:
    """Configuration for the validation system."""
    mode: ValidationMode = ValidationMode.STRICT
    enabled_validators: Set[str] = field(default_factory=set)
    disabled_validators: Set[str] = field(default_factory=set)
    custom_rules: Dict[str, Dict] = field(default_factory=dict)
    max_errors: Optional[int] = None
    max_warnings: Optional[int] = None
    log_level: str = "INFO"
    validation_timeout: float = 30.0  # seconds
    
    def __post_init__(self):
        """Initialize default enabled validators if none specified."""
        if not self.enabled_validators:
            self.enabled_validators = {
                "WorkflowStructureValidator",
                "NodeValidator",
                "ConnectionValidator",
                "WorkflowLogicValidator"
            }
    
    def is_validator_enabled(self, validator_name: str) -> bool:
        """Check if a validator is enabled."""
        if validator_name in self.disabled_validators:
            return False
        if not self.enabled_validators:
            return True
        return validator_name in self.enabled_validators
    
    def get_custom_rule(self, rule_name: str) -> Optional[Dict]:
        """Get a custom validation rule."""
        return self.custom_rules.get(rule_name)
    
    def add_custom_rule(self, rule_name: str, rule_config: Dict) -> None:
        """Add a custom validation rule."""
        self.custom_rules[rule_name] = rule_config
    
    def remove_custom_rule(self, rule_name: str) -> None:
        """Remove a custom validation rule."""
        self.custom_rules.pop(rule_name, None)
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {
            'mode': self.mode.value,
            'enabled_validators': list(self.enabled_validators),
            'disabled_validators': list(self.disabled_validators),
            'custom_rules': self.custom_rules,
            'max_errors': self.max_errors,
            'max_warnings': self.max_warnings,
            'log_level': self.log_level,
            'validation_timeout': self.validation_timeout
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'ValidationConfig':
        """Create configuration from dictionary."""
        return cls(
            mode=ValidationMode(config_dict.get('mode', ValidationMode.STRICT.value)),
            enabled_validators=set(config_dict.get('enabled_validators', [])),
            disabled_validators=set(config_dict.get('disabled_validators', [])),
            custom_rules=config_dict.get('custom_rules', {}),
            max_errors=config_dict.get('max_errors'),
            max_warnings=config_dict.get('max_warnings'),
            log_level=config_dict.get('log_level', 'INFO'),
            validation_timeout=config_dict.get('validation_timeout', 30.0)
        )

# Default configuration
DEFAULT_CONFIG = ValidationConfig(
    mode=ValidationMode.STRICT,
    enabled_validators={
        "WorkflowStructureValidator",
        "NodeValidator",
        "ConnectionValidator",
        "WorkflowLogicValidator"
    },
    log_level="INFO",
    validation_timeout=30.0
)

# Debug configuration
DEBUG_CONFIG = ValidationConfig(
    mode=ValidationMode.DEBUG,
    enabled_validators={
        "WorkflowStructureValidator",
        "NodeValidator",
        "ConnectionValidator",
        "WorkflowLogicValidator"
    },
    log_level="DEBUG",
    validation_timeout=60.0
)

# Lenient configuration
LENIENT_CONFIG = ValidationConfig(
    mode=ValidationMode.LENIENT,
    enabled_validators={
        "WorkflowStructureValidator",
        "NodeValidator",
        "ConnectionValidator"
    },
    log_level="WARNING",
    validation_timeout=30.0
) 