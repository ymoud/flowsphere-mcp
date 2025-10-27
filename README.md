# FlowSphere MCP Server

**Model Context Protocol (MCP) Server for FlowSphere Code Generation**

This MCP server provides deep schema knowledge and code generation templates to help AI agents generate executable code in multiple programming languages from FlowSphere configuration files.

## What It Does

Transforms FlowSphere config files (JSON) into standalone, production-ready test code in:
- **Python** - ✅ pytest (complete), ✅ behave/BDD (complete)
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
│   ├── server.py                 # MCP server entry point (5 tools)
│   ├── schema/
│   │   ├── config_schema.py      # FlowSphere config schema documentation
│   │   └── features.py           # Feature descriptions (18 features)
│   ├── templates/
│   │   └── python/
│   │       ├── base_template.py              # APISequence base class
│   │       ├── pytest_template.jinja2        # pytest test template
│   │       ├── gherkin_template.jinja2       # Gherkin feature file template
│   │       └── step_definitions_template.jinja2  # behave step definitions
│   └── generators/
│       ├── base_generator.py      # Base generator class
│       ├── python_generator.py    # Python pytest generator
│       └── behave_generator.py    # Python behave/BDD generator
├── tests/
│   ├── fixtures/                  # 5 test configs
│   ├── generated_code/            # Example outputs
│   ├── test_schema.py             # Schema tests (3 tests)
│   ├── test_python_generator.py   # pytest generator tests (31 tests)
│   └── test_behave_generator.py   # behave generator tests (34 tests)
├── requirements.txt
└── README.md
```

## Development Phases

- **Phase 1** ✅ - Schema provider (FlowSphere config documentation)
- **Phase 2** ✅ - Python pytest code generator (production-ready)
- **Phase 3** ✅ - Python behave code generator (BDD/Cucumber) - **COMPLETE**
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

## Phase 3 Complete: Python Behave/BDD Code Generation

**Status:** ✅ Complete - All 34 tests passing (68 total tests)

Phase 3 delivers production-ready Python behave/BDD code generation with:
- ✅ Gherkin feature file generation with proper BDD syntax
- ✅ Python step definitions with behave decorators (@given, @when, @then)
- ✅ APIContext class for state management across steps
- ✅ Complete support for all 18 FlowSphere features in BDD format
- ✅ Human-readable test scenarios for stakeholders
- ✅ Reusable step definitions
- ✅ 34 comprehensive tests (100% passing)
- ✅ Full integration with behave test runner

### Example: Behave/BDD Generation

```python
# AI agent generates BDD tests
result = mcp_server.call_tool(
    "generate_python_behave",
    {
        "config": {
            "name": "User Registration API",
            "defaults": {
                "baseUrl": "https://api.example.com"
            },
            "nodes": [
                {
                    "id": "register_user",
                    "name": "Register a new user",
                    "method": "POST",
                    "url": "/users",
                    "body": {
                        "email": "test@example.com",
                        "name": "Test User"
                    },
                    "validations": [
                        {"httpStatusCode": 201},
                        {"field": "email", "value": "test@example.com"}
                    ]
                }
            ]
        }
    }
)
```

**Generated Output:**

1. **Gherkin Feature File** (`user_registration_api.feature`):
```gherkin
Feature: User Registration API

  Scenario: Register a new user
    When I execute POST request to "/users" with body
    And I set the request body to:
      """
      {
        "email": "test@example.com",
        "name": "Test User"
      }
      """
    Then the response status code should be 201
    And the response field "email" should be "test@example.com"
```

2. **Step Definitions** (`user_registration_api_steps.py`):
- Complete APIContext class with variable substitution
- Behave decorators for all steps
- HTTP request execution
- Response validation
- All FlowSphere features supported

### Running Generated Behave Tests

```bash
# Organize files
mkdir -p features/steps
mv user_registration_api.feature features/
mv user_registration_api_steps.py features/steps/

# Install dependencies
pip install behave requests jsonpath-ng

# Run tests
behave

# Run with verbose output
behave -v

# Run specific scenario
behave -n "Register a new user"
```

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

### 4. `generate_python_pytest`
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

### 5. `generate_python_behave` ✨ NEW
Generates production-ready Python behave/BDD tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name

**Output:**
- `status`: "success" or "error"
- `code`: Combined output with Gherkin feature file and step definitions
- `language`: "Python"
- `framework`: "behave"
- `dependencies`: List of required pip packages (behave, requests, jsonpath-ng)
- `note`: Instructions on separating the two files

**Features:**
- Human-readable Gherkin syntax for stakeholders
- Complete step definitions with all FlowSphere features
- Reusable steps across multiple feature files
- BDD-style test organization
- Living documentation

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
