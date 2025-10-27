"""
Python Behave/BDD Code Generator for FlowSphere

Generates production-ready Python behave tests from FlowSphere configurations.
Produces Gherkin feature files and step definitions.
Supports all 18 FlowSphere features.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from .base_generator import BaseGenerator


class PythonBehaveGenerator(BaseGenerator):
    """
    Generator for Python behave/BDD test code.

    Produces:
    1. Gherkin feature file (.feature) with test scenarios
    2. Step definitions file (.py) with Python behave steps

    Both files can be used directly with the behave test runner.
    """

    def __init__(self):
        """Initialize the Python behave generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "Python"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "behave"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required Python packages.

        Returns:
            List of pip package names
        """
        return [
            "behave>=1.2.6",
            "requests>=2.28.0",
            "jsonpath-ng>=1.5.3"
        ]

    def generate(self, config: Dict[str, Any], **options) -> Dict[str, str]:
        """
        Generate Python behave code from FlowSphere configuration.

        Returns both the Gherkin feature file and step definitions.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - feature_name: Name for feature file (default: auto-generated)
                - include_comments: Include detailed comments (default: True)

        Returns:
            Dictionary with two keys:
            - 'feature': Gherkin feature file content
            - 'steps': Python step definitions file content
        """
        # Validate config first
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        # Generate feature name
        feature_name = options.get('feature_name')
        if not feature_name:
            config_name = config.get('name', 'API Test')
            feature_name = self._sanitize_feature_name(config_name)

        # Prepare template context
        context = {
            'config': config,
            'config_json': json.dumps(config, indent=4),
            'feature_name': feature_name,
            'generation_timestamp': datetime.now().isoformat(),
            'include_comments': options.get('include_comments', True)
        }

        # Generate feature file
        feature_template = self.load_template('python/gherkin_template.jinja2')
        feature_code = self.render_template(feature_template, context)
        feature_code = self.format_gherkin(feature_code)

        # Generate step definitions file
        steps_template = self.load_template('python/step_definitions_template.jinja2')
        steps_code = self.render_template(steps_template, context)
        steps_code = self.format_code(steps_code)

        return {
            'feature': feature_code,
            'steps': steps_code
        }

    def generate_single_file(self, config: Dict[str, Any], **options) -> str:
        """
        Generate a combined output for MCP tool usage.

        Returns both files with clear separators for easy parsing.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional generator options

        Returns:
            Combined string with both files separated by markers
        """
        files = self.generate(config, **options)

        feature_name = options.get('feature_name', self._sanitize_feature_name(
            config.get('name', 'api_test')
        ))

        output = f"""# ========================================
# FEATURE FILE: {feature_name}.feature
# ========================================

{files['feature']}

# ========================================
# STEP DEFINITIONS: steps/{feature_name}_steps.py
# ========================================

{files['steps']}

# ========================================
# USAGE INSTRUCTIONS
# ========================================

{self.get_usage_instructions()}
"""
        return output

    def _sanitize_feature_name(self, name: str) -> str:
        """
        Convert a string to a valid feature file name.

        Args:
            name: Input string

        Returns:
            Valid feature file name (lowercase with underscores)
        """
        # Convert to lowercase and replace spaces/special chars with underscores
        name = name.lower()
        name = re.sub(r'[^a-z0-9_]', '_', name)

        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)

        # Remove leading/trailing underscores
        name = name.strip('_')

        # Default name if empty
        if not name:
            name = 'api_test'

        return name

    def format_gherkin(self, code: str) -> str:
        """
        Format Gherkin feature file.

        Args:
            code: Raw generated Gherkin

        Returns:
            Formatted Gherkin
        """
        # Remove excessive blank lines (more than 2 consecutive)
        code = re.sub(r'\n{3,}', '\n\n', code)

        # Ensure proper spacing around scenarios
        code = re.sub(r'(\n  Scenario:)', r'\n\1', code)

        # Ensure file ends with single newline
        code = code.rstrip() + '\n'

        return code

    def format_code(self, code: str) -> str:
        """
        Format Python code (basic formatting).

        Args:
            code: Raw generated code

        Returns:
            Formatted code
        """
        # Remove excessive blank lines (more than 2 consecutive)
        code = re.sub(r'\n{4,}', '\n\n\n', code)

        # Ensure file ends with single newline
        code = code.rstrip() + '\n'

        return code

    def generate_dependencies_file(self) -> str:
        """
        Generate requirements.txt content.

        Returns:
            requirements.txt file content
        """
        dependencies = self.get_required_dependencies()
        return '\n'.join(dependencies) + '\n'

    def validate_generated_code(self, steps_code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated step definitions are syntactically correct Python.

        Args:
            steps_code: Generated Python step definitions code

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            compile(steps_code, '<generated>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"

    def get_usage_instructions(self) -> str:
        """
        Get instructions for running generated behave tests.

        Returns:
            Markdown-formatted usage instructions
        """
        return """
## Running the Generated Behave Tests

### Project Structure

Organize your files as follows:

```
project/
├── features/
│   ├── api_test.feature          # Generated feature file
│   └── steps/
│       └── api_test_steps.py     # Generated step definitions
└── requirements.txt
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install behave requests jsonpath-ng
```

### Run Tests

```bash
# Run all features
behave

# Run specific feature
behave features/api_test.feature

# Run with verbose output
behave -v

# Run with debug output (shows prints)
behave --no-capture

# Run specific scenario by name
behave -n "Get a single post"

# Generate HTML report
behave --format=html --outfile=report.html
```

### BDD/Gherkin Advantages

- **Human-Readable**: Feature files describe tests in plain English
- **Business Alignment**: Non-technical stakeholders can understand tests
- **Reusable Steps**: Step definitions can be shared across features
- **Living Documentation**: Tests serve as executable specifications

### Step Definitions

The generated step definitions implement all FlowSphere features:

- HTTP execution (GET, POST, PUT, DELETE, PATCH)
- Variable substitution (4 types)
- Condition evaluation (8 operators)
- Response validation (status + JSONPath)
- Field extraction
- User prompts
- Browser launch
- Skip flags

### Customization

You can extend the step definitions with your own custom steps:

```python
@when('I do something custom')
def step_custom_action(context):
    # Your custom logic here
    pass
```

### Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.

### Best Practices

1. Keep feature files focused and readable
2. Use descriptive scenario names
3. Reuse step definitions across features
4. Run tests in CI/CD pipelines
5. Generate reports for stakeholders
"""

    def get_file_structure(self, feature_name: str) -> Dict[str, str]:
        """
        Get the recommended file structure for behave tests.

        Args:
            feature_name: Name of the feature

        Returns:
            Dictionary mapping file paths to descriptions
        """
        return {
            f"features/{feature_name}.feature": "Gherkin feature file with test scenarios",
            f"features/steps/{feature_name}_steps.py": "Python step definitions",
            "features/environment.py": "Optional: behave hooks and setup (create manually if needed)",
            "requirements.txt": "Python dependencies"
        }


# Convenience function for CLI usage
def generate_python_behave(config_str: str, **options) -> Dict[str, str]:
    """
    Generate Python behave code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Dictionary with 'feature' and 'steps' keys containing generated code

    Raises:
        ValueError: If config is invalid
    """
    generator = PythonBehaveGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)


def generate_python_behave_single(config_str: str, **options) -> str:
    """
    Generate Python behave code as a single combined string.

    Useful for MCP tools that return a single string output.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Combined string with both feature and steps files

    Raises:
        ValueError: If config is invalid
    """
    generator = PythonBehaveGenerator()
    config = generator.load_config(config_str)
    return generator.generate_single_file(config, **options)
