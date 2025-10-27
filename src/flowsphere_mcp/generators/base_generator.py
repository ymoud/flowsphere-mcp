"""
Base Generator for FlowSphere Code Generation

Provides common functionality for all code generators including:
- Configuration validation
- Template loading and rendering
- Error handling
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


class BaseGenerator(ABC):
    """
    Base class for all FlowSphere code generators.

    Provides common functionality for loading configs, templates, and generating code.
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize the generator.

        Args:
            template_dir: Directory containing Jinja2 templates (defaults to templates/)
        """
        if template_dir is None:
            # Default to templates directory relative to this file
            template_dir = Path(__file__).parent.parent / 'templates'

        self.template_dir = Path(template_dir)
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate a FlowSphere configuration.

        Args:
            config: The configuration dictionary to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required top-level fields
        if 'nodes' not in config:
            return False, "Config must contain 'nodes' array"

        nodes = config.get('nodes', [])

        if not isinstance(nodes, list):
            return False, "'nodes' must be an array"

        if len(nodes) == 0:
            return False, "'nodes' array cannot be empty"

        # Validate each node
        seen_ids = set()

        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                return False, f"Node at index {i} must be an object"

            # Check required node fields
            required_fields = ['id', 'name', 'method', 'url']
            for field in required_fields:
                if field not in node:
                    return False, f"Node at index {i} missing required field: {field}"

            # Check for duplicate node IDs
            node_id = node['id']
            if node_id in seen_ids:
                return False, f"Duplicate node ID: {node_id}"
            seen_ids.add(node_id)

            # Validate method
            valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
            method = node.get('method', '').upper()
            if method not in valid_methods:
                return False, f"Node {node_id}: invalid method '{method}'. Must be one of: {', '.join(valid_methods)}"

        return True, None

    def load_config(self, config_str: str) -> Dict[str, Any]:
        """
        Load and parse a FlowSphere configuration from JSON string.

        Args:
            config_str: JSON string containing the configuration

        Returns:
            Parsed configuration dictionary

        Raises:
            ValueError: If config is invalid JSON or fails validation
        """
        try:
            config = json.loads(config_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")

        # Validate config
        is_valid, error_msg = self.validate_config(config)
        if not is_valid:
            raise ValueError(f"Invalid configuration: {error_msg}")

        return config

    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template by name.

        Args:
            template_name: Name of the template file (relative to template_dir)

        Returns:
            Loaded Jinja2 template

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        try:
            return self.jinja_env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(f"Template '{template_name}' not found: {str(e)}")

    def render_template(self, template: Template, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.

        Args:
            template: Jinja2 template to render
            context: Dictionary of variables to pass to template

        Returns:
            Rendered template as string
        """
        return template.render(**context)

    @abstractmethod
    def generate(self, config: Dict[str, Any], **options) -> str:
        """
        Generate code from a FlowSphere configuration.

        This method must be implemented by subclasses.

        Args:
            config: Validated FlowSphere configuration dictionary
            **options: Additional generator-specific options

        Returns:
            Generated code as string
        """
        pass

    @abstractmethod
    def get_language_name(self) -> str:
        """
        Get the name of the language this generator produces.

        Returns:
            Language name (e.g., "Python", "JavaScript", "C#")
        """
        pass

    @abstractmethod
    def get_framework_name(self) -> str:
        """
        Get the name of the testing framework this generator uses.

        Returns:
            Framework name (e.g., "pytest", "jest", "xunit")
        """
        pass

    def get_required_dependencies(self) -> list[str]:
        """
        Get list of required dependencies for generated code.

        Returns:
            List of dependency strings (format depends on language)
        """
        return []

    def format_code(self, code: str) -> str:
        """
        Format the generated code (optional, can be overridden).

        Args:
            code: Raw generated code

        Returns:
            Formatted code
        """
        # Base implementation does no formatting
        return code
