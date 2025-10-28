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
from generators.python_generator import PythonPytestGenerator
from generators.behave_generator import PythonBehaveGenerator
from generators.javascript_generator import JavaScriptJestGenerator, JavaScriptMochaGenerator, JavaScriptCucumberGenerator


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
            description="Generate production-ready Python pytest code from a FlowSphere configuration. Supports all 18 FlowSphere features including HTTP execution, variable substitution, conditions, validations, and more.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object with nodes, defaults, variables, etc."
                    },
                    "test_class_name": {
                        "type": "string",
                        "description": "Optional: Custom name for the test class (auto-generated if not provided)"
                    }
                },
                "required": ["config"]
            }
        ),
        Tool(
            name="generate_python_behave",
            description="Generate production-ready Python behave/BDD tests from a FlowSphere configuration. Produces Gherkin feature files and step definitions. Supports all 18 FlowSphere features with human-readable BDD syntax.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object with nodes, defaults, variables, etc."
                    },
                    "feature_name": {
                        "type": "string",
                        "description": "Optional: Custom name for the feature file (auto-generated if not provided)"
                    }
                },
                "required": ["config"]
            }
        ),
        Tool(
            name="generate_javascript_jest",
            description="Generate production-ready JavaScript Jest code from a FlowSphere configuration. Supports all 18 FlowSphere features including async/await, HTTP execution, variable substitution, conditions, validations, and more.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object with nodes, defaults, variables, etc."
                    },
                    "test_class_name": {
                        "type": "string",
                        "description": "Optional: Custom name for the test class (auto-generated if not provided)"
                    }
                },
                "required": ["config"]
            }
        ),
        Tool(
            name="generate_javascript_mocha",
            description="Generate production-ready JavaScript Mocha code from a FlowSphere configuration. Uses Mocha test framework with Chai assertions. Supports all 18 FlowSphere features including async/await, HTTP execution, variable substitution, conditions, validations, and more.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object with nodes, defaults, variables, etc."
                    },
                    "test_class_name": {
                        "type": "string",
                        "description": "Optional: Custom name for the test class (auto-generated if not provided)"
                    }
                },
                "required": ["config"]
            }
        ),
        Tool(
            name="generate_javascript_cucumber",
            description="Generate production-ready JavaScript Cucumber/BDD code from a FlowSphere configuration. Produces Gherkin feature files and cucumber-js step definitions. Supports all 18 FlowSphere features. Perfect for BDD-style testing and living documentation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config": {
                        "type": "object",
                        "description": "FlowSphere configuration object with nodes, defaults, variables, etc."
                    },
                    "feature_name": {
                        "type": "string",
                        "description": "Optional: Custom name for the feature file (auto-generated if not provided)"
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
        try:
            config = arguments.get("config")
            if not config:
                raise ValueError("Missing required argument: config")

            # Initialize generator
            generator = PythonPytestGenerator()

            # Generate code
            options = {}
            if "test_class_name" in arguments:
                options["test_class_name"] = arguments["test_class_name"]

            generated_code = generator.generate(config, **options)

            # Return generated code with metadata
            result = {
                "status": "success",
                "language": generator.get_language_name(),
                "framework": generator.get_framework_name(),
                "code": generated_code,
                "dependencies": generator.get_required_dependencies(),
                "usage_instructions": generator.get_usage_instructions()
            }

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": f"Code generation failed: {str(e)}"
                    }, indent=2)
                )
            ]

    elif name == "generate_python_behave":
        try:
            config = arguments.get("config")
            if not config:
                raise ValueError("Missing required argument: config")

            # Initialize generator
            generator = PythonBehaveGenerator()

            # Generate code
            options = {}
            if "feature_name" in arguments:
                options["feature_name"] = arguments["feature_name"]

            generated_code = generator.generate_single_file(config, **options)

            # Return generated code with metadata
            result = {
                "status": "success",
                "language": generator.get_language_name(),
                "framework": generator.get_framework_name(),
                "code": generated_code,
                "dependencies": generator.get_required_dependencies(),
                "note": "Output contains both Gherkin feature file and Python step definitions. See file separators in the output."
            }

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": f"Code generation failed: {str(e)}"
                    }, indent=2)
                )
            ]

    elif name == "generate_javascript_jest":
        try:
            config = arguments.get("config")
            if not config:
                raise ValueError("Missing required argument: config")

            # Initialize generator
            generator = JavaScriptJestGenerator()

            # Generate code
            options = {}
            if "test_class_name" in arguments:
                options["test_class_name"] = arguments["test_class_name"]

            generated_code = generator.generate(config, **options)

            # Return generated code with metadata
            result = {
                "status": "success",
                "language": generator.get_language_name(),
                "framework": generator.get_framework_name(),
                "code": generated_code,
                "dependencies": generator.get_required_dependencies(),
                "usage_instructions": generator.get_usage_instructions(),
                "package_json": generator.get_package_json_template()
            }

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": f"Code generation failed: {str(e)}"
                    }, indent=2)
                )
            ]

    elif name == "generate_javascript_mocha":
        try:
            config = arguments.get("config")
            if not config:
                raise ValueError("Missing required argument: config")

            # Initialize generator
            generator = JavaScriptMochaGenerator()

            # Generate code
            options = {}
            if "test_class_name" in arguments:
                options["test_class_name"] = arguments["test_class_name"]

            generated_code = generator.generate(config, **options)

            # Return generated code with metadata
            result = {
                "status": "success",
                "language": generator.get_language_name(),
                "framework": generator.get_framework_name(),
                "code": generated_code,
                "dependencies": generator.get_required_dependencies(),
                "usage_instructions": generator.get_usage_instructions(),
                "package_json": generator.get_package_json_template()
            }

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": f"Code generation failed: {str(e)}"
                    }, indent=2)
                )
            ]

    elif name == "generate_javascript_cucumber":
        try:
            config = arguments.get("config")
            if not config:
                raise ValueError("Missing required argument: config")

            # Initialize generator
            generator = JavaScriptCucumberGenerator()

            # Generate code
            options = {}
            if "feature_name" in arguments:
                options["feature_name"] = arguments["feature_name"]

            generated = generator.generate(config, **options)

            # Return generated code with metadata
            result = {
                "status": "success",
                "language": generator.get_language_name(),
                "framework": generator.get_framework_name(),
                "feature": generated["feature"],
                "steps": generated["steps"],
                "dependencies": generator.get_required_dependencies(),
                "package_json": generator.get_package_json_template(),
                "note": "Save feature file as *.feature and steps file as *_steps.js in features/step_definitions/ directory"
            }

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]

        except ValueError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error": f"Code generation failed: {str(e)}"
                    }, indent=2)
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
