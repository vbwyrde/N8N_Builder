# N8N Builder API - Quick Reference

> **📖 New to N8N_Builder?** Start with [Lightning Start](../../LIGHTNING_START.md) or [Getting Started](../../GETTING_STARTED.md)
> **📚 Complete API Docs**: [API Documentation](API_DOCUMENTATION.md)
> **🏠 Back to Documentation**: [Documentation Index](../../DOCUMENTATION_INDEX.md)

**Standard API:** `http://localhost:8002`
**AG-UI Protocol:** `http://localhost:8003`

---

## 🤖 **AG-UI Protocol Quick Start**

### **1. Generate Workflow with AG-UI**
```bash
curl -X POST "http://localhost:8003/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "thread-123",
    "run_id": "run-456",
    "forwarded_props": {},
    "messages": [
      {
        "role": "user",
        "content": "Create a workflow that sends email notifications for new files"
      }
    ],
    "context": [
      {
        "description": "Workflow generation request",
        "value": "email notification workflow"
      }
    ],
    "tools": [],
    "state": null
  }' \
  --no-buffer
```

### **2. Check AG-UI Server Health**
```bash
curl -X GET "http://localhost:8003/health"
```

### **3. Get AG-UI Server Status**
```bash
curl -X GET "http://localhost:8003/status"
```

---

## 🚀 **Standard API Quick Start**

### **1. Generate New Workflow**
```bash
curl -X POST "http://localhost:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{"description": "Create a workflow that sends email notifications for new files"}' \
  --no-buffer
```

### **2. Modify Existing Workflow**
```bash
curl -X POST "http://localhost:8002/modify" \
  -H "Content-Type: application/json" \
  -d '{
    "existing_workflow_json": "{ your workflow JSON }",
    "modification_description": "Add error handling for email failures"
  }' \
  --no-buffer
```

### **3. Iterate Based on Testing**
```bash
curl -X POST "http://localhost:8002/iterate" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "my-workflow-123",
    "existing_workflow_json": "{ your workflow JSON }",
    "feedback_from_testing": "Email works but needs retry logic",
    "additional_requirements": "Add database logging"
  }' \
  --no-buffer
```

### **4. Create Project & Save Workflow**
```bash
# Create project
curl -X POST "http://localhost:8002/projects/my-automation" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-automation", "description": "Customer workflows"}'

# Save workflow to project
curl -X PUT "http://localhost:8002/projects/my-automation/workflows/welcome.json" \
  -H "Content-Type: application/json" \
  -d '{"workflow_data": {...}, "create_backup": true}'
```

### **5. Get Iteration History**
```bash
curl -X GET "http://localhost:8002/iterations/my-workflow-123"
```

---

## 🤖 **AG-UI Request Bodies**

### **Basic AG-UI Workflow Generation:**
```json
{
  "thread_id": "optional-thread-id",
  "run_id": "optional-run-id",
  "forwarded_props": {},
  "messages": [
    {
      "role": "user",
      "content": "Generate a workflow that processes CSV files and sends results via email"
    }
  ],
  "context": [
    {
      "description": "Workflow type",
      "value": "data_processing"
    },
    {
      "description": "Output format",
      "value": "email_notification"
    }
  ],
  "tools": [],
  "state": null
}
```

### **AG-UI with Workflow Modification Context:**
```json
{
  "thread_id": "thread-123",
  "run_id": "run-456",
  "forwarded_props": {},
  "messages": [
    {
      "role": "user",
      "content": "Modify the existing workflow to add error handling"
    }
  ],
  "context": [
    {
      "description": "Operation type",
      "value": "workflow_modification"
    },
    {
      "description": "Existing workflow",
      "value": "{\"name\": \"Email Workflow\", \"nodes\": [...]}"
    },
    {
      "description": "Modification request",
      "value": "Add error handling for SMTP failures"
    }
  ],
  "tools": [],
  "state": {
    "current_workflow": "email-workflow-v1",
    "modification_history": ["initial_creation", "email_validation_added"]
  }
}
```

---

## 📋 **Standard API Request Bodies**

### **Basic Modification:**
```json
{
  "existing_workflow_json": "{\"name\": \"Email Workflow\", \"nodes\": [...]}",
  "modification_description": "Add database logging after email is sent"
}
```

### **Feedback-Based Iteration:**
```json
{
  "workflow_id": "email-workflow-v1",
  "existing_workflow_json": "{\"name\": \"Email Workflow\", \"nodes\": [...]}",
  "feedback_from_testing": "Emails are sent successfully but there's no error handling when SMTP fails",
  "additional_requirements": "Add retry mechanism with exponential backoff"
}
```

### **Project Creation:**
```json
{
  "name": "my-project",
  "description": "Automation workflows for customer onboarding",
  "initial_workflows": ["welcome-email.json"]
}
```

---

## 🤖 **AG-UI Response Events**

AG-UI endpoints return structured event streams with the following event types:

### **AG-UI Event Types:**
| Event Type | Description |
|------------|-------------|
| `RUN_STARTED` | Agent execution initiated |
| `RUN_FINISHED` | Agent execution completed |
| `RUN_ERROR` | Error occurred during execution |
| `TEXT_MESSAGE_START` | Text message begins |
| `TEXT_MESSAGE_CONTENT` | Message content chunk (streaming) |
| `TEXT_MESSAGE_END` | Text message complete |
| `STEP_STARTED` | Processing step begins |
| `STEP_FINISHED` | Processing step complete |
| `STATE_SNAPSHOT` | Complete state update |
| `STATE_DELTA` | Incremental state change |
| `TOOL_CALL_START` | Tool execution begins |
| `TOOL_CALL_ARGS` | Tool arguments provided |
| `TOOL_CALL_END` | Tool execution complete |

### **AG-UI Event Examples:**
```json
{"type": "RUN_STARTED", "timestamp": 1704067106}
{"type": "TEXT_MESSAGE_START", "message_id": "msg_123", "role": "assistant", "timestamp": 1704067106}
{"type": "TEXT_MESSAGE_CONTENT", "message_id": "msg_123", "delta": "Starting workflow generation...", "timestamp": 1704067106}
{"type": "STEP_STARTED", "step_name": "workflow_generation", "timestamp": 1704067107}
{"type": "STATE_SNAPSHOT", "snapshot": {"current_step": "generation", "progress": 0.5}, "timestamp": 1704067108}
{"type": "STEP_FINISHED", "step_name": "workflow_generation", "timestamp": 1704067110}
{"type": "RUN_FINISHED", "timestamp": 1704067111}
```

---

## 🔄 **Standard API Response Events (SSE)**

Standard API endpoints return **Server-Sent Events (SSE)** with enhanced event types:

### **Core Events:**
| Event Type | Description |
|------------|-------------|
| `MODIFICATION_STARTED` | Process initiated |
| `VALIDATION_STARTED` | Input validation started |
| `VALIDATION_ERROR` | Validation failed (with detailed guidance) |
| `LLM_CHECK_STARTED` | LLM availability check started |
| `LLM_UNAVAILABLE` | LLM service unavailable (with recovery guidance) |
| `PROCESSING_STARTED` | Workflow processing started |
| `WORKFLOW_MODIFIED` | Contains the modified workflow JSON |
| `MODIFICATION_FINISHED` | Process completed successfully |

### **Enhanced Error Response:**
```json
{
  "type": "VALIDATION_ERROR",
  "error": {
    "category": "workflow_structure",
    "title": "Invalid Workflow JSON",
    "user_guidance": "Ensure your workflow JSON contains required properties",
    "fix_suggestions": ["Add 'nodes' array", "Check JSON syntax"]
  }
}
```

---

## 🗂️ **Key Endpoints**

### **AG-UI Protocol Endpoints:**
- `POST /run-agent` - Execute agent with RunAgentInput (AG-UI)
- `GET /health` - AG-UI server health check
- `GET /status` - Detailed AG-UI server status

### **Standard API Workflow Operations:**
- `POST /generate` - Generate new workflow
- `POST /modify` - Modify existing workflow
- `POST /iterate` - Iterate with feedback
- `GET /iterations/{id}` - Get iteration history
- `GET /feedback/{id}` - Get feedback history

### **Project Management:**
- `GET /projects` - List all projects
- `POST /projects/{name}` - Create project
- `GET /projects/{name}` - Get project details
- `PUT /projects/{name}/workflows/{file}` - Save workflow
- `DELETE /projects/{name}` - Delete project

### **Version Control:**
- `GET /projects/{name}/workflows/{file}/versions` - List versions
- `POST /projects/{name}/workflows/{file}/versions/{ver}/restore` - Restore version
- `GET /projects/{name}/workflows/{file}/compare/{v1}/{v2}` - Compare versions

### **Health & Status:**
- `GET /health` - Standard API health check
- `GET /llm/health` - LLM service health

---

## 💻 **Client Examples**

### **AG-UI JavaScript Client:**
```javascript
async function runAGUIAgent(messages, context = []) {
  const response = await fetch('http://localhost:8003/run-agent', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      thread_id: crypto.randomUUID(),
      run_id: crypto.randomUUID(),
      forwarded_props: {},
      messages: messages,
      context: context,
      tools: [],
      state: null
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const {value, done} = await reader.read();
    if (done) break;

    const event = JSON.parse(decoder.decode(value));

    switch(event.type) {
      case 'RUN_STARTED':
        console.log('Agent started');
        break;
      case 'TEXT_MESSAGE_CONTENT':
        console.log('Agent:', event.delta);
        break;
      case 'STEP_STARTED':
        console.log('Step:', event.step_name);
        break;
      case 'STATE_SNAPSHOT':
        console.log('State:', event.snapshot);
        break;
      case 'RUN_FINISHED':
        console.log('Agent completed');
        return;
      case 'RUN_ERROR':
        console.error('Agent error:', event.message);
        return;
    }
  }
}

// Usage
await runAGUIAgent([
  {role: "user", content: "Generate an email workflow"}
], [
  {description: "Workflow type", value: "email_automation"}
]);
```

### **Standard API JavaScript (Enhanced Error Handling):**
```javascript
async function modifyWorkflow(workflowJson, description) {
  const response = await fetch('/modify', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      existing_workflow_json: workflowJson,
      modification_description: description
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const {value, done} = await reader.read();
    if (done) break;
    
    const event = JSON.parse(decoder.decode(value));
    
    switch(event.type) {
      case 'VALIDATION_ERROR':
        console.error('Validation failed:', event.error.user_guidance);
        showFixSuggestions(event.error.fix_suggestions);
        return null;
      case 'LLM_UNAVAILABLE':
        console.warn('LLM unavailable:', event.error.message);
        return null;
      case 'WORKFLOW_MODIFIED':
        return event.data.workflow_json;
    }
  }
}
```

### **AG-UI Python Client:**
```python
import requests
import json
import uuid

def run_agui_agent(messages, context=None):
    if context is None:
        context = []

    response = requests.post(
        'http://localhost:8003/run-agent',
        json={
            'thread_id': str(uuid.uuid4()),
            'run_id': str(uuid.uuid4()),
            'forwarded_props': {},
            'messages': messages,
            'context': context,
            'tools': [],
            'state': None
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            event = json.loads(line.decode('utf-8'))

            if event['type'] == 'RUN_STARTED':
                print("Agent execution started")
            elif event['type'] == 'TEXT_MESSAGE_CONTENT':
                print(f"Agent: {event['delta']}")
            elif event['type'] == 'STEP_STARTED':
                print(f"Step started: {event['step_name']}")
            elif event['type'] == 'STATE_SNAPSHOT':
                print(f"State: {event['snapshot']}")
            elif event['type'] == 'RUN_FINISHED':
                print("Agent execution completed")
                break
            elif event['type'] == 'RUN_ERROR':
                print(f"Agent error: {event['message']}")
                break

# Usage
run_agui_agent([
    {"role": "user", "content": "Create a file processing workflow"}
], [
    {"description": "Workflow type", "value": "file_processing"}
])
```

### **Standard API Python (with Error Handling):**
```python
import requests
import json

def modify_workflow(workflow_json, description):
    response = requests.post(
        'http://localhost:8002/modify',
        json={
            'existing_workflow_json': workflow_json,
            'modification_description': description
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            event = json.loads(line.decode('utf-8'))
            
            if event['type'] == 'VALIDATION_ERROR':
                print(f"Validation failed: {event['error']['user_guidance']}")
                return None
            elif event['type'] == 'LLM_UNAVAILABLE':
                print(f"LLM unavailable: {event['error']['message']}")
                return None
            elif event['type'] == 'WORKFLOW_MODIFIED':
                return event['data']['workflow_json']
```

---

## ⚡ **Status Codes & Health Checks**

### **HTTP Status Codes:**
| Code | Description |
|------|-------------|
| 200 | Success (SSE stream) |
| 400 | Invalid request body |
| 404 | Workflow/project/iterations not found |
| 500 | Internal server error |

### **Quick Health Checks:**
```bash
# AG-UI server health
curl http://localhost:8003/health

# AG-UI server detailed status
curl http://localhost:8003/status

# Standard API health
curl http://localhost:8002/health

# LLM service health (with detailed response)
curl http://localhost:8002/llm/health
```

---

## 🎯 **Best Practices**

### **✅ DO:**
- **AG-UI Protocol**: Use structured RunAgentInput format with proper context
- **AG-UI Protocol**: Handle all AG-UI event types (RUN_STARTED, TEXT_MESSAGE_*, STEP_*, etc.)
- **Standard API**: Use specific, actionable modification descriptions
- **Both APIs**: Check health endpoints before complex operations
- **Both APIs**: Use projects to organize related workflows
- **Both APIs**: Enable auto-backup for important workflows
- **Both APIs**: Monitor response times (local LLMs: 20-45s, cloud: 5-10s)
- **Both APIs**: Include thread_id and run_id for tracking
- **AG-UI Protocol**: Provide meaningful context array for better agent selection

### **❌ DON'T:**
- **AG-UI Protocol**: Send malformed RunAgentInput structure
- **AG-UI Protocol**: Ignore RUN_ERROR events
- **Standard API**: Send malformed JSON in workflow fields
- **Both APIs**: Use overly vague descriptions ("make it better")
- **Both APIs**: Ignore validation errors and user guidance
- **Both APIs**: Make concurrent modifications to the same workflow
- **Both APIs**: Skip error handling for LLM unavailability
- **Both APIs**: Forget to set --no-buffer for streaming responses
- **AG-UI Protocol**: Mix AG-UI and Standard API request formats

---

## 🔍 **Debugging & Troubleshooting**

### **Common Issues:**

**1. AG-UI Server Issues:**
```bash
# Check AG-UI server health
curl http://localhost:8003/health
# Get detailed AG-UI status including agent states
curl http://localhost:8003/status
```

**2. LLM Service Issues:**
```bash
# Check LLM health with details
curl http://localhost:8002/llm/health
# Response includes crash detection and recovery guidance
```

**3. Validation Failures:**
- Check `validation_result` in workflow responses
- Review `user_guidance` and `fix_suggestions` in error events
- Ensure workflow JSON has required properties: `name`, `nodes`, `connections`

**4. Performance Issues:**
- Local LLMs may take 20-45 seconds for complex operations
- Monitor system resources (CPU/RAM) for local LLM
- Consider using smaller models if memory-constrained

### **Enhanced Error Categories:**

**AG-UI Protocol Errors:**
- `RUN_ERROR` - General agent execution error
- `agent_selection` - Unable to select appropriate agent
- `context_parsing` - Invalid context or message format
- `state_management` - State update or snapshot errors

**Standard API Errors:**
- `workflow_structure` - Invalid workflow JSON
- `llm_service` - LLM unavailable or crashed
- `validation` - Input validation failures
- `processing` - Workflow generation errors

### **Log Monitoring:**
```
INFO:n8n_builder.iteration:Starting workflow modification [ID: abc123]
INFO:n8n_builder.performance:LLM availability confirmed in 2.34s
INFO:n8n_builder.validation:Workflow validation completed successfully
```

---

## 🚀 **Performance Tips**

- **Local LLMs:** Allow 20-45 seconds for complex workflows
- **Cloud LLMs:** Expect 5-10 seconds response time
- **Concurrent Operations:** Use unique workflow_id, thread_id, run_id
- **Large Workflows:** Consider breaking into smaller modifications
- **Project Management:** Use version control for important workflows

---

## 🎯 **Choosing the Right API**

### **Use AG-UI Protocol when:**
- Building AI-powered applications
- Need structured agent interactions
- Want fine-grained progress tracking
- Building systems that integrate with other AG-UI compatible tools
- Need advanced state management

### **Use Standard REST API when:**
- Building traditional web applications
- Need simple HTTP request/response patterns
- Working with existing REST tooling
- Prefer familiar HTTP status codes

---

*For complete documentation including all endpoints, data models, and advanced features, see API_DOCUMENTATION.md*