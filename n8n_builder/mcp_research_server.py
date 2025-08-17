#!/usr/bin/env python3
"""
MCP Research Server for N8N_Builder
Exposes N8N research capabilities as MCP tools for VS Code integration
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
import logging

# MCP imports (we'll need to install mcp package)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# N8N_Builder imports
from .mcp_research_tool import N8NResearchTool
from .config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("n8n-research")

# Initialize research tool
research_tool = None

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available N8N research tools."""
    return [
        Tool(
            name="search_n8n_docs",
            description="Search official N8N documentation for specific topics",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for N8N documentation"
                    },
                    "node_name": {
                        "type": "string", 
                        "description": "Optional specific node name to focus search"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="find_community_examples",
            description="Find community workflow examples and templates",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the workflow or use case"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of examples to return",
                        "default": 5
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="get_node_documentation",
            description="Get detailed documentation for a specific N8N node",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "Name of the N8N node (e.g., 'HTTP Request', 'Gmail', 'Slack')"
                    }
                },
                "required": ["node_name"]
            }
        ),
        Tool(
            name="research_integration_patterns",
            description="Research integration patterns for specific services",
            inputSchema={
                "type": "object",
                "properties": {
                    "services": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of services to research integration patterns for"
                    }
                },
                "required": ["services"]
            }
        ),
        Tool(
            name="get_best_practices",
            description="Get N8N workflow best practices for specific use cases",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_type": {
                        "type": "string",
                        "description": "Type of workflow or use case"
                    }
                },
                "required": ["workflow_type"]
            }
        ),
        Tool(
            name="comprehensive_research",
            description="Perform comprehensive research for a workflow description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Plain English description of the desired workflow"
                    }
                },
                "required": ["description"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from MCP clients."""
    global research_tool
    
    # Initialize research tool if needed
    if research_tool is None:
        research_tool = N8NResearchTool()
    
    try:
        if name == "search_n8n_docs":
            query = arguments["query"]
            node_name = arguments.get("node_name")
            results = await research_tool.search_n8n_docs(query, node_name)
            
            # Format results for MCP
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.title,
                    "url": result.url,
                    "content": result.content,
                    "relevance_score": result.relevance_score
                })
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_results, indent=2)
            )]
            
        elif name == "find_community_examples":
            description = arguments["description"]
            max_results = arguments.get("max_results", 5)
            results = await research_tool.find_community_examples(description)
            
            # Limit results
            limited_results = results[:max_results]
            formatted_results = []
            for result in limited_results:
                formatted_results.append({
                    "title": result.title,
                    "url": result.url,
                    "content": result.content,
                    "source": result.source
                })
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_results, indent=2)
            )]
            
        elif name == "get_node_documentation":
            node_name = arguments["node_name"]
            doc = await research_tool.get_node_documentation(node_name)
            
            if doc:
                result = {
                    "node_name": doc.node_name,
                    "node_type": doc.node_type,
                    "description": doc.description,
                    "parameters": doc.parameters,
                    "examples": doc.examples,
                    "best_practices": doc.best_practices,
                    "common_issues": doc.common_issues
                }
            else:
                result = {"error": f"No documentation found for node: {node_name}"}
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "research_integration_patterns":
            services = arguments["services"]
            patterns = await research_tool.research_integration_patterns(services)
            
            # Convert patterns to serializable format
            serializable_patterns = {}
            for service, service_patterns in patterns.items():
                serializable_patterns[service] = []
                for pattern in service_patterns:
                    serializable_patterns[service].append({
                        "pattern_name": pattern.pattern_name,
                        "description": pattern.description,
                        "use_cases": pattern.use_cases,
                        "complexity_level": pattern.complexity_level,
                        "required_nodes": pattern.required_nodes
                    })
            
            return [TextContent(
                type="text",
                text=json.dumps(serializable_patterns, indent=2)
            )]
            
        elif name == "get_best_practices":
            workflow_type = arguments["workflow_type"]
            practices = await research_tool.get_best_practices(workflow_type)
            
            return [TextContent(
                type="text",
                text=json.dumps({"best_practices": practices}, indent=2)
            )]
            
        elif name == "comprehensive_research":
            description = arguments["description"]
            results = await research_tool.comprehensive_research(description)
            
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2, default=str)
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
    logger.info("Starting N8N Research MCP Server")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
