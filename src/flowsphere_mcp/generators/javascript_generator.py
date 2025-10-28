"""
JavaScript Code Generators for FlowSphere

Generates production-ready JavaScript test code from FlowSphere configurations.
Supports Jest and Mocha frameworks.
Supports all 18 FlowSphere features.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from .base_generator import BaseGenerator


class JavaScriptJestGenerator(BaseGenerator):
    """
    Generator for JavaScript Jest test code.

    Produces a complete Jest test file that can be executed without modification.
    """

    def __init__(self):
        """Initialize the JavaScript Jest generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "JavaScript"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "Jest"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required npm packages.

        Returns:
            List of npm package names
        """
        return [
            "jest@^29.0.0",
            "axios@^1.6.0",
            "jsonpath-plus@^7.2.0",
            "uuid@^9.0.0"
        ]

    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate JavaScript Jest code from FlowSphere configuration.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - test_class_name: Name for test class (default: auto-generated)
                - include_comments: Include detailed comments (default: True)

        Returns:
            Complete JavaScript Jest test file as string
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
        template = self.load_template('javascript/jest_template.jinja2')
        code = self.render_template(template, context)

        # Format code
        code = self.format_code(code)

        return code

    def _sanitize_class_name(self, name: str) -> str:
        """
        Convert a string to a valid JavaScript class name.

        Args:
            name: Input string

        Returns:
            Valid JavaScript class name
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
        Format JavaScript code (basic formatting).

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
        Generate package.json dependencies section.

        Returns:
            JSON string with dependencies
        """
        dependencies = {}
        for dep in self.get_required_dependencies():
            name, version = dep.split('@') if '@' in dep else (dep, '^1.0.0')
            dependencies[name] = version

        return json.dumps({
            "devDependencies": dependencies
        }, indent=2)

    def validate_generated_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated code is syntactically correct JavaScript.

        Note: This is a basic syntax check. Full validation requires Node.js.

        Args:
            code: Generated JavaScript code

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic structure checks (don't count brackets as JSON contains them)
        checks = [
            ('class APISequence' in code, "Missing APISequence class"),
            ('describe(' in code, "Missing Jest describe block"),
            ('const axios = require' in code or 'import axios' in code, "Missing axios import"),
            ('substituteVariables' in code, "Missing substituteVariables method"),
            ('executeHttpRequest' in code, "Missing executeHttpRequest method"),
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

### Install Dependencies

```bash
npm install --save-dev jest axios jsonpath-plus uuid
```

Or add to your package.json:

```json
{
  "devDependencies": {
    "jest": "^29.0.0",
    "axios": "^1.6.0",
    "jsonpath-plus": "^7.2.0",
    "uuid": "^9.0.0"
  },
  "scripts": {
    "test": "jest"
  }
}
```

### Run Tests

```bash
# Run all tests
npm test

# Run with verbose output
npm test -- --verbose

# Run specific test file
npm test test_generated.test.js

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Run Directly with Node.js

```bash
node test_generated.test.js
```

## Customization

The generated test file includes the `APISequence` class which provides all core functionality:

- `substituteVariables()` - Variable substitution
- `extractField()` - Field extraction using JSONPath
- `evaluateConditions()` - Condition evaluation
- `validateResponse()` - Response validation
- `executeHttpRequest()` - HTTP request execution
- `executeSequence()` - Complete sequence execution

You can extend or override these methods for custom behavior.

## Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.

## ES Modules

If using ES modules (type: "module" in package.json), change:

```javascript
const axios = require('axios');
// to
import axios from 'axios';

module.exports = { APISequence };
// to
export { APISequence };
```
"""

    def get_package_json_template(self, project_name: str = "flowsphere-tests") -> str:
        """
        Generate a complete package.json file.

        Args:
            project_name: Name for the package

        Returns:
            Complete package.json content
        """
        deps = {}
        for dep in self.get_required_dependencies():
            if '@' in dep:
                name, version = dep.split('@', 1)
                deps[name] = version
            else:
                deps[dep] = "latest"

        package = {
            "name": project_name,
            "version": "1.0.0",
            "description": "FlowSphere generated API tests",
            "main": "index.js",
            "scripts": {
                "test": "jest",
                "test:watch": "jest --watch",
                "test:coverage": "jest --coverage"
            },
            "keywords": ["flowsphere", "api", "testing", "jest"],
            "author": "",
            "license": "MIT",
            "devDependencies": deps
        }

        return json.dumps(package, indent=2)


# Convenience function for CLI usage
def generate_javascript_jest(config_str: str, **options) -> str:
    """
    Generate JavaScript Jest code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Generated JavaScript Jest code

    Raises:
        ValueError: If config is invalid
    """
    generator = JavaScriptJestGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)


class JavaScriptMochaGenerator(BaseGenerator):
    """
    Generator for JavaScript Mocha test code.

    Produces a complete Mocha test file that can be executed without modification.
    """

    def __init__(self):
        """Initialize the JavaScript Mocha generator."""
        super().__init__()

    def get_language_name(self) -> str:
        """Get language name."""
        return "JavaScript"

    def get_framework_name(self) -> str:
        """Get framework name."""
        return "Mocha"

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required npm packages.

        Returns:
            List of npm package names
        """
        return [
            "mocha@^10.0.0",
            "chai@^4.3.0",
            "axios@^1.6.0",
            "jsonpath-plus@^7.2.0",
            "uuid@^9.0.0"
        ]

    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate JavaScript Mocha code from FlowSphere configuration.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional options
                - test_class_name: Name for test class (default: auto-generated)
                - include_comments: Include detailed comments (default: True)

        Returns:
            Complete JavaScript Mocha test file as string
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
            'nodes': config.get('nodes', []),
            'generation_timestamp': datetime.now().isoformat(),
            'include_comments': options.get('include_comments', True)
        }

        # Load and render template
        template = self.load_template('javascript/mocha_template.jinja2')
        code = self.render_template(template, context)

        # Format code
        code = self.format_code(code)

        return code

    def _sanitize_class_name(self, name: str) -> str:
        """
        Convert a string to a valid JavaScript class name.

        Args:
            name: Input string

        Returns:
            Valid JavaScript class name
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
        Format JavaScript code (basic formatting).

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
        Generate package.json dependencies section.

        Returns:
            JSON string with dependencies
        """
        dependencies = {}
        for dep in self.get_required_dependencies():
            name, version = dep.split('@') if '@' in dep else (dep, '^1.0.0')
            dependencies[name] = version

        return json.dumps({
            "devDependencies": dependencies
        }, indent=2)

    def validate_generated_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate that generated code is syntactically correct JavaScript.

        Note: This is a basic syntax check. Full validation requires Node.js.

        Args:
            code: Generated JavaScript code

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic structure checks
        checks = [
            ('class APISequence' in code, "Missing APISequence class"),
            ('describe(' in code, "Missing Mocha describe block"),
            ('const axios = require' in code or 'import axios' in code, "Missing axios import"),
            ('const { expect } = require(\'chai\')' in code, "Missing chai import"),
            ('substituteVariables' in code, "Missing substituteVariables method"),
            ('executeNode' in code, "Missing executeNode method"),
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

### Install Dependencies

```bash
npm install --save-dev mocha chai axios jsonpath-plus uuid
```

Or add to your package.json:

```json
{
  "devDependencies": {
    "mocha": "^10.0.0",
    "chai": "^4.3.0",
    "axios": "^1.6.0",
    "jsonpath-plus": "^7.2.0",
    "uuid": "^9.0.0"
  },
  "scripts": {
    "test": "mocha"
  }
}
```

### Run Tests

```bash
# Run all tests
npm test

# Run with verbose output
npm test -- --reporter spec

# Run specific test file
npm test test_generated.test.js

# Run with grep (filter tests)
npm test -- --grep "API Test"

# Run in watch mode
npm test -- --watch
```

### Run Directly with Node.js

```bash
npx mocha test_generated.test.js
```

## Customization

The generated test file includes the `APISequence` class which provides all core functionality:

- `substituteVariables()` - Variable substitution
- `extractField()` - Field extraction using JSONPath
- `evaluateCondition()` - Condition evaluation
- `shouldExecuteNode()` - Condition checking
- `validateResponse()` - Response validation with Chai assertions
- `executeNode()` - HTTP request execution
- `run()` - Complete sequence execution

You can extend or override these methods for custom behavior.

## Debugging

Set `enableDebug: true` in your FlowSphere config to see detailed debug output during test execution.

## ES Modules

If using ES modules (type: "module" in package.json), change:

```javascript
const axios = require('axios');
// to
import axios from 'axios';

module.exports = { APISequence };
// to
export { APISequence };
```
"""

    def get_package_json_template(self, project_name: str = "flowsphere-tests") -> str:
        """
        Generate a complete package.json file.

        Args:
            project_name: Name for the package

        Returns:
            Complete package.json content
        """
        deps = {}
        for dep in self.get_required_dependencies():
            if '@' in dep:
                name, version = dep.split('@', 1)
                deps[name] = version
            else:
                deps[dep] = "latest"

        package = {
            "name": project_name,
            "version": "1.0.0",
            "description": "FlowSphere generated API tests",
            "main": "index.js",
            "scripts": {
                "test": "mocha",
                "test:watch": "mocha --watch",
                "test:grep": "mocha --grep"
            },
            "keywords": ["flowsphere", "api", "testing", "mocha"],
            "author": "",
            "license": "MIT",
            "devDependencies": deps
        }

        return json.dumps(package, indent=2)


# Convenience function for CLI usage
def generate_javascript_mocha(config_str: str, **options) -> str:
    """
    Generate JavaScript Mocha code from FlowSphere config JSON string.

    Args:
        config_str: FlowSphere configuration as JSON string
        **options: Additional generator options

    Returns:
        Generated JavaScript Mocha code

    Raises:
        ValueError: If config is invalid
    """
    generator = JavaScriptMochaGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)



class JavaScriptCucumberGenerator(BaseGenerator):
    """
    Generator for JavaScript Cucumber/BDD test code.

    Produces:
    1. Gherkin feature file (.feature) with test scenarios
    2. Step definitions file (.js) with cucumber-js steps
    """

    def __init__(self):
        super().__init__()

    def get_language_name(self) -> str:
        return "JavaScript"

    def get_framework_name(self) -> str:
        return "Cucumber"

    def get_required_dependencies(self) -> list[str]:
        return [
            "@cucumber/cucumber@^10.0.0",
            "axios@^1.6.0",
            "jsonpath-plus@^7.2.0",
            "uuid@^9.0.0",
            "chai@^4.3.0"
        ]

    def generate(self, config: Dict[str, Any], **options) -> Dict[str, str]:
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        feature_name = options.get('feature_name')
        if not feature_name:
            config_name = config.get('name', 'API Test')
            feature_name = self._sanitize_feature_name(config_name)

        context = {
            'config': config,
            'config_json': json.dumps(config, indent=4),
            'feature_name': feature_name,
            'generation_timestamp': datetime.now().isoformat(),
            'include_comments': options.get('include_comments', True)
        }

        feature_template = self.load_template('javascript/cucumber_feature_template.jinja2')
        feature_code = self.render_template(feature_template, context)
        feature_code = self.format_gherkin(feature_code)

        steps_template = self.load_template('javascript/cucumber_steps_template.jinja2')
        steps_code = self.render_template(steps_template, context)
        steps_code = self.format_code(steps_code)

        return {'feature': feature_code, 'steps': steps_code}

    def _sanitize_feature_name(self, name: str) -> str:
        name = re.sub(r'[^a-z0-9]+', '_', name.lower())
        name = name.strip('_')
        return name if name else 'api_test'

    def format_gherkin(self, code: str) -> str:
        code = re.sub(r'\n{3,}', '\n\n', code)
        return code.rstrip() + '\n'

    def format_code(self, code: str) -> str:
        code = re.sub(r'\n{4,}', '\n\n\n', code)
        return code.rstrip() + '\n'

    def validate_generated_code(self, feature: str, steps: str) -> tuple[bool, Optional[str]]:
        if 'Feature:' not in feature:
            return False, "Missing Feature declaration"
        if 'Scenario:' not in feature:
            return False, "Missing Scenario"
        if 'class APIWorld' not in steps:
            return False, "Missing APIWorld class"
        return True, None

    def get_package_json_template(self, project_name: str = "flowsphere-tests") -> str:
        deps = {}
        for dep in self.get_required_dependencies():
            if '@' in dep and not dep.startswith('@'):
                name, version = dep.split('@', 1)
                deps[name] = version
            elif dep.startswith('@'):
                parts = dep.split('@')
                if len(parts) >= 3:
                    name = '@' + parts[1]
                    version = '@'.join(parts[2:])
                    deps[name] = version
        package = {
            "name": project_name,
            "version": "1.0.0",
            "scripts": {"test": "cucumber-js"},
            "devDependencies": deps
        }
        return json.dumps(package, indent=2)


def generate_javascript_cucumber(config_str: str, **options) -> Dict[str, str]:
    generator = JavaScriptCucumberGenerator()
    config = generator.load_config(config_str)
    return generator.generate(config, **options)
