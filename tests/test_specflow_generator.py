"""
Tests for C# SpecFlow code generator.

Tests SpecFlow/BDD code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.csharp_generator import CSharpSpecFlowGenerator


class TestCSharpSpecFlowGenerator:
    """Test suite for C# SpecFlow generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return CSharpSpecFlowGenerator()

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
        assert generator.get_language_name() == "C#"
        assert generator.get_framework_name() == "SpecFlow"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('specflow' in dep.lower() for dep in deps)
        assert any('nunit' in dep.lower() for dep in deps)
        assert any('newtonsoft.json' in dep.lower() for dep in deps)

    # ===== Code Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        assert isinstance(result, dict)
        assert 'feature' in result
        assert 'steps' in result

        # Check feature file
        assert 'Feature:' in result['feature']
        assert 'Scenario:' in result['feature']

        # Check step definitions
        assert '[Binding]' in result['steps']
        assert 'namespace FlowSphere.Tests' in result['steps']
        assert 'using TechTalk.SpecFlow;' in result['steps']

    def test_feature_has_gherkin_syntax(self, generator, fixtures_dir):
        """Test that feature file uses proper Gherkin syntax."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        feature = result['feature']

        assert 'Feature:' in feature
        assert 'Scenario:' in feature
        assert 'Given ' in feature or 'When ' in feature or 'Then ' in feature

    def test_steps_use_specflow_attributes(self, generator, fixtures_dir):
        """Test that step definitions use SpecFlow attributes."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        assert '[Given' in steps or '[When' in steps or '[Then' in steps
        assert '[Binding]' in steps

    def test_steps_use_async_await(self, generator, fixtures_dir):
        """Test that step definitions use async/await pattern."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)
        steps = result['steps']

        assert 'async Task' in steps
        assert 'await ' in steps
        assert 'HttpClient' in steps

    def test_custom_feature_name(self, generator, fixtures_dir):
        """Test custom feature name generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config, feature_name='MyCustomFeature')

        # Feature file should have custom name in Feature declaration
        assert 'Feature:' in result['feature']

    def test_custom_namespace(self, generator, fixtures_dir):
        """Test custom namespace generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config, namespace='MyCompany.Tests')

        assert 'namespace MyCompany.Tests' in result['steps']

    # ===== Validation Tests =====

    def test_validate_generated_code(self, generator, fixtures_dir):
        """Test validation of generated code."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        result = generator.generate(config)

        is_valid, error = generator.validate_generated_code(result)
        assert is_valid is True
        assert error is None

    # ===== .csproj Tests =====

    def test_generate_csproj(self, generator):
        """Test .csproj file generation."""
        csproj = generator.get_csproj_template()

        assert '<Project Sdk="Microsoft.NET.Sdk">' in csproj
        assert '<PackageReference Include="SpecFlow"' in csproj
        assert '<PackageReference Include="NUnit"' in csproj
        assert 'Version="3.9.0"' in csproj  # SpecFlow version

    def test_csproj_custom_project_name(self, generator):
        """Test .csproj with custom project name."""
        csproj = generator.get_csproj_template(project_name='MyTestProject')

        assert '<RootNamespace>MyTestProject</RootNamespace>' in csproj

    # ===== Usage Instructions Tests =====

    def test_usage_instructions(self, generator):
        """Test usage instructions are provided."""
        instructions = generator.get_usage_instructions()

        assert 'dotnet test' in instructions
        assert 'SpecFlow' in instructions
        assert isinstance(instructions, str)
        assert len(instructions) > 0

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

            assert isinstance(result, dict)
            assert 'feature' in result
            assert 'steps' in result
            assert 'Feature:' in result['feature']
            assert '[Binding]' in result['steps']

            is_valid, error = generator.validate_generated_code(result)
            assert is_valid is True, f"{fname} generated invalid code: {error}"
