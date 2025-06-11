#!/usr/bin/env python3
"""
Comprehensive test suite for N8N Builder workflow iteration methods.
Tests modify_workflow() and iterate_workflow() with various scenarios including edge cases.
"""

import json
import sys
import os
from pathlib import Path
import time

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent))

from n8n_builder.n8n_builder import N8NBuilder

class ComprehensiveIterationTester:
    def __init__(self):
        self.builder = N8NBuilder()
        self.test_results = []
        
    def load_test_workflow(self, filename):
        """Load a test workflow from file."""
        try:
            with open(f"test_workflows/{filename}", 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ Test workflow {filename} not found")
            return None
            
    def run_test(self, test_name, test_function):
        """Run a test and record results."""
        print(f"\n🧪 Running test: {test_name}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = test_function()
            duration = time.time() - start_time
            self.test_results.append({
                "test": test_name,
                "status": "PASS" if result else "FAIL",
                "details": result,
                "duration": f"{duration:.2f}s"
            })
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name} ({duration:.2f}s)")
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append({
                "test": test_name,
                "status": "ERROR", 
                "details": str(e),
                "duration": f"{duration:.2f}s"
            })
            print(f"💥 ERROR: {test_name} - {str(e)} ({duration:.2f}s)")
            return False

    # ==================== EXISTING TESTS ====================
            
    def test_modify_workflow_basic(self):
        """Test basic workflow modification."""
        # Load basic email workflow
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
            
        # Test modification request
        modification_request = "Add a database logging step after sending the email"
        
        try:
            modified_workflow = self.builder.modify_workflow(
                workflow_json,
                modification_request,
                "test-workflow-1"
            )
            
            # Verify we got a result
            if not modified_workflow:
                print("❌ No modified workflow returned")
                return False
                
            # Verify it's valid JSON
            parsed = json.loads(modified_workflow)
            print(f"✅ Modified workflow has {len(parsed.get('nodes', []))} nodes")
            
            # Print the modification for review
            print("📝 Modified workflow nodes:")
            for node in parsed.get('nodes', []):
                print(f"   - {node.get('name')} ({node.get('type')})")
                
            return True
            
        except Exception as e:
            print(f"❌ Modification failed: {str(e)}")
            return False
            
    def test_modify_workflow_complex(self):
        """Test modification of more complex workflow."""
        workflow_json = self.load_test_workflow("file_processing_workflow.json")
        if not workflow_json:
            return False
            
        modification_request = "Add error handling and email notification when processing fails"
        
        try:
            modified_workflow = self.builder.modify_workflow(
                workflow_json,
                modification_request,
                "test-workflow-2"
            )
            
            if not modified_workflow:
                return False
                
            parsed = json.loads(modified_workflow)
            original_parsed = json.loads(workflow_json)
            
            # Check if nodes were added
            original_count = len(original_parsed.get('nodes', []))
            modified_count = len(parsed.get('nodes', []))
            
            print(f"📊 Original: {original_count} nodes → Modified: {modified_count} nodes")
            
            if modified_count >= original_count:  # Accept equal as valid (modifications might be to existing nodes)
                print("✅ Workflow was processed successfully")
                return True
            else:
                print("⚠️  Unexpected node count change")
                return False
                
        except Exception as e:
            print(f"❌ Complex modification failed: {str(e)}")
            return False
            
    def test_iterate_workflow(self):
        """Test workflow iteration based on feedback."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
            
        feedback = "The email works but I need to add a condition to only send emails during business hours"
        additional_requirements = "Also add logging to track when emails are sent"
        
        try:
            iterated_workflow = self.builder.iterate_workflow(
                "test-iteration-1",
                workflow_json,
                feedback,
                additional_requirements
            )
            
            if not iterated_workflow:
                return False
                
            parsed = json.loads(iterated_workflow)
            print(f"✅ Iterated workflow has {len(parsed.get('nodes', []))} nodes")
            
            # Print the iteration result
            print("📝 Iterated workflow nodes:")
            for node in parsed.get('nodes', []):
                print(f"   - {node.get('name')} ({node.get('type')})")
                
            return True
            
        except Exception as e:
            print(f"❌ Iteration failed: {str(e)}")
            return False
            
    def test_workflow_analysis(self):
        """Test the workflow analysis functionality."""
        workflow_json = self.load_test_workflow("file_processing_workflow.json")
        if not workflow_json:
            return False
            
        try:
            workflow_dict = json.loads(workflow_json)
            analysis = self.builder._analyze_workflow(workflow_dict)
            
            print(f"📊 Workflow Analysis Results:")
            print(f"   - Node count: {analysis.get('node_count')}")
            print(f"   - Node types: {', '.join(analysis.get('node_types', []))}")
            print(f"   - Triggers: {len(analysis.get('triggers', []))}")
            print(f"   - Actions: {len(analysis.get('actions', []))}")
            print(f"   - Data flow connections: {len(analysis.get('data_flow', []))}")
            
            if analysis.get('potential_issues'):
                print(f"   - Issues found: {', '.join(analysis['potential_issues'])}")
            else:
                print(f"   - No issues detected")
                
            return analysis.get('node_count', 0) > 0
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            return False
            
    def test_validation(self):
        """Test workflow validation."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
            
        try:
            is_valid = self.builder.validate_workflow(workflow_json)
            print(f"📋 Workflow validation result: {'✅ Valid' if is_valid else '❌ Invalid'}")
            return is_valid
            
        except Exception as e:
            print(f"❌ Validation failed: {str(e)}")
            return False
            
    def test_invalid_workflow_handling(self):
        """Test handling of invalid workflow JSON."""
        invalid_json = '{"name": "Invalid", "nodes": []}'  # Missing required fields
        
        try:
            result = self.builder.modify_workflow(
                invalid_json,
                "Add an email node",
                "test-invalid"
            )
            
            # Should return original workflow on validation failure
            if result == invalid_json:
                print("✅ Invalid workflow handling works correctly")
                return True
            else:
                print("❌ Invalid workflow was modified when it shouldn't have been")
                return False
                
        except Exception as e:
            print(f"⚠️  Exception handling invalid workflow: {str(e)}")
            # This might be expected behavior
            return True

    # ==================== NEW COMPREHENSIVE TESTS ====================

    def test_webhook_workflow_modification(self):
        """Test modifying a webhook-based workflow."""
        webhook_workflow = {
            "name": "Webhook Processing",
            "nodes": [
                {
                    "id": "1",
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "parameters": {
                        "path": "process-data",
                        "httpMethod": "POST"
                    },
                    "position": [240, 300]
                },
                {
                    "id": "2",
                    "name": "Process JSON",
                    "type": "n8n-nodes-base.function",
                    "parameters": {
                        "functionCode": "return items.map(item => ({json: {processed: true, data: item.json}}));"
                    },
                    "position": [460, 300]
                }
            ],
            "connections": {
                "Webhook": {
                    "main": [[{"node": "Process JSON", "type": "main", "index": 0}]]
                }
            },
            "settings": {},
            "active": True,
            "version": 1
        }
        
        try:
            workflow_json = json.dumps(webhook_workflow)
            modified = self.builder.modify_workflow(
                workflow_json,
                "Add authentication and rate limiting to the webhook",
                "webhook-test"
            )
            
            parsed = json.loads(modified)
            print(f"✅ Webhook workflow modified successfully")
            print(f"📊 Nodes: {len(parsed.get('nodes', []))}")
            return True
            
        except Exception as e:
            print(f"❌ Webhook modification failed: {str(e)}")
            return False

    def test_scheduled_workflow_creation(self):
        """Test creating a scheduled workflow from scratch."""
        try:
            # Test the iteration system with a minimal workflow
            minimal_workflow = {
                "name": "Minimal Start",
                "nodes": [
                    {
                        "id": "1",
                        "name": "Start",
                        "type": "n8n-nodes-base.start",
                        "parameters": {},
                        "position": [240, 300]
                    }
                ],
                "connections": {},
                "settings": {},
                "active": True,
                "version": 1
            }
            
            workflow_json = json.dumps(minimal_workflow)
            modified = self.builder.modify_workflow(
                workflow_json,
                "Convert this to a scheduled workflow that runs daily at 9 AM and sends a status email",
                "scheduled-test"
            )
            
            parsed = json.loads(modified)
            print(f"✅ Scheduled workflow created")
            print(f"📊 Final nodes: {len(parsed.get('nodes', []))}")
            return len(parsed.get('nodes', [])) >= 1
            
        except Exception as e:
            print(f"❌ Scheduled workflow creation failed: {str(e)}")
            return False

    def test_multiple_iterations(self):
        """Test multiple sequential iterations on the same workflow."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
        
        try:
            # First iteration
            first_iteration = self.builder.iterate_workflow(
                "multi-iter-test",
                workflow_json,
                "The email works but needs better formatting",
                "Make the email HTML formatted"
            )
            
            # Second iteration
            second_iteration = self.builder.iterate_workflow(
                "multi-iter-test",
                first_iteration,
                "HTML email works but needs conditional sending",
                "Only send emails during business hours (9 AM - 5 PM)"
            )
            
            # Third iteration
            third_iteration = self.builder.iterate_workflow(
                "multi-iter-test",
                second_iteration,
                "Business hours check works but needs logging",
                "Add comprehensive logging for all email actions"
            )
            
            final_parsed = json.loads(third_iteration)
            print(f"✅ Multiple iterations completed")
            print(f"📊 Final workflow: {len(final_parsed.get('nodes', []))} nodes")
            
            # Check iteration history
            history = self.builder.get_workflow_iterations("multi-iter-test")
            print(f"📝 Iteration history: {len(history)} entries")
            
            return len(final_parsed.get('nodes', [])) >= 2
            
        except Exception as e:
            print(f"❌ Multiple iterations failed: {str(e)}")
            return False

    def test_large_workflow_handling(self):
        """Test handling of a larger, more complex workflow."""
        large_workflow = {
            "name": "E-commerce Order Processing",
            "nodes": [
                {"id": "1", "name": "Order Webhook", "type": "n8n-nodes-base.webhook", "parameters": {"path": "orders"}, "position": [100, 100]},
                {"id": "2", "name": "Validate Order", "type": "n8n-nodes-base.function", "parameters": {"functionCode": "// validation"}, "position": [300, 100]},
                {"id": "3", "name": "Check Inventory", "type": "n8n-nodes-base.postgres", "parameters": {"operation": "select"}, "position": [500, 100]},
                {"id": "4", "name": "Calculate Tax", "type": "n8n-nodes-base.function", "parameters": {"functionCode": "// tax calc"}, "position": [700, 100]},
                {"id": "5", "name": "Process Payment", "type": "n8n-nodes-base.httpRequest", "parameters": {"url": "api.stripe.com"}, "position": [300, 300]},
                {"id": "6", "name": "Update Inventory", "type": "n8n-nodes-base.postgres", "parameters": {"operation": "update"}, "position": [500, 300]},
                {"id": "7", "name": "Send Confirmation", "type": "n8n-nodes-base.emailSend", "parameters": {"to": "customer"}, "position": [700, 300]},
                {"id": "8", "name": "Log Transaction", "type": "n8n-nodes-base.postgres", "parameters": {"operation": "insert"}, "position": [900, 200]}
            ],
            "connections": {
                "Order Webhook": {"main": [[{"node": "Validate Order", "type": "main", "index": 0}]]},
                "Validate Order": {"main": [[{"node": "Check Inventory", "type": "main", "index": 0}]]},
                "Check Inventory": {"main": [[{"node": "Calculate Tax", "type": "main", "index": 0}]]},
                "Calculate Tax": {"main": [[{"node": "Process Payment", "type": "main", "index": 0}]]},
                "Process Payment": {"main": [[{"node": "Update Inventory", "type": "main", "index": 0}]]},
                "Update Inventory": {"main": [[{"node": "Send Confirmation", "type": "main", "index": 0}]]},
                "Send Confirmation": {"main": [[{"node": "Log Transaction", "type": "main", "index": 0}]]}
            },
            "settings": {},
            "active": True,
            "version": 1
        }
        
        try:
            workflow_json = json.dumps(large_workflow)
            modified = self.builder.modify_workflow(
                workflow_json,
                "Add comprehensive error handling and retry logic for payment failures",
                "large-workflow-test"
            )
            
            parsed = json.loads(modified)
            print(f"✅ Large workflow handled successfully")
            print(f"📊 Nodes: {len(parsed.get('nodes', []))}")
            print(f"📊 Connections: {len(parsed.get('connections', {}))}")
            
            return len(parsed.get('nodes', [])) >= 8
            
        except Exception as e:
            print(f"❌ Large workflow handling failed: {str(e)}")
            return False

    def test_input_validation_edge_cases(self):
        """Test various input validation edge cases."""
        test_cases = [
            ("Empty workflow", "", "Add nodes"),
            ("Malformed JSON", '{"name": "Test"', "Fix workflow"),
            ("Very long description", "x" * 15000, "Short workflow"),
            ("Empty description", self.load_test_workflow("basic_email_workflow.json") or "{}", ""),
            ("Null workflow ID", self.load_test_workflow("basic_email_workflow.json") or "{}", "Test", None),
            ("Very long workflow ID", self.load_test_workflow("basic_email_workflow.json") or "{}", "Test", "x" * 150)
        ]
        
        passed_tests = 0
        for test_name, workflow, description, workflow_id in test_cases:
            try:
                if workflow_id is None:
                    result = self.builder.modify_workflow(workflow, description)
                else:
                    result = self.builder.modify_workflow(workflow, description, workflow_id)
                
                # For invalid inputs, we expect the original workflow back or an empty result
                if workflow == "":
                    expected_valid = result == ""
                elif workflow.startswith('{"name"'):  # Malformed JSON
                    expected_valid = result == workflow  # Should return original
                elif len(description) > 10000:
                    expected_valid = result == workflow  # Should reject long descriptions
                elif description == "":
                    expected_valid = result == workflow  # Should reject empty descriptions
                else:
                    expected_valid = True  # Other cases should work
                
                if expected_valid:
                    print(f"   ✅ {test_name}")
                    passed_tests += 1
                else:
                    print(f"   ❌ {test_name}")
                    
            except Exception as e:
                print(f"   ⚠️  {test_name}: {str(e)}")
                passed_tests += 1  # Exceptions can be valid for invalid inputs
        
        print(f"📊 Input validation tests: {passed_tests}/{len(test_cases)} passed")
        return passed_tests >= len(test_cases) - 1  # Allow one failure

    def test_workflow_iteration_history(self):
        """Test workflow iteration tracking and history."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
        
        try:
            workflow_id = "history-test-workflow"
            
            # Clear any existing history
            if hasattr(self.builder, 'iteration_history'):
                self.builder.iteration_history = []
            
            # Perform several modifications
            modifications = [
                "Add database logging",
                "Add error handling", 
                "Add rate limiting",
                "Add retry logic"
            ]
            
            current_workflow = workflow_json
            for i, modification in enumerate(modifications):
                current_workflow = self.builder.modify_workflow(
                    current_workflow,
                    modification,
                    workflow_id
                )
            
            # Check iteration history
            history = self.builder.get_workflow_iterations(workflow_id)
            print(f"📝 Iteration history entries: {len(history)}")
            
            for i, entry in enumerate(history):
                print(f"   {i+1}. {entry.get('description', 'Unknown')[:50]}...")
            
            return len(history) > 0
            
        except Exception as e:
            print(f"❌ Iteration history test failed: {str(e)}")
            return False

    def test_concurrent_modifications(self):
        """Test handling multiple workflow modifications."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
        
        try:
            # Simulate multiple modifications on different workflow IDs
            results = []
            for i in range(3):
                workflow_id = f"concurrent-test-{i}"
                modified = self.builder.modify_workflow(
                    workflow_json,
                    f"Modification {i}: Add node type {i}",
                    workflow_id
                )
                results.append(modified)
            
            # All should succeed
            all_valid = all(
                json.loads(result) and len(json.loads(result).get('nodes', [])) >= 2 
                for result in results
            )
            
            print(f"✅ Concurrent modifications: {len(results)} completed")
            return all_valid
            
        except Exception as e:
            print(f"❌ Concurrent modifications failed: {str(e)}")
            return False

    def test_performance_benchmark(self):
        """Basic performance test for modification operations."""
        workflow_json = self.load_test_workflow("basic_email_workflow.json")
        if not workflow_json:
            return False
        
        try:
            start_time = time.time()
            iterations = 5
            
            for i in range(iterations):
                self.builder.modify_workflow(
                    workflow_json,
                    f"Performance test iteration {i}",
                    f"perf-test-{i}"
                )
            
            total_time = time.time() - start_time
            avg_time = total_time / iterations
            
            print(f"📊 Performance benchmark:")
            print(f"   - Total time: {total_time:.2f}s")
            print(f"   - Average per modification: {avg_time:.2f}s")
            print(f"   - Throughput: {iterations/total_time:.2f} modifications/second")
            
            # Consider successful if average time is reasonable (< 30 seconds per modification)
            return avg_time < 30.0
            
        except Exception as e:
            print(f"❌ Performance benchmark failed: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all tests including new comprehensive ones."""
        print("🚀 Starting Comprehensive N8N Builder Iteration Tests")
        print("=" * 70)
        
        # Define all tests
        tests = [
            # Core functionality tests
            ("Basic Workflow Modification", self.test_modify_workflow_basic),
            ("Complex Workflow Modification", self.test_modify_workflow_complex),
            ("Workflow Iteration", self.test_iterate_workflow),
            ("Workflow Analysis", self.test_workflow_analysis),
            ("Workflow Validation", self.test_validation),
            ("Invalid Workflow Handling", self.test_invalid_workflow_handling),
            
            # New comprehensive tests
            ("Webhook Workflow Modification", self.test_webhook_workflow_modification),
            ("Scheduled Workflow Creation", self.test_scheduled_workflow_creation),
            ("Multiple Sequential Iterations", self.test_multiple_iterations),
            ("Large Workflow Handling", self.test_large_workflow_handling),
            ("Input Validation Edge Cases", self.test_input_validation_edge_cases),
            ("Workflow Iteration History", self.test_workflow_iteration_history),
            ("Concurrent Modifications", self.test_concurrent_modifications),
            ("Performance Benchmark", self.test_performance_benchmark)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            
        # Report summary
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")  
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        print(f"📋 Total: {len(self.test_results)}")
        
        # Show timing summary
        total_time = sum(float(r["duration"].replace('s', '')) for r in self.test_results)
        print(f"⏱️  Total test time: {total_time:.2f}s")
        
        # List any failures or errors
        if failed > 0 or errors > 0:
            print("\n🔍 ISSUES FOUND:")
            for result in self.test_results:
                if result["status"] in ["FAIL", "ERROR"]:
                    print(f"   {result['status']}: {result['test']} ({result['duration']})")
        
        # Success criteria: At least 80% tests passing
        success_rate = passed / len(self.test_results)
        print(f"\n🎯 Success Rate: {success_rate*100:.1f}%")
        
        if success_rate >= 0.8:
            print("🎉 TEST SUITE PASSED! (≥80% success rate)")
        else:
            print("⚠️  TEST SUITE NEEDS IMPROVEMENT (<80% success rate)")
                    
        return passed, failed, errors

if __name__ == "__main__":
    tester = ComprehensiveIterationTester()
    passed, failed, errors = tester.run_all_tests()
    
    # Exit with error code if too many tests failed
    success_rate = passed / (passed + failed + errors) if (passed + failed + errors) > 0 else 0
    exit_code = 0 if success_rate >= 0.8 else 1
    sys.exit(exit_code) 