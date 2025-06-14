import sys
import json
sys.path.append('.')
from n8n_builder.n8n_builder import N8NBuilder

# Simulate a typical reasoning LLM response with thinking tags and the correct JSON
reasoning_llm_response = '''<think>
The user wants to add an email node to send a notification when the workflow is completed. Looking at the current workflow structure:

1. webhook-trigger -> process-data -> webhook-response

To add an email node at the end, I need to:
1. Add the email node
2. Create a connection from process-data to the email node  
3. Modify the existing connection so webhook-response comes after the email node

The actions needed are:
- add_node for the email node
- add_connection from process-data to email-node
- modify_connection to redirect process-data from webhook-response to email-node
- add_connection from email-node to webhook-response

Let me structure this properly...
</think>

[
  {
    "action": "add_node",
    "details": {
      "node_id": "email-notification",
      "name": "Send Completion Email",
      "node_type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "elthosrpg@elthos.com",
        "subject": "Workflow Completed Successfully",
        "text": "The workflow has completed processing."
      },
      "position": [1000, 300]
    }
  },
  {
    "action": "add_connection",
    "details": {
      "source_node": "process-data",
      "target_node": "email-notification",
      "connection_type": "main",
      "index": 0
    }
  },
  {
    "action": "modify_connection",
    "details": {
      "source_node": "process-data",
      "old_target": "webhook-response",
      "new_target": "email-notification",
      "connection_type": "main"
    }
  },
  {
    "action": "add_connection",
    "details": {
      "source_node": "email-notification",
      "target_node": "webhook-response",
      "connection_type": "main",
      "index": 0
    }
  }
]'''

def test_enhanced_extraction():
    builder = N8NBuilder()
    
    print("=== TESTING ENHANCED JSON EXTRACTION ===")
    print(f"Response length: {len(reasoning_llm_response)}")
    print(f"Contains thinking tags: {'<think>' in reasoning_llm_response}")
    print()
    
    # Test the enhanced extraction
    extracted_json = builder._extract_json_from_response(reasoning_llm_response)
    
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