# FlowSphere MCP Server

**Model Context Protocol (MCP) Server for FlowSphere Code Generation**

This MCP server provides deep schema knowledge and code generation templates to help AI agents generate executable code in multiple programming languages from FlowSphere configuration files.

## What It Does

Transforms FlowSphere config files (JSON) into standalone, production-ready test code in:
- **Python** - pytest, unittest, behave (Cucumber/BDD)
- **JavaScript/TypeScript** - Jest, Mocha, cucumber-js (coming soon)
- **C#** - xUnit, NUnit, SpecFlow (coming soon)

## Architecture

The MCP server follows a **Schema + Templates** approach:

1. **Schema Documentation Provider** - Complete knowledge of FlowSphere config structure
2. **Code Template Library** - Pre-built, battle-tested code snippets for each language
3. **Code Generator Engine** - Combines schema + templates to generate working code

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python src/flowsphere_mcp/server.py
```

## Usage with AI Agents

Once the server is running, AI agents (like Claude Code) can use it to generate code:

```
User: "Generate Python pytest code from config.json"
AI: [Uses MCP server to read schema, get templates, generate complete Python code]

User: "Create Cucumber BDD tests from this config"
AI: [Generates Gherkin feature file + behave step definitions]
```

### Example: Python pytest Code Generation

The MCP server provides the `generate_python_pytest` tool that AI agents can call:

```python
# AI agent calls the MCP tool with a FlowSphere config
result = mcp_server.call_tool(
    "generate_python_pytest",
    {
        "config": {
            "name": "My API Test",
            "defaults": {
                "baseUrl": "https://api.example.com",
                "headers": {"Content-Type": "application/json"}
            },
            "nodes": [
                {
                    "id": "get_users",
                    "name": "Get all users",
                    "method": "GET",
                    "url": "/users"
                }
            ]
        }
    }
)

# Returns complete, runnable Python pytest code
print(result["code"])
```

The generated code includes:
- Complete `APISequence` base class with all FlowSphere features
- Test class extending APISequence
- Full variable substitution ({{ $guid }}, {{ .vars.x }}, etc.)
- Condition evaluation
- Response validation
- HTTP request execution

### Running Generated Tests

```bash
# Save generated code
cat > test_api.py << 'EOF'
# [Generated code from MCP server]
EOF

# Install dependencies
pip install pytest requests jsonpath-ng

# Run tests
pytest test_api.py -v

# Run with debug output
pytest test_api.py -v -s
```

## Project Structure

```
flowsphere-mcp-server/
├── src/flowsphere_mcp/
│   ├── server.py              # MCP server entry point
│   ├── schema/
│   │   ├── config_schema.py   # FlowSphere config schema documentation
│   │   └── features.py        # Feature descriptions (variables, conditions, etc.)
│   ├── templates/
│   │   └── python/
│   │       ├── pytest_base.py # Base pytest template
│   │       └── behave_base.py # Base behave/Cucumber template
│   └── generators/
│       ├── python_generator.py # Python code generator
│       └── base_generator.py   # Base generator class
├── tests/                      # Test configs and generated code examples
├── requirements.txt
└── README.md
```

## Development Phases

- **Phase 1** ✅ - Schema provider (FlowSphere config documentation)
- **Phase 2** ✅ - Python pytest code generator (production-ready)
- **Phase 3** 📋 - Python behave code generator (BDD/Cucumber)
- **Phase 4** 📋 - Add JavaScript/TypeScript and C# support

## Phase 2 Complete: Python pytest Code Generation

**Status:** ✅ Complete - All 31 tests passing

Phase 2 delivers production-ready Python pytest code generation with:
- ✅ Complete support for all 18 FlowSphere features
- ✅ Comprehensive base template with APISequence class
- ✅ Jinja2-based code generation
- ✅ Full validation and error handling
- ✅ 5 test fixture configurations
- ✅ 31 passing tests (100% coverage)

## Available MCP Tools

The server exposes the following tools for AI agents:

### 1. `get_flowsphere_schema`
Returns complete FlowSphere configuration schema documentation including:
- All properties and their types
- Required vs optional fields
- Default values and examples
- Edge cases and validation rules

### 2. `get_flowsphere_features`
Returns detailed documentation of all FlowSphere features:
- Variable substitution (4 types)
- Condition evaluation (8 operators)
- HTTP execution
- Response validation
- Implementation notes for each feature

### 3. `get_feature_checklist`
Returns a checklist of all 18 features that must be implemented in generated code.

### 4. `generate_python_pytest` ✨ NEW
Generates production-ready Python pytest code from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name

**Output:**
- `status`: "success" or "error"
- `code`: Generated Python pytest code
- `language`: "Python"
- `framework`: "pytest"
- `dependencies`: List of required pip packages
- `usage_instructions`: How to run the generated tests

## Complete Feature Coverage

The generated code handles ALL FlowSphere features:

✅ HTTP Execution (all methods, headers, body, timeout)
✅ Variable Substitution ({{ .vars }}, {{ .responses }}, {{ .input }}, {{ $guid }}, {{ $timestamp }})
✅ Condition Evaluation (all operators, AND logic, variable substitution in conditions)
✅ Validation (HTTP status + JSONPath with all operators)
✅ User Interaction (userPrompts, launchBrowser)
✅ State Management (response storage, defaults merging)
✅ Skip Flags (skipDefaultHeaders, skipDefaultValidations)
✅ Debug Mode (enableDebug for detailed logging)

## License

MIT
