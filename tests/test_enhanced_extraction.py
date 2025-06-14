import sys
import json
sys.path.append('.')
from n8n_builder.n8n_builder import N8NBuilder

# Simulate the actual LLM response from LM Studio
actual_llm_response = '''<think>Okay, let's tackle this problem. The user wants to modify the existing n8n workflow by adding an email node that sends a message to mark@mark.com when the process completes.

First, I need to recall how n8n workflows work. The current setup has three nodes: Webhook Trigger, Process Data (a function node), and Webhook Response. The connections are from Webhook Trigger to Process Data, then from Process Data back to Webhook Response. 

The user wants an email sent after the process completes. So the email node should come after the Process Data node but before or instead of the Webhook Response. Wait, looking at the example they provided, when adding the email node at the end, they modified the connection from Process Data to point to the email node instead of Webhook Response. That makes sense because in their example, the original flow was Process Data -> Webhook Response, and after modification, it's Process Data -> Email Node.

So I need to add an email node. The correct node type for sending emails is "n8n-nodes-base.emailSend". The parameters should include "to" set to mark@mark.com, a subject like "Workflow Complete", maybe a message body. Position-wise, placing it after Process Data but before Webhook Response? Or perhaps instead of Webhook Response. Wait, in the current connections, Process Data's main output goes back to Webhook Response. So modifying that connection to point to the new Email Node would make sense.

So steps:
1. Add the email node with appropriate parameters and position.
2. Create a connection from Process Data (main) to Email Node (main).
3. Modify the existing connection from Process Data to Webhook Response, replacing it with the new Email Node connection.

Checking the example provided by the user: they added the email node at position [1000, 300], then connected Process Data's main index 0 to email-node's main index 0. Then modified the existing connection from Process Data (main) which was pointing to Webhook Response to now point to Email Node.

So applying that structure here. The current Workflow has Process Data connected back to Webhook Response. The new email node should be added after Process Data, replacing the webhook response part of the flow.

Therefore, the JSON array actions would be:
- Add the email node with parameters for to and subject.
- Add a connection from Process Data (main) to Email Node (main).
- Modify the existing connection from Process Data's main to Webhook Response to instead point to Email Node.

Need to ensure that all connections are updated correctly. Also, the position of the new email node should be after Process Data but before Webhook Response? Or maybe in line with it. The example had the email node at [1000, 300], which is probably below or next to the existing nodes. But exact positioning isn't critical as long as the connections are correct.

So the JSON actions would be an array with three elements:
1. add_node for the email node.
2. add_connection from Process Data to Email Node.
3. modify_connection changing the target of Process Data's main connection from Webhook Response to Email Node.

Double-checking the parameters: "to" should be mark@mark.com, subject maybe something like "Workflow Completed", and body optional. But the user didn't specify a message, so perhaps just the basics. The example had "user@example.com" as to, so we'll follow that structure.

So putting it all together in JSON format as per the required array.
</think>


[
  {"action":"add_node","details":{"node_id":"email-node","name":"Send Email","node_type":"n8n-nodes-base.emailSend","parameters":{"to":"mark@mark.com","subject":"Workflow Complete"},"position":[1000,300]}},
  {"action":"add_connection","details":{"source_node":"process-data","target_node":"email-node","connection_type":"main","index":0}},
  {"action":"modify_connection","details":{"source_node":"process-data","old_target":"webhook-response","new_target":"email-node"}}
]'''

def test_enhanced_extraction():
    builder = N8NBuilder()
    
    print("=== TESTING ENHANCED JSON EXTRACTION ===")
    print(f"Response length: {len(actual_llm_response)}")
    print(f"Contains thinking tags: {'<think>' in actual_llm_response}")
    print()
    
    # Test the enhanced extraction
    extracted_json = builder._extract_json_from_response(actual_llm_response)
    
    print(f"Extracted JSON length: {len(extracted_json)}")
    print(f"Extracted JSON: {extracted_json}")
    print()
    
    if extracted_json:
        try:
            parsed = json.loads(extracted_json)
            print("✅ JSON parsing successful!")
            print(f"Number of modifications: {len(parsed)}")
            
            # Test validation
            for i, mod in enumerate(parsed):
                is_valid = builder._validate_modification_structure(mod)
                print(f"Modification {i+1}: {mod.get('action')} - Valid: {is_valid}")
                if is_valid:
                    details = mod.get('details', {})
                    if mod.get('action') == 'add_node':
                        print(f"  Adding node: {details.get('name')} ({details.get('node_type')})")
                    elif mod.get('action') == 'add_connection':
                        print(f"  Adding connection: {details.get('source_node')} -> {details.get('target_node')}")
                    elif mod.get('action') == 'modify_connection':
                        print(f"  Modifying connection: {details.get('source_node')} from {details.get('old_target')} to {details.get('new_target')}")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
    else:
        print("❌ No JSON extracted")

if __name__ == "__main__":
    test_enhanced_extraction() 