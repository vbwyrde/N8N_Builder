Here is comprehensive documentation to understand and build n8n workflow JSON structures. Here's a detailed guide:

# N8N Workflow JSON Structure Documentation

## 1. Basic Structure
An n8n workflow JSON consists of these main components:
```json
{
  "name": "Workflow Name",
  "nodes": [],
  "connections": {},
  "settings": {},
  "tags": [],
  "pinData": {},
  "versionId": "",
  "triggerCount": 0,
  "active": false
}
```

## 2. Node Structure
Each node in the `nodes` array follows this format:
```json
{
  "parameters": {},
  "name": "Node Name",
  "type": "n8n-nodes-base.nodetype",
  "typeVersion": 1,
  "position": [x, y],
  "id": "unique-node-id"
}
```

## 3. Connections Structure
Connections define how nodes link together:
```json
{
  "connections": {
    "Node1": {
      "main": [
        [
          {
            "node": "Node2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## 4. Common Parameters
Parameters vary by node type but commonly include:
- Authentication credentials
- API endpoints
- Data mapping
- Operation selection
- Input/output configuration

## 5. Building Guidelines

1. Node Positioning:
- Each node requires unique coordinates
- Recommended spacing: 200px horizontal, 100px vertical
```json
"position": [200, 100]
```

2. Node IDs:
- Must be unique
- Use UUID format or incremental IDs
- Referenced in connections

3. Connection Rules:
- Connect output (main) to input (main)
- Index starts at 0
- Multiple connections possible from one output

## 6. Example Workflow
Here's a simple HTTP Request -> Set workflow:

```json
{
  "name": "Simple HTTP Workflow",
  "nodes": [
    {
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET"
      },
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [250, 300],
      "id": "1"
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "processed_data",
              "value": "={{ $json.data }}"
            }
          ]
        }
      },
      "name": "Set",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [450, 300],
      "id": "2"
    }
  ],
  "connections": {
    "1": {
      "main": [
        [
          {
            "node": "2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {},
  "tags": [],
  "active": false
}
```

## 7. Special Considerations

1. Expression Syntax:
- Use `={{}}` for expressions
- Example: `={{ $json.data }}`

2. Error Handling:
```json
"continueOnFail": true,
"retryOnFail": {
  "enabled": true,
  "tries": 3
}
```

3. Credentials:
- Referenced by name
- Stored separately from workflow JSON
```json
"credentials": {
  "credentialType": {
    "name": "credential-name"
  }
}
```

4. Version Control:
- Include `versionId` for tracking
- Maintain typeVersion for nodes

This documentation should provide an LLM with the necessary structure and rules to generate valid n8n workflow JSON. Would you like me to elaborate on any specific aspect?