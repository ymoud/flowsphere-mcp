# FlowSphere MCP Server

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ymoud/flowsphere-mcp/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-153%20passing-brightgreen.svg)](tests/)
[![Code Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](tests/)
[![MCP](https://img.shields.io/badge/MCP-enabled-purple.svg)](https://modelcontextprotocol.io)

**Model Context Protocol (MCP) Server for FlowSphere Code Generation**

Transform [FlowSphere](https://github.com/ymoud/flowsphere) configuration files into production-ready test code in **Python**, **JavaScript**, and **C#**.

---

## What It Does

Generates standalone, executable test code from FlowSphere JSON configurations:

- **Python** - pytest, behave/BDD
- **JavaScript** - Jest, Mocha, Cucumber/BDD
- **C#** - xUnit, NUnit, SpecFlow/BDD

**Example:** A 20-line JSON config becomes 400+ lines of working test code with full HTTP execution, variable substitution, conditions, and validations.

---

## ✨ Quick Start

### Option 1: Use with Claude Code CLI (Recommended)

```bash
# 1. Install dependencies
cd C:\dev\GitHub\flowsphere-mcp-server
pip install -r requirements.txt

# 2. Add MCP server to Claude Code
claude mcp add --transport stdio flowsphere-mcp python "C:\dev\GitHub\flowsphere-mcp-server\src\flowsphere_mcp\server.py"

# 3. Restart Claude Code
claude

# 4. Verify connection
/mcp
# Should show: flowsphere-mcp ✓ Connected
```

Now ask Claude to generate tests:
```
"Generate Python pytest code from tests/fixtures/simple_config.json"
"Create JavaScript Jest tests from this FlowSphere config"
"Generate C# xUnit tests with namespace MyApp.Tests"
```

### Option 2: Use Python API Directly

```python
import json
from flowsphere_mcp.generators.python_generator import PythonPytestGenerator

# Load your FlowSphere config
with open('tests/fixtures/simple_config.json') as f:
    config = json.load(f)

# Generate Python pytest code
generator = PythonPytestGenerator()
code = generator.generate(config)

# Save to file
with open('test_api.py', 'w') as f:
    f.write(code)

print("✅ Generated test_api.py")
```

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)

### Install Dependencies

```bash
cd C:\dev\GitHub\flowsphere-mcp-server
pip install -r requirements.txt
```

### Configure MCP Server (Claude Code CLI)

```bash
# Add the server
claude mcp add --transport stdio flowsphere-mcp python "C:\path\to\flowsphere-mcp-server\src\flowsphere_mcp\server.py"

# Verify configuration
claude mcp list

# Get server details
claude mcp get flowsphere-mcp

# Restart Claude Code to connect
claude
```

**Configuration saved to:** `%USERPROFILE%\.claude.json`

### Troubleshooting MCP Connection

If the server shows "Failed to connect":

1. **Verify Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Check server path:**
   ```bash
   claude mcp get flowsphere-mcp
   ```
   Path should use backslashes: `C:\path\to\...`

3. **Re-add server if needed:**
   ```bash
   claude mcp remove flowsphere-mcp -s local
   claude mcp add --transport stdio flowsphere-mcp python "C:\correct\path\src\flowsphere_mcp\server.py"
   ```

4. **Restart Claude Code** to pick up changes

---

## 🚀 Usage

### All 8 Supported Generators

| Language | Framework | MCP Tool | Output |
|----------|-----------|----------|--------|
| Python | pytest | `generate_python_pytest` | Single test file |
| Python | behave (BDD) | `generate_python_behave` | Feature + steps |
| JavaScript | Jest | `generate_javascript_jest` | Test + package.json |
| JavaScript | Mocha | `generate_javascript_mocha` | Test + package.json |
| JavaScript | Cucumber (BDD) | `generate_javascript_cucumber` | Feature + steps |
| C# | xUnit | `generate_csharp_xunit` | Test + .csproj |
| C# | NUnit | `generate_csharp_nunit` | Test + .csproj |
| C# | SpecFlow (BDD) | `generate_csharp_specflow` | Feature + steps |

### Example: Python pytest

```python
# Via MCP tool
result = mcp_server.call_tool("generate_python_pytest", {
    "config": your_flowsphere_config,
    "test_class_name": "APITests"  # Optional
})

# Generated output includes:
# - Complete APISequence class with all 18 FlowSphere features
# - Test class with all test methods
# - Variable substitution, conditions, validations
# - Dependencies list and usage instructions
```

**Run the generated tests:**
```bash
pip install pytest requests jsonpath-ng
pytest test_api.py -v
```

### Example: JavaScript Jest

```javascript
// Via MCP tool
result = mcp_server.call_tool("generate_javascript_jest", {
    "config": your_flowsphere_config
})

// Returns:
// - result.code: Complete Jest test file
// - result.package_json: NPM dependencies
// - result.usage_instructions: How to run
```

**Run the generated tests:**
```bash
npm install
npm test
```

### Example: C# xUnit

```csharp
// Via MCP tool
result = mcp_server.call_tool("generate_csharp_xunit", {
    "config": your_flowsphere_config,
    "namespace": "MyApp.Tests"  // Optional
})

// Returns:
// - result.code: Complete xUnit test file
// - result.csproj: Project file with NuGet packages
// - result.usage_instructions: How to run
```

**Run the generated tests:**
```bash
dotnet test
```

### Example Configs

See **[tests/fixtures/](tests/fixtures/)** for 5 sample FlowSphere configurations:
- `simple_config.json` - Basic GET request
- `auth_flow_config.json` - Authentication with token extraction
- `conditional_config.json` - Conditional execution
- `validation_config.json` - Response validation
- `full_features_config.json` - All 18 features

**Learn more about FlowSphere:** https://github.com/ymoud/flowsphere

---

## 🧪 Testing Generated Code

### Python pytest

```bash
# Install dependencies
pip install pytest requests jsonpath-ng

# Run tests
pytest generated_test.py -v

# Run with debug output
pytest generated_test.py -v -s
```

### Python behave (BDD)

```bash
# Install dependencies
pip install behave requests jsonpath-ng

# Organize files
mkdir -p features/steps
mv *.feature features/
mv *_steps.py features/steps/

# Run tests
behave -v
```

### JavaScript Jest

```bash
# Install dependencies (from generated package.json)
npm install

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

### JavaScript Mocha

```bash
# Install dependencies
npm install --save-dev mocha chai axios jsonpath-plus uuid

# Run tests
npx mocha test_file.test.js
```

### JavaScript Cucumber

```bash
# Install dependencies
npm install --save-dev @cucumber/cucumber axios jsonpath-plus chai

# Organize files
mkdir -p features/step_definitions
mv *.feature features/
mv *_steps.js features/step_definitions/

# Run tests
npx cucumber-js
```

### C# xUnit

```bash
# Create project
dotnet new xunit -n MyTests

# Add packages (from generated .csproj)
dotnet add package xunit
dotnet add package Newtonsoft.Json

# Run tests
dotnet test
```

### C# NUnit

```bash
# Create project
dotnet new nunit -n MyTests

# Add packages
dotnet add package NUnit
dotnet add package Newtonsoft.Json

# Run tests
dotnet test
```

### C# SpecFlow

```bash
# Create project
dotnet new classlib -n MyTests

# Add packages
dotnet add package SpecFlow
dotnet add package SpecFlow.NUnit

# Organize files
mkdir Features StepDefinitions
mv *.feature Features/
mv *Steps.cs StepDefinitions/

# Run tests
dotnet test
```

---

## 🔧 Available MCP Tools

The server exposes **11 MCP tools** for AI agents:

### Schema & Documentation Tools

#### 1. `get_flowsphere_schema`
Get complete FlowSphere configuration schema documentation.

**Returns:** Comprehensive schema with all properties, types, defaults, examples

#### 2. `get_flowsphere_features`
Get detailed documentation of all 18 FlowSphere features.

**Returns:** Feature descriptions, implementation notes, examples

#### 3. `get_feature_checklist`
Get checklist of all features that must be implemented in generated code.

**Returns:** 18-item feature checklist

### Python Generators

#### 4. `generate_python_pytest`
Generate production-ready Python pytest code.

**Parameters:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `status`: "success" or "error"
- `code`: Generated Python pytest code
- `config_json`: Separate config file content
- `config_filename`: "config.json"
- `dependencies`: List of pip packages
- `usage_instructions`: How to run tests
- `generation_report`: Optional detailed report (if generate_report=true)

#### 5. `generate_python_behave`
Generate Python behave/BDD tests (Gherkin + step definitions).

**Parameters:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `code`: Combined Gherkin feature + step definitions
- `config_json`: Separate config file content
- `dependencies`: List of pip packages (behave, requests, jsonpath-ng)
- `note`: Instructions on file organization
- `generation_report`: Optional detailed report

### JavaScript Generators

#### 6. `generate_javascript_jest`
Generate JavaScript Jest tests.

**Parameters:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `code`: Generated Jest test file
- `config_json`: Separate config file content
- `package_json`: Complete package.json
- `dependencies`: List of npm packages
- `usage_instructions`: How to run tests
- `generation_report`: Optional detailed report

#### 7. `generate_javascript_mocha`
Generate JavaScript Mocha tests with Chai assertions.

**Parameters:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `code`: Generated Mocha test file
- `config_json`: Separate config file content
- `package_json`: Complete package.json
- `dependencies`: List of npm packages (mocha, chai, axios, jsonpath-plus)
- `generation_report`: Optional detailed report

#### 8. `generate_javascript_cucumber`
Generate JavaScript Cucumber/BDD tests (Gherkin + step definitions).

**Parameters:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `feature`: Gherkin feature file content
- `steps`: Step definitions file content
- `config_json`: Separate config file content
- `package_json`: Complete package.json
- `dependencies`: List of npm packages (@cucumber/cucumber, axios, chai)
- `note`: File organization instructions
- `generation_report`: Optional detailed report

### C# Generators

#### 9. `generate_csharp_xunit`
Generate C# xUnit tests.

**Parameters:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `code`: Generated xUnit test file
- `config_json`: Separate config file content
- `csproj`: Complete .csproj file with NuGet packages
- `dependencies`: List of NuGet packages (xunit, Newtonsoft.Json)
- `usage_instructions`: How to run tests
- `generation_report`: Optional detailed report

#### 10. `generate_csharp_nunit`
Generate C# NUnit tests with constraint model assertions.

**Parameters:**
- `config` (required): FlowSphere configuration object
- `test_class_name` (optional): Custom test class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `code`: Generated NUnit test file
- `config_json`: Separate config file content
- `csproj`: Complete .csproj file with NuGet packages
- `dependencies`: List of NuGet packages (NUnit, Newtonsoft.Json)
- `usage_instructions`: How to run tests
- `generation_report`: Optional detailed report

#### 11. `generate_csharp_specflow`
Generate C# SpecFlow/BDD tests (Gherkin + step definitions).

**Parameters:**
- `config` (required): FlowSphere configuration object
- `feature_name` (optional): Custom feature file name
- `step_class_name` (optional): Custom step definitions class name
- `namespace` (optional): Custom namespace (default: FlowSphere.Tests)
- `generate_report` (optional): Generate comprehensive generation report
- `save_report_to` (optional): File path to save report

**Returns:**
- `feature`: Gherkin feature file content
- `steps`: C# step definitions file content
- `config_json`: Separate config file content
- `csproj`: Complete .csproj file with NuGet packages
- `dependencies`: List of NuGet packages (SpecFlow, NUnit)
- `note`: File organization instructions
- `generation_report`: Optional detailed report

### 📊 Generation Reports

All code generation tools support optional comprehensive reports with:
- **Configuration Analysis** - Size, node count, features detected
- **Token Usage Analysis** - Input/output tokens, real-time tracking
- **Cost Estimation** - GPT-4 pricing reference, savings calculations
- **Optimization Recommendations** - Context-aware tips
- **Scaling Projections** - Daily/weekly/monthly cost estimates

**Example Usage:**
```python
result = mcp_server.call_tool("generate_python_pytest", {
    "config": your_config,
    "generate_report": True,
    "save_report_to": "reports/generation_report.md"
})

# Access the report
print(result['generation_report'])  # Full markdown report
print(result['report_path'])  # File path if saved
```

---

## ✅ Complete Feature Coverage

All generators support **ALL 18 FlowSphere features**:

### HTTP Execution
- ✅ GET, POST, PUT, DELETE, PATCH requests
- ✅ Custom headers (per-request and defaults)
- ✅ Request body (JSON)
- ✅ Timeout configuration

### Variable Substitution (4 Types)
- ✅ `{{ .vars.key }}` - Global variables
- ✅ `{{ .responses.nodeId.field }}` - Response references
- ✅ `{{ .input.variableName }}` - User input
- ✅ `{{ $guid }}`, `{{ $timestamp }}` - Dynamic placeholders

### Condition Evaluation (8 Operators)
- ✅ `equals`, `notEquals`
- ✅ `contains`, `notContains`
- ✅ `greaterThan`, `lessThan`
- ✅ `greaterThanOrEqual`, `lessThanOrEqual`
- ✅ AND logic for multiple conditions
- ✅ Variable substitution in conditions

### Response Validation
- ✅ HTTP status code validation
- ✅ JSONPath field validation with all operators
- ✅ Skip default validations flag

### Advanced Features
- ✅ Field extraction (JSONPath) with variable storage
- ✅ User prompts (`promptMessage`)
- ✅ Browser launch (`launchBrowser`)
- ✅ Skip default headers flag
- ✅ Debug mode (`enableDebug`)

---

## 📂 Project Structure

```
flowsphere-mcp-server/
├── src/flowsphere_mcp/
│   ├── server.py                    # MCP server (11 tools)
│   ├── schema/
│   │   ├── config_schema.py         # FlowSphere schema docs
│   │   └── features.py              # 18 features documentation
│   ├── templates/
│   │   ├── python/                  # pytest, behave templates
│   │   ├── javascript/              # Jest, Mocha, Cucumber templates
│   │   └── csharp/                  # xUnit, NUnit, SpecFlow templates
│   ├── generators/
│   │   ├── base_generator.py        # Base generator class
│   │   ├── python_generator.py      # Python pytest generator
│   │   ├── behave_generator.py      # Python behave generator
│   │   ├── javascript_generator.py  # JS Jest/Mocha/Cucumber generators
│   │   └── csharp_generator.py      # C# xUnit/NUnit/SpecFlow generators
│   └── utils/
│       └── report_generator.py      # Generation report builder
├── tests/
│   ├── fixtures/                    # 5 sample FlowSphere configs
│   ├── test_*_generator.py          # Generator tests (153 tests total)
│   └── generated_code/              # Example outputs
├── requirements.txt
├── ROADMAP.md
└── README.md
```

---

## 🗺️ Development Phases

- ✅ **Phase 1** - Schema provider
- ✅ **Phase 2** - Python pytest generator (31 tests)
- ✅ **Phase 3** - Python behave/BDD generator (34 tests)
- ✅ **Phase 4** - JavaScript generators (Jest, Mocha, Cucumber) (46 tests)
- ✅ **Phase 5** - C# generators (xUnit, NUnit, SpecFlow) (39 tests)
- ✅ **Phase 7.1** - Token optimization (config file loading) - 3,000 tokens saved per generation
- 🔄 **Phase 7** - Token efficiency & performance optimization (in progress)
- 📋 **Phase 6** - Publishing & distribution (PyPI, Smithery)

**Current Status:** 153 tests passing, 100% coverage, 8 production-ready generators

---

## ❓ Troubleshooting

### MCP Server Won't Connect

**Symptom:** Server shows "Failed to connect" in `/mcp` output

**Solutions:**
1. Verify Python packages are installed: `pip install -r requirements.txt`
2. Check server path in config: `claude mcp get flowsphere-mcp`
3. Ensure path uses backslashes on Windows: `C:\path\to\...`
4. Re-add the server: `claude mcp remove flowsphere-mcp -s local` then `claude mcp add...`
5. Restart Claude Code: Exit with `/exit`, then `claude`

### Generated Python Tests Fail

**Solutions:**
```bash
# Install dependencies
pip install pytest requests jsonpath-ng behave

# Verify Python version
python --version  # Should be 3.10+

# Check config file is in correct location
ls config.json  # Should be in same directory as test file
```

### Generated JavaScript Tests Fail

**Solutions:**
```bash
# Install dependencies from generated package.json
npm install

# Verify Node.js version
node --version  # Should be 16+

# Check config file location
ls config.json  # Should be in same directory as test file
```

### Generated C# Tests Fail

**Solutions:**
```bash
# Restore packages
dotnet restore

# Verify .NET SDK version
dotnet --version  # Should be 6.0+

# Check config file location
dir config.json  # Should be in project root or Configuration/ folder
```

### Import Errors in Generated Code

**Solution:** All generated code expects `config.json` to be loaded from file. Make sure to:
1. Save the `config_json` from the MCP response to a file named `config.json`
2. Place it in the same directory as your tests (or in a `configuration/` subdirectory)
3. See the `note` field in the MCP response for specific placement instructions

---

## 🆘 Support & Next Steps

### Quick Links
- **FlowSphere Documentation:** https://github.com/ymoud/flowsphere
- **Sample Configurations:** [tests/fixtures/](tests/fixtures/)
- **Roadmap:** [ROADMAP.md](ROADMAP.md)

### Next Steps

1. **Try Quick Start** - Get running in 5 minutes with Claude Code CLI
2. **Generate Your First Test** - Use one of the sample configs in `tests/fixtures/`
3. **Run the Generated Code** - See it work against real APIs
4. **Customize Configs** - Experiment with different FlowSphere features
5. **Integrate with CI/CD** - Add generated tests to your pipeline

### Running Unit Tests

Verify everything works:
```bash
# Run all tests (153 tests)
pytest tests/ -v

# Run specific generator tests
pytest tests/test_python_generator.py -v       # 31 tests
pytest tests/test_behave_generator.py -v      # 34 tests
pytest tests/test_javascript_generator.py -v  # 30 tests
pytest tests/test_mocha_generator.py -v       # 8 tests
pytest tests/test_cucumber_generator.py -v    # 8 tests
pytest tests/test_xunit_generator.py -v       # 12 tests
pytest tests/test_nunit_generator.py -v       # 14 tests
pytest tests/test_specflow_generator.py -v    # 13 tests
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

**Built with ❤️ for the FlowSphere community**
