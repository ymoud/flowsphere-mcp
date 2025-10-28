# FlowSphere MCP Server v1.0.0 Release Notes

**Release Date:** October 28, 2025

We're excited to announce the first stable release of FlowSphere MCP Server! This MCP server transforms FlowSphere configuration files into production-ready test code across multiple programming languages and testing frameworks.

## What's New in v1.0.0

### 🎉 Complete Feature Set
- **3 Programming Languages:** Python, JavaScript
- **3 Testing Frameworks:** pytest, behave/BDD, Jest
- **6 MCP Tools:** 3 schema documentation + 3 code generators
- **18/18 FlowSphere Features:** 100% feature coverage
- **98 Tests:** All passing (100% test coverage)

### 🚀 Phase 4: JavaScript Jest Code Generation (New!)

Generate modern JavaScript test code with:
- ✅ ES6+ syntax with async/await
- ✅ Complete APISequence class for all FlowSphere features
- ✅ Jest integration with describe/test blocks
- ✅ axios HTTP client
- ✅ JSONPath response validation
- ✅ Auto-generated package.json
- ✅ 30 comprehensive tests (100% passing)

**Example Usage:**
```javascript
// Generated Jest test code runs immediately
describe('API Tests', () => {
  test('User login and profile fetch', async () => {
    const sequence = new APISequence(config);
    await sequence.run();
    // All validations automatically applied
  });
});
```

### 📦 Publishing Ready

This release includes complete distribution setup:
- ✅ PyPI package configuration (`setup.py`, `MANIFEST.in`)
- ✅ Smithery registry submission ready (`smithery.json`)
- ✅ Comprehensive documentation (`PUBLISHING_GUIDE.md`)
- ✅ User testing guide (`USER_TESTING_GUIDE.md`)
- ✅ Complete changelog (`CHANGELOG.md`)

**Installation (after publishing):**
```bash
# Via pip (coming soon)
pip install flowsphere-mcp-server

# Via Smithery (coming soon)
npx @smithery/cli install flowsphere-mcp-server

# From source (available now)
git clone https://github.com/ymoud/flowsphere-mcp.git
cd flowsphere-mcp
pip install -r requirements.txt
```

## All Available Features

### Python pytest Generation (Phase 2)
Generate production-ready pytest code with:
- Complete APISequence base class
- Full variable substitution support
- Comprehensive HTTP request handling
- Response validation with JSONPath
- Condition evaluation
- Debug mode support

### Python behave/BDD Generation (Phase 3)
Generate human-readable BDD tests with:
- Gherkin feature files
- Step definitions with @given/@when/@then decorators
- APIContext state management
- Living documentation
- Stakeholder-friendly test scenarios

### JavaScript Jest Generation (Phase 4)
Generate modern JavaScript tests with:
- ES6+ async/await syntax
- Complete APISequence implementation
- Jest test framework integration
- package.json with all dependencies
- Ready-to-run test suites

## MCP Tools Available

### Schema Documentation Tools
1. **`get_flowsphere_schema`** - Complete FlowSphere config schema
2. **`get_flowsphere_features`** - Detailed feature documentation (18 features)
3. **`get_feature_checklist`** - Implementation checklist

### Code Generation Tools
4. **`generate_python_pytest`** - Generate Python pytest code
5. **`generate_python_behave`** - Generate Python behave/BDD tests
6. **`generate_javascript_jest`** - Generate JavaScript Jest tests (NEW!)

## Complete FlowSphere Feature Support

All generated code supports these 18 features:

✅ **HTTP Execution**
- All HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Custom headers and authentication
- Request body (JSON, form data)
- Timeout configuration

✅ **Variable Substitution** (4 types)
- `{{ .vars.x }}` - Global variables
- `{{ .responses.nodeId.field }}` - Response field references
- `{{ .input.x }}` - User input prompts
- `{{ $guid }}`, `{{ $timestamp }}` - Dynamic values

✅ **Condition Evaluation** (8 operators)
- `equals`, `notEquals`, `contains`, `notContains`
- `greaterThan`, `lessThan`, `exists`, `notExists`
- AND logic for multiple conditions
- Variable substitution in conditions

✅ **Response Validation**
- HTTP status code validation
- JSONPath field extraction and validation
- All comparison operators
- Multiple validations per request

✅ **Additional Features**
- User interaction (prompts, browser launch)
- Skip flags (default headers, default validations)
- Debug mode for detailed logging
- State management across nodes
- Defaults merging (global + node-specific)

## Project Metrics

- **Total Files:** 35+
- **Total Lines of Code:** 6,700+
- **Tests Passing:** 98/98 (100%)
  - 3 schema documentation tests
  - 31 pytest generator tests
  - 34 behave generator tests
  - 30 JavaScript generator tests
- **Code Generators:** 3 (Python pytest, Python behave, JavaScript Jest)
- **Template Files:** 5 (pytest, behave, gherkin, step definitions, Jest)
- **Test Fixtures:** 5 comprehensive configurations
- **Documentation Files:** 7 (README, ROADMAP, CHANGELOG, PUBLISHING_GUIDE, USER_TESTING_GUIDE, LICENSE, RELEASE_NOTES)

## Technical Details

### Dependencies
- Python 3.10+
- MCP SDK (>=0.1.0)
- Jinja2 (>=3.1.0)
- pytest, pytest-asyncio (dev)

### Generated Code Dependencies

**Python (pytest):**
- pytest
- requests
- jsonpath-ng

**Python (behave):**
- behave
- requests
- jsonpath-ng

**JavaScript (Jest):**
- jest
- axios
- jsonpath

## What's Next?

### Phase 5: C# Code Generation (Planned)
- xUnit test generator
- NUnit test generator
- SpecFlow BDD generator

### Phase 6: Distribution (In Progress)
- PyPI publication
- Smithery registry submission
- Docker image (optional)
- Community outreach

See [ROADMAP.md](ROADMAP.md) for complete development plan.

## Breaking Changes

None - this is the first stable release.

## Bug Fixes

None - this is the first stable release.

## Known Issues

None at this time.

## How to Use

### 1. Install the MCP Server

```bash
# Clone the repository
git clone https://github.com/ymoud/flowsphere-mcp.git
cd flowsphere-mcp

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the MCP Server

```bash
python src/flowsphere_mcp/server.py
```

### 3. Use with Claude Code or Other MCP Clients

The server provides 6 MCP tools that AI agents can call to generate code from FlowSphere configurations.

### 4. Generate Test Code

```python
# Example: Generate Python pytest code
result = mcp_client.call_tool(
    "generate_python_pytest",
    {"config": your_flowsphere_config}
)

# Example: Generate JavaScript Jest code
result = mcp_client.call_tool(
    "generate_javascript_jest",
    {"config": your_flowsphere_config}
)
```

See [USER_TESTING_GUIDE.md](USER_TESTING_GUIDE.md) for detailed usage examples.

## Documentation

- **README.md** - Project overview and quick start
- **ROADMAP.md** - Development phases and progress
- **CHANGELOG.md** - Detailed version history
- **PUBLISHING_GUIDE.md** - Distribution instructions
- **USER_TESTING_GUIDE.md** - User testing and examples

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **GitHub Issues:** https://github.com/ymoud/flowsphere-mcp/issues
- **Documentation:** https://github.com/ymoud/flowsphere-mcp/blob/main/README.md

## Credits

Created and maintained by Yannis Moudilos ([@ymoud](https://github.com/ymoud))

---

Thank you for using FlowSphere MCP Server! We're excited to see what you build with it. 🚀
