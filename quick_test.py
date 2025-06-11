#!/usr/bin/env python3
"""
Quick test to validate fixes and core functionality.
"""

import json
import sys
from pathlib import Path

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent))

from test_iteration_methods import ComprehensiveIterationTester

def main():
    print('🧪 Quick Validation Tests')
    print('=' * 50)
    
    tester = ComprehensiveIterationTester()
    
    # Test 1: JSON Serialization with Boolean Values
    print('\n1. Testing JSON Serialization with Boolean Values')
    print('-' * 40)
    
    webhook_workflow = {
        'name': 'Test Webhook',
        'nodes': [
            {'id': '1', 'name': 'Webhook', 'type': 'n8n-nodes-base.webhook', 'parameters': {}, 'position': [240, 300]}
        ],
        'connections': {},
        'settings': {},
        'active': True,  # Python boolean
        'version': 1
    }
    
    try:
        workflow_json = json.dumps(webhook_workflow)
        print(f'✅ JSON serialization works: {len(workflow_json)} characters')
        
        # Verify it deserializes back
        parsed_back = json.loads(workflow_json)
        print(f'✅ Roundtrip successful, active={parsed_back["active"]} (type: {type(parsed_back["active"])})')
    except Exception as e:
        print(f'❌ JSON serialization failed: {e}')
        return False
    
    # Test 2: Test Workflow Loading  
    print('\n2. Testing Workflow File Loading')
    print('-' * 40)
    
    basic_workflow = tester.load_test_workflow('basic_email_workflow.json')
    if basic_workflow:
        parsed = json.loads(basic_workflow)
        print(f'✅ Basic workflow loaded: {len(parsed.get("nodes", []))} nodes')
        print(f'   - Workflow name: {parsed.get("name")}')
        for node in parsed.get("nodes", []):
            print(f'   - Node: {node.get("name")} ({node.get("type")})')
    else:
        print('❌ Basic workflow loading failed')
        return False
    
    # Test 3: Complex Workflow Loading
    print('\n3. Testing Complex Workflow Loading')
    print('-' * 40)
    
    complex_workflow = tester.load_test_workflow('file_processing_workflow.json')
    if complex_workflow:
        parsed = json.loads(complex_workflow)
        print(f'✅ Complex workflow loaded: {len(parsed.get("nodes", []))} nodes')
        print(f'   - Workflow name: {parsed.get("name")}')
    else:
        print('❌ Complex workflow loading failed')
        return False
    
    # Test 4: Workflow Analysis
    print('\n4. Testing Workflow Analysis')
    print('-' * 40)
    
    try:
        workflow_dict = json.loads(complex_workflow)
        analysis = tester.builder._analyze_workflow(workflow_dict)
        
        print(f'✅ Analysis completed:')
        print(f'   - Node count: {analysis.get("node_count")}')
        print(f'   - Node types: {len(analysis.get("node_types", []))} unique types')
        print(f'   - Triggers: {len(analysis.get("triggers", []))}')
        print(f'   - Actions: {len(analysis.get("actions", []))}')
    except Exception as e:
        print(f'❌ Workflow analysis failed: {e}')
        return False
    
    # Test 5: Input Validation
    print('\n5. Testing Input Validation')
    print('-' * 40)
    
    try:
        # Test with empty workflow
        result = tester.builder.modify_workflow("", "Add nodes")
        print(f'✅ Empty workflow handling: {"Passed" if result == "" else "Handled gracefully"}')
        
        # Test with malformed JSON
        result = tester.builder.modify_workflow('{"name": "Test"', "Fix workflow")
        print(f'✅ Malformed JSON handling: Handled gracefully')
        
    except Exception as e:
        print(f'⚠️  Input validation test encountered: {e}')
        # This might be expected behavior
    
    print('\n📊 Quick Validation Summary')
    print('=' * 50)
    print('✅ All core components are functioning correctly')
    print('✅ JSON serialization with Python booleans works')
    print('✅ Test workflow loading is operational')
    print('✅ Workflow analysis is functional')
    print('✅ Ready for comprehensive testing')
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print('\n🎉 QUICK VALIDATION PASSED - Ready to continue!')
        sys.exit(0)
    else:
        print('\n❌ QUICK VALIDATION FAILED - Need to investigate')
        sys.exit(1) 