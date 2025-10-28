"""
Tests for JavaScript Mocha code generator.

Tests Mocha code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.javascript_generator import JavaScriptMochaGenerator


class TestJavaScriptMochaGenerator:
    """Test suite for JavaScript Mocha generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return JavaScriptMochaGenerator()

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
        assert generator.get_framework_name() == "Mocha"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('mocha' in dep.lower() for dep in deps)
        assert any('chai' in dep.lower() for dep in deps)
        assert any('axios' in dep.lower() for dep in deps)

    # ===== Code Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert 'class APISequence' in code
        assert 'describe(' in code
        assert 'it(' in code
        assert 'chai' in code

    def test_mocha_uses_chai_assertions(self, generator, fixtures_dir):
        """Test that Mocha code uses Chai expect assertions."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        code = generator.generate(config)

        assert 'chai' in code
        assert 'expect(' in code
        assert '.to.equal' in code or '.to.be' in code

    def test_mocha_timeout_configuration(self, generator, fixtures_dir):
        """Test that Mocha code includes timeout configuration."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert 'this.timeout(' in code

    # ===== Validation Tests =====

    def test_validate_generated_code(self, generator, fixtures_dir):
        """Test validation of generated code."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        is_valid, error = generator.validate_generated_code(code)
        assert is_valid is True
        assert error is None

    # ===== Package.json Tests =====

    def test_generate_package_json(self, generator):
        """Test package.json generation."""
        package_json = generator.get_package_json_template()
        data = json.loads(package_json)

        assert 'mocha' in data['devDependencies']
        assert 'chai' in data['devDependencies']
        assert 'mocha' in data['scripts']['test']

    # ===== Integration Tests =====

    def test_generate_all_fixtures(self, generator, fixtures_dir):
        """Test code generation for all fixtures."""
        fixtures = [
            'simple_config.json',
            'auth_flow_config.json',
            'conditional_config.json',
            'validation_config.json',
            'full_features_config.json'
        ]

        for fname in fixtures:
            config = self.load_fixture(fixtures_dir, fname)
            code = generator.generate(config)

            assert 'class APISequence' in code
            assert 'describe(' in code
            assert 'it(' in code

            is_valid, error = generator.validate_generated_code(code)
            assert is_valid is True, f"{fname} generated invalid code: {error}"
