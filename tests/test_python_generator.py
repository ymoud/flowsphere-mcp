"""
Tests for Python pytest code generator.

Tests code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.python_generator import PythonPytestGenerator
from generators.base_generator import BaseGenerator


class TestPythonPytestGenerator:
    """Test suite for Python pytest generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return PythonPytestGenerator()

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to fixtures directory."""
        return Path(__file__).parent / 'fixtures'

    def load_fixture(self, fixtures_dir: Path, filename: str) -> dict:
        """Load a test fixture config."""
        with open(fixtures_dir / filename, 'r') as f:
            return json.load(f)

    def test_generator_initialization(self, generator):
        """Test generator initializes correctly."""
        assert generator is not None
        assert generator.get_language_name() == "Python"
        assert generator.get_framework_name() == "pytest"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('pytest' in dep for dep in deps)
        assert any('requests' in dep for dep in deps)
        assert any('jsonpath-ng' in dep for dep in deps)

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

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert code is not None
        assert len(code) > 0
        assert "import pytest" in code
        assert "import requests" in code
        assert "class APISequence" in code
        assert "def test_execute_sequence" in code
        assert "Simple API Test" in code or "TestSimpleApiTest" in code

    def test_generate_auth_flow_config(self, generator, fixtures_dir):
        """Test code generation for authentication flow."""
        config = self.load_fixture(fixtures_dir, 'auth_flow_config.json')
        code = generator.generate(config)

        assert "Authentication Flow Test" in code or "TestAuthenticationFlowTest" in code
        # Verify variable substitution logic exists in generated code
        assert "substitute_variables" in code
        assert "responses" in code.lower()
        assert "login" in code.lower()

    def test_generate_conditional_config(self, generator, fixtures_dir):
        """Test code generation for conditional execution."""
        config = self.load_fixture(fixtures_dir, 'conditional_config.json')
        code = generator.generate(config)

        assert "evaluate_conditions" in code
        assert "conditions" in code.lower()

    def test_generate_validation_config(self, generator, fixtures_dir):
        """Test code generation for multiple validations."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        code = generator.generate(config)

        assert "validate_response" in code
        assert "validations" in code.lower()
        assert "skipDefaultValidations" in code

    def test_generate_full_features_config(self, generator, fixtures_dir):
        """Test code generation for all features."""
        config = self.load_fixture(fixtures_dir, 'full_features_config.json')
        code = generator.generate(config)

        # Check for all major features
        assert "substitute_variables" in code
        assert "evaluate_conditions" in code
        assert "validate_response" in code
        assert "extract_field" in code
        assert "execute_http_request" in code

        # Check for variable types
        assert "generate_guid" in code
        assert "generate_timestamp" in code

    def test_generated_code_is_valid_python(self, generator, fixtures_dir):
        """Test that all generated code is syntactically valid Python."""
        fixture_files = [
            'simple_config.json',
            'auth_flow_config.json',
            'conditional_config.json',
            'validation_config.json',
            'full_features_config.json'
        ]

        for fixture_file in fixture_files:
            config = self.load_fixture(fixtures_dir, fixture_file)
            code = generator.generate(config)

            # Try to compile the code
            try:
                compile(code, f'<{fixture_file}>', 'exec')
            except SyntaxError as e:
                pytest.fail(f"Generated code for {fixture_file} has syntax error: {e}")

    def test_custom_test_class_name(self, generator, fixtures_dir):
        """Test custom test class name option."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config, test_class_name="CustomTestName")

        assert "TestCustomTestName" in code

    def test_sanitize_class_name(self, generator):
        """Test class name sanitization."""
        test_cases = [
            ("My Test", "MyTest"),
            ("test-with-dashes", "TestWithDashes"),
            ("test_with_underscores", "TestWithUnderscores"),
            ("123 starts with number", "_123StartsWithNumber"),
            ("special!@#chars", "SpecialChars"),
        ]

        for input_name, expected_pattern in test_cases:
            result = generator._sanitize_class_name(input_name)
            assert result is not None
            assert len(result) > 0
            # Should be valid Python identifier
            assert result.isidentifier()

    def test_format_code(self, generator):
        """Test code formatting."""
        code_with_excess_lines = "line1\n\n\n\n\nline2"
        formatted = generator.format_code(code_with_excess_lines)

        # Should reduce excessive blank lines
        assert "\n\n\n\n\n" not in formatted
        # Should end with newline
        assert formatted.endswith('\n')

    def test_generate_dependencies_file(self, generator):
        """Test requirements.txt generation."""
        requirements = generator.generate_dependencies_file()

        assert "pytest" in requirements
        assert "requests" in requirements
        assert "jsonpath-ng" in requirements
        assert requirements.endswith('\n')

    def test_usage_instructions(self, generator):
        """Test usage instructions are provided."""
        instructions = generator.get_usage_instructions()

        assert instructions is not None
        assert len(instructions) > 0
        assert "pytest" in instructions.lower()
        assert "install" in instructions.lower()

    def test_load_config_from_json_string(self, generator, fixtures_dir):
        """Test loading config from JSON string."""
        config_path = fixtures_dir / 'simple_config.json'
        with open(config_path, 'r') as f:
            config_str = f.read()

        config = generator.load_config(config_str)
        assert isinstance(config, dict)
        assert 'nodes' in config

    def test_load_config_invalid_json(self, generator):
        """Test error handling for invalid JSON."""
        with pytest.raises(ValueError) as exc_info:
            generator.load_config("not valid json {")

        assert "JSON" in str(exc_info.value)

    def test_load_config_invalid_structure(self, generator):
        """Test error handling for invalid config structure."""
        with pytest.raises(ValueError) as exc_info:
            generator.load_config('{"invalid": "config"}')

        assert "nodes" in str(exc_info.value).lower()

    def test_validate_generated_code(self, generator, fixtures_dir):
        """Test generated code validation method."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        is_valid, error = generator.validate_generated_code(code)
        assert is_valid is True
        assert error is None

    def test_validate_invalid_python_code(self, generator):
        """Test validation catches invalid Python code."""
        invalid_code = "def test(:\n    pass"

        is_valid, error = generator.validate_generated_code(invalid_code)
        assert is_valid is False
        assert error is not None

    def test_all_http_methods_supported(self, generator):
        """Test that all HTTP methods are supported in generated code."""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

        for method in methods:
            config = {
                "nodes": [
                    {
                        "id": "test",
                        "name": f"Test {method}",
                        "method": method,
                        "url": "/test"
                    }
                ]
            }

            code = generator.generate(config)
            assert f"method == '{method}'" in code or f'method == "{method}"' in code

    def test_defaults_handling(self, generator):
        """Test that defaults are properly handled in generated code."""
        config = {
            "defaults": {
                "baseUrl": "https://api.example.com",
                "timeout": 60,
                "headers": {"Authorization": "Bearer token"},
                "validations": [{"httpStatusCode": 200}]
            },
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)
        assert "'baseUrl'" in code
        assert "'timeout'" in code
        assert "'headers'" in code
        assert "'validations'" in code

    def test_variables_handling(self, generator):
        """Test that variables are properly handled."""
        config = {
            "variables": {
                "apiKey": "test-key",
                "environment": "test"
            },
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)
        assert "'variables'" in code
        assert "apiKey" in code

    def test_user_prompts_handling(self, generator):
        """Test that user prompts are handled in generated code."""
        config = {
            "userPrompts": [
                {
                    "variableName": "username",
                    "message": "Enter username",
                    "defaultValue": "test_user"
                }
            ],
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)
        assert "user_inputs" in code
        assert "username" in code

    def test_debug_mode_handling(self, generator):
        """Test that debug mode is handled."""
        config = {
            "enableDebug": True,
            "nodes": [
                {"id": "test", "name": "Test", "method": "GET", "url": "/test"}
            ]
        }

        code = generator.generate(config)
        assert "log_debug" in code or "enableDebug" in code


class TestGeneratorIntegration:
    """Integration tests for the complete generation flow."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return PythonPytestGenerator()

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to fixtures directory."""
        return Path(__file__).parent / 'fixtures'

    def test_end_to_end_generation(self, generator, fixtures_dir):
        """Test complete end-to-end code generation."""
        # Load config
        config_path = fixtures_dir / 'simple_config.json'
        with open(config_path, 'r') as f:
            config_str = f.read()

        # Parse config
        config = generator.load_config(config_str)

        # Generate code
        code = generator.generate(config)

        # Validate generated code
        is_valid, error = generator.validate_generated_code(code)
        assert is_valid, f"Generated code is invalid: {error}"

        # Verify code structure
        assert "import pytest" in code
        assert "import requests" in code
        assert "def test_execute_sequence" in code

    def test_generate_all_fixtures(self, generator, fixtures_dir):
        """Test generation for all fixture files."""
        fixture_files = list(fixtures_dir.glob('*.json'))
        assert len(fixture_files) >= 5, "Should have at least 5 fixture files"

        for fixture_file in fixture_files:
            with open(fixture_file, 'r') as f:
                config = json.load(f)

            # Generate code
            code = generator.generate(config)

            # Validate
            is_valid, error = generator.validate_generated_code(code)
            assert is_valid, f"Generated code for {fixture_file.name} is invalid: {error}"

            # Basic structure checks
            assert len(code) > 100, f"Generated code for {fixture_file.name} seems too short"
            assert "import pytest" in code
            assert "def test_execute_sequence" in code


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
