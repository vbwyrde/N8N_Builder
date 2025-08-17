# N8N MCP Integration with VS Code

This guide explains how to use the N8N_Builder MCP (Model Context Protocol) integration with Visual Studio Code for workflow automation across all your projects.

## 🎯 Overview

The N8N MCP integration provides powerful workflow automation tools directly in VS Code through the MCP protocol. You can now:

- **Research N8N documentation** and best practices
- **Query the Enterprise_Database** for validated facts and solutions
- **Generate N8N workflows** from plain English descriptions
- **Validate and optimize** existing workflows
- **Access these tools from any VS Code project**

## ✅ Prerequisites

- **VS Code 1.102+** (you have 1.103.0 ✓)
- **MCP package installed** (✓)
- **N8N_Builder MCP servers configured** (✓)

## 🚀 Getting Started

### 1. Open VS Code in Any Project

The MCP servers are configured to work across all VS Code workspaces. You can use N8N tools from any project.

### 2. Start a Chat Session

1. Open the **Chat view** (`Ctrl+Alt+I`)
2. Select **Agent mode** from the dropdown
3. Click the **Tools** button to see available tools

### 3. Verify N8N Tools Are Available

You should see these N8N_Builder tools:

**Research Tools:**
- `search_n8n_docs` - Search official N8N documentation
- `find_community_examples` - Find community workflow examples
- `get_node_documentation` - Get detailed node documentation
- `research_integration_patterns` - Research service integration patterns
- `get_best_practices` - Get workflow best practices
- `comprehensive_research` - Perform comprehensive workflow research

**Database Tools:**
- `get_database_schema` - Get Enterprise_Database schema
- `execute_query` - Execute SQL queries
- `get_table_info` - Get table information
- `search_Enterprise_Database` - Search for validated facts
- `execute_stored_procedure` - Run stored procedures

**Workflow Tools:**
- `generate_workflow` - Generate N8N workflows from descriptions
- `validate_workflow` - Validate workflow JSON
- `optimize_workflow` - Optimize existing workflows
- `explain_workflow` - Explain workflows in plain English
- `suggest_improvements` - Suggest workflow improvements
- `convert_to_template` - Convert workflows to reusable templates

## 🧪 Test Commands

Try these commands in VS Code chat to test the integration:

### Research Tests

```
Search for HTTP Request node documentation
```

```
Find community examples for Slack integration workflows
```

```
Get best practices for email automation workflows
```

### Database Tests

```
Show me the database schema
```

```
Search the knowledge base for "N8N workflow patterns"
```

### Workflow Generation Tests

```
Create a workflow that sends a Slack message when a new email arrives
```

```
Generate a workflow to backup files to Google Drive daily
```

```
Create a workflow that monitors a website and sends alerts if it's down
```

### Workflow Analysis Tests

```
Validate this N8N workflow: [paste workflow JSON]
```

```
Explain what this workflow does: [paste workflow JSON]
```

```
Suggest improvements for this workflow: [paste workflow JSON]
```

## 🔧 Configuration Details

### MCP Server Configuration

The MCP servers are configured in `.vscode/mcp.json`:

- **N8N_Builder_Research** - Provides N8N research capabilities
- **N8N_Builder_Database** - Provides Enterprise_Database access
- **N8N_Workflow_Generator** - Provides workflow generation tools

### Environment Variables

The servers use these environment variables:
- `PYTHONPATH` - Set to workspace folder
- `MIMO_ENDPOINT` - Local LLM endpoint (localhost:1234/v1)
- `MIMO_MODEL` - AI model (mimo-vl-7b-rl)
- `MCP_RESEARCH_ENABLED` - Enable research features
- `MCP_DATABASE_ENABLED` - Enable database features

## 🎯 Usage Patterns

### 1. Workflow Planning

```
I need to create a workflow that:
1. Monitors my Gmail for invoices
2. Extracts invoice data
3. Adds the data to a Google Sheet
4. Sends a Slack notification

Can you research the best approach and generate the workflow?
```

### 2. Learning N8N

```
I'm new to N8N. Can you:
1. Explain what the HTTP Request node does
2. Show me some examples of how it's used
3. Give me best practices for API integrations
```

### 3. Workflow Optimization

```
I have this N8N workflow [paste JSON]. Can you:
1. Explain what it does
2. Identify any performance issues
3. Suggest improvements
4. Show me the optimized version
```

### 4. Troubleshooting

```
My N8N workflow is failing. Can you:
1. Search the knowledge base for similar issues
2. Check the community forums for solutions
3. Suggest debugging steps
```

## 🛠️ Troubleshooting

### Tools Not Appearing

1. **Check VS Code version**: Must be 1.102+
2. **Verify MCP configuration**: Check `.vscode/mcp.json` exists
3. **Restart VS Code**: Sometimes needed after configuration changes
4. **Check server status**: Look at VS Code output panel for errors

### Server Connection Issues

1. **Check Python environment**: Ensure virtual environment is active
2. **Verify dependencies**: Run `pip list | grep mcp`
3. **Check logs**: Look in `logs/` folder for error messages
4. **Test server imports**: Run the test commands from terminal

### Performance Issues

1. **Limit tool selection**: Don't enable all tools at once
2. **Use specific queries**: Be precise in your requests
3. **Check LLM status**: Ensure LM Studio is running (localhost:1234)

## 📚 Advanced Usage

### Custom Prompts

You can create custom prompts that leverage multiple tools:

```
Create a comprehensive automation solution for my e-commerce business:
1. Research best practices for order processing workflows
2. Generate workflows for order confirmation emails
3. Create inventory management automation
4. Set up customer support ticket routing
```

### Cross-Project Workflow Sharing

Since MCP works across all VS Code projects, you can:

1. Generate workflows in one project
2. Save them to your N8N instance
3. Reference them from other projects
4. Build a library of reusable automation patterns

### Integration with Other Tools

The N8N MCP tools work alongside other VS Code extensions and MCP servers, allowing you to:

- Combine N8N workflow generation with code development
- Use database tools for application development
- Research automation patterns while building applications

## 🎉 Success!

You now have N8N workflow automation capabilities available in every VS Code project through MCP integration. This powerful combination allows you to:

- **Research** N8N solutions while coding
- **Generate** workflows from natural language
- **Validate** and optimize automation
- **Access** your Enterprise_Database from anywhere
- **Work efficiently** across all projects

Happy automating! 🚀
