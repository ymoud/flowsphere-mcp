"""
Base Python Template for FlowSphere Code Generation

This module provides the core functionality that all generated Python test classes
will include. It handles:
- HTTP request execution
- Variable substitution (dynamic placeholders, global vars, response refs, user input)
- Field extraction using JSONPath
- Condition evaluation
- Response validation
"""

import re
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Union
from jsonpath_ng import parse as jsonpath_parse


class APISequence:
    """
    Base class for executing FlowSphere HTTP API sequences.

    This class provides all the core functionality needed to execute a sequence
    of HTTP requests with variables, conditions, validations, and response extraction.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the API sequence executor.

        Args:
            config: FlowSphere configuration dictionary
        """
        self.config = config
        self.variables = config.get('variables', {})
        self.defaults = config.get('defaults', {})
        self.responses: Dict[str, Any] = {}  # Stores responses by node ID
        self.user_inputs: Dict[str, str] = {}  # Stores user prompts responses
        self.debug = config.get('enableDebug', False)

    def log_debug(self, message: str):
        """Log debug messages if debug mode is enabled."""
        if self.debug:
            print(f"[DEBUG] {message}")

    def generate_guid(self) -> str:
        """Generate a new GUID/UUID."""
        return str(uuid.uuid4())

    def generate_timestamp(self) -> int:
        """Generate current Unix timestamp in milliseconds."""
        return int(time.time() * 1000)

    def substitute_variables(self, value: Any, step_timestamp: Optional[int] = None) -> Any:
        """
        Perform variable substitution on a value.

        Substitution order:
        1. Dynamic placeholders ({{ $guid }}, {{ $timestamp }})
        2. Global variables ({{ .vars.key }})
        3. User input ({{ .input.variableName }})
        4. Response references ({{ .responses.nodeId.field }})

        Args:
            value: The value to substitute (can be string, dict, list, etc.)
            step_timestamp: Timestamp to use for {{ $timestamp }} (same per step)

        Returns:
            Value with all substitutions applied
        """
        if isinstance(value, str):
            # Generate step timestamp once if not provided
            if step_timestamp is None:
                step_timestamp = self.generate_timestamp()

            # 1. Dynamic placeholders
            # {{ $guid }} - generate new UUID for each occurrence
            value = re.sub(r'\{\{\s*\$guid\s*\}\}', lambda m: self.generate_guid(), value)

            # {{ $timestamp }} - use same timestamp for the entire step
            value = re.sub(r'\{\{\s*\$timestamp\s*\}\}', str(step_timestamp), value)

            # 2. Global variables - {{ .vars.key }}
            for var_name, var_value in self.variables.items():
                pattern = r'\{\{\s*\.vars\.' + re.escape(var_name) + r'\s*\}\}'
                value = re.sub(pattern, str(var_value), value)

            # 3. User input - {{ .input.variableName }}
            for input_name, input_value in self.user_inputs.items():
                pattern = r'\{\{\s*\.input\.' + re.escape(input_name) + r'\s*\}\}'
                value = re.sub(pattern, str(input_value), value)

            # 4. Response references - {{ .responses.nodeId.field.subfield }}
            # Extract all response reference patterns
            response_pattern = r'\{\{\s*\.responses\.([a-zA-Z0-9_-]+)\.(.+?)\s*\}\}'
            matches = re.finditer(response_pattern, value)

            for match in matches:
                node_id = match.group(1)
                field_path = match.group(2)

                if node_id in self.responses:
                    extracted_value = self.extract_field(self.responses[node_id], field_path)
                    if extracted_value is not None:
                        value = value.replace(match.group(0), str(extracted_value))
                    else:
                        self.log_debug(f"Could not extract {field_path} from {node_id} response")
                else:
                    self.log_debug(f"Response for node {node_id} not found")

            return value

        elif isinstance(value, dict):
            return {k: self.substitute_variables(v, step_timestamp) for k, v in value.items()}

        elif isinstance(value, list):
            return [self.substitute_variables(item, step_timestamp) for item in value]

        else:
            return value

    def extract_field(self, data: Any, field_path: str) -> Any:
        """
        Extract a field from response data using dot notation or JSONPath.

        Supports:
        - Simple keys: "id", "name"
        - Nested keys: "user.profile.email"
        - Array indices: "users[0].name"
        - JSONPath syntax: "$.users[*].name"

        Args:
            data: The response data (usually a dict or list)
            field_path: The field path to extract

        Returns:
            The extracted value, or None if not found
        """
        try:
            # Try JSONPath first if it looks like JSONPath syntax
            if field_path.startswith('$'):
                jsonpath_expr = jsonpath_parse(field_path)
                matches = [match.value for match in jsonpath_expr.find(data)]
                return matches[0] if len(matches) == 1 else matches if matches else None

            # Otherwise use simple dot notation with array support
            parts = field_path.split('.')
            current = data

            for part in parts:
                # Handle array indexing: field[0]
                if '[' in part and ']' in part:
                    key, index_str = part.split('[', 1)
                    index = int(index_str.rstrip(']'))

                    if key:  # e.g., "users[0]"
                        current = current[key][index]
                    else:  # e.g., "[0]"
                        current = current[index]
                else:
                    current = current[part]

            return current

        except (KeyError, IndexError, TypeError, ValueError) as e:
            self.log_debug(f"Field extraction failed for {field_path}: {e}")
            return None

    def evaluate_conditions(self, node: Dict[str, Any]) -> bool:
        """
        Evaluate all conditions for a node. All conditions must be true (AND logic).

        Supported operators:
        - statusCode: Check HTTP status of previous response
        - equals: Check for equality
        - notEquals: Check for inequality
        - exists: Check if field exists
        - greaterThan: Numeric comparison >
        - lessThan: Numeric comparison <
        - greaterThanOrEqual: Numeric comparison >=
        - lessThanOrEqual: Numeric comparison <=

        Args:
            node: The node configuration with conditions

        Returns:
            True if all conditions pass, False otherwise
        """
        conditions = node.get('conditions', [])

        if not conditions:
            return True  # No conditions means always execute

        for condition in conditions:
            # Extract condition details
            source = condition.get('node') or condition.get('variable') or condition.get('input')
            field = condition.get('field', '')
            operator = condition.get('operator')
            expected_value = condition.get('value')

            # Substitute variables in expected value
            if expected_value is not None:
                expected_value = self.substitute_variables(expected_value)

            # Get actual value based on source
            actual_value = None

            if condition.get('node'):
                # From previous response
                node_id = condition['node']
                if node_id in self.responses:
                    if operator == 'statusCode':
                        actual_value = self.responses[node_id].get('_status_code')
                    elif field:
                        response_body = self.responses[node_id].get('body', {})
                        actual_value = self.extract_field(response_body, field)
                else:
                    self.log_debug(f"Condition failed: node {node_id} not found")
                    return False

            elif condition.get('variable'):
                # From global variables
                var_name = condition['variable']
                actual_value = self.variables.get(var_name)

            elif condition.get('input'):
                # From user input
                input_name = condition['input']
                actual_value = self.user_inputs.get(input_name)

            # Evaluate operator
            result = self._evaluate_operator(operator, actual_value, expected_value)

            if not result:
                self.log_debug(f"Condition failed: {operator} - actual: {actual_value}, expected: {expected_value}")
                return False

        return True

    def _evaluate_operator(self, operator: str, actual: Any, expected: Any) -> bool:
        """Evaluate a single operator comparison."""
        if operator == 'statusCode':
            return actual == expected
        elif operator == 'equals':
            return actual == expected
        elif operator == 'notEquals':
            return actual != expected
        elif operator == 'exists':
            return actual is not None
        elif operator == 'greaterThan':
            return float(actual) > float(expected)
        elif operator == 'lessThan':
            return float(actual) < float(expected)
        elif operator == 'greaterThanOrEqual':
            return float(actual) >= float(expected)
        elif operator == 'lessThanOrEqual':
            return float(actual) <= float(expected)
        else:
            self.log_debug(f"Unknown operator: {operator}")
            return False

    def validate_response(self, node: Dict[str, Any], response_data: Dict[str, Any]) -> List[str]:
        """
        Validate a response against node and default validations.

        Args:
            node: The node configuration
            response_data: Response data with status_code and body

        Returns:
            List of validation error messages (empty if all pass)
        """
        errors = []

        # Collect validations
        validations = []

        # Add default validations unless skipped
        if not node.get('skipDefaultValidations', False):
            validations.extend(self.defaults.get('validations', []))

        # Add node-specific validations
        validations.extend(node.get('validations', []))

        # If no validations specified, default to status 200
        if not validations:
            validations = [{'httpStatusCode': 200}]

        # Perform each validation
        for validation in validations:
            # HTTP Status Code validation
            if 'httpStatusCode' in validation:
                expected_status = validation['httpStatusCode']
                actual_status = response_data.get('_status_code')

                if actual_status != expected_status:
                    errors.append(
                        f"HTTP status validation failed: expected {expected_status}, got {actual_status}"
                    )

            # JSONPath field validation
            if 'field' in validation:
                field_path = validation['field']
                expected_value = validation.get('value')

                # Substitute variables in expected value
                if expected_value is not None:
                    expected_value = self.substitute_variables(expected_value)

                # Extract actual value from response body
                response_body = response_data.get('body', {})
                actual_value = self.extract_field(response_body, field_path)

                # Check if value matches (if value specified)
                if expected_value is not None:
                    if actual_value != expected_value:
                        errors.append(
                            f"Field validation failed for {field_path}: expected {expected_value}, got {actual_value}"
                        )
                # Otherwise just check field exists
                elif actual_value is None:
                    errors.append(f"Field validation failed: {field_path} not found in response")

        return errors

    def build_url(self, node: Dict[str, Any]) -> str:
        """Build full URL from node URL and base URL."""
        url = node['url']

        # Apply variable substitution to URL
        url = self.substitute_variables(url)

        # Prepend base URL if URL is relative
        if not url.startswith('http://') and not url.startswith('https://'):
            base_url = self.defaults.get('baseUrl', '')
            url = base_url.rstrip('/') + '/' + url.lstrip('/')

        return url

    def build_headers(self, node: Dict[str, Any]) -> Dict[str, str]:
        """Build headers by merging defaults with node headers."""
        headers = {}

        # Add default headers unless skipped
        if not node.get('skipDefaultHeaders', False):
            headers.update(self.defaults.get('headers', {}))

        # Add/override with node headers
        headers.update(node.get('headers', {}))

        # Apply variable substitution to all headers
        headers = self.substitute_variables(headers)

        return headers

    def build_body(self, node: Dict[str, Any]) -> Optional[str]:
        """Build request body with variable substitution."""
        body = node.get('body')

        if body is None:
            return None

        # Apply variable substitution to body
        body = self.substitute_variables(body)

        # Convert dict to JSON string
        if isinstance(body, dict):
            return json.dumps(body)

        return str(body)
