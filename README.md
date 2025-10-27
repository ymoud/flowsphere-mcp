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
- **Phase 2** 🚧 - Python pytest code generator (traditional tests)
- **Phase 3** 📋 - Python behave code generator (BDD/Cucumber)
- **Phase 4** 📋 - Add JavaScript/TypeScript and C# support

## Complete Feature Coverage

The generated code handles ALL FlowSphere features:

✅ HTTP Execution (all methods, headers, body, timeout)
✅ Variable Substitution ({{ .vars }}, {{ .responses }}, {{ .input }}, {{ $guid }}, {{ $timestamp }})
✅ Condition Evaluation (all operators, AND logic, variable substitution in conditions)
✅ Validation (HTTP status + JSONPath with all operators)
✅ User Interaction (userPrompts, launchBrowser)
✅ State Management (response storage, defaults merging)

## License

MIT
