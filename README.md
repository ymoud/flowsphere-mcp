# FlowSphere MCP Server

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ymoud/flowsphere-mcp/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-153%20passing-brightgreen.svg)](tests/)
[![Code Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](tests/)
[![MCP](https://img.shields.io/badge/MCP-enabled-purple.svg)](https://modelcontextprotocol.io)

**Model Context Protocol (MCP) Server for FlowSphere Code Generation**

This MCP server provides deep schema knowledge and code generation templates to help AI agents generate executable code in multiple programming languages from FlowSphere configuration files.

## What It Does

Transforms FlowSphere config files (JSON) into standalone, production-ready test code in:
- **Python** - ✅ pytest, ✅ behave/BDD
- **JavaScript** - ✅ Jest, ✅ Mocha, ✅ Cucumber/BDD
- **C#** - ✅ xUnit, ✅ NUnit, ✅ SpecFlow/BDD

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
│   ├── server.py                 # MCP server entry point (11 tools)
│   ├── schema/
│   │   ├── config_schema.py      # FlowSphere config schema documentation
│   │   └── features.py           # Feature descriptions (18 features)
│   ├── templates/
│   │   ├── python/
│   │   │   ├── base_template.py              # APISequence base class
│   │   │   ├── pytest_template.jinja2        # pytest test template
│   │   │   ├── gherkin_template.jinja2       # Gherkin feature file template
│   │   │   └── step_definitions_template.jinja2  # behave step definitions
│   │   ├── javascript/
│   │   │   ├── jest_template.jinja2          # Jest test template
│   │   │   ├── mocha_template.jinja2         # Mocha test template
│   │   │   ├── cucumber_feature_template.jinja2  # Cucumber feature file
│   │   │   └── cucumber_steps_template.jinja2    # Cucumber step definitions
│   │   └── csharp/
│   │       ├── xunit_template.jinja2         # xUnit test template
│   │       ├── nunit_template.jinja2         # NUnit test template
│   │       ├── specflow_feature_template.jinja2  # SpecFlow feature file
│   │       └── specflow_steps_template.jinja2    # SpecFlow step definitions
│   └── generators/
│       ├── base_generator.py      # Base generator class
│       ├── python_generator.py    # Python pytest generator
│       ├── behave_generator.py    # Python behave/BDD generator
│       ├── javascript_generator.py # JavaScript Jest/Mocha/Cucumber generators
│       └── csharp_generator.py    # C# xUnit/NUnit/SpecFlow generators
├── tests/
│   ├── fixtures/                  # 5 test configs
│   ├── generated_code/            # Example outputs
│   ├── test_schema.py             # Schema tests (3 tests)
│   ├── test_python_generator.py   # pytest generator tests (31 tests)
│   ├── test_behave_generator.py   # behave generator tests (34 tests)
│   ├── test_javascript_generator.py # Jest generator tests (30 tests)
│   ├── test_mocha_generator.py    # Mocha generator tests (8 tests)
│   ├── test_cucumber_generator.py # Cucumber generator tests (8 tests)
│   ├── test_xunit_generator.py    # xUnit generator tests (12 tests)
│   ├── test_nunit_generator.py    # NUnit generator tests (14 tests)
│   └── test_specflow_generator.py # SpecFlow generator tests (13 tests)
├── requirements.txt
└── README.md
```

## Development Phases

- **Phase 1** ✅ - Schema provider (FlowSphere config documentation)
- **Phase 2** ✅ - Python pytest code generator (production-ready)
- **Phase 3** ✅ - Python behave code generator (BDD/Cucumber)
- **Phase 4** ✅ - JavaScript code generators (Jest, Mocha, Cucumber) - **COMPLETE**
- **Phase 5** ✅ - C# code generators (xUnit, NUnit, SpecFlow) - **COMPLETE**
- **Phase 6** 📋 - Publishing & Distribution (PyPI, Smithery)

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

## Phase 4 Complete: JavaScript Code Generation (Jest, Mocha, Cucumber)

**Status:** ✅ Complete - All 46 tests passing (114 total tests)

Phase 4 delivers production-ready JavaScript code generation with three frameworks:

### Framework Overview
- **Jest** (30 tests) - Modern testing with expect assertions
- **Mocha** (8 tests) - Traditional testing with Chai assertions
- **Cucumber** (8 tests) - BDD/Gherkin for living documentation

### Common Features (All Frameworks)
- ✅ Modern ES6+ syntax with async/await
- ✅ Complete APISequence/APIWorld class with all FlowSphere features
- ✅ axios for HTTP requests
- ✅ JSONPath support for response validation
- ✅ Complete package.json generation
- ✅ Full support for all 18 FlowSphere features

### Example: JavaScript Jest Generation

```javascript
// AI agent generates Jest tests
result = mcp_server.call_tool(
    "generate_javascript_jest",
    {
        "config": {
            "name": "Product API Tests",
            "defaults": {
                "baseUrl": "https://api.store.com",
                "headers": {"Authorization": "Bearer token123"}
            },
            "nodes": [
                {
                    "id": "get_products",
                    "name": "Get all products",
                    "method": "GET",
                    "url": "/products",
                    "validations": [
                        {"httpStatusCode": 200},
                        {"field": "$[0].name", "operator": "exists"}
                    ]
                }
            ]
        }
    }
)
```

**Generated Output:**

1. **Jest Test File** (`product_api_tests.test.js`):
```javascript
const axios = require('axios');
const jp = require('jsonpath');

class APISequence {
    constructor(config) {
        this.config = config;
        this.responses = {};
        this.variables = {};
    }

    // Complete implementation with all 18 FlowSphere features
    async executeNode(node) { /* ... */ }
    substituteVariables(text) { /* ... */ }
    evaluateCondition(condition) { /* ... */ }
    validateResponse(response, validations) { /* ... */ }
}

describe('Product API Tests', () => {
    test('Get all products', async () => {
        const sequence = new APISequence(config);
        await sequence.executeNode(nodes[0]);
        // Validations automatically applied
    });
});
```

2. **Package.json** - Complete with all dependencies

### Running Generated Jest Tests

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- -t "Get all products"
```

### Mocha + Chai Generation

**Differences from Jest:**
- Uses `describe` and `it` (instead of `test`)
- Uses Chai `expect` assertions
- Includes `beforeEach` hooks
- Configurable timeout with `this.timeout()`

**Example Usage:**
```javascript
result = mcp_server.call_tool("generate_javascript_mocha", {"config": flowsphere_config})
```

**Generated Output:**
- Complete Mocha test file with Chai assertions
- APISequence class with all features
- Package.json with mocha, chai, axios, jsonpath-plus

**Running Mocha Tests:**
```bash
npm install --save-dev mocha chai axios jsonpath-plus uuid
npm test  # or: npx mocha test_file.test.js
```

### Cucumber/BDD Generation

**BDD Features:**
- Gherkin feature files with human-readable scenarios
- Step definitions with Given/When/Then
- APIWorld class for state management
- Living documentation for stakeholders
- Reusable steps across features

**Example Usage:**
```javascript
result = mcp_server.call_tool("generate_javascript_cucumber", {"config": flowsphere_config})
// Returns: result.feature and result.steps
```

**Generated Output:**

1. **Feature File** (`api_test.feature`):
```gherkin
Feature: Product API Tests

  Scenario: Get all products
    When I execute GET request to "/products"
    Then the response status code should be 200
    And the response field "$[0].name" should be "Product 1"
```

2. **Step Definitions** (`api_test_steps.js`):
- APIWorld class with context management
- Given/When/Then step implementations
- Full variable substitution support
- Response validation with Chai

**Running Cucumber Tests:**
```bash
npm install --save-dev @cucumber/cucumber axios jsonpath-plus uuid chai

# Organize files
mkdir -p features/step_definitions
mv *.feature features/
mv *_steps.js features/step_definitions/

# Run tests
npx cucumber-js
```

## Phase 5 Complete: C# Code Generation (xUnit, NUnit, SpecFlow)

**Status:** ✅ Complete - All 39 tests passing (153 total tests)

Phase 5 delivers production-ready C# code generation with three frameworks:

### Framework Overview
- **xUnit** (12 tests) - Modern .NET testing with Fact/Theory attributes
- **NUnit** (14 tests) - Traditional .NET testing with constraint model
- **SpecFlow** (13 tests) - BDD/Gherkin for living documentation

### Common Features (All Frameworks)
- ✅ Modern C# with async/await and HttpClient
- ✅ Complete APISequence class with all FlowSphere features
- ✅ HttpClient for HTTP requests
- ✅ JSONPath support via Newtonsoft.Json.Linq
- ✅ Complete .csproj file generation
- ✅ Full support for all 18 FlowSphere features

### Example: C# xUnit Generation

```csharp
// AI agent generates xUnit tests
result = mcp_server.call_tool(
    "generate_csharp_xunit",
    {
        "config": {
            "name": "User API Tests",
            "defaults": {
                "baseUrl": "https://api.example.com",
                "headers": {"Content-Type": "application/json"}
            },
            "nodes": [
                {
                    "id": "create_user",
                    "name": "Create new user",
                    "method": "POST",
                    "url": "/users",
                    "body": {
                        "name": "John Doe",
                        "email": "john@example.com"
                    },
                    "validations": [
                        {"httpStatusCode": 201},
                        {"field": "$.id", "operator": "exists"}
                    ]
                }
            ]
        },
        "namespace": "MyApp.Tests"
    }
)
```

**Generated Output:**

1. **xUnit Test File** (`UserApiTests.cs`):
```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;
using Xunit;
using Newtonsoft.Json.Linq;

namespace MyApp.Tests
{
    public class APISequence
    {
        private readonly HttpClient _httpClient;
        private readonly Dictionary<string, object> _responses;

        public APISequence(Dictionary<string, object> config) { /* ... */ }

        // Complete implementation with all 18 FlowSphere features
        public async Task<HttpResponseMessage> ExecuteNodeAsync(Dictionary<string, object> node) { /* ... */ }
        private object SubstituteVariables(object value) { /* ... */ }
        private bool EvaluateCondition(Dictionary<string, object> condition) { /* ... */ }
        private void ValidateResponse(Dictionary<string, object> node, HttpResponseMessage response) { /* ... */ }
    }

    public class UserApiTests
    {
        [Fact]
        public async Task Create_new_user()
        {
            var sequence = new APISequence(config);
            var response = await sequence.ExecuteNodeAsync(node);
            Assert.NotNull(response);
        }
    }
}
```

2. **.csproj File** - Complete with all NuGet packages

### Running Generated xUnit Tests

```bash
# Create project
dotnet new xunit -n UserApiTests
cd UserApiTests

# Add packages
dotnet add package xunit --version 2.6.0
dotnet add package Newtonsoft.Json --version 13.0.3

# Copy generated file
# (save as UserApiTests.cs)

# Run tests
dotnet test

# Run with verbose output
dotnet test --logger "console;verbosity=detailed"
```

### NUnit Generation

NUnit uses the constraint model for assertions:

```csharp
// NUnit uses Assert.That with constraints
Assert.That(actualValue, Is.EqualTo(expectedValue));
Assert.That(response.StatusCode, Is.EqualTo(200));
Assert.That(fieldValue, Does.Contain("expected"));
```

**Key differences from xUnit:**
- `[TestFixture]` attribute for test classes
- `[Test]` attribute instead of `[Fact]`
- `[SetUp]` method instead of constructor
- Constraint model: `Assert.That(actual, Is.EqualTo(expected))`

### SpecFlow/BDD Generation

SpecFlow generates two files:

1. **Gherkin Feature File** (`UserApi.feature`):
```gherkin
Feature: User API Tests
  API testing scenarios for user management

  Scenario: Create new user
    Given I have the API base URL from configuration
    When I execute POST request to "/users"
    Then the response status code should be 201
    And the response field "$.id" should exists ""
```

2. **Step Definitions** (`UserApiSteps.cs`):
```csharp
using TechTalk.SpecFlow;
using NUnit.Framework;

[Binding]
public class UserApiSteps
{
    private HttpClient _httpClient;
    private HttpResponseMessage _lastResponse;

    [Given(@"I have the API base URL from configuration")]
    public void GivenIHaveTheAPIBaseURL() { /* ... */ }

    [When(@"I execute (GET|POST|PUT|DELETE|PATCH) request to ""([^""]*)""")]
    public async Task WhenIExecuteRequest(string method, string url) { /* ... */ }

    [Then(@"the response status code should be (\d+)")]
    public void ThenStatusCodeShouldBe(int expectedStatus) { /* ... */ }
}
```

### Running Generated SpecFlow Tests

```bash
# Create project
dotnet new classlib -n UserApiTests
cd UserApiTests

# Add packages
dotnet add package SpecFlow --version 3.9.0
dotnet add package SpecFlow.NUnit --version 3.9.0

# Create folder structure
mkdir Features
mkdir StepDefinitions

# Copy generated files
mv *.feature Features/
mv *Steps.cs StepDefinitions/

# Run tests
dotnet test

# Generate living documentation
livingdoc test-assembly UserApiTests.dll -t TestExecution.json
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

### 6. `generate_javascript_jest`
Generates production-ready JavaScript Jest tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_suite_name` (optional): Custom test suite name

**Output:**
- `status`: "success" or "error"
- `code`: Generated JavaScript Jest test code
- `package_json`: Complete package.json with all dependencies
- `language`: "JavaScript"
- `framework`: "Jest"
- `dependencies`: List of required npm packages (jest, axios, jsonpath)
- `usage_instructions`: How to run the generated tests

**Features:**
- Modern ES6+ syntax with async/await
- Complete APISequence class implementation
- Full support for all 18 FlowSphere features
- Ready-to-run test suite
- Comprehensive error handling

### 7. `generate_javascript_mocha`
Generates production-ready JavaScript Mocha tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name

**Output:**
- `status`: "success" or "error"
- `code`: Generated JavaScript Mocha test code
- `package_json`: Complete package.json with all dependencies
- `language`: "JavaScript"
- `framework`: "Mocha"
- `dependencies`: List of required npm packages (mocha, chai, axios, jsonpath-plus, uuid)
- `usage_instructions`: How to run the generated tests

**Features:**
- Mocha describe/it syntax
- Chai expect assertions
- beforeEach hooks for setup
- Configurable timeouts
- Full support for all 18 FlowSphere features

### 8. `generate_javascript_cucumber`
Generates production-ready JavaScript Cucumber/BDD tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name

**Output:**
- `status`: "success" or "error"
- `feature`: Generated Gherkin feature file content
- `steps`: Generated step definitions file content
- `language`: "JavaScript"
- `framework`: "Cucumber"
- `dependencies`: List of required npm packages (@cucumber/cucumber, axios, jsonpath-plus, uuid, chai)
- `package_json`: Complete package.json with all dependencies
- `note`: Instructions on file organization

**Features:**
- Gherkin feature files with human-readable scenarios
- Given/When/Then step definitions
- APIWorld class for state management
- Living documentation for stakeholders
- Reusable steps across multiple features
- Full support for all 18 FlowSphere features

### 9. `generate_csharp_xunit`
Generates production-ready C# xUnit tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)

**Output:**
- `status`: "success" or "error"
- `code`: Generated C# xUnit test file content
- `language`: "C#"
- `framework`: "xUnit"
- `dependencies`: List of required NuGet packages (xunit, Newtonsoft.Json, etc.)
- `csproj`: Complete .csproj file with all package references
- `usage_instructions`: Markdown guide for running tests

**Features:**
- Modern C# with async/await
- HttpClient for HTTP requests
- [Fact] and [Theory] attributes
- xUnit Assert methods
- Complete .csproj template
- Full support for all 18 FlowSphere features

### 10. `generate_csharp_nunit`
Generates production-ready C# NUnit tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)

**Output:**
- `status`: "success" or "error"
- `code`: Generated C# NUnit test file content
- `language`: "C#"
- `framework`: "NUnit"
- `dependencies`: List of required NuGet packages (NUnit, Newtonsoft.Json, etc.)
- `csproj`: Complete .csproj file with all package references
- `usage_instructions`: Markdown guide for running tests

**Features:**
- Modern C# with async/await
- HttpClient for HTTP requests
- [TestFixture] and [Test] attributes
- [SetUp] lifecycle methods
- Constraint model assertions (Assert.That, Is.EqualTo, Does.Contain)
- Complete .csproj template
- Full support for all 18 FlowSphere features

### 11. `generate_csharp_specflow`
Generates production-ready C# SpecFlow/BDD tests from a FlowSphere config.

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name
- `step_class_name` (optional): Custom step definitions class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)

**Output:**
- `status`: "success" or "error"
- `feature`: Generated Gherkin feature file content
- `steps`: Generated C# step definitions file content
- `language`: "C#"
- `framework`: "SpecFlow"
- `dependencies`: List of required NuGet packages (SpecFlow, NUnit, etc.)
- `csproj`: Complete .csproj file with all package references
- `note`: Instructions on file organization

**Features:**
- Gherkin feature files with human-readable scenarios
- C# step definitions with [Binding], [Given], [When], [Then] attributes
- Async/await support in step definitions
- Living documentation support
- SpecFlow + NUnit integration
- Complete .csproj template
- Full support for all 18 FlowSphere features

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
