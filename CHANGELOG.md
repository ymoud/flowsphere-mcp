# Changelog

All notable changes to the FlowSphere MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-28

### Added - Phase 4: JavaScript Jest Code Generation
- Complete JavaScript Jest code generator
- Modern ES6+ syntax with async/await
- Complete APISequence class implementation for JavaScript
- Jest test framework integration with describe/test blocks
- axios HTTP client for request execution
- JSONPath support for response field extraction
- Comprehensive package.json generation
- 30 passing tests for JavaScript generator (100% coverage)
- Support for all 18 FlowSphere features in JavaScript
- `generate_javascript_jest` MCP tool
- Template: `src/flowsphere_mcp/templates/javascript/jest_template.jinja2` (408 lines)
- Generator: `src/flowsphere_mcp/generators/javascript_generator.py` (280 lines)
- Tests: `tests/test_javascript_generator.py` (435 lines, 30 tests)

### Added - Phase 6: Publishing & Distribution Preparation
- Complete setup.py for PyPI distribution
- MANIFEST.in for package data inclusion
- smithery.json for Smithery registry submission
- PUBLISHING_GUIDE.md with multi-platform distribution instructions
- USER_TESTING_GUIDE.md for user testing
- test_user_experience.py demo script
- Updated all author information (Yannis Moudilos)
- Updated repository URLs (github.com/ymoud/flowsphere-mcp)
- CHANGELOG.md (this file)

### Changed
- Updated README.md with Phase 4 completion status
- Updated project structure documentation
- Added JavaScript Jest tool to Available MCP Tools section
- Updated development phases roadmap in README

---

## [0.3.0] - 2025-10-27

### Added - Phase 3: Python Behave/BDD Code Generation
- Complete Python behave/BDD code generator
- Gherkin feature file generation with proper BDD syntax
- Python step definitions with behave decorators (@given, @when, @then)
- APIContext class for state management across steps
- Complete support for all 18 FlowSphere features in BDD format
- Human-readable test scenarios for stakeholders
- Reusable step definitions across multiple feature files
- 34 passing tests for behave generator (100% coverage)
- `generate_python_behave` MCP tool
- Template: `src/flowsphere_mcp/templates/python/gherkin_template.jinja2` (60 lines)
- Template: `src/flowsphere_mcp/templates/python/step_definitions_template.jinja2` (350 lines)
- Generator: `src/flowsphere_mcp/generators/behave_generator.py` (380 lines)
- Tests: `tests/test_behave_generator.py` (34 tests)

### Changed
- Updated README.md with Phase 3 completion status
- Enhanced documentation with behave/BDD examples
- Added Gherkin usage instructions

---

## [0.2.0] - 2025-10-27

### Added - Phase 2: Python pytest Code Generation
- Complete Python pytest code generator
- BaseGenerator class with config validation and template rendering
- PythonPytestGenerator with full code generation pipeline
- APISequence base template with all FlowSphere feature implementations
- Jinja2 pytest template for generated test classes
- `generate_python_pytest` MCP tool
- Support for all 18 FlowSphere features:
  - HTTP execution (GET, POST, PUT, DELETE, PATCH)
  - Variable substitution (4 types: dynamic, global, response refs, user input)
  - Condition evaluation (8 operators with AND logic)
  - Response validation (HTTP status + JSONPath)
  - Skip flags (headers/validations)
  - Debug mode support
  - User prompts and browser launch
- 31 passing tests for pytest generator (100% coverage)
- 5 test fixture configurations covering all features
- End-to-end integration tests
- Code syntax validation
- Template: `src/flowsphere_mcp/templates/python/base_template.py` (372 lines)
- Template: `src/flowsphere_mcp/templates/python/pytest_template.jinja2` (364 lines)
- Generator: `src/flowsphere_mcp/generators/base_generator.py` (204 lines)
- Generator: `src/flowsphere_mcp/generators/python_generator.py` (237 lines)
- Tests: `tests/test_python_generator.py` (428 lines, 31 tests)
- Test fixtures: `tests/fixtures/*.json` (5 configs)

### Changed
- Updated README.md with Phase 2 completion status and usage examples
- Added comprehensive code generation documentation
- Improved troubleshooting guide

---

## [0.1.0] - 2025-10-26

### Added - Phase 1: Schema Documentation Provider
- Initial project structure with src/ and tests/ directories
- Comprehensive FlowSphere config schema documentation
- Detailed feature documentation (18 features)
- Feature checklist for validation
- MCP server with stdio transport
- Three MCP tools:
  - `get_flowsphere_schema` - Complete config schema documentation
  - `get_flowsphere_features` - Detailed feature descriptions
  - `get_feature_checklist` - Implementation checklist
- Schema module: `src/flowsphere_mcp/schema/config_schema.py` (300+ lines)
- Features module: `src/flowsphere_mcp/schema/features.py` (200+ lines)
- MCP server: `src/flowsphere_mcp/server.py`
- Tests: `tests/test_schema.py` (3 passing tests)
- Development roadmap documenting all planned phases
- MIT License
- README.md with project overview
- requirements.txt with dependencies

### Infrastructure
- Python 3.10+ compatibility
- MCP protocol integration
- Jinja2 template engine
- pytest test framework
- Git repository initialization

---

## Project Metrics (as of v1.0.0)

- **Total Files:** 35+
- **Total Lines of Code:** 6,700+
- **Tests Passing:** 98/98 (100%)
  - 3 schema tests
  - 31 pytest generator tests
  - 34 behave generator tests
  - 30 JavaScript generator tests
- **MCP Tools:** 6
  - 3 schema documentation tools
  - 3 code generation tools
- **Supported Languages:** 2
  - Python (pytest, behave/BDD)
  - JavaScript (Jest)
- **Supported Frameworks:** 3
  - Python pytest
  - Python behave (BDD/Cucumber)
  - JavaScript Jest
- **FlowSphere Features Supported:** 18/18 (100%)

---

## Upcoming Releases

### [2.0.0] - Planned
**Phase 5: C# Code Generation**
- xUnit test generator
- NUnit test generator
- SpecFlow BDD generator
- Complete C# async/await support
- HttpClient integration
- Newtonsoft.Json support

### [1.1.0] - Planned
**Additional JavaScript Frameworks**
- Mocha test generator
- cucumber-js BDD generator
- TypeScript type definitions
- ES6 modules vs CommonJS support

---

## Links

- **Repository:** https://github.com/ymoud/flowsphere-mcp
- **Issues:** https://github.com/ymoud/flowsphere-mcp/issues
- **Documentation:** https://github.com/ymoud/flowsphere-mcp/blob/main/README.md
- **PyPI:** Coming soon
- **Smithery:** Coming soon

---

## Contributors

- Yannis Moudilos ([@ymoud](https://github.com/ymoud)) - Creator and maintainer
