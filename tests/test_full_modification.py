#!/usr/bin/env python3

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from n8n_builder.n8n_builder import N8NBuilder

# The actual LLM response from your logs
actual_llm_response = '''<think>
Okay, let's tackle this problem step by step. The user wants to modify the existing n8n workflow to send an email to mark@mark.com when the process is completed. First, I need to understand the current workflow structure.

Looking at the provided JSON, there are three nodes: Webhook Trigger, Process Data (a function node), and Webhook Response. The connections show that the Webhook Trigger's main output goes to Process Data, which then connects back to Webhook Response. So the flow is Trigger → Process → Response.

The user's feedback requires adding an email node at the end of this workflow. The example given shows how to add a new node and modify existing connections. I need to replicate that structure here.

First, I'll use the "add_node" action to insert the email node. The name should be "Send Email", using the n8n-nodes-base.emailSend type. Parameters include "to": "mark@mark.com", subject: "Workflow Complete". Position-wise, it should come after the Process Data node. Maybe position [1200, 300] to place it below and a bit to the right.

Next, I need to add a connection from Process Data's main output to the new email node. The source is "process-data", target is "email-node", type "main", index 0. That's an "add_connection" action.

Then, modify the existing connection from Process Data to Webhook Response. The current connection in the workflow connects Process Data's main to Webhook Response. So I need to change that to point to the new email node instead. Using "modify_connection", source_node is "process-data", old_target is "webhook-response", new_target is "email-node".

Wait, but in the original connections, the Process Data's main connects to Webhook Response. The user wants the email sent when the process completes, so perhaps after processing data, we should send an email and then respond via webhook? Or replace the webhook response with the email?

The example provided by the user replaces the connection from Process Data to the new email node, removing the original connection to Webhook Response. That makes sense if the goal is to have the email sent upon completion instead of the webhook response. So modifying the existing connection from Process Data's main to point to the email node instead of the webhook response should work.

Let me structure this properly:

1. Add the email node with proper parameters
2. Add a connection from Process Data to the email node
3. Modify the existing connection from Process Data to point to the email node instead of Webhook Response

Actually, looking at this again, I think the user wants to add the email step but still maintain the webhook response. So the flow should be: Trigger → Process → Email → Response. In that case, I should:

1. Add the email node
2. Modify the connection from Process Data to point to the email node
3. Add a connection from the email node to the webhook response

But the example shows just replacing the connection, so I'll go with that approach for simplicity.
</think>

[
  {
    "action": "add_node",
    "details": {
      "node_id": "email-node",
      "name": "Send Email",
      "node_type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "mark@mark.com",
        "subject": "Workflow Complete",
        "text": "The workflow has completed successfully."
      },
      "position": [1200, 300]
    }
  },
  {
    "action": "add_connection",
    "details": {
      "source_node": "process-data",
      "target_node": "email-node",
      "connection_type": "main",
      "index": 0
    }
  },
  {
    "action": "modify_connection",
    "details": {
      "source_node": "process-data",
      "old_target": "webhook-response",
      "new_target": "email-node",
      "connection_type": "main"
    }
  }
]'''

# Original test workflow
original_workflow = {
  "name": "Basic Webhook Workflow",
  "nodes": [
    {
      "id": "webhook-trigger",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "basic-workflow",
        "responseMode": "responseNode"
      },
      "position": [
        250,
        300
      ]
    },
    {
      "id": "process-data",
      "name": "Process Data",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// Process incoming data\nconst data = $input.first().json;\nreturn [{ json: { ...data, processed: true, timestamp: new Date().toISOString() } }];"
      },
      "position": [
        500,
        300
      ]
    },
    {
      "id": "webhook-response",
      "name": "Webhook Response",
      "type": "n8n-nodes-base.httpResponse",
      "parameters": {
        "responseMode": "json",
        "responseBody": "{\"status\": \"success\", \"message\": \"Data processed\"}"
      },
      "position": [
        750,
        300
      ]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "Process Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Data": {
      "main": [
        [
          {
            "node": "Webhook Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {},
  "active": True,
  "version": 1
}

def test_full_modification():
    """Test the full workflow modification process with the actual LLM response."""
    
    # The actual LLM response from your logs
    actual_llm_response = '''<think>
Okay, let's tackle this problem step by step. The user wants to modify the existing n8n workflow to send an email to mark@mark.com when the process is completed. First, I need to understand the current workflow structure.

Looking at the provided JSON, there are three nodes: Webhook Trigger, Process Data (a function node), and Webhook Response. The connections show that the Webhook Trigger's main output goes to Process Data, which then connects back to Webhook Response. So the flow is Trigger → Process → Response.

The user's feedback requires adding an email node at the end of this workflow. The example given shows how to add a new node and modify existing connections. I need to replicate that structure here.

First, I'll use the "add_node" action to insert the email node. The name should be "Send Email", using the n8n-nodes-base.emailSend type. Parameters include "to": "mark@mark.com", subject: "Workflow Complete". Position-wise, it should come after the Process Data node. Maybe position [1200, 300] to place it below and a bit to the right.

Next, I need to add a connection from Process Data's main output to the new email node. The source is "process-data", target is "email-node", type "main", index 0. That's an "add_connection" action.

Then, modify the existing connection from Process Data to Webhook Response. The current connection in the workflow connects Process Data's main to Webhook Response. So I need to change that to point to the new email node instead. Using "modify_connection", source_node is "process-data", old_target is "webhook-response", new_target is "email-node".

Wait, but in the original connections, the Process Data's main connects to Webhook Response. The user wants the email sent when the process completes, so perhaps after processing data, we should send an email and then respond via webhook? Or replace the webhook response with the email?

The example provided by the user replaces the connection from Process Data to the new email node, removing the original connection to Webhook Response. That makes sense if the goal is to have the email sent upon completion instead of the webhook response. So modifying the existing connection from Process Data's main to point to the email node instead of the webhook response should work.

Let me structure this properly:

1. Add the email node with proper parameters
2. Add a connection from Process Data to the email node
3. Modify the existing connection from Process Data to point to the email node instead of Webhook Response

Actually, looking at this again, I think the user wants to add the email step but still maintain the webhook response. So the flow should be: Trigger → Process → Email → Response. In that case, I should:

1. Add the email node
2. Modify the connection from Process Data to point to the email node
3. Add a connection from the email node to the webhook response

But the example shows just replacing the connection, so I'll go with that approach for simplicity.
</think>

[
  {
    "action": "add_node",
    "details": {
      "node_id": "email-node",
      "name": "Send Email",
      "node_type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "mark@mark.com",
        "subject": "Workflow Complete",
        "text": "The workflow has completed successfully."
      },
      "position": [1200, 300]
    }
  },
  {
    "action": "add_connection",
    "details": {
      "source_node": "process-data",
      "target_node": "email-node",
      "connection_type": "main",
      "index": 0
    }
  },
  {
    "action": "modify_connection",
    "details": {
      "source_node": "process-data",
      "old_target": "webhook-response",
      "new_target": "email-node",
      "connection_type": "main"
    }
  }
]'''

    # Original workflow
    original_workflow = {
        "name": "Basic Webhook Workflow",
        "nodes": [
            {
                "id": "webhook-trigger",
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "parameters": {
                    "httpMethod": "POST",
                    "path": "basic-workflow",
                    "responseMode": "responseNode"
                },
                "position": [250, 300]
            },
            {
                "id": "process-data",
                "name": "Process Data",
                "type": "n8n-nodes-base.function",
                "parameters": {
                    "functionCode": "// Process incoming data\nconst data = $input.first().json;\nreturn [{ json: { ...data, processed: true, timestamp: new Date().toISOString() } }];"
                },
                "position": [500, 300]
            },
            {
                "id": "webhook-response",
                "name": "Webhook Response",
                "type": "n8n-nodes-base.httpResponse",
                "parameters": {
                    "responseMode": "json",
                    "responseBody": "{\"status\": \"success\", \"message\": \"Data processed\"}"
                },
                "position": [750, 300]
            }
        ],
        "connections": {
            "Webhook Trigger": {
                "main": [
                    [
                        {
                            "node": "Process Data",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Process Data": {
                "main": [
                    [
                        {
                            "node": "Webhook Response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {},
        "active": True,
        "version": 1
    }

    print("Testing full modification process...")
    
    # Step 1: Test JSON extraction
    print("Step 1: Extract JSON from LLM response...")
    builder = N8NBuilder()
    extracted_json = builder._extract_json_from_response(actual_llm_response)
    
    if extracted_json:
        print(f"[OK] Extracted JSON: {len(extracted_json)} characters")
    else:
        print("[FAIL] Could not extract JSON from response")
        return None, False
    
    # Step 2: Apply modifications
    print("\nStep 2: Apply modifications to workflow...")
    modified_workflow = builder._apply_workflow_modifications(original_workflow, actual_llm_response)
    
    print(f"Modified workflow nodes: {len(modified_workflow.get('nodes', []))}")
    print(f"Modified connections: {list(modified_workflow.get('connections', {}).keys())}")
    
    # Step 3: Validate the result
    print("\n=== CHANGES ANALYSIS ===")
    original_nodes = [node['name'] for node in original_workflow['nodes']]
    modified_nodes = [node['name'] for node in modified_workflow['nodes']]
    
    print(f"Original nodes: {original_nodes}")
    print(f"Modified nodes: {modified_nodes}")
    
    new_nodes = [node for node in modified_nodes if node not in original_nodes]
    if new_nodes:
        print(f"[OK] New nodes added: {new_nodes}")
    else:
        print("[WARN] No new nodes added")
    
    print(f"\nOriginal connections:")
    for source, targets in original_workflow['connections'].items():
        for conn_type, target_lists in targets.items():
            for target_list in target_lists:
                for target in target_list:
                    print(f"  {source} -> {target['node']} ({conn_type})")
    
    print(f"\nModified connections:")
    for source, targets in modified_workflow['connections'].items():
        for conn_type, target_lists in targets.items():
            for target_list in target_lists:
                for target in target_list:
                    print(f"  {source} -> {target['node']} ({conn_type})")
    
    # Step 4: Test validation
    print("\n=== VALIDATION TEST ===")
    modified_workflow_json = json.dumps(modified_workflow)
    is_valid = builder.validate_workflow(modified_workflow_json)
    
    if is_valid:
        print("Modified workflow validation: [OK] VALID")
    else:
        print("Modified workflow validation: [FAIL] INVALID")
        print("Validation failed - this explains why the workflow isn't updating!")
    
    return modified_workflow, is_valid

if __name__ == "__main__":
    print("=== TESTING FULL WORKFLOW MODIFICATION ===")
    
    # Load original workflow
    with open("projects/test-1/test-workflow.json", "r") as f:
        original_workflow = json.load(f)
    
    print(f"Original workflow nodes: {len(original_workflow['nodes'])}")
    print(f"Original connections: {list(original_workflow['connections'].keys())}")
    print()
    
    # Test the modification
    modified_workflow, is_valid = test_full_modification()
    
    if not is_valid:
        print("\n[FAIL] Validation failed - this is why the workflow isn't updating!")
        print("The system reverts to the original workflow when validation fails.")
    else:
        print("\n[OK] Validation passed - workflow should update successfully!") 