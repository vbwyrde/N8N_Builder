#!/usr/bin/env python3

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import just the core functionality without heavy logging
import logging
logging.basicConfig(level=logging.CRITICAL)  # Suppress all logging

from n8n_builder.n8n_builder import N8NBuilder

# This is the exact workflow structure that our debug test showed should work
working_workflow = {
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
    },
    {
      "id": "email-node",
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "mark@mark.com",
        "subject": "Workflow Complete",
        "text": "The workflow has completed successfully."
      },
      "position": [1200, 300]
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
            "node": "Send Email",
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

print("=== TESTING VALIDATION WITH WORKING WORKFLOW ===")

builder = N8NBuilder()

# Convert to JSON string for validation
workflow_json = json.dumps(working_workflow)

print("Workflow structure:")
print(f"  Nodes: {[node['name'] for node in working_workflow['nodes']]}")
print(f"  Connections:")
for source, targets in working_workflow['connections'].items():
    for conn_type, target_lists in targets.items():
        for target_list in target_lists:
            for target in target_list:
                print(f"    {source} -> {target['node']} ({conn_type})")

print(f"\nValidating workflow...")
is_valid = builder.validate_workflow(workflow_json)

if is_valid:
    print("✅ VALIDATION PASSED: Workflow is valid")
else:
    print("❌ VALIDATION FAILED: Workflow is invalid")
    print("This means there's a bug in the validation logic itself!")

print("\n=== MANUAL VALIDATION CHECK ===")
# Manual validation to double-check
nodes = working_workflow.get("nodes", [])
connections = working_workflow.get("connections", {})
connected_nodes = set()

# Collect all connected nodes
for source, targets in connections.items():
    connected_nodes.add(source)
    for target_lists in targets.values():
        for target_list in target_lists:
            for target in target_list:
                if "node" in target:
                    connected_nodes.add(target["node"])

# Find isolated nodes
all_node_names = {node.get("name", f"Node_{i}") for i, node in enumerate(nodes)}
isolated_nodes = all_node_names - connected_nodes

print(f"All node names: {all_node_names}")
print(f"Connected nodes: {connected_nodes}")
print(f"Isolated nodes: {isolated_nodes}")

if isolated_nodes == {"Webhook Response"}:
    print("Manual validation: ✅ SHOULD PASS - Only Webhook Response is isolated (expected)")
else:
    print("Manual validation: ❌ SHOULD FAIL - Unexpected isolated nodes detected")
    print(f"Problem nodes: {isolated_nodes - {'Webhook Response'}}")

# Check if there are any trigger nodes
trigger_nodes = []
for node in nodes:
    node_type = node.get("type", "").lower()
    if "webhook" in node_type or "trigger" in node_type:
        trigger_nodes.append(node.get("name"))

print(f"Trigger nodes found: {trigger_nodes}")
if trigger_nodes:
    print("✅ Has trigger nodes")
else:
    print("❌ No trigger nodes found") 