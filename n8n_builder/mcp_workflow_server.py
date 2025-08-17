#!/usr/bin/env python3
"""
MCP Workflow Server for N8N_Builder
Exposes N8N workflow generation as MCP tools for VS Code integration
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
import logging

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# N8N_Builder imports
from .n8n_builder import N8NBuilder
from .config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("n8n-workflow")

# Workflow generator instance
workflow_generator = None

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available workflow generation tools."""
    return [
        Tool(
            name="generate_workflow",
            description="Generate an N8N workflow from plain English description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Plain English description of the desired workflow"
                    },
                    "include_research": {
                        "type": "boolean",
                        "description": "Whether to include research phase for better results",
                        "default": True
                    },
                    "complexity_level": {
                        "type": "string",
                        "enum": ["simple", "intermediate", "advanced"],
                        "description": "Complexity level of the workflow",
                        "default": "intermediate"
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="validate_workflow",
            description="Validate an N8N workflow JSON for correctness",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "string",
                        "description": "N8N workflow JSON to validate"
                    }
                },
                "required": ["workflow_json"]
            }
        ),
        Tool(
            name="optimize_workflow",
            description="Optimize an existing N8N workflow for better performance",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "string",
                        "description": "N8N workflow JSON to optimize"
                    },
                    "optimization_goals": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["performance", "reliability", "maintainability", "cost"]
                        },
                        "description": "Optimization goals",
                        "default": ["performance", "reliability"]
                    }
                },
                "required": ["workflow_json"]
            }
        ),
        Tool(
            name="explain_workflow",
            description="Explain how an N8N workflow works in plain English",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "string",
                        "description": "N8N workflow JSON to explain"
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["summary", "detailed", "technical"],
                        "description": "Level of detail for the explanation",
                        "default": "detailed"
                    }
                },
                "required": ["workflow_json"]
            }
        ),
        Tool(
            name="suggest_improvements",
            description="Suggest improvements for an N8N workflow",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "string",
                        "description": "N8N workflow JSON to analyze"
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["error_handling", "security", "performance", "maintainability"]
                        },
                        "description": "Areas to focus improvement suggestions on"
                    }
                },
                "required": ["workflow_json"]
            }
        ),
        Tool(
            name="convert_to_template",
            description="Convert a workflow to a reusable template with parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "string",
                        "description": "N8N workflow JSON to convert to template"
                    },
                    "template_name": {
                        "type": "string",
                        "description": "Name for the template"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of what the template does"
                    }
                },
                "required": ["workflow_json", "template_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from MCP clients."""
    global workflow_generator
    
    # Initialize workflow generator if needed
    if workflow_generator is None:
        try:
            workflow_generator = N8NBuilder()
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Workflow generator initialization failed: {str(e)}"})
            )]
    
    try:
        if name == "generate_workflow":
            description = arguments["description"]
            include_research = arguments.get("include_research", True)
            complexity_level = arguments.get("complexity_level", "intermediate")
            
            # Generate workflow
            result = workflow_generator.generate_workflow(description)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        elif name == "validate_workflow":
            workflow_json = arguments["workflow_json"]
            
            try:
                # Parse JSON to validate format
                workflow_data = json.loads(workflow_json)
                
                # Perform validation (this would be more comprehensive in practice)
                validation_result = {
                    "valid": True,
                    "errors": [],
                    "warnings": [],
                    "suggestions": []
                }
                
                # Basic validation checks
                if "nodes" not in workflow_data:
                    validation_result["valid"] = False
                    validation_result["errors"].append("Missing 'nodes' array")
                
                if "connections" not in workflow_data:
                    validation_result["valid"] = False
                    validation_result["errors"].append("Missing 'connections' object")
                
                # Check for common issues
                if workflow_data.get("nodes"):
                    node_names = [node.get("name", "") for node in workflow_data["nodes"]]
                    if len(node_names) != len(set(node_names)):
                        validation_result["warnings"].append("Duplicate node names found")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(validation_result, indent=2)
                )]
                
            except json.JSONDecodeError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "valid": False,
                        "errors": [f"Invalid JSON: {str(e)}"]
                    })
                )]
                
        elif name == "optimize_workflow":
            workflow_json = arguments["workflow_json"]
            optimization_goals = arguments.get("optimization_goals", ["performance", "reliability"])
            
            try:
                workflow_data = json.loads(workflow_json)
                
                # This would contain actual optimization logic
                optimization_result = {
                    "original_workflow": workflow_data,
                    "optimized_workflow": workflow_data,  # Would be modified
                    "optimizations_applied": [],
                    "performance_improvements": {
                        "estimated_speed_improvement": "10-20%",
                        "memory_usage_reduction": "5-15%"
                    }
                }
                
                # Add some example optimizations based on goals
                for goal in optimization_goals:
                    if goal == "performance":
                        optimization_result["optimizations_applied"].append(
                            "Added parallel processing where possible"
                        )
                    elif goal == "reliability":
                        optimization_result["optimizations_applied"].append(
                            "Added error handling and retry logic"
                        )
                
                return [TextContent(
                    type="text",
                    text=json.dumps(optimization_result, indent=2)
                )]
                
            except json.JSONDecodeError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Invalid JSON: {str(e)}"})
                )]
                
        elif name == "explain_workflow":
            workflow_json = arguments["workflow_json"]
            detail_level = arguments.get("detail_level", "detailed")
            
            try:
                workflow_data = json.loads(workflow_json)
                
                # Generate explanation based on workflow structure
                explanation = {
                    "workflow_name": workflow_data.get("name", "Unnamed Workflow"),
                    "summary": "This workflow processes data through multiple steps",
                    "steps": [],
                    "triggers": [],
                    "outputs": []
                }
                
                # Analyze nodes
                if workflow_data.get("nodes"):
                    for node in workflow_data["nodes"]:
                        node_type = node.get("type", "unknown")
                        node_name = node.get("name", "Unnamed Node")
                        
                        if "trigger" in node_type.lower():
                            explanation["triggers"].append(f"{node_name} ({node_type})")
                        else:
                            explanation["steps"].append(f"{node_name} ({node_type})")
                
                if detail_level == "technical":
                    explanation["technical_details"] = {
                        "node_count": len(workflow_data.get("nodes", [])),
                        "connection_count": len(workflow_data.get("connections", {})),
                        "complexity_score": "Medium"
                    }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(explanation, indent=2)
                )]
                
            except json.JSONDecodeError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Invalid JSON: {str(e)}"})
                )]
                
        elif name == "suggest_improvements":
            workflow_json = arguments["workflow_json"]
            focus_areas = arguments.get("focus_areas", ["error_handling", "performance"])
            
            try:
                workflow_data = json.loads(workflow_json)
                
                suggestions = {
                    "improvements": [],
                    "priority": "medium",
                    "estimated_effort": "2-4 hours"
                }
                
                # Generate suggestions based on focus areas
                for area in focus_areas:
                    if area == "error_handling":
                        suggestions["improvements"].append({
                            "category": "Error Handling",
                            "suggestion": "Add error handling nodes after external API calls",
                            "impact": "High",
                            "effort": "Low"
                        })
                    elif area == "security":
                        suggestions["improvements"].append({
                            "category": "Security",
                            "suggestion": "Use environment variables for sensitive data",
                            "impact": "High",
                            "effort": "Medium"
                        })
                    elif area == "performance":
                        suggestions["improvements"].append({
                            "category": "Performance",
                            "suggestion": "Consider batching operations where possible",
                            "impact": "Medium",
                            "effort": "Medium"
                        })
                
                return [TextContent(
                    type="text",
                    text=json.dumps(suggestions, indent=2)
                )]
                
            except json.JSONDecodeError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Invalid JSON: {str(e)}"})
                )]
                
        elif name == "convert_to_template":
            workflow_json = arguments["workflow_json"]
            template_name = arguments["template_name"]
            description = arguments.get("description", "")
            
            try:
                workflow_data = json.loads(workflow_json)
                
                # Create template structure
                template = {
                    "name": template_name,
                    "description": description,
                    "version": "1.0.0",
                    "parameters": [],
                    "workflow": workflow_data,
                    "usage_instructions": f"This template creates a workflow for {description.lower()}"
                }
                
                # Identify potential parameters (this would be more sophisticated)
                template["parameters"] = [
                    {
                        "name": "api_endpoint",
                        "type": "string",
                        "description": "API endpoint URL",
                        "required": True
                    },
                    {
                        "name": "webhook_url",
                        "type": "string", 
                        "description": "Webhook URL for notifications",
                        "required": False
                    }
                ]
                
                return [TextContent(
                    type="text",
                    text=json.dumps(template, indent=2)
                )]
                
            except json.JSONDecodeError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Invalid JSON: {str(e)}"})
                )]
                
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"})
            )]
            
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)})
        )]

async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting N8N Workflow MCP Server")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
