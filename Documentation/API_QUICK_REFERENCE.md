# N8N Builder API - Quick Reference

**Base URL:** `http://localhost:8002`

---

## 🚀 **Quick Start**

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

## 📋 **Common Request Bodies**

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

## 🔄 **Response Events (SSE)**

All workflow endpoints return **Server-Sent Events (SSE)** with enhanced event types:

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

### **Workflow Operations:**
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
- `GET /health` - API health check
- `GET /llm/health` - LLM service health

---

## 💻 **Client Examples**

### **JavaScript (Enhanced Error Handling):**
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

### **Python (with Error Handling):**
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
# Basic API health
curl http://localhost:8002/health

# LLM service health (with detailed response)
curl http://localhost:8002/llm/health
```

---

## 🎯 **Best Practices**

### **✅ DO:**
- Use specific, actionable modification descriptions
- Handle all SSE event types (validation, LLM, processing)
- Check LLM health before complex operations
- Use projects to organize related workflows
- Enable auto-backup for important workflows
- Monitor response times (local LLMs: 20-45s, cloud: 5-10s)
- Include thread_id and run_id for tracking

### **❌ DON'T:**
- Send malformed JSON in workflow fields
- Use overly vague descriptions ("make it better")
- Ignore validation errors and user guidance
- Make concurrent modifications to the same workflow
- Skip error handling for LLM unavailability
- Forget to set --no-buffer for streaming responses

---

## 🔍 **Debugging & Troubleshooting**

### **Common Issues:**

**1. LLM Service Issues:**
```bash
# Check LLM health with details
curl http://localhost:8002/llm/health
# Response includes crash detection and recovery guidance
```

**2. Validation Failures:**
- Check `validation_result` in workflow responses
- Review `user_guidance` and `fix_suggestions` in error events
- Ensure workflow JSON has required properties: `name`, `nodes`, `connections`

**3. Performance Issues:**
- Local LLMs may take 20-45 seconds for complex operations
- Monitor system resources (CPU/RAM) for local LLM
- Consider using smaller models if memory-constrained

### **Enhanced Error Categories:**
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

*For complete documentation including all endpoints, data models, and advanced features, see API_DOCUMENTATION.md* 