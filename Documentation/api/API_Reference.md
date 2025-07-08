# N8N Builder API Documentation

> **📖 New to N8N_Builder?** Start with [Getting Started](../../GETTING_STARTED.md)
> **🔧 Need Technical Details?** See [Technical Specifications](../technical/Specifications.md)
> **🏠 Back to Documentation**: [Architecture Overview](../Architecture.md)

**Version:** 1.0
**Base URL:** `http://localhost:8002`
**AG-UI Server:** `http://localhost:8003` (when running separately)
**Last Updated:** January 2025

---

## 📋 **Overview**

The N8N Builder API provides endpoints for generating, modifying, and iterating on N8N workflows using natural language descriptions. The API supports real-time streaming responses, comprehensive workflow iteration capabilities, project management, version control, and advanced error handling.

### **🔄 Dual API Architecture**

N8N Builder now supports **two complementary API interfaces**:

1. **Standard REST API** (`http://localhost:8002`) - Traditional HTTP endpoints with Server-Sent Events
2. **AG-UI Protocol API** (`http://localhost:8003`) - Advanced agent-based interface following AG-UI standards

Both APIs provide the same core functionality but with different interaction patterns optimized for different use cases.

---

## 🤖 **AG-UI Protocol Endpoints**

The AG-UI (Agent-Generated User Interface) protocol provides a standardized way to interact with AI agents through structured events and streaming responses. This is the recommended interface for advanced integrations and AI-powered applications.

### **1. Run Agent (AG-UI)**
**`POST /run-agent`** ✨ **AG-UI Protocol**

Execute workflow operations using the AG-UI protocol with `RunAgentInput`.

**Request Body (AG-UI Format):**
```json
{
  "thread_id": "optional-thread-id",
  "run_id": "optional-run-id",
  "forwarded_props": {},
  "messages": [
    {
      "role": "user",
      "content": "Generate a workflow that sends email notifications for new files"
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
}
```

**Response:** AG-UI Event Stream with the following event types:
- `RUN_STARTED` - Agent execution initiated
- `TEXT_MESSAGE_START` - Text message begins
- `TEXT_MESSAGE_CONTENT` - Message content chunk
- `TEXT_MESSAGE_END` - Text message complete
- `STEP_STARTED` - Processing step begins
- `STEP_FINISHED` - Processing step complete
- `STATE_SNAPSHOT` - Current state update
- `TOOL_CALL_START` - Tool execution begins
- `TOOL_CALL_END` - Tool execution complete
- `RUN_FINISHED` - Agent execution complete
- `RUN_ERROR` - Error occurred

**Example AG-UI Response Events:**
```json
{"type": "RUN_STARTED", "timestamp": 1704067106}
{"type": "TEXT_MESSAGE_START", "message_id": "msg_123", "role": "assistant", "timestamp": 1704067106}
{"type": "TEXT_MESSAGE_CONTENT", "message_id": "msg_123", "delta": "Starting workflow generation...", "timestamp": 1704067106}
{"type": "STEP_STARTED", "step_name": "workflow_generation", "timestamp": 1704067107}
{"type": "STATE_SNAPSHOT", "snapshot": {"current_step": "generation", "progress": 0.5}, "timestamp": 1704067108}
{"type": "STEP_FINISHED", "step_name": "workflow_generation", "timestamp": 1704067110}
{"type": "TEXT_MESSAGE_END", "message_id": "msg_123", "timestamp": 1704067110}
{"type": "RUN_FINISHED", "timestamp": 1704067111}
```

### **2. AG-UI Health Check**
**`GET /health`** (AG-UI Server)

Check the health of the AG-UI server and agents.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-11T00:58:26.000Z",
  "active_runs": 2,
  "agents": ["generator", "validator", "orchestrator"]
}
```

### **3. AG-UI Server Status**
**`GET /status`** (AG-UI Server)

Get detailed status of the AG-UI server and all agents.

**Response:**
```json
{
  "server": {
    "running": true,
    "active_runs": 2,
    "uptime": "2h 15m"
  },
  "agents": {
    "generator": {"status": "ready", "active_tasks": 1},
    "validator": {"status": "ready", "active_tasks": 0},
    "orchestrator": {"status": "ready", "active_tasks": 1}
  },
  "config": {
    "allowed_origins": ["*"],
    "ag_ui_version": "1.0.0"
  }
}
```

---

## 🔧 **Core Workflow Endpoints (Standard REST API)**

### **1. Generate Workflow**
**`POST /generate`**

Generate a new N8N workflow from a plain English description.

**Request Body:**
```json
{
  "description": "Create a workflow that watches for new files in a folder and sends an email notification",
  "thread_id": "optional-thread-id",
  "run_id": "optional-run-id"
}
```

**Response:** Server-Sent Events (SSE) stream with the following events:
- `RUN_STARTED` - Process initiated
- `VALIDATION_STARTED` - Input validation started
- `VALIDATION_COMPLETED` - Input validation completed
- `LLM_CHECK_STARTED` - LLM availability check started
- `LLM_AVAILABLE` - LLM service confirmed available
- `LLM_UNAVAILABLE` - LLM service unavailable (error case)
- `PROCESSING_STARTED` - Workflow generation started
- `WORKFLOW_GENERATED` - Workflow created successfully  
- `RUN_FINISHED` - Process completed
- `RUN_ERROR` - Error occurred

**Example Response Events:**
```json
{"type": "RUN_STARTED", "workflow_id": "uuid", "thread_id": "uuid", "run_id": "uuid", "timestamp": "2025-01-11T00:58:26.000Z"}
{"type": "VALIDATION_STARTED", "workflow_id": "uuid", "message": "Validating workflow generation request..."}
{"type": "LLM_CHECK_STARTED", "workflow_id": "uuid", "message": "Checking LLM service availability..."}
{"type": "LLM_AVAILABLE", "workflow_id": "uuid", "message": "LLM service is available and ready"}
{"type": "PROCESSING_STARTED", "workflow_id": "uuid", "message": "Generating workflow..."}
{"type": "WORKFLOW_GENERATED", "workflow_id": "uuid", "data": {"workflow_json": "...", "validation_result": {...}}}
{"type": "RUN_FINISHED", "success": true}
```

---

## 🔄 **Workflow Iteration Endpoints**

### **2. Modify Workflow**
**`POST /modify`** ✨

Modify an existing workflow based on a description of changes needed.

**Request Body:**
```json
{
  "existing_workflow_json": "{\"name\": \"Email Workflow\", \"nodes\": [...], \"connections\": {...}}",
  "modification_description": "Add database logging after sending the email",
  "workflow_id": "optional-workflow-id",
  "thread_id": "optional-thread-id", 
  "run_id": "optional-run-id"
}
```

**Response:** Server-Sent Events (SSE) stream with the following events:
- `MODIFICATION_STARTED` - Modification process initiated
- `VALIDATION_STARTED` - Input validation started
- `VALIDATION_ERROR` - Validation failed (error case)
- `VALIDATION_COMPLETED` - Input validation completed
- `LLM_CHECK_STARTED` - LLM availability check started
- `LLM_AVAILABLE` - LLM service confirmed available
- `LLM_UNAVAILABLE` - LLM service unavailable (error case)
- `PROCESSING_STARTED` - Workflow modification started
- `WORKFLOW_MODIFIED` - Workflow modified successfully
- `MODIFICATION_FINISHED` - Process completed
- `MODIFICATION_ERROR` - Error occurred

### **3. Iterate Workflow**
**`POST /iterate`** ✨

Iterate on a workflow based on testing feedback and additional requirements.

**Request Body:**
```json
{
  "workflow_id": "workflow-uuid-here",
  "existing_workflow_json": "{\"name\": \"Email Workflow\", \"nodes\": [...], \"connections\": {...}}",
  "feedback_from_testing": "The email sending works but we need to handle cases where the recipient is invalid",
  "additional_requirements": "Also add logging to track all email attempts",
  "thread_id": "optional-thread-id",
  "run_id": "optional-run-id"
}
```

**Response:** Server-Sent Events (SSE) stream with the following events:
- `ITERATION_STARTED` - Iteration process initiated
- `VALIDATION_STARTED` - Input validation started
- `VALIDATION_ERROR` - Validation failed (error case)
- `VALIDATION_COMPLETED` - Input validation completed
- `LLM_CHECK_STARTED` - LLM availability check started
- `LLM_AVAILABLE` - LLM service confirmed available
- `LLM_UNAVAILABLE` - LLM service unavailable (error case)
- `PROCESSING_STARTED` - Workflow iteration started
- `WORKFLOW_ITERATED` - Workflow iterated successfully
- `ITERATION_FINISHED` - Process completed
- `ITERATION_ERROR` - Error occurred

### **4. Get Workflow Iterations**
**`GET /iterations/{workflow_id}`** ✨

Retrieve the complete iteration history for a specific workflow.

**Path Parameters:**
- `workflow_id` (string, required): The unique identifier of the workflow

**Response:**
```json
[
  {
    "workflow_id": "abc123",
    "timestamp": "2025-01-11T00:58:26.000Z",
    "description": "Add database logging after sending the email",
    "original_hash": 1234567890,
    "modified_hash": 9876543210,
    "changes_summary": {
      "nodes_added": 1,
      "connections_changed": true,
      "parameters_modified": true
    },
    "original_size": 1024,
    "modified_size": 1280
  }
]
```

### **5. Get Workflow Feedback**
**`GET /feedback/{workflow_id}`** ✨

Retrieve feedback history for a specific workflow.

**Path Parameters:**
- `workflow_id` (string, required): The unique identifier of the workflow

**Response:**
```json
[
  {
    "workflow_id": "abc123",
    "feedback": "Email sending works but needs error handling",
    "timestamp": "2025-01-11T00:58:26.000Z",
    "feedback_type": "testing_results"
  }
]
```

---

## 🗂️ **Project Management Endpoints**

### **6. List Projects**
**`GET /projects`**

List all projects in the system.

**Response:**
```json
[
  {
    "name": "ecommerce-workflows",
    "path": "/projects/ecommerce-workflows",
    "description": "E-commerce automation workflows",
    "created_date": "2025-01-10T10:00:00.000Z",
    "last_modified": "2025-01-11T15:30:00.000Z",
    "workflow_count": 5,
    "workflows": ["order-processing.json", "inventory-sync.json"],
    "settings": {"auto_backup": true, "version_limit": 10}
  }
]
```

### **7. Get Project Statistics**
**`GET /projects/stats`**

Get comprehensive statistics about all projects.

**Response:**
```json
{
  "total_projects": 3,
  "total_workflows": 15,
  "projects_root": "/projects",
  "average_workflows_per_project": 5.0,
  "project_names": ["ecommerce-workflows", "crm-automation", "data-processing"],
  "largest_project": "ecommerce-workflows",
  "most_recent_project": "data-processing"
}
```

### **8. Create Project**
**`POST /projects/{name}`**

Create a new project.

**Path Parameters:**
- `name` (string, required): Project name

**Request Body:**
```json
{
  "name": "my-new-project",
  "description": "Project for customer automation workflows",
  "initial_workflows": ["welcome-email.json"]
}
```

### **9. Get Project Details**
**`GET /projects/{name}`**

Get detailed information about a specific project.

### **10. List Project Workflows**
**`GET /projects/{name}/workflows`**

List all workflows in a specific project.

### **11. Get Workflow File**
**`GET /projects/{name}/workflows/{filename}`**

Get details about a specific workflow file.

### **12. Save Workflow File**
**`PUT /projects/{name}/workflows/{filename}`**

Save or update a workflow file in a project.

**Request Body:**
```json
{
  "workflow_data": {"name": "My Workflow", "nodes": [], "connections": {}},
  "create_backup": true
}
```

### **13. Delete Project**
**`DELETE /projects/{name}?confirm=true`**

Delete a project and all its workflows.

---

## 📋 **Version Management Endpoints**

### **14. List Workflow Versions**
**`GET /projects/{name}/workflows/{filename}/versions`**

List all versions/backups of a workflow file.

### **15. Get Version Information**
**`GET /projects/{name}/workflows/{filename}/versions/{version_filename}`**

Get detailed information about a specific workflow version.

**Response:**
```json
{
  "filename": "welcome-email_backup_20250111_143022.json",
  "timestamp": "2025-01-11T14:30:22.000Z",
  "created_date": "2025-01-11T14:30:22.000Z",
  "modified_date": "2025-01-11T14:30:22.000Z",
  "file_size": 2048,
  "file_size_mb": 0.002,
  "workflow_name": "Welcome Email Workflow",
  "node_count": 3,
  "tags": ["email", "automation"],
  "is_backup": true
}
```

### **16. Get Version Content**
**`GET /projects/{name}/workflows/{filename}/versions/{version_filename}/content`**

Get the actual workflow JSON content of a specific version.

### **17. Restore Version**
**`POST /projects/{name}/workflows/{filename}/versions/{version_filename}/restore`**

Restore a workflow to a previous version.

**Request Body:**
```json
{
  "create_backup": true
}
```

### **18. Compare Versions**
**`GET /projects/{name}/workflows/{filename}/compare/{version1}/{version2}`**

Compare two versions of a workflow.

**Response:**
```json
{
  "version1": {"workflow_data": "..."},
  "version2": {"workflow_data": "..."},
  "differences": {
    "nodes_changed": true,
    "connections_changed": false,
    "settings_changed": true
  },
  "summary": {
    "nodes_added": 1,
    "nodes_removed": 0,
    "nodes_modified": 2,
    "connections_added": 1,
    "connections_removed": 0
  }
}
```

### **19. Delete Version**
**`DELETE /projects/{name}/workflows/{filename}/versions/{version_filename}?confirm=true`**

Delete a specific workflow version.

### **20. Cleanup Versions**
**`POST /projects/{name}/workflows/{filename}/cleanup-versions`**

Remove old versions keeping only the most recent ones.

**Request Body:**
```json
{
  "keep_versions": 10
}
```

---

## 🏥 **Health Check Endpoints**

### **21. Basic Health Check (Standard API)**
**`GET /health`**

Check the overall health of the standard REST API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-11T00:58:26.000Z",
  "version": "1.0.0"
}
```

### **22. LLM Health Check**
**`GET /llm/health`**

Check the health and availability of the LLM service.

**Response:**
```json
{
  "status": "available",
  "llm_endpoint": "http://localhost:1234/v1",
  "llm_model": "llama-3.2-3b-instruct",
  "is_local": true,
  "timestamp": "2025-01-11T00:58:26.000Z",
  "response_time_ms": 1250.45
}
```

**Error Response:**
```json
{
  "status": "unavailable",
  "llm_endpoint": "http://localhost:1234/v1",
  "llm_model": "llama-3.2-3b-instruct",
  "is_local": true,
  "timestamp": "2025-01-11T00:58:26.000Z",
  "error": "LLM service did not respond within 30 seconds"
}
```

---

## 🤖 **AG-UI Data Models**

### **RunAgentInput (AG-UI Protocol)**
```typescript
{
  thread_id?: string;                    // Optional thread identifier
  run_id?: string;                      // Optional run identifier
  forwarded_props: Record<string, any>; // Additional properties
  messages: Message[];                  // Conversation messages
  context: Context[];                   // Request context
  tools: Tool[];                       // Available tools
  state?: State;                       // Current state
}
```

### **AG-UI Message**
```typescript
{
  role: "user" | "assistant" | "system"; // Message role
  content: string;                       // Message content
  timestamp?: number;                    // Optional timestamp
}
```

### **AG-UI Context**
```typescript
{
  description: string;                   // Context description
  value: any;                           // Context value
  type?: string;                        // Optional context type
}
```

### **AG-UI Event Types**
```typescript
// Core event types
"RUN_STARTED" | "RUN_FINISHED" | "RUN_ERROR" |
"TEXT_MESSAGE_START" | "TEXT_MESSAGE_CONTENT" | "TEXT_MESSAGE_END" |
"STEP_STARTED" | "STEP_FINISHED" |
"STATE_SNAPSHOT" | "STATE_DELTA" |
"TOOL_CALL_START" | "TOOL_CALL_ARGS" | "TOOL_CALL_END" |
"MESSAGES_SNAPSHOT" | "RAW" | "CUSTOM"
```

---

## 📊 **Enhanced Data Models (Standard API)**

### **WorkflowModificationRequest**
```typescript
{
  existing_workflow_json: string;     // Valid N8N workflow JSON
  modification_description: string;   // Plain English description of changes
  workflow_id?: string;              // Optional workflow identifier
  thread_id?: string;                // Optional thread tracking
  run_id?: string;                   // Optional run tracking
}
```

### **WorkflowIterationRequest**
```typescript
{
  workflow_id: string;               // Required workflow identifier
  existing_workflow_json: string;    // Valid N8N workflow JSON
  feedback_from_testing: string;     // Testing feedback description
  additional_requirements?: string;  // Optional additional requirements
  thread_id?: string;               // Optional thread tracking
  run_id?: string;                  // Optional run tracking
}
```

### **Enhanced ValidationResult**
```typescript
{
  is_valid: boolean;
  errors: ErrorDetail[];            // Enhanced error objects
  warnings: string[];
  validation_summary: {
    nodes_validated: number;
    connections_validated: number;
    critical_issues: number;
    warnings_count: number;
  };
}
```

### **ErrorDetail (Enhanced Error Handling)**
```typescript
{
  category: string;                 // "validation", "llm_service", "workflow_structure"
  severity: string;                 // "error", "warning", "info"
  title: string;                   // Human-readable error title
  message: string;                 // Detailed error message
  user_guidance: string;           // What the user should do
  fix_suggestions: string[];       // Specific fix recommendations
  technical_details: string;       // Technical information for debugging
}
```

### **ProjectResponse**
```typescript
{
  name: string;
  path: string;
  description: string;
  created_date: string;            // ISO 8601 timestamp
  last_modified: string;           // ISO 8601 timestamp
  workflow_count: number;
  workflows: string[];             // List of workflow filenames
  settings: {                      // Project-specific settings
    auto_backup: boolean;
    version_limit: number;
    [key: string]: any;
  };
}
```

---

## 🚨 **Enhanced Error Handling**

### **Validation Errors**
The system provides comprehensive validation with detailed guidance:

```json
{
  "type": "VALIDATION_ERROR",
  "workflow_id": "abc123",
  "error": {
    "category": "workflow_structure",
    "severity": "error",
    "title": "Invalid Workflow JSON Structure",
    "message": "The provided workflow JSON is missing required 'nodes' property",
    "user_guidance": "Ensure your workflow JSON contains all required properties: name, nodes, and connections",
    "fix_suggestions": [
      "Add a 'nodes' array to your workflow JSON",
      "Verify the workflow was exported correctly from N8N",
      "Check for any JSON syntax errors"
    ],
    "technical_details": "Property 'nodes' is required but was not found in the root object"
  }
}
```

### **LLM Service Errors**
Enhanced LLM error detection and crash recovery:

```json
{
  "type": "LLM_UNAVAILABLE",
  "error": {
    "category": "llm_service",
    "severity": "error",
    "title": "LLM Service Crashed",
    "message": "Model crashed with exit code 137 (Process killed - out of memory or forced termination)",
    "user_guidance": "The AI service crashed, likely due to memory constraints. Check system resources and restart your LLM service.",
    "fix_suggestions": [
      "Restart your LLM service (e.g., LM Studio)",
      "Check available system memory and close other applications",
      "Consider using a smaller model if memory is limited",
      "Verify your LLM service configuration"
    ]
  }
}
```

---

## ⚡ **Real-Time Streaming**

All workflow operations return **Server-Sent Events (SSE)** for real-time progress updates with enhanced event types:

### **Complete Event Flow Example:**
```javascript
const eventSource = new EventSource('/modify', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    existing_workflow_json: workflowJson,
    modification_description: "Add error handling"
  })
});

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'MODIFICATION_STARTED':
      console.log('Starting modification...');
      break;
    case 'VALIDATION_STARTED':
      console.log('Validating inputs...');
      break;
    case 'VALIDATION_ERROR':
      console.error('Validation failed:', data.error);
      showUserGuidance(data.error.user_guidance, data.error.fix_suggestions);
      break;
    case 'LLM_CHECK_STARTED':
      console.log('Checking LLM availability...');
      break;
    case 'LLM_UNAVAILABLE':
      console.error('LLM service unavailable:', data.error);
      showRetryOptions();
      break;
    case 'PROCESSING_STARTED':
      console.log('Processing workflow...');
      break;
    case 'WORKFLOW_MODIFIED':
      console.log('Workflow modified:', data.data.workflow_json);
      break;
    case 'MODIFICATION_FINISHED':
      console.log('Modification completed!');
      eventSource.close();
      break;
  }
};
```

---

## 🎯 **Best Practices**

### **For Workflow Operations:**
- ✅ Always validate workflow JSON before sending to modification endpoints
- ✅ Handle all SSE event types, especially validation and LLM errors
- ✅ Implement retry logic for LLM unavailability scenarios
- ✅ Monitor response times - local LLMs may take 20-45 seconds
- ✅ Use thread_id and run_id for tracking complex operations

### **For Project Management:**
- ✅ Use project structure for organizing related workflows
- ✅ Enable auto-backup for important workflows
- ✅ Regular cleanup of old versions to manage storage
- ✅ Use descriptive project and workflow names

### **Error Recovery:**
- ✅ Always check validation results before deploying workflows
- ✅ Implement user-friendly error display using error.user_guidance
- ✅ Show fix suggestions to help users resolve issues
- ✅ Monitor LLM health and provide fallback options

---

## 📈 **Performance Considerations**

- **Average Response Time:** 
  - Cloud LLMs: ~5-10 seconds
  - Local LLMs: ~20-45 seconds for complex operations
- **Concurrent Requests:** Supported with unique operation IDs
- **Timeout:** 45 seconds for LLM operations, 30 seconds for health checks
- **Rate Limiting:** Not currently implemented
- **Caching:** Workflow iterations cached in memory
- **Project Management:** File-based storage with in-memory caching

---

## 🔗 **Integration Examples**

### **AG-UI Protocol Integration:**
```javascript
// Using AG-UI protocol for workflow generation
async function generateWorkflowWithAGUI(description) {
  const response = await fetch('http://localhost:8003/run-agent', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      thread_id: crypto.randomUUID(),
      run_id: crypto.randomUUID(),
      forwarded_props: {},
      messages: [
        {
          role: "user",
          content: description
        }
      ],
      context: [
        {
          description: "Workflow generation request",
          value: description
        }
      ],
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
        console.log('Agent execution started');
        break;
      case 'TEXT_MESSAGE_CONTENT':
        console.log('Agent message:', event.delta);
        break;
      case 'STEP_STARTED':
        console.log('Step started:', event.step_name);
        break;
      case 'STATE_SNAPSHOT':
        console.log('State update:', event.snapshot);
        break;
      case 'RUN_FINISHED':
        console.log('Agent execution completed');
        return;
      case 'RUN_ERROR':
        console.error('Agent error:', event.message);
        return;
    }
  }
}
```

### **Complete Workflow Lifecycle (Standard API):**
```bash
# 1. Create a project
curl -X POST "http://localhost:8002/projects/my-automation" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-automation", "description": "Customer automation workflows"}'

# 2. Generate initial workflow
curl -X POST "http://localhost:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{"description": "Send welcome email to new customers"}' \
  --no-buffer

# 3. Save workflow to project
curl -X PUT "http://localhost:8002/projects/my-automation/workflows/welcome-email.json" \
  -H "Content-Type: application/json" \
  -d '{"workflow_data": {...}, "create_backup": true}'

# 4. Modify workflow based on testing
curl -X POST "http://localhost:8002/modify" \
  -H "Content-Type: application/json" \
  -d '{"existing_workflow_json": "...", "modification_description": "Add error handling for invalid emails"}' \
  --no-buffer

# 5. Check iteration history
curl -X GET "http://localhost:8002/iterations/workflow-id-here"
```

### **AG-UI Health Monitoring:**
```bash
# Check AG-UI server health
curl -X GET "http://localhost:8003/health"

# Get detailed AG-UI server status
curl -X GET "http://localhost:8003/status"
```

---

## 📞 **Support**

For technical support or feature requests:
- **GitHub Issues:** [Project Repository]
- **Documentation:** This file
- **API Version:** 1.0
- **Last Updated:** January 2025

---

## 🎯 **Choosing Between API Interfaces**

### **Use Standard REST API when:**
- Building traditional web applications
- Need simple HTTP request/response patterns
- Working with existing REST API tooling
- Prefer familiar HTTP status codes and patterns

### **Use AG-UI Protocol when:**
- Building AI-powered applications
- Need advanced agent interaction patterns
- Want structured event streaming
- Building applications that integrate with other AG-UI compatible systems
- Need fine-grained progress tracking and state management

### **Key Differences:**

| Feature | Standard REST API | AG-UI Protocol |
|---------|------------------|----------------|
| **Request Format** | JSON with specific fields | RunAgentInput structure |
| **Response Format** | Server-Sent Events | AG-UI Event Stream |
| **Agent Selection** | Automatic based on endpoint | Intelligent based on context |
| **State Management** | Basic | Advanced with snapshots |
| **Progress Tracking** | Event-based | Step-based with detailed states |
| **Error Handling** | HTTP status codes | Structured error events |

---

*This documentation covers the complete N8N Builder API including both Standard REST and AG-UI Protocol interfaces, workflow generation, project management, version control, and advanced error handling. For implementation details, see the codebase in `/n8n_builder/app.py` (Standard API) and `/n8n_builder/agui_server.py` (AG-UI Protocol).*