# FlowSphere MCP Server - Development Roadmap

This document outlines the development phases for the FlowSphere MCP Server code generation project.

## ✅ Phase 1: Schema Documentation Provider (COMPLETED)

**Status:** Complete
**Commit:** `f400d9e`

**Deliverables:**
- [x] Project structure with src/ and tests/ directories
- [x] Comprehensive config schema documentation (`config_schema.py`)
- [x] Detailed feature documentation (`features.py`)
- [x] Feature checklist (18 items) for validation
- [x] MCP server with stdio transport
- [x] Three MCP tools: get_flowsphere_schema, get_flowsphere_features, get_feature_checklist
- [x] Comprehensive tests (all passing)

**Files Created:**
- `src/flowsphere_mcp/schema/config_schema.py` (300+ lines)
- `src/flowsphere_mcp/schema/features.py` (200+ lines)
- `src/flowsphere_mcp/server.py`
- `tests/test_schema.py`

---

## ✅ Phase 2: Python pytest Code Generation (COMPLETED)

**Status:** Complete
**Completion Date:** 2025-10-27
**Goal:** Generate production-ready Python pytest code from FlowSphere configs

### Tasks

#### 2.1 Create Python Code Templates
- [x] Create base template class (`templates/python/base_template.py`)
- [x] Create pytest test class template with:
  - [x] APISequence class structure
  - [x] Variable substitution method
  - [x] Field extraction method (JSONPath)
  - [x] Condition evaluation method
  - [x] HTTP request execution method
  - [x] Validation method
- [x] Create Jinja2 templates for code generation
- [x] Add template helpers for:
  - [x] Header generation
  - [x] Body generation
  - [x] Validation code generation

#### 2.2 Build Python Code Generator
- [x] Create `generators/base_generator.py` base class
- [x] Create `generators/python_generator.py` with:
  - [x] Config parser (read and validate FlowSphere config)
  - [x] Code builder (combine templates with config data)
  - [x] Import statement generator
  - [x] Class method generator for each node
  - [x] Test function generator
  - [x] Defaults merging logic
- [x] Add support for all FlowSphere features:
  - [x] HTTP execution (all methods)
  - [x] Variable substitution (all 4 types)
  - [x] Condition evaluation (all operators)
  - [x] Validation (status + JSONPath)
  - [x] User prompts
  - [x] Browser launch
  - [x] Skip default headers/validations flags

#### 2.3 Implement MCP Tool
- [x] Add `generate_python_pytest` tool implementation to server.py
- [x] Tool accepts FlowSphere config as input
- [x] Tool returns complete Python code as output
- [x] Add error handling and validation

#### 2.4 Testing
- [x] Create test configs in `tests/fixtures/`:
  - [x] `simple_config.json` - Basic GET/POST flow
  - [x] `auth_flow_config.json` - Login + authenticated requests
  - [x] `conditional_config.json` - Nodes with conditions
  - [x] `validation_config.json` - Multiple validations
  - [x] `full_features_config.json` - All features combined
- [x] Generate Python code for each test config
- [x] Verify generated code runs successfully
- [x] Create `tests/test_python_generator.py`
- [x] All tests must pass (31/31 passing)

#### 2.5 Documentation
- [x] Update README.md with Phase 2 completion
- [x] Add usage examples to README
- [x] Document generated code structure
- [x] Add troubleshooting guide

### Success Criteria
- ✅ All 18 features from checklist supported
- ✅ Generated code runs without modification
- ✅ Generated code passes all validations
- ✅ All test configs generate valid Python code
- ✅ Tests passing

### Estimated Files
- `src/flowsphere_mcp/templates/python/base_template.py`
- `src/flowsphere_mcp/templates/python/pytest_template.jinja2`
- `src/flowsphere_mcp/generators/base_generator.py`
- `src/flowsphere_mcp/generators/python_generator.py`
- `tests/fixtures/*.json` (5+ config files)
- `tests/test_python_generator.py`
- `tests/generated_code/*.py` (generated examples)

---

## ✅ Phase 3: Python Behave/Cucumber Code Generation

**Status:** Complete
**Completion Date:** 2025-10-27
**Goal:** Generate BDD/Cucumber tests with Gherkin features + behave step definitions

### Tasks

#### 3.1 Create Behave Templates
- [x] Create Gherkin feature file template
- [x] Create behave step definitions template
- [x] Create `APIContext` class for state management
- [x] Add step definition decorators (@given, @when, @then)

#### 3.2 Build Behave Code Generator
- [x] Create `generators/behave_generator.py`
- [x] Convert FlowSphere nodes to Gherkin scenarios
- [x] Generate step definitions from nodes
- [x] Map FlowSphere validations to BDD assertions
- [x] Support all FlowSphere features in step definitions

#### 3.3 Implement MCP Tool
- [x] Add `generate_python_behave` tool to server.py
- [x] Tool returns both feature file and step definitions
- [x] Multi-file output support

#### 3.4 Testing
- [x] Create behave test fixtures (reused from Phase 2)
- [x] Generate feature files and step definitions
- [x] Run generated behave tests
- [x] Verify all features work in BDD context
- [x] Create `tests/test_behave_generator.py` (34 tests, all passing)

#### 3.5 Documentation
- [x] Update README with behave examples
- [x] Document Gherkin feature structure
- [x] Add step definition usage guide

### Success Criteria
- ✅ Valid Gherkin syntax generated
- ✅ Step definitions implement all FlowSphere features
- ✅ Generated tests run with `behave` command
- ✅ All validations translated to BDD assertions
- ✅ 34/34 tests passing (100%)

### Estimated Files
- `src/flowsphere_mcp/templates/python/gherkin_template.jinja2`
- `src/flowsphere_mcp/templates/python/step_definitions_template.jinja2`
- `src/flowsphere_mcp/generators/behave_generator.py`
- `tests/test_behave_generator.py`

---

## 📋 Phase 4: JavaScript/TypeScript Code Generation

**Status:** Planned
**Goal:** Generate Jest/Mocha tests and cucumber-js BDD tests

### Tasks

#### 4.1 JavaScript/TypeScript Templates
- [ ] Create Jest test template
- [ ] Create Mocha test template
- [ ] Create cucumber-js feature + step definition templates
- [ ] TypeScript type definitions

#### 4.2 JS/TS Code Generator
- [ ] Create `generators/javascript_generator.py`
- [ ] Create `generators/typescript_generator.py`
- [ ] Support axios for HTTP requests
- [ ] Generate async/await code
- [ ] Handle ES6 modules vs CommonJS

#### 4.3 Implement MCP Tools
- [ ] Add `generate_javascript_jest` tool
- [ ] Add `generate_javascript_mocha` tool
- [ ] Add `generate_javascript_cucumber` tool
- [ ] Add `generate_typescript_jest` tool

#### 4.4 Testing
- [ ] Generate JavaScript code for test configs
- [ ] Verify generated code runs with Node.js
- [ ] Test with both Jest and Mocha
- [ ] Test cucumber-js generation
- [ ] Create `tests/test_javascript_generator.py`

#### 4.5 Documentation
- [ ] Add JavaScript examples to README
- [ ] Document package.json requirements
- [ ] Add TypeScript setup guide

### Success Criteria
- ✅ Valid JavaScript/TypeScript generated
- ✅ Code runs with Jest/Mocha
- ✅ Cucumber-js tests work
- ✅ All FlowSphere features supported

### Estimated Files
- `src/flowsphere_mcp/templates/javascript/jest_template.jinja2`
- `src/flowsphere_mcp/templates/javascript/mocha_template.jinja2`
- `src/flowsphere_mcp/templates/javascript/cucumber_template.jinja2`
- `src/flowsphere_mcp/generators/javascript_generator.py`
- `src/flowsphere_mcp/generators/typescript_generator.py`

---

## 📋 Phase 5: C# Code Generation

**Status:** Planned
**Goal:** Generate xUnit/NUnit tests and SpecFlow BDD tests

### Tasks

#### 5.1 C# Templates
- [ ] Create xUnit test template
- [ ] Create NUnit test template
- [ ] Create SpecFlow feature + step definition templates
- [ ] Add proper namespaces and using statements

#### 5.2 C# Code Generator
- [ ] Create `generators/csharp_generator.py`
- [ ] Support HttpClient for requests
- [ ] Generate async/await Task-based code
- [ ] Handle Newtonsoft.Json for JSON parsing
- [ ] .NET 6+ compatibility

#### 5.3 Implement MCP Tools
- [ ] Add `generate_csharp_xunit` tool
- [ ] Add `generate_csharp_nunit` tool
- [ ] Add `generate_csharp_specflow` tool

#### 5.4 Testing
- [ ] Generate C# code for test configs
- [ ] Verify compilation with dotnet CLI
- [ ] Test with xUnit and NUnit
- [ ] Test SpecFlow generation
- [ ] Create `tests/test_csharp_generator.py`

#### 5.5 Documentation
- [ ] Add C# examples to README
- [ ] Document NuGet package requirements
- [ ] Add .csproj setup guide

### Success Criteria
- ✅ Valid C# code generated
- ✅ Code compiles with dotnet CLI
- ✅ Tests run with xUnit/NUnit
- ✅ SpecFlow tests work
- ✅ All FlowSphere features supported

### Estimated Files
- `src/flowsphere_mcp/templates/csharp/xunit_template.jinja2`
- `src/flowsphere_mcp/templates/csharp/nunit_template.jinja2`
- `src/flowsphere_mcp/templates/csharp/specflow_template.jinja2`
- `src/flowsphere_mcp/generators/csharp_generator.py`

---

## 📦 Phase 6: Publishing & Distribution

**Status:** Planned
**Goal:** Publish the MCP server to multiple distribution channels for easy user installation

### Tasks

#### 6.1 Prepare for Publishing
- [ ] Update all author information in project files
- [ ] Verify all documentation is complete and accurate
- [ ] Add comprehensive examples and usage guides
- [ ] Create demo video or GIF showing code generation
- [ ] Ensure all dependencies are properly specified
- [ ] Run final security audit on code
- [ ] Create CHANGELOG.md documenting all versions

#### 6.2 GitHub Release
- [ ] Create comprehensive release notes
- [ ] Tag version 1.0.0
- [ ] Create GitHub release with binaries/artifacts
- [ ] Add installation instructions to README
- [ ] Create GitHub topics for discoverability
- [ ] Enable GitHub Discussions for community support

#### 6.3 PyPI Publication
- [ ] Update `setup.py` with correct metadata
- [ ] Test package build locally
- [ ] Upload to TestPyPI for validation
- [ ] Test installation from TestPyPI
- [ ] Upload to production PyPI
- [ ] Verify `pip install flowsphere-mcp-server` works
- [ ] Add PyPI badge to README

#### 6.4 Smithery Submission
- [ ] Update `smithery.json` with correct information
- [ ] Create compelling description and examples
- [ ] Submit to Smithery registry (https://smithery.ai)
- [ ] Respond to any feedback from Smithery team
- [ ] Verify installation via Smithery CLI works
- [ ] Add Smithery badge to README

#### 6.5 Docker Image (Optional)
- [ ] Create optimized Dockerfile
- [ ] Build and test Docker image locally
- [ ] Push to Docker Hub
- [ ] Create docker-compose.yml for easy setup
- [ ] Document Docker usage in README

#### 6.6 Marketing & Outreach
- [ ] Write announcement blog post
- [ ] Share on social media (Twitter, LinkedIn, Reddit)
- [ ] Post to relevant communities:
  - [ ] r/Python
  - [ ] r/programming
  - [ ] r/Claude
  - [ ] Dev.to
  - [ ] Hacker News
- [ ] Create demo repository with examples
- [ ] Record demo video for YouTube

#### 6.7 Documentation Site (Optional)
- [ ] Set up GitHub Pages or Read the Docs
- [ ] Create comprehensive API documentation
- [ ] Add tutorials and guides
- [ ] Include interactive examples
- [ ] Set up documentation versioning

### Success Criteria
- ✅ Available on at least 2 distribution channels (GitHub + PyPI or Smithery)
- ✅ Installation works with single command
- ✅ All documentation links work
- ✅ At least 10 GitHub stars in first week
- ✅ Zero critical bugs reported in first release
- ✅ Clear update/maintenance process established

### Estimated Files
- `setup.py` (created ✅)
- `MANIFEST.in` (created ✅)
- `smithery.json` (created ✅)
- `PUBLISHING_GUIDE.md` (created ✅)
- `CHANGELOG.md`
- `Dockerfile` (optional)
- `docker-compose.yml` (optional)

### Timeline
- Week 1: GitHub release and PyPI
- Week 2: Smithery submission
- Week 3: Marketing and outreach
- Ongoing: Maintenance and updates

---

## 🔮 Future Enhancements (Phase 7+)

### Advanced Features
- [ ] **Custom Template Overrides** - Allow users to provide custom Jinja2 templates
- [ ] **Code Style Options** - Support different formatting styles (black, prettier, etc.)
- [ ] **Plugin System** - Enable community-contributed language support
- [ ] **Config Validation** - Validate FlowSphere configs before generation
- [ ] **Incremental Generation** - Only regenerate changed nodes
- [ ] **Multi-file Output** - Split large configs into multiple test files

### Additional Languages
- [ ] **Go** - Generate Go test code
- [ ] **Java** - Generate JUnit/RestAssured tests
- [ ] **Ruby** - Generate RSpec tests
- [ ] **PHP** - Generate PHPUnit tests

### Developer Experience
- [ ] **CLI Tool** - Standalone CLI for code generation without MCP
- [ ] **VS Code Extension** - Generate code directly in editor
- [ ] **Web UI** - Browser-based code generator
- [ ] **GitHub Action** - Auto-generate tests in CI/CD
- [ ] **Live Preview** - Show generated code as you edit config

### Quality & Testing
- [ ] **Code Coverage Analysis** - Ensure all FlowSphere features are tested
- [ ] **Performance Benchmarks** - Measure generation speed
- [ ] **Integration Tests** - Test with real APIs
- [ ] **Fuzz Testing** - Generate code from malformed configs

---

## Development Guidelines

### Before Starting Each Phase
1. Create a new branch: `git checkout -b phase-N-description`
2. Review previous phase implementation
3. Update this roadmap with any learnings
4. Create test fixtures first (TDD approach)

### During Phase Development
1. Write tests before implementation
2. Commit frequently with clear messages
3. Update README as features are completed
4. Run all tests before moving to next task

### Completing Each Phase
1. All tests must pass
2. Update README.md with completion status
3. Create detailed commit message
4. Tag release: `git tag v0.N.0`
5. Update this roadmap to mark phase complete
6. Review and plan next phase

### Code Quality Standards
- All Python code must be formatted with `black`
- All generated code must be syntactically valid
- All generated code must run without modification
- 100% feature coverage (all 18 checklist items)
- Clear error messages for validation failures

---

## Current Status

**Completed Phases:** 4 / 6 (67%)
**Current Phase:** Phase 5 (C# Code Generation) or Phase 6 (Publishing & Distribution)
**Progress:** Phase 4 completed with JavaScript Jest support. Ready for Phase 5 (C#) or Phase 6 (Publishing).

**Project Metrics:**
- Total Files: 35+
- Total Lines: 6,700+
- Tests Passing: 98/98 (100%) - 30 JavaScript + 34 behave + 31 pytest + 3 schema tests
- MCP Tools: 6 (3 schema + 3 code generators)
- Supported Languages: 2 (Python with 2 frameworks + JavaScript with Jest)
- Code Generators: 3 (Python pytest, Python behave, JavaScript Jest)

**Phase 4 Deliverables (JavaScript Jest):**
- ✅ `src/flowsphere_mcp/templates/javascript/jest_template.jinja2` (408+ lines)
- ✅ `src/flowsphere_mcp/generators/javascript_generator.py` (280+ lines)
- ✅ `tests/test_javascript_generator.py` (435 lines, 30 passing tests)
- ✅ `tests/generated_code/simple_api_test.test.js` (example output)
- ✅ `setup.py` - PyPI package configuration
- ✅ `smithery.json` - Smithery registry configuration
- ✅ `PUBLISHING_GUIDE.md` - Distribution documentation
- ✅ `USER_TESTING_GUIDE.md` - User testing instructions
- ✅ `test_user_experience.py` - Demo script for users

**Phase 3 Deliverables (Python Behave):**
- ✅ `src/flowsphere_mcp/templates/python/gherkin_template.jinja2` (60+ lines)
- ✅ `src/flowsphere_mcp/templates/python/step_definitions_template.jinja2` (350+ lines)
- ✅ `src/flowsphere_mcp/generators/behave_generator.py` (380+ lines)
- ✅ `tests/test_behave_generator.py` (34 passing tests)

**Phase 2 Deliverables (Python pytest):**
- ✅ `src/flowsphere_mcp/templates/python/base_template.py` (400+ lines)
- ✅ `src/flowsphere_mcp/templates/python/pytest_template.jinja2` (350+ lines)
- ✅ `src/flowsphere_mcp/generators/base_generator.py` (180+ lines)
- ✅ `src/flowsphere_mcp/generators/python_generator.py` (220+ lines)
- ✅ `tests/test_python_generator.py` (31 passing tests)

**Available for Users NOW:**
- ✅ Python pytest code generation (production-ready)
- ✅ Python behave/BDD code generation (production-ready)
- ✅ JavaScript Jest code generation (production-ready)
- ✅ All 18 FlowSphere features fully supported
- ✅ Comprehensive testing suite (98 tests)
- ✅ User testing guide and demo script
- ✅ Publishing configuration for PyPI and Smithery

**Next Milestone Options:**
1. **Phase 5:** C# code generation (xUnit, NUnit, SpecFlow)
2. **Phase 6:** Publishing & Distribution (PyPI, Smithery, GitHub releases)
3. **Both:** Publish current version while developing Phase 5

**Recommended:** Start Phase 6 (Publishing) to make current features available to users, then continue with Phase 5 (C#) for additional language support.

---

Last Updated: 2025-10-28
