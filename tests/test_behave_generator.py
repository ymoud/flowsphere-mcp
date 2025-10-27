"""
Tests for Python behave/BDD code generator.

Tests code generation from FlowSphere configurations for behave tests.
"""

import json
import pytest
from pathlib import Path
import sys
import re

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.behave_generator import PythonBehaveGenerator
from generators.base_generator import BaseGenerator


class TestPythonBehaveGenerator:
    """Test suite for Python behave generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return PythonBehaveGenerator()

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to fixtures directory."""
        return Path(__file__).parent / 'fixtures'

    def load_fixture(self, fixtures_dir: Path, filename: str) -> dict:
        """Load a test fixture config."""
        with open(fixtures_dir / filename, 'r') as f:
            return json.load(f)

    # ===== Basic Generator Tests =====

    def test_generator_initialization(self, generator):
        """Test generator initializes correctly."""
        assert generator is not None
        assert generator.get_language_name() == "Python"
        assert generator.get_framework_name() == "behave"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('behave' in dep for dep in deps)
        assert any('requests' in dep for dep in deps)
        assert any('jsonpath-ng' in dep for dep in deps)

    # ===== Validation Tests =====

    def test_validate_valid_config(self, generator, fixtures_dir):
        """Test validation passes for valid configs."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        is_valid, error = generator.validate_config(config)
        assert is_valid is True
        assert error is None

    def test_validate_missing_nodes(self, generator):
        """Test validation fails when nodes are missing."""
        config = {"name": "Test", "defaults": {}}
        is_valid, error = generator.validate_config(config)
        assert is_valid is False
        assert "nodes" in error.lower()

    def test_validate_empty_nodes(self, generator):
        """Test validation fails when nodes array is empty."""
        config = {"nodes": []}
        is_valid, error = generator.validate_config(config)
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_missing_required_node_fields(self, generator):
        """Test validation fails when node missing required fields."""
        config = {
            "nodes": [
                {"id": "test", "name": "Test"}  # Missing method and url
            ]
        }
        is_valid, error = generator.validate_config(config)
        assert is_valid is False
        assert "method" in error.lower() or "url" in error.lower()

    def test_validate_invalid_http_method(self, generator):
        """Test validation fails for invalid HTTP method."""
        config = {
            "nodes": [
                {
                    "id": "test",
                    "name": "Test",
                    "method": "INVALID",
                    "url": "/test"
                }
            ]
        }
        is_valid, error = generator.validate_config(config)
        assert is_valid is False
        assert "method" in error.lower()

    def test_validate_duplicate_node_ids(self, generator):
        """Test validation fails for duplicate node IDs."""
        config = {
            "nodes": [
                {"id": "test", "name": "Test 1", "method": "GET", "url": "/test1"},
                {"id": "test", "name": "Test 2", "method": "GET", "url": "/test2"}
            ]
        }
        is_valid, error = generator.validate_config(config)
        assert is_valid is False
        assert "duplicate" in error.lower()

    # ===== Simple Config Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        assert result is not None
        assert isinstance(result, dict)
        assert 'feature' in result
        assert 'steps' in result

        feature = result['feature']
        steps = result['steps']

        # Check feature file
        assert "Feature:" in feature
        assert "Scenario:" in feature
        assert "Simple API Test" in feature or "API Test" in feature

        # Check step definitions
        assert "from behave import" in steps
        assert "@given" in steps or "@when" in steps or "@then" in steps
        assert "class APIContext" in steps
        assert "import requests" in steps

    def test_generate_single_file_output(self, generator, fixtures_dir):
        """Test single file output for MCP tool."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        output = generator.generate_single_file(config)

        assert output is not None
        assert "FEATURE FILE:" in output
        assert "STEP DEFINITIONS:" in output
        assert "USAGE INSTRUCTIONS" in output

    # ===== Feature File Tests =====

    def test_feature_file_structure(self, generator, fixtures_dir):
        """Test feature file has correct Gherkin structure."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        feature = result['feature']

        # Check for proper Gherkin keywords
        assert "Feature:" in feature
        assert "Scenario:" in feature
        assert "When" in feature or "Given" in feature or "Then" in feature

    def test_feature_file_scenarios_from_nodes(self, generator, fixtures_dir):
        """Test each node creates a scenario in feature file."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        feature = result['feature']

        # Simple config has 3 nodes, so should have 3 scenarios
        scenario_count = feature.count("Scenario:")
        assert scenario_count == 3

    def test_feature_file_includes_http_methods(self, generator, fixtures_dir):
        """Test feature file includes HTTP method information."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        feature = result['feature']

        # Should reference GET and POST from the config
        assert "GET" in feature
        assert "POST" in feature

    def test_feature_file_includes_validations(self, generator, fixtures_dir):
        """Test feature file includes validation steps."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        feature = result['feature']

        # Should have status code validations
        assert "status code should be" in feature or "response status" in feature

    # ===== Step Definitions Tests =====

    def test_step_definitions_structure(self, generator, fixtures_dir):
        """Test step definitions have correct structure."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Check for behave imports
        assert "from behave import given, when, then" in steps

        # Check for APIContext class
        assert "class APIContext:" in steps

        # Check for step decorators
        assert "@given" in steps or "@when" in steps or "@then" in steps

    def test_step_definitions_have_http_steps(self, generator, fixtures_dir):
        """Test step definitions implement HTTP request steps."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Should have when step for executing requests
        assert "@when" in steps
        assert "GET|POST|PUT|DELETE|PATCH" in steps
        assert "execute" in steps.lower() and "request" in steps.lower()

    def test_step_definitions_have_validation_steps(self, generator, fixtures_dir):
        """Test step definitions implement validation steps."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Should have then steps for validations
        assert "@then" in steps
        assert "status code" in steps.lower()
        assert "should be" in steps.lower()

    def test_step_definitions_have_api_context(self, generator, fixtures_dir):
        """Test step definitions include APIContext class."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Check APIContext methods
        assert "class APIContext:" in steps
        assert "def substitute_variables" in steps
        assert "def extract_field" in steps
        assert "def evaluate_condition" in steps

    def test_step_definitions_embed_config(self, generator, fixtures_dir):
        """Test step definitions embed the FlowSphere config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Config should be embedded in the file
        assert "config = {" in steps or "config =" in steps
        # Should contain config name
        assert config['name'] in steps

    # ===== Authentication Flow Tests =====

    def test_generate_auth_flow(self, generator, fixtures_dir):
        """Test code generation for authentication flow."""
        config = self.load_fixture(fixtures_dir, 'auth_flow_config.json')
        result = generator.generate(config)

        feature = result['feature']
        steps = result['steps']

        # Feature should mention auth scenarios
        assert "login" in feature.lower() or "auth" in feature.lower()

        # Step definitions should have variable substitution
        assert "substitute_variables" in steps
        assert "responses" in steps.lower()

    # ===== Conditional Execution Tests =====

    def test_generate_conditional_config(self, generator, fixtures_dir):
        """Test code generation for conditional execution."""
        config = self.load_fixture(fixtures_dir, 'conditional_config.json')
        result = generator.generate(config)

        feature = result['feature']
        steps = result['steps']

        # Feature may reference conditions in comments
        assert "Scenario:" in feature

        # Step definitions must have condition evaluation
        assert "evaluate_condition" in steps
        assert "condition" in steps.lower()

    # ===== Validation Tests =====

    def test_generate_validation_config(self, generator, fixtures_dir):
        """Test code generation for multiple validations."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        result = generator.generate(config)

        feature = result['feature']
        steps = result['steps']

        # Feature should have validation steps
        assert "should be" in feature.lower()

        # Step definitions should have validation logic
        assert "check_status_code" in steps or "status code" in steps.lower()

    # ===== Full Features Tests =====

    def test_generate_full_features_config(self, generator, fixtures_dir):
        """Test code generation with all features enabled."""
        config = self.load_fixture(fixtures_dir, 'full_features_config.json')
        result = generator.generate(config)

        feature = result['feature']
        steps = result['steps']

        # Check that all major features are present
        assert "Scenario:" in feature
        assert "APIContext" in steps
        assert "substitute_variables" in steps
        assert "extract_field" in steps
        assert "evaluate_condition" in steps

    # ===== Code Syntax Validation Tests =====

    def test_generated_steps_are_valid_python(self, generator, fixtures_dir):
        """Test generated step definitions are syntactically valid Python."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        # Should compile without syntax errors
        is_valid, error = generator.validate_generated_code(steps)
        assert is_valid is True, f"Generated code has syntax error: {error}"

    def test_all_fixtures_generate_valid_python(self, generator, fixtures_dir):
        """Test all fixture configs generate valid Python."""
        fixtures = [
            'simple_config.json',
            'auth_flow_config.json',
            'conditional_config.json',
            'validation_config.json',
            'full_features_config.json'
        ]

        for fixture_name in fixtures:
            config = self.load_fixture(fixtures_dir, fixture_name)
            result = generator.generate(config)
            steps = result['steps']

            is_valid, error = generator.validate_generated_code(steps)
            assert is_valid is True, f"{fixture_name} generated invalid code: {error}"

    # ===== Feature Name Sanitization Tests =====

    def test_sanitize_feature_name_simple(self, generator):
        """Test feature name sanitization for simple names."""
        result = generator._sanitize_feature_name("Simple API Test")
        assert result == "simple_api_test"

    def test_sanitize_feature_name_special_chars(self, generator):
        """Test feature name sanitization handles special characters."""
        result = generator._sanitize_feature_name("Test-API@2024!")
        assert result == "test_api_2024"
        assert re.match(r'^[a-z0-9_]+$', result)

    def test_sanitize_feature_name_empty(self, generator):
        """Test feature name sanitization handles empty string."""
        result = generator._sanitize_feature_name("")
        assert len(result) > 0
        assert result == "api_test"

    # ===== Custom Options Tests =====

    def test_custom_feature_name(self, generator, fixtures_dir):
        """Test custom feature name option."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config, feature_name="my_custom_test")

        output = generator.generate_single_file(config, feature_name="my_custom_test")
        assert "my_custom_test" in output

    # ===== Dependencies Tests =====

    def test_generate_dependencies_file(self, generator):
        """Test requirements.txt generation."""
        deps_content = generator.generate_dependencies_file()

        assert "behave" in deps_content
        assert "requests" in deps_content
        assert "jsonpath-ng" in deps_content

    # ===== Usage Instructions Tests =====

    def test_usage_instructions(self, generator):
        """Test usage instructions are generated."""
        instructions = generator.get_usage_instructions()

        assert instructions is not None
        assert len(instructions) > 0
        assert "behave" in instructions.lower()
        assert "feature" in instructions.lower()

    # ===== File Structure Tests =====

    def test_get_file_structure(self, generator):
        """Test file structure recommendations."""
        structure = generator.get_file_structure("my_test")

        assert isinstance(structure, dict)
        assert any("feature" in path for path in structure.keys())
        assert any("steps" in path for path in structure.keys())

    # ===== Integration Tests =====

    def test_end_to_end_simple_flow(self, generator, fixtures_dir):
        """Test complete end-to-end code generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')

        # Generate code
        result = generator.generate(config)

        # Validate structure
        assert 'feature' in result
        assert 'steps' in result

        # Validate feature file
        feature = result['feature']
        assert len(feature) > 100  # Non-trivial content
        assert feature.count("Scenario:") > 0

        # Validate steps file
        steps = result['steps']
        assert len(steps) > 500  # Substantial code
        is_valid, _ = generator.validate_generated_code(steps)
        assert is_valid is True

    def test_end_to_end_complex_flow(self, generator, fixtures_dir):
        """Test complex config with all features."""
        config = self.load_fixture(fixtures_dir, 'full_features_config.json')

        # Generate code
        result = generator.generate(config)

        # Validate both files are substantial
        assert len(result['feature']) > 200
        assert len(result['steps']) > 1000

        # Validate Python syntax
        is_valid, error = generator.validate_generated_code(result['steps'])
        assert is_valid is True, f"Complex flow generated invalid code: {error}"
