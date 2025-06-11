# N8N Workflow Builder - Complete Documentation

## 🎯 What is N8N Builder?

N8N Builder is an intelligent workflow automation tool that translates plain English descriptions into executable N8N workflows. Think of it as a "conversation-to-code" translator for workflow automation - you describe what you want to happen, and it creates the technical blueprint to make it happen.

### 🌟 Why Use N8N Builder?

**For Beginners:**
- No need to learn complex workflow syntax
- Just describe what you want in plain English
- Get instant, working automation workflows
- Perfect for business users who want to automate tasks without technical knowledge

**For Developers:**
- Rapid prototyping of automation workflows
- AI-powered code generation with validation
- REST API for integration into larger systems
- Extensible architecture for custom workflow patterns

---

## 🚀 Quick Start Guide

### What You'll Need
- Python 3.8 or higher
- A local AI model (Mimo VL 7B) or access to an LLM API
- Basic understanding of what workflows do (optional but helpful)

### Getting Started in 3 Steps

1. **Install and Setup**
   ```bash
   git clone <your-repo-url>
   cd N8N_Builder
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python -m n8n_builder.cli serve
   ```

3. **Create Your First Workflow**
   - Open your browser to `http://localhost:8000`
   - Type: "Send me an email when a new file is uploaded to my folder"
   - Click "Generate Workflow"
   - Copy the generated JSON to your N8N instance

### Example Use Cases
- **File Monitoring**: "Alert me when files are added to a specific folder"
- **Data Processing**: "Convert CSV files to JSON and send to a webhook"
- **Social Media**: "Post to Twitter when I publish a new blog article"
- **E-commerce**: "Send customer welcome emails after purchase"
- **System Monitoring**: "Check website status every 5 minutes and alert if down"

---

## 🏗️ Technical Architecture

### System Overview

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Web UI<br/>index.html]
        CLI[Command Line<br/>Interface]
        API[REST API<br/>FastAPI]
    end
    
    subgraph "Core Processing Layer"
        Builder[N8N Builder<br/>Core Engine]
        Validator[Workflow<br/>Validator]
        LLM[LLM Integration<br/>Mimo VL 7B]
    end
    
    subgraph "Agent System"
        BaseAgent[Base Agent<br/>Abstract Class]
        AgentConfig[Agent<br/>Configuration]
        AgentResult[Agent<br/>Results]
    end
    
    subgraph "Data Layer"
        Patterns[Workflow<br/>Patterns]
        Feedback[Feedback<br/>Storage]
        Config[Configuration<br/>Management]
    end
    
    UI --> API
    CLI --> Builder
    API --> Builder
    Builder --> Validator
    Builder --> LLM
    Builder --> Patterns
    Builder --> Feedback
    BaseAgent --> AgentConfig
    BaseAgent --> AgentResult
    
    classDef userLayer fill:#e1f5fe
    classDef coreLayer fill:#f3e5f5
    classDef agentLayer fill:#e8f5e8
    classDef dataLayer fill:#fff3e0
    
    class UI,CLI,API userLayer
    class Builder,Validator,LLM coreLayer
    class BaseAgent,AgentConfig,AgentResult agentLayer
    class Patterns,Feedback,Config dataLayer
```

### Workflow Generation Process

```mermaid
sequenceDiagram
    participant User
    participant UI as Web UI/CLI
    participant API as FastAPI Server
    participant Builder as N8N Builder
    participant LLM as Mimo VL 7B
    participant Validator as Workflow Validator
    
    User->>UI: Enter plain English description
    UI->>API: POST /generate {description}
    API->>Builder: generate_workflow()
    
    Builder->>Builder: Build AI prompt with context
    Builder->>LLM: Send prompt to Mimo VL 7B
    LLM-->>Builder: Return structured workflow data
    
    Builder->>Builder: Map to N8N workflow structure
    Builder->>Validator: validate_workflow()
    Validator-->>Builder: Validation results
    
    alt Validation Successful
        Builder-->>API: Return validated workflow JSON
        API-->>UI: Stream workflow result
        UI-->>User: Display formatted workflow
    else Validation Failed
        Builder-->>API: Return error with details
        API-->>UI: Stream error event
        UI-->>User: Display error message
    end
```

### Agent Architecture

```mermaid
classDiagram
    class BaseAgent {
        <<abstract>>
        +config: AgentConfig
        +logger: Logger
        +name: str
        +process(request)* AgentResult
        +start() void
        +stop() void
        +get_status() Dict
        +close() void
    }
    
    class AgentConfig {
        +name: str
        +capabilities: Dict
        +max_concurrent_workflows: int
        +timeout: int
        +security: Dict
        +error_recovery: Dict
        +monitoring: Dict
        +resource_limits: Dict
        +get(key, default) Any
    }
    
    class AgentResult {
        +success: bool
        +data: Dict
        +error: str
        +metadata: Dict
    }
    
    class WorkflowAgent {
        +process_workflow(description) AgentResult
        +validate_output() bool
        +apply_patterns() void
    }
    
    class ValidationAgent {
        +validate_structure() bool
        +check_node_types() bool
        +verify_connections() bool
    }
    
    BaseAgent <|-- WorkflowAgent
    BaseAgent <|-- ValidationAgent
    BaseAgent --> AgentConfig
    BaseAgent --> AgentResult
```

---

## 🔧 Component Deep Dive

### Core Components

#### 1. N8N Builder Engine (`n8n_builder/n8n_builder.py`)
The heart of the system that orchestrates workflow generation:

```python
class N8NBuilder:
    def generate_workflow(self, description: str) -> str:
        # 1. Build AI prompt with context
        # 2. Call LLM (Mimo VL 7B)
        # 3. Map response to N8N structure  
        # 4. Validate and return JSON
```

**Key Features:**
- Intelligent prompt engineering for better AI responses
- Fallback mock responses for development/testing
- Comprehensive workflow validation
- Feedback collection and learning system

#### 2. Workflow Validator (`n8n_builder/validators.py`)
Ensures generated workflows meet N8N standards:

- **Structure Validation**: Required fields, proper JSON format
- **Node Validation**: Valid node types, required parameters
- **Connection Validation**: Proper node linking and data flow
- **Best Practices**: Security checks, performance considerations

#### 3. Agent System (`agents/base_agent.py`)
Extensible architecture for different processing agents:

```python
@abstractmethod
async def process(self, request: Dict[str, Any]) -> AgentResult:
    """Each agent implements its specific processing logic"""
```

**Agent Types:**
- **Workflow Generation Agents**: Convert descriptions to workflows
- **Validation Agents**: Ensure quality and compliance
- **Enhancement Agents**: Optimize and improve workflows
- **Integration Agents**: Connect with external systems

### Data Flow Architecture

```mermaid
flowchart TD
    A[Plain English Input] --> B{Input Validation}
    B -->|Valid| C[Prompt Engineering]
    B -->|Invalid| D[Error Response]
    
    C --> E[LLM Processing]
    E --> F[Response Parsing]
    F --> G[Workflow Mapping]
    G --> H[Structure Validation]
    
    H -->|Pass| I[Final Workflow JSON]
    H -->|Fail| J[Validation Errors]
    
    I --> K[Success Response]
    J --> L[Error Response with Suggestions]
    
    K --> M[User Interface]
    L --> M
    D --> M
    
    subgraph "Feedback Loop"
        N[User Feedback] --> O[Learning System]
        O --> P[Pattern Updates]
        P --> C
    end
    
    M --> N
```

---

## 🛠️ Advanced Configuration

### Environment Variables

```bash
# LLM Configuration
MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions
MIMO_MODEL=mimo-vl-7b
MIMO_TEMPERATURE=0.7
MIMO_MAX_TOKENS=2000

# Application Settings
API_HOST=localhost
API_PORT=8000
DEBUG_MODE=true
LOG_LEVEL=INFO

# Agent Configuration
MAX_CONCURRENT_AGENTS=5
AGENT_TIMEOUT=300
ENABLE_MONITORING=true
```

### Custom Agent Development

```python
from agents.base_agent import BaseAgent, AgentConfig, AgentResult

class CustomWorkflowAgent(BaseAgent):
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        # Your custom logic here
        try:
            # Process the request
            result_data = await self.custom_processing(request)
            
            return AgentResult(
                success=True,
                data=result_data,
                metadata={"processing_time": elapsed_time}
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
```

### Extending Workflow Patterns

Add new workflow patterns in `code_generation_patterns.py`:

```python
CUSTOM_PATTERNS = {
    "api_integration": {
        "description": "API data fetching and processing",
        "template": "...",
        "use_cases": ["data_sync", "webhook_processing"]
    }
}
```

---

## 📊 Monitoring and Analytics

### System Health Monitoring

```mermaid
graph LR
    A[Health Check Endpoint] --> B[Component Status]
    B --> C[LLM Availability]
    B --> D[Agent Status]
    B --> E[Resource Usage]
    
    F[Metrics Collection] --> G[Success Rates]
    F --> H[Response Times]
    F --> I[Error Patterns]
    
    G --> J[Dashboard/Alerts]
    H --> J
    I --> J
```

### Performance Metrics

- **Workflow Generation Success Rate**: % of successful generations
- **Validation Pass Rate**: % of workflows passing validation
- **Average Response Time**: Time from request to result
- **LLM Response Quality**: Accuracy of AI-generated workflows
- **User Satisfaction**: Based on feedback collection

---

## 🔄 API Reference

### Core Endpoints

```yaml
POST /generate:
  description: Generate workflow from description
  body:
    description: string (required)
    thread_id: string (optional)
    run_id: string (optional)
  response: Server-Sent Events stream

GET /health:
  description: System health check
  response:
    status: string
    timestamp: string

GET /feedback/{workflow_id}:
  description: Get workflow feedback
  response: Array of feedback entries
```

### Server-Sent Events Format

```json
{
  "type": "RUN_STARTED|WORKFLOW_GENERATED|RUN_FINISHED|RUN_ERROR",
  "workflow_id": "uuid",
  "thread_id": "uuid", 
  "run_id": "uuid",
  "timestamp": "ISO-8601",
  "data": { /* workflow or error data */ }
}
```

---

## 🧪 Testing and Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Load testing
python -m pytest tests/load/
```

### Development Workflow

1. **Local Development**: Use mock LLM responses for fast iteration
2. **Integration Testing**: Test with actual LLM endpoints
3. **Load Testing**: Verify performance under concurrent requests
4. **User Acceptance Testing**: Validate with real workflow scenarios

### Debugging Tips

- Enable debug logging: `LOG_LEVEL=DEBUG`
- Use mock responses for LLM testing
- Monitor agent status via health endpoint
- Check validation logs for workflow issues

---

## 🤝 Contributing

### Architecture Principles

1. **Modular Design**: Each component has a single responsibility
2. **Agent-Based**: Extensible through agent implementations  
3. **Async-First**: Non-blocking operations for better performance
4. **Validation-Heavy**: Multiple validation layers for reliability
5. **Feedback-Driven**: Continuous improvement through user feedback

### Adding New Features

1. **New Workflow Types**: Extend patterns and validation rules
2. **Custom Agents**: Implement BaseAgent for new capabilities
3. **UI Enhancements**: Modify static/index.html and API endpoints
4. **Integration Points**: Add new LLM providers or external services

---

## 📝 Conclusion

N8N Builder bridges the gap between natural language intent and technical workflow implementation. Its agent-based architecture ensures extensibility, while comprehensive validation guarantees reliable workflow generation. Whether you're a business user automating simple tasks or a developer building complex integration systems, N8N Builder provides the tools and flexibility you need.

The combination of AI-powered generation, robust validation, and extensible architecture makes it a powerful platform for workflow automation in any context. 