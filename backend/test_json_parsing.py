#!/usr/bin/env python3
"""
Test script to verify the JSON parsing fix works correctly
"""

import json
import ast
from typing import Dict, Any


def _safe_parse_arguments(args) -> Dict[str, Any]:
    """
    Safely parse tool call arguments using JSON-first approach.
    This is a standalone copy of the function in agent_runner.py for testing.
    """
    # If args is already a dictionary, return it directly
    if isinstance(args, dict):
        return args

    # If args is a string, try to parse as JSON first
    if isinstance(args, str):
        try:
            # Try to parse as JSON
            return json.loads(args)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to normalize JSON literals and use ast.literal_eval as fallback
            try:
                # Normalize JSON booleans and null values to Python equivalents
                normalized_args = args.replace('true', 'True').replace('false', 'False').replace('null', 'None')
                return ast.literal_eval(normalized_args)
            except (ValueError, SyntaxError) as e:
                # If all parsing attempts fail, return a helpful error
                raise ValueError(f"Unable to parse tool call arguments: {str(e)}. Arguments must be valid JSON or Python dictionary format.")

    # If args is neither dict nor str, return as-is (may be other valid type)
    return args


def test_json_parsing():
    """Test various JSON parsing scenarios"""

    print("Testing JSON parsing fix...")

    # Test case 1: parse_tool_args('{"completed": true}') returns {"completed": True}
    test1 = '{"completed": true}'
    result1 = _safe_parse_arguments(test1)
    expected1 = {"completed": True}
    print(f"Test 1 - Input: {test1}")
    print(f"Result: {result1}")
    print(f"Expected: {expected1}")
    print(f"Pass: {result1 == expected1}\n")

    # Test case 2: parse_tool_args('{"completed": false}') returns {"completed": False}
    test2 = '{"completed": false}'
    result2 = _safe_parse_arguments(test2)
    expected2 = {"completed": False}
    print(f"Test 2 - Input: {test2}")
    print(f"Result: {result2}")
    print(f"Expected: {expected2}")
    print(f"Pass: {result2 == expected2}\n")

    # Test case 3: Mixed data types
    test3 = '{"id": 1, "title": "Test Task", "completed": true, "description": null}'
    result3 = _safe_parse_arguments(test3)
    expected3 = {"id": 1, "title": "Test Task", "completed": True, "description": None}
    print(f"Test 3 - Input: {test3}")
    print(f"Result: {result3}")
    print(f"Expected: {expected3}")
    print(f"Pass: {result3 == expected3}\n")

    # Test case 4: Already a dict (should pass through)
    test4 = {"id": 1, "completed": True}
    result4 = _safe_parse_arguments(test4)
    expected4 = {"id": 1, "completed": True}
    print(f"Test 4 - Input: {test4}")
    print(f"Result: {result4}")
    print(f"Expected: {expected4}")
    print(f"Pass: {result4 == expected4}\n")

    # Test case 5: String that looks like Python dict but isn't JSON
    test5 = "{'id': 1, 'completed': true}"  # Python-style dict string
    try:
        result5 = _safe_parse_arguments(test5)
        expected5 = {"id": 1, "completed": True}
        print(f"Test 5 - Input: {test5}")
        print(f"Result: {result5}")
        print(f"Expected: {expected5}")
        print(f"Pass: {result5 == expected5}\n")
    except Exception as e:
        print(f"Test 5 - Input: {test5}")
        print(f"Error: {e}\n")


if __name__ == "__main__":
    test_json_parsing()
    print("JSON parsing tests completed!")