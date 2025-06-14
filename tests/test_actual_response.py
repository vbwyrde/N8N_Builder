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

The example provided by the user replaces the connection from Process Data to the new email node, removing the original connection to Webhook Response. That makes sense if the goal is to have the email sent upon completion instead of the webhook response. So modifying the existing connection from Process Data's main to point to the email node instead of the webhook response.

So the steps are:

1. Add the email node.
2. Connect Process Data to Email node.
3. Modify the existing connection from Process Data to Webhook Response, changing it to Email node.

I need to structure these as three separate actions in a JSON array: add_node, add_connection, modify_connection.

Check for valid node types and parameters. The emailSend node is correct. Position should be after the existing nodes. Maybe [1200, 300] for the email node's position.

Also, ensure that all connections are properly updated. The original workflow has Process Data connected to Webhook Response. After modification, it connects to Email node instead. So the modify_connection action is necessary to redirect where the data goes after processing.

Testing this in my mind: the flow would be Trigger → Process → Email, and the Webhook Response is no longer part of the main connection. But wait, does the webhook response need to still exist? The user's example replaces it, so perhaps the email takes over the completion step, and the webhook response might not be needed anymore. Or maybe the email is an additional action after processing.

Wait, in the original workflow, Process Data connects back to Webhook Response. So when the function node finishes, it sends data back to the HTTP response node, which probably closes the webhook connection. Now, adding the email node would mean that after processing, we send the email and then maybe still need to respond via webhook? Or does modifying the connection to point to the email node instead of the webhook response remove the response part?

In the user's example, they modified the connection from Process Data to replace Webhook Response with Email. So in their case, the flow becomes Trigger → Process → Email, and the HTTP response is no longer connected. But maybe that's acceptable if the goal is just to send an email upon completion. Alternatively, perhaps both should be connected in series. However, the user's example shows replacing, so I'll follow that.

Therefore, the JSON actions would be:

- Add the email node with parameters and position.
- Add a connection from Process Data to Email.
- Modify the existing connection from Process Data to point to Email instead of Webhook Response.

Yes, that should integrate the new node into the workflow correctly without leaving any nodes isolated. All connections are updated properly.
</think>


```json
[
  {
    "action": "add_node",
    "details": {
      "node_id": "email-node",
      "name": "Send Email",
      "node_type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "mark@mark.com",
        "subject": "Workflow Complete"
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
      "new_target": "email-node"
    }
  }
]
```'''

def test_actual_response():
    print("=== TESTING ACTUAL LLM RESPONSE ===")
    print(f"Response length: {len(actual_llm_response)}")
    print(f"Contains thinking tags: {'<think>' in actual_llm_response}")
    print(f"Contains code blocks: {'```' in actual_llm_response}")
    print()
    
    builder = N8NBuilder()
    
    # Test the JSON extraction
    print("Testing JSON extraction...")
    extracted_json = builder._extract_json_from_response(actual_llm_response)
    
    print(f"Extracted JSON length: {len(extracted_json) if extracted_json else 0}")
    print(f"Extracted JSON: {extracted_json}")
    print()
    
    if extracted_json:
        try:
            parsed = json.loads(extracted_json)
            print("✅ JSON parsing successful!")
            print(f"Number of modifications: {len(parsed)}")
            print()
            
            # Test validation
            for i, mod in enumerate(parsed):
                is_valid = builder._validate_modification_structure(mod)
                print(f"Modification {i+1}: {mod.get('action')} - Valid: {is_valid}")
                if is_valid:
                    details = mod.get('details', {})
                    if mod.get('action') == 'add_node':
                        print(f"  Adding node: {details.get('name')} ({details.get('node_type')})")
                        print(f"  Parameters: {details.get('parameters')}")
                    elif mod.get('action') == 'add_connection':
                        print(f"  Adding connection: {details.get('source_node')} -> {details.get('target_node')}")
                    elif mod.get('action') == 'modify_connection':
                        print(f"  Modifying connection: {details.get('source_node')} from {details.get('old_target')} to {details.get('new_target')}")
                print()
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return False
    else:
        print("❌ No JSON extracted")
        return False

if __name__ == "__main__":
    success = test_actual_response()
    if success:
        print("✅ JSON extraction working correctly!")
    else:
        print("❌ JSON extraction failed!")
        sys.exit(1) 