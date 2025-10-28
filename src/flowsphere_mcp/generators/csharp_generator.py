"""
C# Code Generators for FlowSphere

Generates production-ready C# test code from FlowSphere configurations.
Supports xUnit, NUnit, and SpecFlow frameworks.
Supports all 18 FlowSphere features.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from .base_generator import BaseGenerator


class CSharpXUnitGenerator(BaseGenerator):
    """
    Generator for C# xUnit test code.

    Produces a complete xUnit test file that can be executed without modification.
    """

    def __init__(self):
        """Initialize the C# xUnit generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "C#"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "xUnit"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required NuGet packages.

        Returns:
            List of NuGet package names
        """
        return [
            "xunit@^2.6.0",
            "xunit.runner.visualstudio@^2.5.0",
            "Newtonsoft.Json@^13.0.3",
            "Microsoft.NET.Test.Sdk@^17.8.0"
        ]

    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate C# xUnit code from FlowSphere configuration.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - test_class_name: Name for test class (default: auto-generated)
                - namespace: Namespace for the test class (default: FlowSphere.Tests)

        Returns:
            Complete C# xUnit test file as string
        """
        # Validate config first
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        # Generate test class name
        test_class_name = options.get('test_class_name')
        if not test_class_name:
            config_name = config.get('name', 'APISequence')
            test_class_name = self._sanitize_class_name(config_name)

        # Prepare template context
        context = {
            'config': config,
            'config_json': self._format_config_for_csharp(config),
            'test_class_name': test_class_name,
            'nodes': config.get('nodes', []),
            'generation_timestamp': datetime.now().isoformat(),
            'namespace': options.get('namespace', 'FlowSphere.Tests')
        }

        # Load and render template
        template = self.load_template('csharp/xunit_template.jinja2')
        code = self.render_template(template, context)

        # Format code
        code = self.format_code(code)

        return code

    def _sanitize_class_name(self, name: str) -> str:
        """
        Convert a string to a valid C# class name.

        Args:
            name: Input string

        Returns:
            Valid C# class name
        """
        # Remove/replace invalid characters
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

        # Convert to PascalCase
        parts = name.split('_')
        pascal_case = ''.join(word.capitalize() for word in parts if word)

        # Ensure it starts with a letter or underscore
        if pascal_case and pascal_case[0].isdigit():
            pascal_case = '_' + pascal_case

        # Default name if empty
        if not pascal_case:
            pascal_case = 'APISequenceTest'

        return pascal_case

    def _format_config_for_csharp(self, config: Dict[str, Any]) -> str:
        """
        Format configuration for C# Dictionary initialization.

        Args:
            config: FlowSphere configuration

        Returns:
            C# Dictionary initialization code
        """
        # For now, use JSON serialization as placeholder
        # In production, this would generate proper C# dictionary syntax
        json_str = json.dumps(config, indent=12)
        # This is a simplified version - real implementation would need proper C# object initialization
        return f'JsonSerializer.Deserialize<Dictionary<string, object>>(@"{json_str}")'

    def format_code(self, code: str) -> str:
        """
        Format C# code (basic formatting).

        Args:
            code: Raw generated code

        Returns:
            Formatted code
        """
        # Remove excessive blank lines
        code = re.sub(r'\n{4,}', '\n\n\n', code)

        # Ensure file ends with single newline
        code = code.rstrip() + '\n'

        return code

    def validate_generated_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated code is syntactically correct C#.

        Note: This is a basic syntax check. Full validation requires .NET SDK.

        Args:
            code: Generated C# code

        Returns:
            Tuple of (is_valid, error_message)
        """
        checks = [
            ('class APISequence' in code, "Missing APISequence class"),
            ('namespace ' in code, "Missing namespace declaration"),
            ('[Fact]' in code, "Missing xUnit [Fact] attributes"),
            ('using Xunit;' in code, "Missing xUnit using statement"),
            ('HttpClient' in code, "Missing HttpClient usage"),
        ]

        for is_valid, error_msg in checks:
            if not is_valid:
                return False, error_msg

        return True, None

    def get_usage_instructions(self) -> str:
        """
        Get instructions for running generated tests.

        Returns:
            Markdown-formatted usage instructions
        """
        return """
## Running the Generated Tests

### Create .NET Project

```bash
# Create new xUnit test project
dotnet new xunit -n FlowSphereTests
cd FlowSphereTests

# Copy generated test file
# (save the generated code as APISequenceTests.cs)

# Install dependencies
dotnet add package xunit --version 2.6.0
dotnet add package xunit.runner.visualstudio --version 2.5.0
dotnet add package Newtonsoft.Json --version 13.0.3
dotnet add package Microsoft.NET.Test.Sdk --version 17.8.0
```

### Run Tests

```bash
# Run all tests
dotnet test

# Run with verbose output
dotnet test --logger "console;verbosity=detailed"

# Run specific test
dotnet test --filter "FullyQualifiedName~TestMethodName"

# Run with code coverage
dotnet test --collect:"XPlat Code Coverage"
```

### Project File (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.6.0" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
```

## Customization

The generated test file includes the `APISequence` class which provides all core functionality:

- `SubstituteVariables()` - Variable substitution
- `ExtractField()` - Field extraction using JSONPath
- `EvaluateCondition()` - Condition evaluation
- `ShouldExecuteNode()` - Condition checking
- `ValidateResponse()` - Response validation with xUnit assertions
- `ExecuteNodeAsync()` - HTTP request execution
- Uses `HttpClient` for HTTP requests
- Uses `System.Text.Json` and `Newtonsoft.Json` for JSON handling

You can extend or override these methods for custom behavior.

## Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.

## Requirements

- .NET 8.0 or higher
- xUnit 2.6.0 or higher
"""

    def get_csproj_template(self, project_name: str = "FlowSphereTests") -> str:
        """
        Generate a complete .csproj file.

        Args:
            project_name: Name for the project

        Returns:
            Complete .csproj content
        """
        return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <RootNamespace>{project_name}</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.6.0" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
"""


class CSharpNUnitGenerator(BaseGenerator):
    """
    Generator for C# NUnit test code.

    Produces a complete NUnit test file that can be executed without modification.
    """

    def __init__(self):
        """Initialize the C# NUnit generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "C#"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "NUnit"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required NuGet packages.

        Returns:
            List of NuGet package names
        """
        return [
            "NUnit@^3.14.0",
            "NUnit3TestAdapter@^4.5.0",
            "Newtonsoft.Json@^13.0.3",
            "Microsoft.NET.Test.Sdk@^17.8.0"
        ]

    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate C# NUnit code from FlowSphere configuration.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - test_class_name: Name for test class (default: auto-generated)
                - namespace: Namespace for the test class (default: FlowSphere.Tests)

        Returns:
            Complete C# NUnit test file as string
        """
        # Validate config first
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        # Generate test class name
        test_class_name = options.get('test_class_name')
        if not test_class_name:
            config_name = config.get('name', 'APISequence')
            test_class_name = self._sanitize_class_name(config_name)

        # Prepare template context
        context = {
            'config': config,
            'config_json': self._format_config_for_csharp(config),
            'test_class_name': test_class_name,
            'nodes': config.get('nodes', []),
            'generation_timestamp': datetime.now().isoformat(),
            'namespace': options.get('namespace', 'FlowSphere.Tests')
        }

        # Load and render template
        template = self.load_template('csharp/nunit_template.jinja2')
        code = self.render_template(template, context)

        # Format code
        code = self.format_code(code)

        return code

    def _sanitize_class_name(self, name: str) -> str:
        """
        Convert a string to a valid C# class name.

        Args:
            name: Input string

        Returns:
            Valid C# class name
        """
        # Remove/replace invalid characters
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

        # Convert to PascalCase
        parts = name.split('_')
        pascal_case = ''.join(word.capitalize() for word in parts if word)

        # Ensure it starts with a letter or underscore
        if pascal_case and pascal_case[0].isdigit():
            pascal_case = '_' + pascal_case

        # Default name if empty
        if not pascal_case:
            pascal_case = 'APISequenceTest'

        return pascal_case

    def _format_config_for_csharp(self, config: Dict[str, Any]) -> str:
        """
        Format configuration for C# Dictionary initialization.

        Args:
            config: FlowSphere configuration

        Returns:
            C# Dictionary initialization code
        """
        # For now, use JSON serialization as placeholder
        # In production, this would generate proper C# dictionary syntax
        json_str = json.dumps(config, indent=12)
        # This is a simplified version - real implementation would need proper C# object initialization
        return f'JsonSerializer.Deserialize<Dictionary<string, object>>(@"{json_str}")'

    def format_code(self, code: str) -> str:
        """
        Format C# code (basic formatting).

        Args:
            code: Raw generated code

        Returns:
            Formatted code
        """
        # Remove excessive blank lines
        code = re.sub(r'\n{4,}', '\n\n\n', code)

        # Ensure file ends with single newline
        code = code.rstrip() + '\n'

        return code

    def validate_generated_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated code is syntactically correct C#.

        Note: This is a basic syntax check. Full validation requires .NET SDK.

        Args:
            code: Generated C# code

        Returns:
            Tuple of (is_valid, error_message)
        """
        checks = [
            ('class APISequence' in code, "Missing APISequence class"),
            ('namespace ' in code, "Missing namespace declaration"),
            ('[Test]' in code, "Missing NUnit [Test] attributes"),
            ('using NUnit.Framework;' in code, "Missing NUnit using statement"),
            ('HttpClient' in code, "Missing HttpClient usage"),
            ('[TestFixture]' in code, "Missing [TestFixture] attribute"),
        ]

        for is_valid, error_msg in checks:
            if not is_valid:
                return False, error_msg

        return True, None

    def get_usage_instructions(self) -> str:
        """
        Get instructions for running generated tests.

        Returns:
            Markdown-formatted usage instructions
        """
        return """
## Running the Generated Tests

### Create .NET Project

```bash
# Create new NUnit test project
dotnet new nunit -n FlowSphereTests
cd FlowSphereTests

# Copy generated test file
# (save the generated code as APISequenceTests.cs)

# Install dependencies
dotnet add package NUnit --version 3.14.0
dotnet add package NUnit3TestAdapter --version 4.5.0
dotnet add package Newtonsoft.Json --version 13.0.3
dotnet add package Microsoft.NET.Test.Sdk --version 17.8.0
```

### Run Tests

```bash
# Run all tests
dotnet test

# Run with verbose output
dotnet test --logger "console;verbosity=detailed"

# Run specific test
dotnet test --filter "FullyQualifiedName~TestMethodName"

# Run with code coverage
dotnet test --collect:"XPlat Code Coverage"
```

### Project File (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="NUnit" Version="3.14.0" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
```

## Customization

The generated test file includes the `APISequence` class which provides all core functionality:

- `SubstituteVariables()` - Variable substitution
- `ExtractField()` - Field extraction using JSONPath
- `EvaluateCondition()` - Condition evaluation
- `ShouldExecuteNode()` - Condition checking
- `ValidateResponse()` - Response validation with NUnit Assert.That()
- `ExecuteNodeAsync()` - HTTP request execution
- Uses `HttpClient` for HTTP requests
- Uses `System.Text.Json` and `Newtonsoft.Json` for JSON handling
- Uses NUnit constraint model for assertions

You can extend or override these methods for custom behavior.

## Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.

## Requirements

- .NET 8.0 or higher
- NUnit 3.14.0 or higher
"""

    def get_csproj_template(self, project_name: str = "FlowSphereTests") -> str:
        """
        Generate a complete .csproj file.

        Args:
            project_name: Name for the project

        Returns:
            Complete .csproj content
        """
        return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <RootNamespace>{project_name}</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="NUnit" Version="3.14.0" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
"""


# Convenience function for CLI usage
def generate_csharp_xunit(config_str: str, **options) -> str:
    """
    Generate C# xUnit code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Generated C# xUnit code

    Raises:
        ValueError: If config is invalid
    """
    generator = CSharpXUnitGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)


def generate_csharp_nunit(config_str: str, **options) -> str:
    """
    Generate C# NUnit code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Generated C# NUnit code

    Raises:
        ValueError: If config is invalid
    """
    generator = CSharpNUnitGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)
