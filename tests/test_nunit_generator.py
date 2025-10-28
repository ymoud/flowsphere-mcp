"""
Tests for C# NUnit code generator.

Tests NUnit code generation from FlowSphere configurations.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'flowsphere_mcp'))

from generators.csharp_generator import CSharpNUnitGenerator


class TestCSharpNUnitGenerator:
    """Test suite for C# NUnit generator."""

    @pytest.fixture
    def generator(self):
        """Create a generator instance."""
        return CSharpNUnitGenerator()

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
        assert generator.get_framework_name() == "NUnit"

    def test_required_dependencies(self, generator):
        """Test generator returns required dependencies."""
        deps = generator.get_required_dependencies()
        assert isinstance(deps, list)
        assert len(deps) > 0
        assert any('nunit' in dep.lower() for dep in deps)
        assert any('newtonsoft.json' in dep.lower() for dep in deps)
        assert any('microsoft.net.test.sdk' in dep.lower() for dep in deps)

    # ===== Code Generation Tests =====

    def test_generate_simple_config(self, generator, fixtures_dir):
        """Test code generation for simple config."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert 'class APISequence' in code
        assert 'namespace FlowSphere.Tests' in code
        assert '[Test]' in code
        assert 'using NUnit.Framework;' in code

    def test_nunit_uses_async_await(self, generator, fixtures_dir):
        """Test that NUnit code uses async/await pattern."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert 'async Task' in code
        assert 'await ' in code
        assert 'HttpClient' in code

    def test_nunit_uses_constraint_model(self, generator, fixtures_dir):
        """Test that NUnit code uses Assert.That constraint model."""
        config = self.load_fixture(fixtures_dir, 'validation_config.json')
        code = generator.generate(config)

        assert 'Assert.That' in code
        assert 'Is.EqualTo' in code or 'Is.Not.Null' in code
        assert 'using NUnit.Framework;' in code

    def test_nunit_uses_testfixture_attribute(self, generator, fixtures_dir):
        """Test that NUnit code uses [TestFixture] attribute."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert '[TestFixture]' in code

    def test_nunit_uses_setup_method(self, generator, fixtures_dir):
        """Test that NUnit code uses [SetUp] method."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        assert '[SetUp]' in code
        assert 'public void SetUp()' in code

    def test_custom_test_class_name(self, generator, fixtures_dir):
        """Test custom test class name generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config, test_class_name='MyCustomTests')

        assert 'class MyCustomTests' in code

    def test_custom_namespace(self, generator, fixtures_dir):
        """Test custom namespace generation."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config, namespace='MyCompany.Tests')

        assert 'namespace MyCompany.Tests' in code

    # ===== Validation Tests =====

    def test_validate_generated_code(self, generator, fixtures_dir):
        """Test validation of generated code."""
        config = self.load_fixture(fixtures_dir, 'simple_config.json')
        code = generator.generate(config)

        is_valid, error = generator.validate_generated_code(code)
        assert is_valid is True
        assert error is None

    # ===== .csproj Tests =====

    def test_generate_csproj(self, generator):
        """Test .csproj file generation."""
        csproj = generator.get_csproj_template()

        assert '<Project Sdk="Microsoft.NET.Sdk">' in csproj
        assert '<PackageReference Include="NUnit"' in csproj
        assert '<PackageReference Include="Newtonsoft.Json"' in csproj
        assert 'Version="3.14.0"' in csproj  # NUnit version

    def test_csproj_custom_project_name(self, generator):
        """Test .csproj with custom project name."""
        csproj = generator.get_csproj_template(project_name='MyTestProject')

        assert '<RootNamespace>MyTestProject</RootNamespace>' in csproj

    # ===== Usage Instructions Tests =====

    def test_usage_instructions(self, generator):
        """Test usage instructions are provided."""
        instructions = generator.get_usage_instructions()

        assert 'dotnet test' in instructions
        assert 'dotnet new nunit' in instructions
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
            code = generator.generate(config)

            assert 'class APISequence' in code
            assert 'namespace FlowSphere.Tests' in code
            assert '[Test]' in code
            assert '[TestFixture]' in code

            is_valid, error = generator.validate_generated_code(code)
            assert is_valid is True, f"{fname} generated invalid code: {error}"
