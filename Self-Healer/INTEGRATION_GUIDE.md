# Self-Healer Integration Guide

This guide provides comprehensive instructions for integrating the Self-Healer system with the existing N8N Builder infrastructure.

## Overview

The Self-Healer system is designed to integrate seamlessly with the existing N8N Builder components while maintaining system stability and safety.

## Integration Points

### 1. Error Handling Integration

The Self-Healer extends the existing `EnhancedErrorHandler`:

```python
# In n8n_builder/error_handler.py - No changes needed
# Self-Healer uses existing error categorization

# In your application code:
from Self_Healer.core.healer_manager import SelfHealerManager

# Initialize alongside existing error handler
error_handler = EnhancedErrorHandler()
healer_manager = SelfHealerManager()
```

### 2. Logging System Integration

The Self-Healer uses the existing logging infrastructure:

```python
# Uses existing loggers from n8n_builder.logging_config
# Adds specialized loggers:
# - self_healer.manager
# - self_healer.error_monitor
# - self_healer.context_analyzer
# - self_healer.solution_generator
# - self_healer.solution_validator
# - self_healer.learning_engine
```

### 3. Project Manager Integration

Coordinates with existing project management:

```python
# Self-Healer uses existing project_manager for:
# - Safe file operations
# - Backup management
# - Project integrity maintenance
```

## Installation Steps

### 1. Install Dependencies

```bash
# Install additional dependencies for Self-Healer
pip install watchdog pyyaml psutil fastapi uvicorn websockets
```

### 2. Configure System

```bash
# Copy configuration template
cp Self-Healer/config/healer_config.yaml.template Self-Healer/config/healer_config.yaml

# Edit configuration as needed
nano Self-Healer/config/healer_config.yaml
```

### 3. Initialize Directories

```bash
# Create required directories
mkdir -p Self-Healer/backups
mkdir -p Self-Healer/learning_data
mkdir -p Self-Healer/logs
```

### 4. Update Main Application

Add Self-Healer to your main application:

```python
# In your main application file (e.g., run.py or app.py)
import asyncio
from Self_Healer.core.healer_manager import SelfHealerManager
from Self_Healer.dashboard.dashboard import run_dashboard

async def main():
    # Initialize existing N8N Builder components
    # ... existing initialization code ...
    
    # Initialize Self-Healer
    healer = SelfHealerManager()
    
    try:
        # Start Self-Healer
        await healer.start()
        
        # Optionally start dashboard
        dashboard_task = asyncio.create_task(run_dashboard(healer, port=8081))
        
        # Run your main application
        # ... existing application code ...
        
    finally:
        # Ensure proper shutdown
        await healer.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

### Basic Configuration

Edit `Self-Healer/config/healer_config.yaml`:

```yaml
# Essential settings for integration
monitoring:
  check_interval: 5.0
  max_concurrent_sessions: 3

safety:
  require_validation: true
  auto_rollback_on_failure: true
  max_healing_attempts_per_hour: 10

learning:
  enable_learning: true
  feedback_collection: true
```

### Advanced Configuration

For production environments:

```yaml
# Production settings
safety:
  max_file_changes: 5  # Reduced for safety
  emergency_stop_threshold: 3  # Lower threshold

validation:
  require_backup: true
  require_tests: true
  max_implementation_time: 180  # 3 minutes max

logging:
  level: "INFO"
  file_rotation: true
```

## Testing Integration

### 1. Unit Tests

Create tests for Self-Healer components:

```python
# tests/test_self_healer_integration.py
import pytest
import asyncio
from Self_Healer.core.healer_manager import SelfHealerManager
from n8n_builder.error_handler import ErrorDetail, ErrorCategory, ErrorSeverity

@pytest.mark.asyncio
async def test_healer_initialization():
    """Test Self-Healer initializes correctly."""
    healer = SelfHealerManager()
    
    try:
        await healer.start()
        status = await healer.get_status()
        assert status['is_running'] == True
    finally:
        await healer.stop()

@pytest.mark.asyncio
async def test_error_detection_integration():
    """Test error detection works with existing error handler."""
    healer = SelfHealerManager()
    
    try:
        await healer.start()
        
        # Create test error
        error = ErrorDetail(
            category=ErrorCategory.LLM_COMMUNICATION,
            severity=ErrorSeverity.ERROR,
            title="Test Error",
            message="Test error message",
            user_guidance="Test guidance"
        )
        
        # Test context analysis
        context = await healer.context_analyzer.analyze_error(error)
        assert 'error_category' in context
        
    finally:
        await healer.stop()
```

### 2. Integration Tests

Test with existing N8N Builder components:

```python
# tests/test_full_integration.py
import pytest
from n8n_builder.n8n_builder import N8NBuilder
from Self_Healer.core.healer_manager import SelfHealerManager

@pytest.mark.asyncio
async def test_full_system_integration():
    """Test Self-Healer works with full N8N Builder system."""
    # Initialize both systems
    n8n_builder = N8NBuilder()
    healer = SelfHealerManager()
    
    try:
        await healer.start()
        
        # Test that both systems can coexist
        # ... integration test code ...
        
    finally:
        await healer.stop()
```

### 3. Safety Tests

Test safety mechanisms:

```python
@pytest.mark.asyncio
async def test_safety_mechanisms():
    """Test safety mechanisms prevent harmful operations."""
    healer = SelfHealerManager()
    
    try:
        await healer.start()
        
        # Test emergency stop
        await healer.emergency_stop()
        status = await healer.get_status()
        assert status['is_running'] == False
        
    finally:
        await healer.stop()
```

## Monitoring Integration

### 1. Existing Monitoring

The Self-Healer integrates with existing monitoring:

```python
# Uses existing performance_optimizer for metrics
# Extends existing logging for specialized tracking
# Coordinates with existing retry_manager
```

### 2. Dashboard Integration

Access the Self-Healer dashboard:

```bash
# Start dashboard (if enabled in config)
# Access at: http://localhost:8081
```

### 3. Metrics Integration

Self-Healer metrics are available through:

```python
# Get comprehensive status
status = await healer.get_status()

# Get learning statistics
learning_stats = healer.learning_engine.get_learning_statistics()

# Get error monitoring statistics
error_stats = healer.error_monitor.get_error_statistics()
```

## Production Deployment

### 1. Environment Setup

```bash
# Production environment variables
export SELF_HEALER_CONFIG_PATH="/path/to/production/config.yaml"
export SELF_HEALER_LOG_LEVEL="INFO"
export SELF_HEALER_BACKUP_DIR="/secure/backup/location"
```

### 2. Security Considerations

- Ensure backup directory has proper permissions
- Limit file modification permissions
- Monitor Self-Healer logs for security events
- Regular review of healing activities

### 3. Performance Considerations

- Monitor memory usage (learning data can grow)
- Configure appropriate cache sizes
- Set reasonable healing attempt limits
- Regular cleanup of old data

## Troubleshooting Integration

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure Python path includes project root
   export PYTHONPATH="${PYTHONPATH}:/path/to/N8N_Builder"
   ```

2. **Permission Errors**
   ```bash
   # Check backup directory permissions
   chmod 755 Self-Healer/backups
   ```

3. **Configuration Issues**
   ```bash
   # Validate configuration
   python -c "import yaml; yaml.safe_load(open('Self-Healer/config/healer_config.yaml'))"
   ```

### Debugging

Enable debug logging:

```yaml
# In healer_config.yaml
logging:
  level: "DEBUG"
```

Check integration logs:

```bash
# Monitor Self-Healer logs
tail -f logs/n8n_builder.log | grep self_healer

# Check for integration issues
grep -i "self_healer" logs/errors.log
```

## Rollback Plan

If integration issues occur:

1. **Immediate Rollback**
   ```python
   # Emergency stop Self-Healer
   await healer.emergency_stop()
   ```

2. **Disable Auto-Start**
   ```python
   # Comment out Self-Healer initialization in main app
   # healer = SelfHealerManager()
   # await healer.start()
   ```

3. **Restore Backups**
   ```bash
   # Restore from Self-Healer backups if needed
   # Backups are stored in Self-Healer/backups/
   ```

## Validation Checklist

Before deploying to production:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Safety mechanisms tested
- [ ] Configuration validated
- [ ] Backup/restore tested
- [ ] Performance impact assessed
- [ ] Security review completed
- [ ] Monitoring configured
- [ ] Rollback plan tested
- [ ] Documentation updated

## Support and Maintenance

### Regular Maintenance

- Monitor learning data growth
- Review healing success rates
- Update solution templates
- Clean old backup files
- Review and update patterns

### Performance Monitoring

- Memory usage trends
- Healing response times
- Error detection accuracy
- Solution success rates
- System stability impact

### Updates and Improvements

- Regular pattern analysis
- Solution template updates
- Configuration optimization
- Performance tuning
- Feature enhancements

## Conclusion

The Self-Healer system is designed to integrate seamlessly with the existing N8N Builder infrastructure while providing powerful automatic healing capabilities. Follow this guide carefully to ensure a smooth integration process and optimal system performance.
