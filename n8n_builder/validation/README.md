# N8N Builder Validation System

The validation system provides a robust framework for validating N8N workflows. It ensures that workflows are structurally sound, logically valid, and follow best practices.

## Features

- **Comprehensive Validation**: Validates workflow structure, nodes, connections, and logic
- **Detailed Error Reporting**: Provides clear error messages and warnings
- **Extensible Design**: Easy to add new validation rules and checks
- **Configurable Validation**: Supports different validation modes and custom rules
- **Rich Metadata**: Collects detailed information about the workflow

## Components

### Validators

1. **WorkflowStructureValidator**
   - Validates the basic structure of workflows
   - Checks required and optional fields
   - Ensures proper data types
   - Provides workflow-level metadata

2. **NodeValidator**
   - Validates individual nodes
   - Checks node structure and fields
   - Validates node types and parameters
   - Detects duplicate node IDs

3. **ConnectionValidator**
   - Validates connections between nodes
   - Checks connection structure and fields
   - Validates node references
   - Detects cycles in the workflow

4. **WorkflowLogicValidator**
   - Validates the logical structure of workflows
   - Checks for isolated nodes
   - Validates node type compatibility
   - Ensures workflow completeness

### Error Codes

The system uses a standardized set of error and warning codes:

- **Structure Errors**: Invalid workflow structure, missing fields, etc.
- **Node Errors**: Invalid node structure, types, parameters, etc.
- **Connection Errors**: Invalid connections, references, cycles, etc.
- **Logic Errors**: Incompatible node types, missing start/end nodes, etc.

## Usage

### Basic Usage

```python
from n8n_builder.validation import ValidationService
from n8n_builder.validation.config import DEFAULT_CONFIG

# Create a validation service
validator = ValidationService(config=DEFAULT_CONFIG)

# Validate a workflow
result = validator.validate_workflow(workflow_data)

# Check validation results
if result.is_valid:
    print("Workflow is valid")
else:
    print("Validation errors:")
    for error in result.errors:
        print(f"- {error.message}")
```

### Custom Configuration

```python
from n8n_builder.validation import ValidationService
from n8n_builder.validation.config import ValidationConfig, ValidationMode

# Create a custom configuration
config = ValidationConfig(
    mode=ValidationMode.STRICT,
    enabled_validators=['WorkflowStructureValidator', 'NodeValidator'],
    max_errors=10,
    max_warnings=20
)

# Create a validation service with custom configuration
validator = ValidationService(config=config)
```

### Adding Custom Rules

```python
from n8n_builder.validation import ValidationService
from n8n_builder.validation.config import ValidationConfig

# Create a custom rule
def custom_node_rule(node):
    # Custom validation logic
    return True

# Add the rule to the configuration
config = ValidationConfig()
config.add_custom_rule('node', custom_node_rule)

# Create a validation service with the custom rule
validator = ValidationService(config=config)
```

## Best Practices

1. **Use Appropriate Validation Mode**
   - Use `STRICT` mode for critical validations
   - Use `LENIENT` mode for development and testing

2. **Handle Validation Results**
   - Always check `is_valid` before proceeding
   - Review both errors and warnings
   - Use metadata for additional insights

3. **Custom Rules**
   - Keep custom rules focused and specific
   - Document rule requirements and behavior
   - Test rules thoroughly

4. **Error Handling**
   - Use appropriate error codes
   - Provide clear error messages
   - Include relevant context in errors

## Contributing

When adding new validation rules or features:

1. Follow the existing code structure
2. Add appropriate tests
3. Update documentation
4. Use standard error codes
5. Include metadata where relevant

## Testing

Run the validation tests:

```bash
pytest tests/validation/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 