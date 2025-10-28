# FlowSphere MCP Server Usage Guide

This skill teaches you how to use the FlowSphere MCP Server to generate production-ready test code from FlowSphere configuration files.

## What is FlowSphere MCP Server?

FlowSphere MCP Server is a Model Context Protocol (MCP) server that generates executable test code in multiple languages (Python, JavaScript, C#) from FlowSphere configuration files (JSON).

**Key Capabilities:**
- Generates production-ready test code in 8 frameworks across 3 languages
- Supports all 18 FlowSphere features (HTTP methods, variables, conditions, validations)
- Provides complete schema documentation
- Returns runnable code with all dependencies specified

## Available Languages & Frameworks

1. **Python**
   - pytest (unit testing)
   - behave (BDD/Gherkin)

2. **JavaScript**
   - Jest (modern testing)
   - Mocha + Chai (traditional testing)
   - Cucumber (BDD/Gherkin)

3. **C#**
   - xUnit (modern .NET testing)
   - NUnit (traditional .NET testing)
   - SpecFlow (BDD/Gherkin)

## Available MCP Tools (11 Total)

### Schema Tools (3)

#### 1. `get_flowsphere_schema`
Returns complete FlowSphere configuration schema documentation.

**Usage:**
```python
result = mcp.call_tool("get_flowsphere_schema", {})
```

**When to use:** When you need to understand the FlowSphere config structure, available properties, or validation rules.

#### 2. `get_flowsphere_features`
Returns detailed documentation of all 18 FlowSphere features with implementation notes.

**Usage:**
```python
result = mcp.call_tool("get_flowsphere_features", {})
```

**When to use:** When you need to understand specific features like variable substitution, conditions, or validations.

#### 3. `get_feature_checklist`
Returns a checklist of all 18 features that must be supported in generated code.

**Usage:**
```python
result = mcp.call_tool("get_feature_checklist", {})
```

**When to use:** When verifying that generated code supports all required features.

### Python Code Generation Tools (2)

#### 4. `generate_python_pytest`
Generates production-ready Python pytest code.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name

**Output:**
- `status`: "success" or "error"
- `code`: Generated pytest code
- `dependencies`: List of required pip packages
- `usage_instructions`: How to run the tests

**Example:**
```python
result = mcp.call_tool("generate_python_pytest", {
    "config": {
        "name": "User API Tests",
        "defaults": {
            "baseUrl": "https://api.example.com",
            "headers": {"Authorization": "Bearer token123"}
        },
        "nodes": [
            {
                "id": "get_users",
                "name": "Get all users",
                "method": "GET",
                "url": "/users",
                "validations": [
                    {"httpStatusCode": 200}
                ]
            }
        ]
    },
    "test_class_name": "UserApiTests"
})

print(result['code'])  # Generated pytest code
```

#### 5. `generate_python_behave`
Generates Python behave/BDD tests (Gherkin feature file + step definitions).

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature name

**Output:**
- `status`: "success" or "error"
- `code`: Combined output with file separators
- `dependencies`: List of required pip packages
- `note`: Instructions on file organization

**Example:**
```python
result = mcp.call_tool("generate_python_behave", {
    "config": {
        "name": "User Management",
        "nodes": [...]
    },
    "feature_name": "user_management"
})

# Result contains both .feature and _steps.py files
```

### JavaScript Code Generation Tools (3)

#### 6. `generate_javascript_jest`
Generates JavaScript Jest tests.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name

**Output:**
- `status`: "success" or "error"
- `code`: Generated Jest code
- `package_json`: Complete package.json with dependencies
- `dependencies`: List of required npm packages

**Example:**
```python
result = mcp.call_tool("generate_javascript_jest", {
    "config": {
        "name": "Product API Tests",
        "defaults": {
            "baseUrl": "https://api.store.com"
        },
        "nodes": [
            {
                "id": "get_products",
                "method": "GET",
                "url": "/products"
            }
        ]
    }
})

print(result['code'])          # Save as *.test.js
print(result['package_json'])  # Save as package.json
```

#### 7. `generate_javascript_mocha`
Generates JavaScript Mocha + Chai tests.

**Input/Output:** Same as Jest, but generates Mocha/Chai syntax.

**Key differences from Jest:**
- Uses `describe()` and `it()` instead of `test()`
- Uses Chai `expect().to.equal()` instead of Jest `expect().toBe()`
- Includes `this.timeout()` configuration

#### 8. `generate_javascript_cucumber`
Generates JavaScript Cucumber/BDD tests (Gherkin + step definitions).

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature name

**Output:**
- `feature`: Gherkin feature file content (save as *.feature)
- `steps`: Step definitions (save as *_steps.js)
- `package_json`: Complete package.json

### C# Code Generation Tools (3)

#### 9. `generate_csharp_xunit`
Generates C# xUnit tests with async/await.

**Input:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)

**Output:**
- `code`: Generated C# xUnit code
- `csproj`: Complete .csproj file with NuGet packages
- `dependencies`: List of NuGet packages

**Example:**
```python
result = mcp.call_tool("generate_csharp_xunit", {
    "config": {
        "name": "Order API Tests",
        "defaults": {
            "baseUrl": "https://api.shop.com"
        },
        "nodes": [...]
    },
    "namespace": "MyCompany.Tests"
})

# Save as OrderApiTests.cs
```

#### 10. `generate_csharp_nunit`
Generates C# NUnit tests with constraint model assertions.

**Input/Output:** Same as xUnit, but generates NUnit syntax.

**Key differences from xUnit:**
- Uses `[TestFixture]` and `[Test]` instead of `[Fact]`
- Uses `Assert.That(actual, Is.EqualTo(expected))` constraint model
- Includes `[SetUp]` method

#### 11. `generate_csharp_specflow`
Generates C# SpecFlow/BDD tests (Gherkin + C# step definitions).

**Input:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature name
- `step_class_name` (optional): Custom step class name
- `namespace` (optional): Custom namespace

**Output:**
- `feature`: Gherkin feature file (save as *.feature)
- `steps`: C# step definitions (save as *Steps.cs)
- `csproj`: Complete .csproj file

## FlowSphere Configuration Structure

### Basic Structure

```json
{
  "name": "Test Suite Name",
  "description": "Optional description",
  "enableDebug": false,
  "defaults": {
    "baseUrl": "https://api.example.com",
    "headers": {
      "Content-Type": "application/json"
    },
    "timeout": 30000
  },
  "variables": {
    "apiKey": "your-api-key",
    "userId": "123"
  },
  "nodes": [
    {
      "id": "node1",
      "name": "Test Name",
      "method": "GET|POST|PUT|DELETE|PATCH",
      "url": "/endpoint",
      "headers": {},
      "body": {},
      "conditions": [],
      "validations": []
    }
  ]
}
```

### Node Structure (Full)

```json
{
  "id": "unique_node_id",
  "name": "Human readable name",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "url": "/api/endpoint",
  "headers": {
    "Authorization": "Bearer {{ .vars.token }}"
  },
  "body": {
    "field": "{{ $guid }}",
    "timestamp": "{{ $timestamp }}"
  },
  "conditions": [
    {
      "leftValue": "{{ .vars.userId }}",
      "operator": "greaterThan",
      "rightValue": "0"
    }
  ],
  "validations": [
    {
      "httpStatusCode": 200
    },
    {
      "field": "$.data.id",
      "operator": "exists"
    },
    {
      "field": "$.data.name",
      "operator": "equals",
      "value": "Expected Name"
    }
  ],
  "skipDefaultHeaders": false,
  "skipDefaultValidations": false
}
```

## Variable Substitution (4 Types)

### 1. Dynamic Placeholders
- `{{ $guid }}` - Generates a new UUID
- `{{ $timestamp }}` - Generates Unix timestamp in milliseconds

### 2. Global Variables
- `{{ .vars.variableName }}` - References variables from config.variables

### 3. Response References
- `{{ .responses.nodeId.field }}` - References field from previous node's response
- Supports JSONPath: `{{ .responses.login.$.token }}`

### 4. User Input
- `{{ .input.variableName }}` - References user-provided input

## Condition Operators (8)

1. `equals` - Exact match
2. `notEquals` - Not equal
3. `contains` - String contains
4. `notContains` - String does not contain
5. `greaterThan` - Numeric comparison
6. `lessThan` - Numeric comparison
7. `exists` - Field exists (not null)
8. `notExists` - Field is null

## Validation Operators (Same 8 + HTTP Status)

Plus: `httpStatusCode` validation for HTTP response codes.

## Best Practices for Using the MCP Server

### 1. Start with Schema
Always check the schema first if you're unsure about config structure:
```python
schema = mcp.call_tool("get_flowsphere_schema", {})
```

### 2. Validate Your Config
Before generating code, ensure your config is valid:
- All nodes have required fields (id, method, url)
- HTTP methods are uppercase
- JSONPath expressions start with $
- Variable references use correct syntax

### 3. Use Appropriate Framework
- **Unit testing:** pytest, Jest, xUnit, NUnit
- **BDD/Living docs:** behave, Cucumber, SpecFlow
- **Traditional testing:** Mocha, NUnit
- **Modern testing:** Jest, xUnit

### 4. Check Generated Dependencies
All tools return a `dependencies` field - make sure to install these before running tests.

### 5. Use Custom Names When Needed
Provide `test_class_name`, `feature_name`, or `namespace` for better organization.

## Common Usage Patterns

### Pattern 1: Simple API Test
```python
config = {
    "name": "Health Check",
    "defaults": {"baseUrl": "https://api.example.com"},
    "nodes": [{
        "id": "health",
        "method": "GET",
        "url": "/health",
        "validations": [{"httpStatusCode": 200}]
    }]
}

code = mcp.call_tool("generate_python_pytest", {"config": config})
```

### Pattern 2: Authentication Flow
```python
config = {
    "name": "Auth Flow",
    "nodes": [
        {
            "id": "login",
            "method": "POST",
            "url": "/auth/login",
            "body": {"username": "test", "password": "pass"}
        },
        {
            "id": "get_profile",
            "method": "GET",
            "url": "/user/profile",
            "headers": {
                "Authorization": "Bearer {{ .responses.login.token }}"
            }
        }
    ]
}
```

### Pattern 3: Conditional Execution
```python
config = {
    "nodes": [
        {
            "id": "check_feature",
            "method": "GET",
            "url": "/feature-flags"
        },
        {
            "id": "use_feature",
            "method": "POST",
            "url": "/feature/action",
            "conditions": [{
                "leftValue": "{{ .responses.check_feature.enabled }}",
                "operator": "equals",
                "rightValue": "true"
            }]
        }
    ]
}
```

### Pattern 4: Multi-Framework Generation
Generate tests in multiple languages for the same config:
```python
config = {...}

# Generate for all frameworks
pytest_code = mcp.call_tool("generate_python_pytest", {"config": config})
jest_code = mcp.call_tool("generate_javascript_jest", {"config": config})
xunit_code = mcp.call_tool("generate_csharp_xunit", {"config": config})
```

## Error Handling

All tools return `status: "success"` or `status: "error"`.

Check status before using the code:
```python
result = mcp.call_tool("generate_python_pytest", {"config": config})

if result['status'] == 'error':
    print(f"Error: {result['error']}")
else:
    print(result['code'])
```

## When to Use Each Tool

| Tool | Use When |
|------|----------|
| `get_flowsphere_schema` | Need config structure documentation |
| `get_flowsphere_features` | Need feature implementation details |
| `get_feature_checklist` | Verifying feature support |
| `generate_python_pytest` | Python unit testing |
| `generate_python_behave` | Python BDD/Gherkin |
| `generate_javascript_jest` | Modern JavaScript testing |
| `generate_javascript_mocha` | Traditional JavaScript testing |
| `generate_javascript_cucumber` | JavaScript BDD/Gherkin |
| `generate_csharp_xunit` | Modern .NET testing |
| `generate_csharp_nunit` | Traditional .NET testing |
| `generate_csharp_specflow` | .NET BDD/Gherkin |

## Complete Example Workflow

```python
# 1. Get schema to understand structure
schema = mcp.call_tool("get_flowsphere_schema", {})

# 2. Create your FlowSphere config
config = {
    "name": "User API Tests",
    "defaults": {
        "baseUrl": "https://api.example.com",
        "headers": {"Content-Type": "application/json"}
    },
    "variables": {
        "testUserId": "12345"
    },
    "nodes": [
        {
            "id": "get_user",
            "name": "Get user by ID",
            "method": "GET",
            "url": "/users/{{ .vars.testUserId }}",
            "validations": [
                {"httpStatusCode": 200},
                {"field": "$.id", "operator": "equals", "value": "{{ .vars.testUserId }}"}
            ]
        },
        {
            "id": "update_user",
            "name": "Update user name",
            "method": "PUT",
            "url": "/users/{{ .vars.testUserId }}",
            "body": {
                "name": "Updated Name {{ $timestamp }}"
            },
            "validations": [
                {"httpStatusCode": 200}
            ]
        }
    ]
}

# 3. Generate code in your preferred language
result = mcp.call_tool("generate_python_pytest", {
    "config": config,
    "test_class_name": "UserApiTests"
})

# 4. Check for errors
if result['status'] == 'error':
    print(f"Generation failed: {result['error']}")
    exit(1)

# 5. Save the generated code
with open('test_user_api.py', 'w') as f:
    f.write(result['code'])

# 6. Install dependencies (from result['dependencies'])
# pip install pytest requests jsonpath-ng

# 7. Run the tests
# pytest test_user_api.py -v
```

## Summary

The FlowSphere MCP Server provides 11 MCP tools to generate production-ready test code from JSON configurations. It supports 8 frameworks across 3 languages, all 18 FlowSphere features, and returns complete, runnable code with dependencies and usage instructions.

**Key Points:**
- Always validate your FlowSphere config structure
- Choose the appropriate framework for your needs
- Check the `status` field in responses
- Install dependencies before running generated tests
- Use variable substitution for dynamic values
- Leverage conditions for complex test flows
