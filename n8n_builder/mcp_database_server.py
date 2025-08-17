#!/usr/bin/env python3
"""
MCP Database Server for N8N_Builder
Exposes database operations as MCP tools for VS Code integration
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
from .mcp_database_tool import MCPDatabaseTool, get_mcp_database
from .config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("n8n-database")

# Database tool instance
db_tool = None

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available database tools."""
    return [
        Tool(
            name="get_database_schema",
            description="Get comprehensive database schema information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="execute_query",
            description="Execute a SQL query and return results",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Optional query parameters"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_table_info",
            description="Get detailed information about a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema_name": {
                        "type": "string",
                        "description": "Schema name (default: dbo)",
                        "default": "dbo"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="get_sample_data",
            description="Get sample data from a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema_name": {
                        "type": "string",
                        "description": "Schema name (default: dbo)",
                        "default": "dbo"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of rows to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="execute_stored_procedure",
            description="Execute a stored procedure with parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "procedure_name": {
                        "type": "string",
                        "description": "Name of the stored procedure"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters for the stored procedure"
                    }
                },
                "required": ["procedure_name"]
            }
        ),
        Tool(
            name="search_Enterprise_Database",
            description="Search the knowledge base for facts and opinions",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Term to search for in the knowledge base"
                    },
                    "fact_type": {
                        "type": "string",
                        "description": "Type of fact to search for (optional)"
                    },
                    "min_validity": {
                        "type": "number",
                        "description": "Minimum validity rating (0.0-1.0)",
                        "default": 0.5
                    }
                },
                "required": ["search_term"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from MCP clients."""
    global db_tool
    
    # Initialize database tool if needed
    if db_tool is None:
        try:
            db_tool = get_mcp_database()
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Database connection failed: {str(e)}"})
            )]
    
    try:
        if name == "get_database_schema":
            schema = await db_tool.get_database_schema()
            
            # Convert to serializable format
            result = {
                "database_name": schema.database_name,
                "tables": [
                    {
                        "name": table["name"],
                        "schema": table["schema"],
                        "type": table["type"]
                    } for table in schema.tables
                ],
                "views": [
                    {
                        "name": view["name"],
                        "schema": view["schema"]
                    } for view in schema.views
                ],
                "procedures": [
                    {
                        "name": proc["name"],
                        "schema": proc["schema"]
                    } for proc in schema.procedures
                ],
                "functions": [
                    {
                        "name": func["name"],
                        "schema": func["schema"]
                    } for func in schema.functions
                ]
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "execute_query":
            query = arguments["query"]
            parameters = arguments.get("parameters")
            
            result = await db_tool.execute_query(query, parameters)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        elif name == "get_table_info":
            table_name = arguments["table_name"]
            schema_name = arguments.get("schema_name", "dbo")
            
            table_info = await db_tool.get_table_info(table_name, schema_name)
            
            # Convert to serializable format
            result = {
                "table_name": table_info.table_name,
                "schema_name": table_info.schema_name,
                "row_count": table_info.row_count,
                "columns": [
                    {
                        "name": col["name"],
                        "type": col["type"],
                        "nullable": col["nullable"],
                        "default": col.get("default"),
                        "is_primary_key": col.get("is_primary_key", False)
                    } for col in table_info.columns
                ],
                "indexes": table_info.indexes,
                "foreign_keys": table_info.foreign_keys
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
            
        elif name == "get_sample_data":
            table_name = arguments["table_name"]
            schema_name = arguments.get("schema_name", "dbo")
            limit = arguments.get("limit", 10)
            
            result = await db_tool.get_sample_data(table_name, schema_name, limit)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        elif name == "execute_stored_procedure":
            procedure_name = arguments["procedure_name"]
            parameters = arguments.get("parameters")
            
            result = await db_tool.execute_stored_procedure(procedure_name, parameters)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        elif name == "search_Enterprise_Database":
            search_term = arguments["search_term"]
            fact_type = arguments.get("fact_type")
            min_validity = arguments.get("min_validity", 0.5)
            
            # Build search query for knowledge base
            query = """
            SELECT TOP 20 
                FactID, FactType, FactText, ValidityRating, 
                CreatedDate, LastUpdated, Source
            FROM REF_FACT 
            WHERE FactText LIKE ? 
            AND ValidityRating >= ?
            """
            
            params = [f"%{search_term}%", min_validity]
            
            if fact_type:
                query += " AND FactType = ?"
                params.append(fact_type)
                
            query += " ORDER BY ValidityRating DESC, LastUpdated DESC"
            
            result = await db_tool.execute_query(query, params)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
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
    logger.info("Starting N8N Database MCP Server")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
