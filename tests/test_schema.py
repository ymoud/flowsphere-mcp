"""
Tests for FlowSphere schema documentation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'flowsphere_mcp'))

from schema.config_schema import get_schema_documentation
from schema.features import get_feature_documentation, get_feature_checklist


def test_schema_documentation():
    """Test that schema documentation is complete"""
    docs = get_schema_documentation()

    assert "schema" in docs
    assert "variable_substitution" in docs
    assert "edge_cases" in docs

    # Check main schema sections
    schema = docs["schema"]
    assert "properties" in schema
    assert "nodes" in schema["properties"]
    assert "defaults" in schema["properties"]
    assert "variables" in schema["properties"]

    print("[PASS] Schema documentation structure is correct")


def test_feature_documentation():
    """Test that feature documentation is complete"""
    features = get_feature_documentation()

    # Check all major features are documented
    expected_features = [
        "http_execution",
        "variable_substitution",
        "condition_evaluation",
        "validation",
        "user_interaction",
        "state_management",
        "debug_logging"
    ]

    for feature in expected_features:
        assert feature in features, f"Missing feature documentation: {feature}"

    print(f"[PASS] All {len(expected_features)} feature categories documented")


def test_feature_checklist():
    """Test that feature checklist is comprehensive"""
    checklist = get_feature_checklist()

    assert len(checklist) > 0
    assert "HTTP Execution (all methods)" in checklist
    assert "Variable Substitution (dynamic placeholders)" in checklist
    assert "Condition Evaluation (all operators)" in checklist
    assert "Validation (HTTP status code)" in checklist

    print(f"[PASS] Feature checklist contains {len(checklist)} items")


if __name__ == "__main__":
    print("Running schema documentation tests...\n")

    try:
        test_schema_documentation()
        test_feature_documentation()
        test_feature_checklist()

        print("\n" + "=" * 50)
        print("[SUCCESS] All tests passed!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
