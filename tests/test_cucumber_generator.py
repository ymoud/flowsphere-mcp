"""
Tests for JavaScript Cucumber/BDD code generator.

Tests Cucumber code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.javascript_generator import JavaScriptCucumberGenerator


class TestJavaScriptCucumberGenerator:
    """Test suite for JavaScript Cucumber generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return JavaScriptCucumberGenerator()

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
        assert generator.get_framework_name() == "Cucumber"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('cucumber' in dep.lower() for dep in deps)
        assert any('chai' in dep.lower() for dep in deps)
        assert any('axios' in dep.lower() for dep in deps)

    # ===== Code Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        assert 'feature' in result
        assert 'steps' in result
        assert 'Feature:' in result['feature']
        assert 'Scenario:' in result['feature']
        assert 'class APIWorld' in result['steps']

    def test_feature_has_gherkin_syntax(self, generator, fixtures_dir):
        """Test that feature file has proper Gherkin syntax."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        result = generator.generate(config)

        feature = result['feature']
        assert 'Feature:' in feature
        assert 'Scenario:' in feature
        assert 'When' in feature or 'Given' in feature or 'Then' in feature

    def test_steps_have_cucumber_imports(self, generator, fixtures_dir):
        """Test that steps file has cucumber imports."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        steps = result['steps']
        assert '@cucumber/cucumber' in steps
        assert 'Given' in steps or 'When' in steps or 'Then' in steps
        assert 'setWorldConstructor' in steps

    # ===== Validation Tests =====

    def test_validate_generated_code(self, generator, fixtures_dir):
        """Test validation of generated code."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        is_valid, error = generator.validate_generated_code(result['feature'], result['steps'])
        assert is_valid is True
        assert error is None

    # ===== Package.json Tests =====

    def test_generate_package_json(self, generator):
        """Test package.json generation."""
        package_json = generator.get_package_json_template()
        data = json.loads(package_json)

        assert '@cucumber/cucumber' in data['devDependencies']
        assert 'chai' in data['devDependencies']
        assert 'cucumber-js' in data['scripts']['test']

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
            result = generator.generate(config)

            assert 'feature' in result
            assert 'steps' in result
            assert 'Feature:' in result['feature']
            assert 'Scenario:' in result['feature']
            assert 'class APIWorld' in result['steps']

            is_valid, error = generator.validate_generated_code(result['feature'], result['steps'])
            assert is_valid is True, f"{fname} generated invalid code: {error}"
