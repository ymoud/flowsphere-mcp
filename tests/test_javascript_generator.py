"""
Tests for JavaScript Jest code generator.

Tests code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.javascript_generator import JavaScriptJestGenerator
from generators.base_generator import BaseGenerator


class TestJavaScriptJestGenerator:
    """Test suite for JavaScript Jest generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return JavaScriptJestGenerator()

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
        assert generator.get_language_name() == "JavaScript"
        assert generator.get_framework_name() == "Jest"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('jest' in dep.lower() for dep in deps)
        assert any('axios' in dep.lower() for dep in deps)
        assert any('jsonpath' in dep.lower() for dep in deps)
        assert any('uuid' in dep.lower() for dep in deps)

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

    # ===== Code Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert code is not None
        assert len(code) > 0
        assert "const axios = require('axios')" in code
        assert "const { JSONPath } = require('jsonpath-plus')" in code
        assert "class APISequence" in code
        assert "describe(" in code
        assert "test(" in code or "it(" in code
        assert "Simple API Test" in code or "SimpleApiTest" in code

    def test_generate_auth_flow_config(self, generator, fixtures_dir):
        """Test code generation for authentication flow."""
        config = self.load_fixture(fixtures_dir, 'auth_flow_config.json')
        code = generator.generate(config)

        # Verify variable substitution logic exists in generated code
        assert "substituteVariables" in code
        assert "responses" in code.lower()
        assert "login" in code.lower()

    def test_generate_conditional_config(self, generator, fixtures_dir):
        """Test code generation for conditional execution."""
        config = self.load_fixture(fixtures_dir, 'conditional_config.json')
        code = generator.generate(config)

        assert "evaluateCondition" in code
        assert "condition" in code.lower()

    def test_generate_validation_config(self, generator, fixtures_dir):
        """Test code generation for multiple validations."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        code = generator.generate(config)

        assert "validateResponse" in code
        assert "validations" in code.lower()

    def test_generate_full_features_config(self, generator, fixtures_dir):
        """Test code generation with all features enabled."""
        config = self.load_fixture(fixtures_dir, 'full_features_config.json')
        code = generator.generate(config)

        # Check that all major features are present
        assert "class APISequence" in code
        assert "substituteVariables" in code
        assert "extractField" in code
        assert "evaluateCondition" in code
        assert "validateResponse" in code
        assert "executeHttpRequest" in code

    # ===== Code Syntax Validation Tests =====

    def test_generated_code_is_valid_javascript(self, generator, fixtures_dir):
        """Test generated code has basic JavaScript syntax validity."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        # Should pass basic syntax checks
        is_valid, error = generator.validate_generated_code(code)
        assert is_valid is True, f"Generated code has syntax error: {error}"

    def test_all_fixtures_generate_valid_javascript(self, generator, fixtures_dir):
        """Test all fixture configs generate valid JavaScript."""
        fixtures = [
            'simple_config.json',
            'auth_flow_config.json',
            'conditional_config.json',
            'validation_config.json',
            'full_features_config.json'
        ]

        for fixture_name in fixtures:
            config = self.load_fixture(fixtures_dir, fixture_name)
            code = generator.generate(config)

            is_valid, error = generator.validate_generated_code(code)
            assert is_valid is True, f"{fixture_name} generated invalid code: {error}"

    # ===== Class Name Sanitization Tests =====

    def test_sanitize_class_name_simple(self, generator):
        """Test class name sanitization for simple names."""
        result = generator._sanitize_class_name("Simple API Test")
        assert result == "SimpleApiTest"

    def test_sanitize_class_name_special_chars(self, generator):
        """Test class name sanitization handles special characters."""
        result = generator._sanitize_class_name("Test-API@2024!")
        assert result == "TestApi2024"

    def test_sanitize_class_name_empty(self, generator):
        """Test class name sanitization handles empty string."""
        result = generator._sanitize_class_name("")
        assert len(result) > 0
        assert result == "APISequenceTest"

    # ===== Custom Options Tests =====

    def test_custom_test_class_name(self, generator, fixtures_dir):
        """Test custom test class name option."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config, test_class_name="MyCustomTest")

        assert "MyCustomTest" in code

    # ===== Dependencies Tests =====

    def test_generate_dependencies_file(self, generator):
        """Test package.json dependencies generation."""
        deps_content = generator.generate_dependencies_file()

        assert "devDependencies" in deps_content
        assert "jest" in deps_content
        assert "axios" in deps_content
        assert "jsonpath" in deps_content
        assert "uuid" in deps_content

    def test_generate_package_json(self, generator):
        """Test complete package.json generation."""
        package_json = generator.get_package_json_template()

        assert "name" in package_json
        assert "scripts" in package_json
        assert "devDependencies" in package_json
        assert "test" in package_json  # test script

    # ===== Usage Instructions Tests =====

    def test_usage_instructions(self, generator):
        """Test usage instructions are generated."""
        instructions = generator.get_usage_instructions()

        assert instructions is not None
        assert len(instructions) > 0
        assert "jest" in instructions.lower()
        assert "npm" in instructions.lower()

    # ===== Code Format Tests =====

    def test_format_code(self, generator):
        """Test code formatting."""
        code = "function test() {\n\n\n\n\nreturn true;\n}\n\n\n\n"
        formatted = generator.format_code(code)

        # Should not have more than 3 consecutive newlines
        assert "\n\n\n\n" not in formatted

        # Should end with single newline
        assert formatted.endswith("\n")
        assert not formatted.endswith("\n\n")

    # ===== HTTP Methods Tests =====

    def test_all_http_methods_supported(self, generator):
        """Test all HTTP methods are supported in generated code."""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

        for method in methods:
            config = {
                "nodes": [
                    {
                        "id": f"test_{method.lower()}",
                        "name": f"Test {method}",
                        "method": method,
                        "url": "/test"
                    }
                ]
            }

            code = generator.generate(config)
            assert "executeHttpRequest" in code
            # Method should appear in config JSON
            assert method in code

    # ===== Defaults Handling Tests =====

    def test_defaults_handling(self, generator):
        """Test default values are properly handled."""
        config = {
            "defaults": {
                "baseUrl": "https://api.example.com",
                "headers": {
                    "Authorization": "Bearer token"
                },
                "timeout": 5000
            },
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)

        # Defaults should be in the config JSON embedded in code
        assert "baseUrl" in code
        assert "https://api.example.com" in code

    # ===== Variables Handling Tests =====

    def test_variables_handling(self, generator):
        """Test variables are properly handled."""
        config = {
            "variables": {
                "userId": "12345",
                "apiKey": "secret"
            },
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)

        # Variables should be in the config JSON embedded in code
        assert "variables" in code
        assert "userId" in code

    # ===== User Prompts Handling Tests =====

    def test_user_prompts_handling(self, generator):
        """Test user prompts are properly handled."""
        config = {
            "nodes": [
                {
                    "id": "test",
                    "name": "Test",
                    "method": "GET",
                    "url": "/test",
                    "promptMessage": "Enter your name:",
                    "variableName": "userName"
                }
            ]
        }

        code = generator.generate(config)

        # User prompt handling should be in generated code
        assert "promptMessage" in code or "userInputs" in code

    # ===== Debug Mode Handling Tests =====

    def test_debug_mode_handling(self, generator):
        """Test debug mode is properly handled."""
        config = {
            "enableDebug": True,
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)

        # Debug logging should be in generated code
        assert "logDebug" in code
        assert "enableDebug" in code or "debug" in code


class TestGeneratorIntegration:
    """Integration tests for JavaScript Jest generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return JavaScriptJestGenerator()

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to fixtures directory."""
        return Path(__file__).parent / 'fixtures'

    def load_fixture(self, fixtures_dir: Path, filename: str) -> dict:
        """Load a test fixture config."""
        with open(fixtures_dir / filename, 'r') as f:
            return json.load(f)

    def test_end_to_end_generation(self, generator, fixtures_dir):
        """Test complete end-to-end code generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')

        # Generate code
        code = generator.generate(config)

        # Validate structure
        assert len(code) > 100  # Non-trivial content
        assert code.count("class APISequence") == 1
        assert "describe(" in code

        # Validate syntax
        is_valid, error = generator.validate_generated_code(code)
        assert is_valid is True, f"Generated code invalid: {error}"

    def test_generate_all_fixtures(self, generator, fixtures_dir):
        """Test code generation for all fixture configs."""
        fixtures = [
            'simple_config.json',
            'auth_flow_config.json',
            'conditional_config.json',
            'validation_config.json',
            'full_features_config.json'
        ]

        for fixture_name in fixtures:
            config = self.load_fixture(fixtures_dir, fixture_name)
            code = generator.generate(config)

            # Each should generate valid code
            is_valid, error = generator.validate_generated_code(code)
            assert is_valid is True, f"{fixture_name} generated invalid code: {error}"

            # Each should have core features
            assert "class APISequence" in code
            assert "describe(" in code
