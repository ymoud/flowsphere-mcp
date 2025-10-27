"""
FlowSphere Feature Descriptions

Detailed documentation of all FlowSphere features and how they should be
implemented in generated code.
"""

FEATURES = {
    "http_execution": {
        "description": "Execute HTTP requests with full control over method, headers, body, and timeout",
        "implementation_notes": [
            "Support all HTTP methods: GET, POST, PUT, DELETE, PATCH",
            "Handle relative URLs by prepending baseUrl",
            "Merge node headers with default headers (unless skipDefaultHeaders is true)",
            "Support JSON and form-urlencoded body formats",
            "Apply timeout per request (node timeout overrides default)",
            "Handle timeout errors with clear error messages"
        ],
        "example": {
            "config": {
                "method": "POST",
                "url": "/api/users",
                "headers": {"Authorization": "Bearer token"},
                "body": {"name": "John"},
                "timeout": 30
            }
        }
    },

    "variable_substitution": {
        "description": "Replace {{ }} placeholders with actual values at runtime",
        "types": [
            {
                "name": "Dynamic Placeholders",
                "patterns": ["{{ $guid }}", "{{ $timestamp }}"],
                "behavior": "Generated fresh for each occurrence (except timestamp which is same per step)",
                "implementation": "Use UUID library for $guid, time library for $timestamp"
            },
            {
                "name": "Global Variables",
                "pattern": "{{ .vars.key }}",
                "behavior": "Replaced with value from config variables section",
                "implementation": "Simple string replacement from variables dict"
            },
            {
                "name": "Response References",
                "pattern": "{{ .responses.nodeId.field.subfield }}",
                "behavior": "Extract nested field from previous node response",
                "implementation": "Use JSONPath or dot-notation field extraction from stored responses"
            },
            {
                "name": "User Input",
                "pattern": "{{ .input.variableName }}",
                "behavior": "Replaced with value collected from userPrompts",
                "implementation": "String replacement from user input dict for current node"
            }
        ],
        "substitution_order": [
            "1. Dynamic placeholders",
            "2. Global variables",
            "3. User input",
            "4. Response references"
        ],
        "applies_to": ["URLs", "headers", "body", "condition values"]
    },

    "condition_evaluation": {
        "description": "Conditionally execute nodes based on previous responses or variables",
        "operators": [
            {"name": "statusCode", "description": "Check HTTP status of previous response", "types": ["integer"]},
            {"name": "equals", "description": "Check for equality", "types": ["string", "number", "boolean"]},
            {"name": "notEquals", "description": "Check for inequality", "types": ["string", "number", "boolean"]},
            {"name": "exists", "description": "Check if field exists", "types": ["boolean"]},
            {"name": "greaterThan", "description": "Numeric comparison >", "types": ["number"]},
            {"name": "lessThan", "description": "Numeric comparison <", "types": ["number"]},
            {"name": "greaterThanOrEqual", "description": "Numeric comparison >=", "types": ["number"]},
            {"name": "lessThanOrEqual", "description": "Numeric comparison <=", "types": ["number"]}
        ],
        "logic": "AND - all conditions must be true",
        "sources": ["node (by node ID)", "variable", "input"],
        "variable_substitution": "All condition values support variable substitution",
        "skip_behavior": "Failed conditions cause node to be skipped (not fail)",
        "implementation_notes": [
            "Evaluate all conditions before executing node",
            "Return false immediately if any condition fails (short-circuit)",
            "Support variable substitution in condition values",
            "Handle numeric comparisons with float/int conversion",
            "Maintain response array indexing even for skipped nodes"
        ]
    },

    "validation": {
        "description": "Validate HTTP responses to ensure correct behavior",
        "types": [
            {
                "name": "HTTP Status Code",
                "field": "httpStatusCode",
                "description": "Validate response status code",
                "default": 200,
                "example": {"httpStatusCode": 201}
            },
            {
                "name": "JSONPath Validation",
                "field": "jsonpath",
                "description": "Validate fields in response body",
                "operators": ["exists", "equals", "notEquals", "greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual"],
                "example": {"jsonpath": ".token", "exists": True}
            }
        ],
        "merge_behavior": {
            "default": "Node validations are concatenated with default validations",
            "skip": "If skipDefaultValidations is true, only node validations are used"
        },
        "fail_behavior": "Execution stops immediately on validation failure",
        "implementation_notes": [
            "Run all validations after response is received",
            "Stop immediately on first validation failure",
            "Support all validation operators",
            "Handle nested JSONPath extraction",
            "Provide clear error messages with expected vs actual values"
        ]
    },

    "user_interaction": {
        "description": "Collect user input and launch browser for interactive flows",
        "user_prompts": {
            "description": "Interactively collect values before node execution",
            "format": {"variableName": "Prompt message"},
            "access": "Use {{ .input.variableName }} to reference collected values",
            "scope": "Input is reset for each node with userPrompts",
            "implementation": "Collect all prompts before executing node"
        },
        "browser_launch": {
            "description": "Automatically open URLs in default browser",
            "field": "launchBrowser",
            "value": "JSONPath to URL in response",
            "behavior": "Launch browser after successful node execution",
            "platforms": ["Windows (start)", "macOS (open)", "Linux (xdg-open)"],
            "implementation": "Use platform-specific browser launcher (webbrowser module in Python)"
        }
    },

    "state_management": {
        "description": "Maintain state across node executions",
        "components": [
            {
                "name": "Response Storage",
                "description": "Store all responses by node ID",
                "structure": "Dict with node ID as key, response data as value",
                "includes": "Response body + _status_code field"
            },
            {
                "name": "User Input Storage",
                "description": "Store user input for current node",
                "scope": "Reset for each node with userPrompts",
                "structure": "Dict with variable name as key, input value as value"
            },
            {
                "name": "Defaults Merging",
                "description": "Merge node config with defaults",
                "rules": [
                    "Headers: merge unless skipDefaultHeaders is true",
                    "Validations: concatenate unless skipDefaultValidations is true",
                    "Timeout: node value overrides default",
                    "BaseUrl: prepend to relative URLs"
                ]
            }
        ]
    },

    "debug_logging": {
        "description": "Optional detailed logging for troubleshooting",
        "enabled_by": "enableDebug: true in config",
        "includes": [
            "Variable substitution details",
            "Condition evaluation results",
            "Request details (URL, headers, body)",
            "Response details (status, body)",
            "Validation results"
        ],
        "destination": "stderr (to keep stdout clean)"
    }
}


def get_feature_documentation() -> dict:
    """
    Returns complete FlowSphere feature documentation.

    Returns:
        dict: Detailed feature descriptions and implementation notes
    """
    return FEATURES


def get_feature_checklist() -> list:
    """
    Returns a checklist of all features that must be implemented in generated code.

    Returns:
        list: Feature names that generated code must support
    """
    return [
        "HTTP Execution (all methods)",
        "Variable Substitution (dynamic placeholders)",
        "Variable Substitution (global variables)",
        "Variable Substitution (response references)",
        "Variable Substitution (user input)",
        "Condition Evaluation (all operators)",
        "Condition Evaluation (AND logic)",
        "Condition Evaluation (variable substitution in conditions)",
        "Validation (HTTP status code)",
        "Validation (JSONPath with all operators)",
        "Validation (defaults merging/skipping)",
        "User Prompts",
        "Browser Launch",
        "Response Storage",
        "Defaults Merging (headers)",
        "Defaults Merging (validations)",
        "Defaults Merging (skip flags)",
        "Debug Logging"
    ]
