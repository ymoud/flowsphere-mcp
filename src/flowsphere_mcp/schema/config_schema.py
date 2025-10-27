"""
FlowSphere Configuration Schema Documentation

This module provides comprehensive documentation of the FlowSphere config structure,
including all properties, their types, behaviors, and edge cases.
"""

FLOWSPHERE_CONFIG_SCHEMA = {
    "description": "FlowSphere configuration file for HTTP sequence execution",
    "type": "object",
    "properties": {
        "enableDebug": {
            "type": "boolean",
            "default": False,
            "description": "Enable detailed debug logging for troubleshooting"
        },
        "variables": {
            "type": "object",
            "description": "Global variables accessible in all steps via {{ .vars.key }} syntax",
            "examples": {
                "apiKey": "your-api-key-123",
                "userId": "12345",
                "baseEnvironment": "production"
            }
        },
        "defaults": {
            "type": "object",
            "description": "Default settings applied to all nodes (can be overridden per node)",
            "properties": {
                "baseUrl": {
                    "type": "string",
                    "description": "Base URL prepended to relative node URLs",
                    "example": "https://api.example.com"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Request timeout in seconds (uses curl's --max-time)",
                    "default": 30,
                    "example": 30
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP headers merged with node headers (unless skipDefaultHeaders is true)",
                    "example": {
                        "Content-Type": "application/json",
                        "User-Agent": "FlowSphere/1.0"
                    }
                },
                "validations": {
                    "type": "array",
                    "description": "Default validations concatenated with node validations (unless skipDefaultValidations is true)",
                    "example": [
                        {"httpStatusCode": 200}
                    ]
                }
            }
        },
        "nodes": {
            "type": "array",
            "description": "Array of HTTP request steps to execute sequentially",
            "required": True,
            "items": {
                "type": "object",
                "required_fields": ["id", "name", "method", "url"],
                "properties": {
                    "id": {
                        "type": "string",
                        "required": True,
                        "pattern": "^[a-zA-Z0-9_-]+$",
                        "description": "Unique identifier for this node (used in response references)",
                        "example": "authenticate"
                    },
                    "name": {
                        "type": "string",
                        "required": True,
                        "description": "Human-readable description of what this step does",
                        "example": "Authenticate user"
                    },
                    "method": {
                        "type": "string",
                        "required": True,
                        "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                        "description": "HTTP method for the request"
                    },
                    "url": {
                        "type": "string",
                        "required": True,
                        "description": "Full URL or relative path (prepended with baseUrl if relative)",
                        "examples": [
                            "/api/users",
                            "https://api.example.com/auth/login"
                        ]
                    },
                    "headers": {
                        "type": "object",
                        "description": "HTTP headers (merged with defaults unless skipDefaultHeaders is true)",
                        "example": {
                            "Authorization": "Bearer {{ .responses.login.token }}"
                        }
                    },
                    "skipDefaultHeaders": {
                        "type": "boolean",
                        "default": False,
                        "description": "If true, only use node headers (ignore default headers)"
                    },
                    "body": {
                        "type": "object",
                        "description": "Request body (JSON or form-urlencoded based on bodyFormat)",
                        "example": {
                            "username": "user",
                            "password": "{{ .input.password }}"
                        }
                    },
                    "bodyFormat": {
                        "type": "string",
                        "enum": ["json", "form-urlencoded"],
                        "default": "json",
                        "description": "Format for request body encoding"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Request timeout in seconds (overrides default timeout)",
                        "example": 10
                    },
                    "userPrompts": {
                        "type": "object",
                        "description": "Interactive prompts to collect user input before execution",
                        "example": {
                            "username": "Enter your username:",
                            "password": "Enter your password:"
                        }
                    },
                    "conditions": {
                        "type": "array",
                        "description": "Array of conditions (all must be true for step to execute - AND logic)",
                        "items": {
                            "type": "object",
                            "description": "Single condition to evaluate",
                            "properties": {
                                "node": {
                                    "type": "string",
                                    "description": "Node ID to check (for step-based conditions)",
                                    "example": "authenticate"
                                },
                                "field": {
                                    "type": "string",
                                    "description": "JSONPath to field in response (starts with .)",
                                    "example": ".token"
                                },
                                "statusCode": {
                                    "type": "integer",
                                    "description": "HTTP status code to check (step source only)",
                                    "example": 200
                                },
                                "equals": {
                                    "type": ["string", "number", "boolean"],
                                    "description": "Value must equal this (supports variable substitution)",
                                    "example": "success"
                                },
                                "notEquals": {
                                    "type": ["string", "number", "boolean"],
                                    "description": "Value must not equal this (supports variable substitution)",
                                    "example": "error"
                                },
                                "exists": {
                                    "type": "boolean",
                                    "description": "Field must exist (true) or not exist (false)",
                                    "example": True
                                },
                                "greaterThan": {
                                    "type": "number",
                                    "description": "Numeric value must be greater than this",
                                    "example": 0
                                },
                                "lessThan": {
                                    "type": "number",
                                    "description": "Numeric value must be less than this",
                                    "example": 100
                                },
                                "greaterThanOrEqual": {
                                    "type": "number",
                                    "description": "Numeric value must be >= this",
                                    "example": 18
                                },
                                "lessThanOrEqual": {
                                    "type": "number",
                                    "description": "Numeric value must be <= this",
                                    "example": 120
                                }
                            }
                        }
                    },
                    "validations": {
                        "type": "array",
                        "description": "Validation rules (concatenated with defaults unless skipDefaultValidations is true)",
                        "items": {
                            "type": "object",
                            "description": "Single validation rule",
                            "properties": {
                                "httpStatusCode": {
                                    "type": "integer",
                                    "description": "Expected HTTP status code",
                                    "example": 200
                                },
                                "jsonpath": {
                                    "type": "string",
                                    "description": "JSONPath to field in response (starts with .)",
                                    "example": ".data.id"
                                },
                                "exists": {
                                    "type": "boolean",
                                    "description": "Field must exist (true) or not exist (false)",
                                    "example": True
                                },
                                "equals": {
                                    "type": ["string", "number", "boolean"],
                                    "description": "Field value must equal this",
                                    "example": "success"
                                },
                                "notEquals": {
                                    "type": ["string", "number", "boolean"],
                                    "description": "Field value must not equal this",
                                    "example": "error"
                                },
                                "greaterThan": {
                                    "type": "number",
                                    "description": "Numeric field value must be > this",
                                    "example": 0
                                },
                                "lessThan": {
                                    "type": "number",
                                    "description": "Numeric field value must be < this",
                                    "example": 1000
                                },
                                "greaterThanOrEqual": {
                                    "type": "number",
                                    "description": "Numeric field value must be >= this",
                                    "example": 18
                                },
                                "lessThanOrEqual": {
                                    "type": "number",
                                    "description": "Numeric field value must be <= this",
                                    "example": 120
                                }
                            }
                        }
                    },
                    "skipDefaultValidations": {
                        "type": "boolean",
                        "default": False,
                        "description": "If true, only use node validations (ignore default validations)"
                    },
                    "launchBrowser": {
                        "type": "string",
                        "description": "JSONPath to URL in response to open in browser after success",
                        "example": ".authorizationUrl"
                    }
                }
            }
        }
    }
}


# Variable Substitution Syntax Documentation
VARIABLE_SUBSTITUTION = {
    "dynamic_placeholders": {
        "description": "Dynamic values generated at runtime",
        "syntax": [
            {
                "pattern": "{{ $guid }}",
                "description": "Generates a unique UUID v4 for each occurrence",
                "example": "{{ $guid }}",
                "output_example": "550e8400-e29b-41d4-a716-446655440000"
            },
            {
                "pattern": "{{ $timestamp }}",
                "description": "Current Unix timestamp in seconds (same value for all occurrences in one step)",
                "example": "{{ $timestamp }}",
                "output_example": "1704067200"
            }
        ]
    },
    "global_variables": {
        "description": "References to config-level variables section",
        "syntax": "{{ .vars.key }}",
        "example": "{{ .vars.apiKey }}",
        "usage": [
            "In URLs: /api/users/{{ .vars.userId }}",
            "In headers: { \"X-API-Key\": \"{{ .vars.apiKey }}\" }",
            "In body: { \"key\": \"{{ .vars.secretKey }}\" }"
        ]
    },
    "response_references": {
        "description": "References to fields from previous node responses",
        "syntax": "{{ .responses.nodeId.field.subfield }}",
        "examples": [
            "{{ .responses.authenticate.token }}",
            "{{ .responses.getUser.data.id }}",
            "{{ .responses.createOrder.order.items[0].id }}"
        ],
        "usage": [
            "In URLs: /api/users/{{ .responses.getUser.id }}",
            "In headers: { \"Authorization\": \"Bearer {{ .responses.login.token }}\" }",
            "In body: { \"userId\": \"{{ .responses.authenticate.userId }}\" }"
        ]
    },
    "user_input": {
        "description": "References to values collected from userPrompts in the same node",
        "syntax": "{{ .input.variableName }}",
        "example": "{{ .input.username }}",
        "usage": [
            "In body: { \"user\": \"{{ .input.username }}\", \"pass\": \"{{ .input.password }}\" }",
            "In headers: { \"X-User-Token\": \"{{ .input.token }}\" }"
        ]
    },
    "substitution_order": {
        "description": "Order in which variable substitution occurs",
        "order": [
            "1. Dynamic placeholders ({{ $guid }}, {{ $timestamp }})",
            "2. Global variables ({{ .vars.* }})",
            "3. User input ({{ .input.* }})",
            "4. Response references ({{ .responses.* }})"
        ]
    }
}


# Edge Cases and Special Behaviors
EDGE_CASES = {
    "defaults_merging": {
        "headers": {
            "merge_behavior": "Node headers are merged with default headers. Node headers override conflicting keys.",
            "skip_behavior": "If skipDefaultHeaders is true, only node headers are used (defaults ignored).",
            "no_headers": "If skipDefaultHeaders is true and no node headers defined, no headers are sent."
        },
        "validations": {
            "concatenate_behavior": "Node validations are concatenated with default validations.",
            "skip_behavior": "If skipDefaultValidations is true, only node validations are used (defaults ignored).",
            "no_validations": "If skipDefaultValidations is true and no node validations defined, no validations are performed."
        }
    },
    "conditional_execution": {
        "and_logic": "All conditions in the conditions array must be true for the node to execute.",
        "skip_behavior": "If any condition fails, the node is skipped but array indexing is maintained.",
        "variable_substitution": "All condition values support variable substitution ({{ .vars }}, {{ .input }}, {{ .responses }}, {{ $timestamp }}, {{ $guid }})"
    },
    "validation_behavior": {
        "fail_fast": "Execution stops immediately on validation failure.",
        "default_status": "If no httpStatusCode validation is defined, defaults to expecting 200.",
        "numeric_comparisons": "Support both integers and floats for greaterThan/lessThan/etc operators."
    },
    "response_storage": {
        "by_id": "Responses are stored by node ID, not by array index.",
        "skipped_nodes": "Skipped nodes maintain array position but have no response data.",
        "reference_resolution": "Response references use node ID: {{ .responses.nodeId.field }}"
    }
}


def get_schema_documentation() -> dict:
    """
    Returns complete FlowSphere config schema documentation.

    Returns:
        dict: Complete schema with descriptions, types, examples, and edge cases
    """
    return {
        "schema": FLOWSPHERE_CONFIG_SCHEMA,
        "variable_substitution": VARIABLE_SUBSTITUTION,
        "edge_cases": EDGE_CASES
    }
