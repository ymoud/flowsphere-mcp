# FlowSphere MCP Server - User Testing Guide

This guide shows you how to test the FlowSphere MCP Server like a real user.

## Quick Start: Generate Code Now

### Option 1: Run the User Experience Test Script (Easiest)

```bash
python test_user_experience.py
```

This generates 5 files in seconds:
- `generated_user_test.py` - Python pytest test
- `generated_user_test.feature` - Gherkin feature file
- `generated_user_test_steps.py` - Python behave step definitions
- `generated_user_test.test.js` - JavaScript Jest test
- `package.json` - NPM dependencies

### Option 2: Use Python API Directly

```python
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path('src/flowsphere_mcp')))

# Choose your generator
from generators.python_generator import PythonPytestGenerator
from generators.behave_generator import PythonBehaveGenerator
from generators.javascript_generator import JavaScriptJestGenerator

# Your FlowSphere config
config = {
    "name": "My API Test",
    "defaults": {
        "baseUrl": "https://api.example.com"
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

# Generate Python pytest code
generator = PythonPytestGenerator()
code = generator.generate(config)
print(code)

# Generate Python behave code
behave_gen = PythonBehaveGenerator()
files = behave_gen.generate(config)
print(files['feature'])  # Gherkin feature
print(files['steps'])    # Step definitions

# Generate JavaScript Jest code
js_gen = JavaScriptJestGenerator()
js_code = js_gen.generate(config)
print(js_code)
```

### Option 3: Use as MCP Server with Claude Desktop

1. **Start the MCP server:**
   ```bash
   python src/flowsphere_mcp/server.py
   ```

2. **Configure Claude Desktop** - Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "flowsphere": {
         "command": "python",
         "args": [
           "C:\\dev\\GitHub\\flowsphere-mcp-server\\src\\flowsphere_mcp\\server.py"
         ]
       }
     }
   }
   ```

3. **Use in Claude Desktop:**
   - Upload your FlowSphere config JSON
   - Ask: "Generate Python pytest code from this config"
   - Ask: "Generate JavaScript Jest tests from this config"
   - Ask: "Generate Python behave BDD tests from this config"

## Testing Generated Code

### Python pytest Tests

```bash
# Install dependencies
pip install pytest requests jsonpath-ng

# Run the tests
pytest generated_user_test.py -v

# Run with debug output
pytest generated_user_test.py -v -s
```

### Python behave Tests

```bash
# Install dependencies
pip install behave requests jsonpath-ng

# Organize files
mkdir -p features/steps
mv generated_user_test.feature features/
mv generated_user_test_steps.py features/steps/

# Run the tests
behave

# Run with verbose output
behave -v

# Run specific scenario
behave -n "Get all users"
```

### JavaScript Jest Tests

```bash
# Install dependencies
npm install

# Run the tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Available MCP Tools

The server provides 6 MCP tools:

### 1. `get_flowsphere_schema`
Get complete FlowSphere configuration schema documentation.

**Example:**
```python
result = mcp_server.call_tool("get_flowsphere_schema", {})
# Returns comprehensive schema docs
```

### 2. `get_flowsphere_features`
Get detailed documentation of all 18 FlowSphere features.

**Example:**
```python
result = mcp_server.call_tool("get_flowsphere_features", {})
# Returns feature implementation notes
```

### 3. `get_feature_checklist`
Get a checklist of all features that must be implemented.

**Example:**
```python
result = mcp_server.call_tool("get_feature_checklist", {})
# Returns 18-item checklist
```

### 4. `generate_python_pytest`
Generate production-ready Python pytest code.

**Example:**
```python
result = mcp_server.call_tool("generate_python_pytest", {
    "config": {
        "name": "My Test",
        "nodes": [...]
    },
    "test_class_name": "MyCustomTest"  # Optional
})

print(result['code'])  # Generated pytest code
```

### 5. `generate_python_behave`
Generate Python behave/BDD tests (Gherkin + step definitions).

**Example:**
```python
result = mcp_server.call_tool("generate_python_behave", {
    "config": {
        "name": "My Test",
        "nodes": [...]
    },
    "feature_name": "my_test"  # Optional
})

# Result contains both files separated by markers
print(result['code'])
```

### 6. `generate_javascript_jest`
Generate JavaScript Jest tests.

**Example:**
```python
result = mcp_server.call_tool("generate_javascript_jest", {
    "config": {
        "name": "My Test",
        "nodes": [...]
    }
})

print(result['code'])  # Generated Jest code
print(result['package_json'])  # package.json content
```

## Sample FlowSphere Configs

### Basic GET Request

```json
{
  "name": "Simple GET Test",
  "defaults": {
    "baseUrl": "https://jsonplaceholder.typicode.com"
  },
  "nodes": [
    {
      "id": "get_posts",
      "name": "Get all posts",
      "method": "GET",
      "url": "/posts"
    }
  ]
}
```

### POST with Variable Substitution

```json
{
  "name": "Create Post Test",
  "defaults": {
    "baseUrl": "https://jsonplaceholder.typicode.com"
  },
  "nodes": [
    {
      "id": "create_post",
      "name": "Create a new post",
      "method": "POST",
      "url": "/posts",
      "body": {
        "title": "Post {{ $guid }}",
        "body": "Created at {{ $timestamp }}",
        "userId": 1
      },
      "validations": [
        {"httpStatusCode": 201},
        {"field": "title", "operator": "contains", "value": "Post"}
      ]
    }
  ]
}
```

### Auth Flow with Response References

```json
{
  "name": "Authentication Flow",
  "defaults": {
    "baseUrl": "https://api.example.com"
  },
  "nodes": [
    {
      "id": "login",
      "name": "Login to get token",
      "method": "POST",
      "url": "/auth/login",
      "body": {
        "username": "testuser",
        "password": "testpass"
      },
      "extractFields": [
        {
          "jsonPath": "token",
          "variableName": "authToken"
        }
      ]
    },
    {
      "id": "get_profile",
      "name": "Get user profile",
      "method": "GET",
      "url": "/user/profile",
      "headers": {
        "Authorization": "Bearer {{ .vars.authToken }}"
      }
    }
  ]
}
```

### Conditional Execution

```json
{
  "name": "Conditional Test",
  "defaults": {
    "baseUrl": "https://jsonplaceholder.typicode.com"
  },
  "nodes": [
    {
      "id": "get_post",
      "name": "Get post",
      "method": "GET",
      "url": "/posts/1",
      "extractFields": [
        {
          "jsonPath": "userId",
          "variableName": "userId"
        }
      ]
    },
    {
      "id": "get_user",
      "name": "Get user if userId > 0",
      "method": "GET",
      "url": "/users/{{ .vars.userId }}",
      "condition": {
        "leftValue": "{{ .vars.userId }}",
        "operator": "greaterThan",
        "rightValue": "0"
      }
    }
  ]
}
```

## All 18 Supported Features

All generators support these features:

1. ✅ HTTP GET requests
2. ✅ HTTP POST requests
3. ✅ HTTP PUT requests
4. ✅ HTTP DELETE requests
5. ✅ HTTP PATCH requests
6. ✅ Custom headers
7. ✅ Request body
8. ✅ Timeout configuration
9. ✅ Variable substitution - {{ .vars.key }}
10. ✅ Response references - {{ .responses.nodeId.field }}
11. ✅ User input - {{ .input.variableName }}
12. ✅ Dynamic placeholders - {{ $guid }}, {{ $timestamp }}
13. ✅ Condition evaluation (8 operators: equals, notEquals, contains, notContains, greaterThan, lessThan, greaterThanOrEqual, lessThanOrEqual)
14. ✅ Response validation (HTTP status + JSONPath)
15. ✅ Field extraction (JSONPath)
16. ✅ User prompts (promptMessage)
17. ✅ Browser launch (launchBrowser)
18. ✅ Skip flags (skipDefaultHeaders, skipDefaultValidations)

## Running Unit Tests

To verify everything works:

```bash
# Run all tests (98 tests)
pytest tests/ -v

# Run specific generator tests
pytest tests/test_python_generator.py -v      # 31 tests
pytest tests/test_behave_generator.py -v     # 34 tests
pytest tests/test_javascript_generator.py -v  # 30 tests
pytest tests/test_schema.py -v                # 3 tests
```

## Troubleshooting

### Python Tests Fail

```bash
# Make sure dependencies are installed
pip install pytest requests jsonpath-ng behave

# Verify Python version
python --version  # Should be 3.10+
```

### JavaScript Tests Fail

```bash
# Install dependencies
npm install

# Verify Node.js version
node --version  # Should be 16+
```

### MCP Server Won't Start

```bash
# Check Python path
python src/flowsphere_mcp/server.py

# Verify MCP package
pip install mcp
```

## Next Steps

1. **Try the Quick Start script** - `python test_user_experience.py`
2. **Examine the generated code** - See how FlowSphere configs become runnable tests
3. **Run the generated tests** - Execute against real APIs
4. **Modify configs** - Experiment with different features
5. **Integrate with CI/CD** - Add generated tests to your pipeline

## Support

- **Documentation:** README.md
- **Roadmap:** ROADMAP.md
- **Issues:** https://github.com/anthropics/claude-code/issues
