# N8N Builder API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:8000`  
**Last Updated:** January 2025  

---

## 📋 **Overview**

The N8N Builder API provides endpoints for generating, modifying, and iterating on N8N workflows using natural language descriptions. The API supports real-time streaming responses and comprehensive workflow iteration capabilities.

---

## 🔧 **Core Endpoints**

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
- `WORKFLOW_GENERATED` - Workflow created successfully  
- `RUN_FINISHED` - Process completed
- `RUN_ERROR` - Error occurred

**Example Response Events:**
```json
{"type": "RUN_STARTED", "workflow_id": "uuid", "thread_id": "uuid", "run_id": "uuid", "timestamp": "2025-01-11T00:58:26.000Z"}
{"type": "WORKFLOW_GENERATED", "workflow_id": "uuid", "data": {"workflow_json": "...", "validation_result": {...}}}
{"type": "RUN_FINISHED", "success": true}
```

---

## 🔄 **Workflow Iteration Endpoints**

### **2. Modify Workflow**
**`POST /modify`** ✨ **NEW**

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
- `WORKFLOW_MODIFIED` - Workflow modified successfully
- `MODIFICATION_FINISHED` - Process completed
- `MODIFICATION_ERROR` - Error occurred

**Example Usage:**
```bash
curl -X POST "http://localhost:8000/modify" \
  -H "Content-Type: application/json" \
  -d '{
    "existing_workflow_json": "{\"name\": \"Basic Email\", \"nodes\": [{\"id\": \"1\", \"name\": \"Manual Trigger\", \"type\": \"n8n-nodes-base.manualTrigger\"}, {\"id\": \"2\", \"name\": \"Send Email\", \"type\": \"n8n-nodes-base.emailSend\"}], \"connections\": {}}",
    "modification_description": "Add error handling and retry logic for email failures"
  }'
```

### **3. Iterate Workflow**
**`POST /iterate`** ✨ **NEW**

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
- `WORKFLOW_ITERATED` - Workflow iterated successfully
- `ITERATION_FINISHED` - Process completed
- `ITERATION_ERROR` - Error occurred

**Example Response Events:**
```json
{"type": "ITERATION_STARTED", "workflow_id": "abc123", "timestamp": "2025-01-11T00:58:26.000Z"}
{"type": "WORKFLOW_ITERATED", "workflow_id": "abc123", "data": {"workflow_json": "...", "validation_result": {"is_valid": true, "errors": [], "warnings": []}}}
{"type": "ITERATION_FINISHED", "workflow_id": "abc123", "success": true}
```

### **4. Get Workflow Iterations**
**`GET /iterations/{workflow_id}`** ✨ **NEW**

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
  },
  {
    "workflow_id": "abc123", 
    "timestamp": "2025-01-11T01:02:15.000Z",
    "description": "ITERATION - Feedback: The email sending works but we need to handle...",
    "original_hash": 9876543210,
    "modified_hash": 5555555555,
    "changes_summary": {
      "nodes_added": 2,
      "connections_changed": true,
      "parameters_modified": true
    },
    "original_size": 1280,
    "modified_size": 1650
  }
]
```

**Example Usage:**
```bash
curl -X GET "http://localhost:8000/iterations/abc123"
```

**Error Response (404):**
```json
{
  "detail": "No iterations found for this workflow"
}
```

---

## 📊 **Data Models**

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

### **WorkflowResponse**
```typescript
{
  workflow_id: string;              // Unique workflow identifier
  workflow_json: string;            // Generated/modified N8N workflow
  validation_result: {              // Workflow validation status
    is_valid: boolean;
    errors: string[];
    warnings: string[];
  };
  timestamp: string;                // ISO 8601 timestamp
}
```

---

## 🔍 **Usage Patterns**

### **Basic Workflow Iteration Flow**
1. **Generate Initial Workflow:** Use `/generate` to create base workflow
2. **Test in N8N:** Import and test the workflow
3. **Gather Feedback:** Document what works and what needs improvement
4. **Iterate:** Use `/iterate` with testing feedback
5. **Repeat:** Continue iterating until workflow is perfect
6. **Track History:** Use `/iterations/{id}` to view iteration history

### **Workflow Modification Flow**
1. **Load Existing Workflow:** Have a working N8N workflow JSON
2. **Describe Changes:** Specify what modifications are needed
3. **Apply Changes:** Use `/modify` to get updated workflow
4. **Validate:** Check the modified workflow in N8N
5. **Track Changes:** View iteration history for the workflow

---

## ⚡ **Real-Time Streaming**

All workflow operations return **Server-Sent Events (SSE)** for real-time progress updates:

### **JavaScript Client Example:**
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
    case 'WORKFLOW_MODIFIED':
      console.log('Workflow modified:', data.data.workflow_json);
      break;
    case 'MODIFICATION_FINISHED':
      console.log('Modification completed!');
      eventSource.close();
      break;
    case 'MODIFICATION_ERROR':
      console.error('Error:', data.error);
      eventSource.close();
      break;
  }
};
```

### **Python Client Example:**
```python
import requests
import json

response = requests.post(
    'http://localhost:8000/modify',
    json={
        'existing_workflow_json': workflow_json,
        'modification_description': 'Add database logging'
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        event = json.loads(line.decode('utf-8'))
        print(f"Event: {event['type']}")
        
        if event['type'] == 'WORKFLOW_MODIFIED':
            modified_workflow = event['data']['workflow_json']
            print("Modified workflow received")
```

---

## 🚨 **Error Handling**

### **Common Error Types:**

**400 Bad Request:**
```json
{
  "detail": "Invalid workflow JSON structure"
}
```

**404 Not Found:**
```json
{
  "detail": "No iterations found for this workflow"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "LLM service unavailable"
}
```

### **SSE Error Events:**
```json
{
  "type": "MODIFICATION_ERROR",
  "workflow_id": "abc123",
  "error": "Invalid existing workflow structure",
  "timestamp": "2025-01-11T00:58:26.000Z"
}
```

---

## 🔧 **Validation**

All workflows are automatically validated with the following checks:
- ✅ Valid JSON structure
- ✅ Required fields present (`name`, `nodes`, `connections`)
- ✅ Node structure validation
- ✅ Connection integrity
- ✅ Workflow logic validation
- ✅ N8N compatibility

**Validation Response:**
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": ["Workflow should have at least one trigger node"]
}
```

---

## 🎯 **Best Practices**

### **For Modifications:**
- ✅ Provide clear, specific modification descriptions
- ✅ Use proper workflow IDs for tracking
- ✅ Test modified workflows in N8N before further iterations
- ✅ Keep modification descriptions under 1000 characters

### **For Iterations:**
- ✅ Include detailed testing feedback
- ✅ Mention specific issues encountered
- ✅ Separate feedback from additional requirements
- ✅ Use the same workflow_id for related iterations

### **Error Recovery:**
- ✅ Check validation results before deploying
- ✅ Monitor SSE error events
- ✅ Implement retry logic for network issues
- ✅ Fallback to original workflow on validation failures

---

## 📈 **Performance Considerations**

- **Average Response Time:** ~20-25 seconds per modification
- **Concurrent Requests:** Supported with unique operation IDs
- **Timeout:** 20 minutes for LLM operations
- **Rate Limiting:** Not currently implemented
- **Caching:** Workflow iterations are cached in memory

---

## 🔗 **Additional Endpoints**

### **Health Check**
**`GET /health`**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-11T00:58:26.000Z"
}
```

### **Get Workflow Feedback**
**`GET /feedback/{workflow_id}`**
Returns feedback history for a specific workflow.

---

## 📞 **Support**

For technical support or feature requests:
- **GitHub Issues:** [Project Repository]
- **Documentation:** This file
- **API Version:** 1.0
- **Last Updated:** January 2025

---

*This documentation covers the core workflow iteration functionality. For advanced features and upcoming enhancements, see the project roadmap in PRD.MD* 