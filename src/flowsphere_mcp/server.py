"""
FlowSphere MCP Server

Model Context Protocol server that provides FlowSphere schema knowledge
and code generation capabilities to AI agents.
"""

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from schema.config_schema import get_schema_documentation
from schema.features import get_feature_documentation, get_feature_checklist


# Initialize MCP server
app = Server("flowsphere-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools that AI agents can use.

    Returns:
        list[Tool]: Available MCP tools
    """
    return [
        Tool(
            name="get_flowsphere_schema",
            description="Get complete FlowSphere configuration schema documentation including all properties, types, examples, and edge cases",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_flowsphere_features",
            description="Get detailed documentation of all FlowSphere features (variable substitution, conditions, validations, etc.) with implementation notes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_feature_checklist",
            description="Get a checklist of all features that must be implemented in generated code",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="generate_python_pytest",
            description="Generate Python pytest code from a FlowSphere config file (coming in Phase 2)",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object"
                    }
                },
                "required": ["config"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from AI agents.

    Args:
        name: Tool name to execute
        arguments: Tool arguments

    Returns:
        list[TextContent]: Tool execution results
    """
    if name == "get_flowsphere_schema":
        schema_docs = get_schema_documentation()
        return [
            TextContent(
                type="text",
                text=json.dumps(schema_docs, indent=2)
            )
        ]

    elif name == "get_flowsphere_features":
        feature_docs = get_feature_documentation()
        return [
            TextContent(
                type="text",
                text=json.dumps(feature_docs, indent=2)
            )
        ]

    elif name == "get_feature_checklist":
        checklist = get_feature_checklist()
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "features": checklist,
                    "total_count": len(checklist),
                    "note": "All features must be supported in generated code"
                }, indent=2)
            )
        ]

    elif name == "generate_python_pytest":
        return [
            TextContent(
                type="text",
                text="Python pytest code generation is coming in Phase 2. Currently in Phase 1 (schema documentation only)."
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """
    Main entry point for the MCP server.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
