# N8N Builder API - Quick Reference

**Base URL:** `http://localhost:8000`

---

## 🚀 **Quick Start**

### **1. Modify Existing Workflow**
```bash
curl -X POST "http://localhost:8000/modify" \
  -H "Content-Type: application/json" \
  -d '{
    "existing_workflow_json": "{ your workflow JSON }",
    "modification_description": "Add error handling for email failures"
  }'
```

### **2. Iterate Based on Testing**
```bash
curl -X POST "http://localhost:8000/iterate" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "my-workflow-123",
    "existing_workflow_json": "{ your workflow JSON }",
    "feedback_from_testing": "Email works but needs retry logic",
    "additional_requirements": "Add database logging"
  }'
```

### **3. Get Iteration History**
```bash
curl -X GET "http://localhost:8000/iterations/my-workflow-123"
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

---

## 🔄 **Response Events**

All endpoints return **Server-Sent Events (SSE)**:

| Event Type | Description |
|------------|-------------|
| `MODIFICATION_STARTED` | Process initiated |
| `WORKFLOW_MODIFIED` | Contains the modified workflow JSON |
| `MODIFICATION_FINISHED` | Process completed successfully |
| `MODIFICATION_ERROR` | Error occurred with details |

---

## 💻 **Client Examples**

### **JavaScript (Fetch + SSE):**
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
    if (event.type === 'WORKFLOW_MODIFIED') {
      return event.data.workflow_json;
    }
  }
}
```

### **Python (Requests):**
```python
import requests
import json

def modify_workflow(workflow_json, description):
    response = requests.post(
        'http://localhost:8000/modify',
        json={
            'existing_workflow_json': workflow_json,
            'modification_description': description
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            event = json.loads(line.decode('utf-8'))
            if event['type'] == 'WORKFLOW_MODIFIED':
                return event['data']['workflow_json']
```

---

## ⚡ **Status Codes**

| Code | Description |
|------|-------------|
| 200 | Success (SSE stream) |
| 400 | Invalid request body |
| 404 | Workflow/iterations not found |
| 500 | Internal server error |

---

## 🎯 **Best Practices**

### **✅ DO:**
- Use specific, actionable modification descriptions
- Include detailed testing feedback for iterations
- Monitor SSE events for real-time status
- Validate modified workflows before deployment

### **❌ DON'T:**
- Send malformed JSON in workflow fields
- Use overly vague descriptions ("make it better")
- Ignore validation warnings in responses
- Make concurrent modifications to the same workflow

---

## 🔍 **Debugging**

### **Check Health:**
```bash
curl http://localhost:8000/health
```

### **Common Issues:**
1. **Invalid JSON:** Ensure workflow JSON is properly escaped
2. **Empty descriptions:** Provide meaningful modification requests
3. **Missing workflow_id:** Required for iterations endpoint
4. **Validation failures:** Check response validation_result

### **Log Monitoring:**
Monitor server logs for detailed operation tracking:
```
INFO:n8n_builder.iteration:Starting workflow modification [ID: abc123]
INFO:n8n_builder.performance:Workflow modification completed successfully
```

---

*For complete documentation, see API_DOCUMENTATION.md* 