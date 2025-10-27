"""
Python pytest Code Generator for FlowSphere

Generates production-ready Python pytest code from FlowSphere configurations.
Supports all 18 FlowSphere features.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from .base_generator import BaseGenerator


class PythonPytestGenerator(BaseGenerator):
    """
    Generator for Python pytest test code.

    Produces a complete pytest test file that can be executed without modification.
    """

    def __init__(self):
        """Initialize the Python pytest generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "Python"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "pytest"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required Python packages.

        Returns:
            List of pip package names
        """
        return [
            "pytest>=7.0.0",
            "requests>=2.28.0",
            "jsonpath-ng>=1.5.3"
        ]

    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate Python pytest code from FlowSphere configuration.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - test_class_name: Name for test class (default: auto-generated)
                - include_comments: Include detailed comments (default: True)

        Returns:
            Complete Python pytest test file as string
        """
        # Validate config first
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        # Generate test class name
        test_class_name = options.get('test_class_name')
        if not test_class_name:
            # Generate from config name or use generic name
            config_name = config.get('name', 'APISequence')
            test_class_name = self._sanitize_class_name(config_name)

        # Prepare template context
        context = {
            'config': config,
            'config_json': json.dumps(config, indent=4),
            'test_class_name': test_class_name,
            'generation_timestamp': datetime.now().isoformat(),
            'include_comments': options.get('include_comments', True)
        }

        # Load and render template
        template = self.load_template('python/pytest_template.jinja2')
        code = self.render_template(template, context)

        # Format code
        code = self.format_code(code)

        return code

    def _sanitize_class_name(self, name: str) -> str:
        """
        Convert a string to a valid Python class name.

        Args:
            name: Input string

        Returns:
            Valid Python class name
        """
        # Remove/replace invalid characters
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

        # Convert to PascalCase
        parts = name.split('_')
        pascal_case = ''.join(word.capitalize() for word in parts if word)

        # Ensure it starts with a letter or underscore (after PascalCase conversion)
        if pascal_case and pascal_case[0].isdigit():
            pascal_case = '_' + pascal_case

        # Default name if empty
        if not pascal_case:
            pascal_case = 'APISequenceTest'

        return pascal_case

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

    def validate_generated_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated code is syntactically correct Python.

        Args:
            code: Generated Python code

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            compile(code, '<generated>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"

    def get_usage_instructions(self) -> str:
        """
        Get instructions for running generated tests.

        Returns:
            Markdown-formatted usage instructions
        """
        return """
## Running the Generated Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install pytest requests jsonpath-ng
```

### Run Tests

```bash
# Run all tests in the file
pytest test_generated.py -v

# Run with debug output
pytest test_generated.py -v -s

# Run specific test
pytest test_generated.py::TestAPISequence::test_execute_sequence -v
```

### Run Directly

```bash
python test_generated.py
```

## Customization

The generated test class inherits from `APISequence` which provides all core functionality:

- `substitute_variables()` - Variable substitution
- `extract_field()` - Field extraction using JSONPath
- `evaluate_conditions()` - Condition evaluation
- `validate_response()` - Response validation
- `execute_http_request()` - HTTP request execution

You can extend or override these methods for custom behavior.

## Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.
"""


# Convenience function for CLI usage
def generate_python_pytest(config_str: str, **options) -> str:
    """
    Generate Python pytest code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Generated Python pytest code

    Raises:
        ValueError: If config is invalid
    """
    generator = PythonPytestGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)
