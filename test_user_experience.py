"""
User experience test for FlowSphere MCP Server.
This simulates how a user would generate code from configs.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'flowsphere_mcp'))

from generators.python_generator import PythonPytestGenerator
from generators.behave_generator import PythonBehaveGenerator
from generators.javascript_generator import JavaScriptJestGenerator


def main():
    # Sample FlowSphere configuration
    config = {
        "name": "User API Test",
        "description": "Test user registration and login",
        "enableDebug": True,
        "defaults": {
            "baseUrl": "https://jsonplaceholder.typicode.com",
            "timeout": 30,
            "headers": {
                "Content-Type": "application/json"
            },
            "validations": [
                {"httpStatusCode": 200}
            ]
        },
        "variables": {
            "apiVersion": "v1"
        },
        "nodes": [
            {
                "id": "get_users",
                "name": "Get all users",
                "method": "GET",
                "url": "/users",
                "extractFields": [
                    {
                        "jsonPath": "[0].id",
                        "variableName": "firstUserId"
                    }
                ]
            },
            {
                "id": "get_user_details",
                "name": "Get specific user details",
                "method": "GET",
                "url": "/users/{{ .vars.firstUserId }}",
                "validations": [
                    {"httpStatusCode": 200},
                    {"field": "id", "value": "{{ .vars.firstUserId }}"}
                ]
            },
            {
                "id": "create_post",
                "name": "Create a new post",
                "method": "POST",
                "url": "/posts",
                "body": {
                    "title": "Test Post {{ $guid }}",
                    "body": "Created at {{ $timestamp }}",
                    "userId": 1
                },
                "validations": [
                    {"httpStatusCode": 201},
                    {"field": "title", "operator": "contains", "value": "Test Post"}
                ]
            }
        ]
    }

    print("=" * 80)
    print("FlowSphere MCP Server - User Experience Test")
    print("=" * 80)
    print()

    # 1. Generate Python pytest code
    print("1. Generating Python pytest code...")
    print("-" * 80)
    pytest_gen = PythonPytestGenerator()
    pytest_code = pytest_gen.generate(config)

    output_file = Path("generated_user_test.py")
    with open(output_file, 'w') as f:
        f.write(pytest_code)

    print(f"[OK] Generated: {output_file}")
    print(f"   Lines: {len(pytest_code.splitlines())}")
    print(f"   Dependencies: {', '.join(pytest_gen.get_required_dependencies())}")
    print()

    # 2. Generate Python behave/BDD code
    print("2. Generating Python behave/BDD code...")
    print("-" * 80)
    behave_gen = PythonBehaveGenerator()
    behave_files = behave_gen.generate(config)

    feature_file = Path("generated_user_test.feature")
    steps_file = Path("generated_user_test_steps.py")

    with open(feature_file, 'w') as f:
        f.write(behave_files['feature'])
    with open(steps_file, 'w') as f:
        f.write(behave_files['steps'])

    print(f"[OK] Generated: {feature_file}")
    print(f"   Lines: {len(behave_files['feature'].splitlines())}")
    print(f"[OK] Generated: {steps_file}")
    print(f"   Lines: {len(behave_files['steps'].splitlines())}")
    print(f"   Dependencies: {', '.join(behave_gen.get_required_dependencies())}")
    print()

    # 3. Generate JavaScript Jest code
    print("3. Generating JavaScript Jest code...")
    print("-" * 80)
    js_gen = JavaScriptJestGenerator()
    js_code = js_gen.generate(config)

    js_output_file = Path("generated_user_test.test.js")
    with open(js_output_file, 'w') as f:
        f.write(js_code)

    package_json = Path("package.json")
    with open(package_json, 'w') as f:
        f.write(js_gen.get_package_json_template("user-api-tests"))

    print(f"[OK] Generated: {js_output_file}")
    print(f"   Lines: {len(js_code.splitlines())}")
    print(f"[OK] Generated: {package_json}")
    print(f"   Dependencies: {', '.join(js_gen.get_required_dependencies())}")
    print()

    print("=" * 80)
    print("SUCCESS: Code generation complete!")
    print("=" * 80)
    print()
    print("How to run the generated tests:")
    print()
    print("Python pytest:")
    print("  pip install pytest requests jsonpath-ng")
    print("  pytest generated_user_test.py -v")
    print()
    print("Python behave:")
    print("  pip install behave requests jsonpath-ng")
    print("  mkdir -p features/steps")
    print("  mv generated_user_test.feature features/")
    print("  mv generated_user_test_steps.py features/steps/")
    print("  behave")
    print()
    print("JavaScript Jest:")
    print("  npm install")
    print("  npm test")
    print()


if __name__ == "__main__":
    main()
