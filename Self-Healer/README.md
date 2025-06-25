# Self-Healer System

A comprehensive self-healing and self-improving system for the N8N Builder workflow automation platform. The Self-Healer automatically detects, analyzes, and resolves issues while learning from each healing attempt to improve future performance.

## Overview

The Self-Healer system provides:

- **Automatic Error Detection**: Monitors log files and system state for issues
- **Intelligent Analysis**: Gathers comprehensive context using documentation and code analysis
- **Solution Generation**: Creates targeted solutions using local LLM and pattern recognition
- **Safe Implementation**: Validates and safely implements solutions with rollback capabilities
- **Continuous Learning**: Learns from successful and failed healing attempts

## Architecture

### Core Components

1. **Error Monitor** (`core/error_monitor.py`)
   - Real-time log file monitoring
   - Error classification and deduplication
   - Pattern recognition for recurring issues

2. **Context Analyzer** (`core/context_analyzer.py`)
   - Documentation retrieval from structured docs
   - Code context gathering using codebase analysis
   - System state assessment and dependency mapping

3. **Solution Generator** (`core/solution_generator.py`)
   - Local LLM integration for intelligent solutions
   - Pattern-based solutions for common errors
   - Multi-strategy approach with risk assessment

4. **Solution Validator** (`core/solution_validator.py`)
   - Comprehensive safety validation
   - Isolated testing environment
   - Automatic rollback capabilities

5. **Learning Engine** (`core/learning_engine.py`)
   - Pattern recognition and learning
   - Success/failure analysis
   - Continuous improvement insights

6. **Healer Manager** (`core/healer_manager.py`)
   - Main orchestrator coordinating all components
   - Session management and monitoring
   - Metrics collection and reporting

## Installation

### Prerequisites

- Python 3.8+
- N8N Builder system
- Local LLM service (LM Studio with mimo-vl-7b-rl model)
- Required Python packages (see requirements.txt)

### Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install watchdog pyyaml psutil
   ```

2. **Configure System**
   ```bash
   # Copy and customize configuration
   cp Self-Healer/config/healer_config.yaml.template Self-Healer/config/healer_config.yaml
   # Edit configuration as needed
   ```

3. **Initialize Directories**
   ```bash
   mkdir -p Self-Healer/backups
   mkdir -p Self-Healer/learning_data
   ```

## Usage

### Starting the Self-Healer

```python
from Self_Healer import SelfHealerManager

# Initialize and start the self-healer
healer = SelfHealerManager()
await healer.start()

# The system will now automatically monitor and heal issues
```

### Manual Healing Session

```python
# Trigger manual healing for a specific error
error_detail = ErrorDetail(...)
context = await healer.context_analyzer.analyze_error(error_detail)
solutions = await healer.solution_generator.generate_solutions(error_detail, context)

# Validate and implement best solution
best_solution = solutions[0]
validation = await healer.solution_validator.validate_solution(best_solution, context)

if validation['can_proceed']:
    result = await healer.solution_validator.implement_solution(best_solution, context)
```

### Monitoring Status

```python
# Get system status
status = await healer.get_status()
print(f"Status: {status['status']}")
print(f"Active Sessions: {status['active_sessions']}")
print(f"Success Rate: {status['metrics']['success_rate']:.1f}%")

# Get learning statistics
learning_stats = healer.learning_engine.get_learning_statistics()
print(f"Total Patterns: {learning_stats['total_patterns']}")
print(f"Success Rate: {learning_stats['overall_success_rate']:.1f}%")
```

## Configuration

The system is configured through `config/healer_config.yaml`:

### Key Configuration Sections

- **Monitoring**: Error detection and session management
- **Safety**: Validation requirements and safety limits
- **Learning**: Pattern recognition and improvement settings
- **Validation**: Solution testing and verification
- **Integration**: Integration with existing N8N Builder components

### Safety Features

- **Rate Limiting**: Maximum healing attempts per hour
- **Validation Requirements**: Mandatory solution validation
- **Automatic Rollback**: Rollback on implementation failure
- **Emergency Stop**: Automatic shutdown on consecutive failures
- **File Change Limits**: Maximum files that can be modified

## Integration with N8N Builder

The Self-Healer integrates seamlessly with existing N8N Builder components:

- **Error Handler**: Extends existing error categorization
- **Logging System**: Uses existing logging infrastructure
- **Project Manager**: Coordinates with file operations
- **Performance Optimizer**: Integrates with performance monitoring
- **Documentation**: Leverages structured documentation for context

## Learning and Improvement

### Pattern Recognition

The system learns patterns from:
- Error types and their successful solutions
- Context factors that influence solution effectiveness
- System states that predict certain error types
- Solution approaches that work best for specific scenarios

### Continuous Improvement

- **Success Tracking**: Records effectiveness of all solutions
- **Pattern Evolution**: Updates patterns based on new data
- **Insight Generation**: Provides actionable insights for system improvement
- **Predictive Capabilities**: Develops proactive healing strategies

## Safety and Reliability

### Safety Measures

- **Comprehensive Validation**: Multi-layer solution validation
- **Rollback Points**: Automatic backup before changes
- **Impact Assessment**: Analysis of potential side effects
- **Gradual Implementation**: Phased deployment with monitoring
- **Emergency Controls**: Manual override and emergency stop

### Reliability Features

- **Error Recovery**: Graceful handling of system errors
- **State Persistence**: Maintains state across restarts
- **Resource Management**: Efficient memory and CPU usage
- **Monitoring**: Comprehensive system health monitoring

## Monitoring and Metrics

### Key Metrics

- **Error Detection Rate**: Errors detected vs. actual errors
- **Solution Success Rate**: Successful implementations vs. attempts
- **Healing Time**: Average time from detection to resolution
- **System Stability**: Overall system health improvements
- **Learning Effectiveness**: Pattern recognition accuracy

### Dashboard (Future Enhancement)

- Real-time healing activity monitor
- Historical trends and patterns
- System health overview
- Performance impact assessment

## Troubleshooting

### Common Issues

1. **LLM Connection Failures**
   - Verify LM Studio is running
   - Check model is loaded (mimo-vl-7b-rl)
   - Validate endpoint configuration

2. **Permission Errors**
   - Ensure proper file permissions
   - Check backup directory access
   - Verify log file write permissions

3. **High Memory Usage**
   - Adjust `max_records_in_memory` setting
   - Enable record archiving
   - Monitor learning data size

### Debugging

Enable debug logging:
```yaml
logging:
  level: "DEBUG"
```

Check system logs:
```bash
tail -f logs/n8n_builder.log | grep self_healer
```

## Future Enhancements

### Planned Features

- **Distributed Healing**: Multi-instance coordination
- **Advanced ML Models**: Enhanced pattern recognition
- **External Integration**: Integration with monitoring systems
- **Automated Documentation**: Self-updating documentation
- **Predictive Maintenance**: Proactive issue prevention

### Contributing

The Self-Healer system is designed to be extensible:

1. **Custom Solution Templates**: Add domain-specific solutions
2. **Enhanced Pattern Recognition**: Improve learning algorithms
3. **Additional Integrations**: Connect with external systems
4. **Advanced Validation**: Implement specialized validators

## License

This Self-Healer system is part of the N8N Builder project and follows the same licensing terms.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review system logs for error details
3. Consult the N8N Builder documentation
4. Report issues through the project's issue tracking system
