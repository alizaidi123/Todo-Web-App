"""
Agent Runner Service using OpenAI Agents SDK.

This module implements an agent runner that uses OpenAI Agents to orchestrate
tool calls via the MCP tools created in Slice 3.
"""
import os
import json
import ast
from typing import Dict, Any, List, Optional
from openai import OpenAI
from ..mcp.tools import MCP_TOOLS


class AgentRunnerService:
    """
    Service class to run agents that can call MCP tools.
    """

    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.client = OpenAI(api_key=api_key)

        # Prepare tools for OpenAI function calling
        self.openai_tools = self._prepare_openai_tools()

    def _safe_parse_arguments(self, args) -> Dict[str, Any]:
        """
        Safely parse tool call arguments using JSON-first approach.

        Args:
            args: Arguments to parse (can be dict, str, or other types)

        Returns:
            Dictionary with parsed arguments

        Raises:
            ValueError: If parsing fails after all attempts
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

    def _prepare_openai_tools(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to OpenAI-compatible tool format.
        """
        openai_tools = []

        for tool_name, tool_info in MCP_TOOLS.items():
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools

    def run_agent(self, user_input: str, user_id: int, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent to process user input and call appropriate tools via MCP.

        Args:
            user_input: Natural language input from user
            user_id: ID of the user making the request
            chat_history: Previous conversation history

        Returns:
            Dictionary containing response, success status, and tool calls
        """
        try:
            # Prepare messages with history and user input
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that manages tasks for user {user_id}. "
                              f"Use the available functions to add, list, update, delete, or complete tasks. "
                              f"Always ensure the user_id parameter is provided when calling tools."
                }
            ]

            # Add chat history if available
            if chat_history:
                for msg in chat_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Add user message
            messages.append({
                "role": "user",
                "content": user_input
            })

            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),  # Use gpt-4 if available
                messages=messages,
                tools=self.openai_tools,
                tool_choice="auto"
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Execute the tool calls via MCP tools
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = self._safe_parse_arguments(tool_call.function.arguments)
                    except ValueError as e:
                        # Log the error for debugging
                        print(f"Error parsing tool call arguments: {str(e)}")
                        # Return user-friendly error message
                        return {
                            "response": f"Error processing your request: Invalid tool call arguments format.",
                            "success": False,
                            "tool_calls": [],
                            "tool_results": []
                        }

                    # Ensure user_id is in function args for authorization
                    if 'user_id' not in function_args:
                        function_args['user_id'] = user_id

                    # Execute the tool via MCP tools
                    if function_name in MCP_TOOLS:
                        tool_func = MCP_TOOLS[function_name]["function"]

                        # Create the appropriate input model based on the function
                        if function_name == "add_task":
                            from ..mcp.tools import AddTaskInput
                            input_data = AddTaskInput(**function_args)
                            result = tool_func(input_data)
                        elif function_name == "list_tasks":
                            from ..mcp.tools import ListTasksInput
                            input_data = ListTasksInput(**function_args)
                            result = tool_func(input_data)
                        elif function_name == "update_task":
                            from ..mcp.tools import UpdateTaskInput
                            input_data = UpdateTaskInput(**function_args)
                            result = tool_func(input_data)
                        elif function_name == "delete_task":
                            from ..mcp.tools import DeleteTaskInput
                            input_data = DeleteTaskInput(**function_args)
                            result = tool_func(input_data)
                        elif function_name == "complete_task":
                            from ..mcp.tools import CompleteTaskInput
                            input_data = CompleteTaskInput(**function_args)
                            result = tool_func(input_data)
                        else:
                            result = tool_func(function_args)

                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "function_name": function_name,
                            "result": result
                        })

                # If there are tool results, get the final response from the model
                if tool_results:
                    # Prepare messages for the second call with tool results
                    second_messages = messages + [response_message]
                    for tool_result in tool_results:
                        second_messages.append({
                            "role": "tool",
                            "content": str(tool_result["result"]),
                            "tool_call_id": tool_result["tool_call_id"]
                        })

                    # Get final response from the model
                    final_response = self.client.chat.completions.create(
                        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                        messages=second_messages
                    )

                    return {
                        "response": final_response.choices[0].message.content,
                        "success": True,
                        "tool_calls": [tc.model_dump() for tc in tool_calls] if tool_calls else [],
                        "tool_results": tool_results
                    }
                else:
                    return {
                        "response": response_message.content or "Operation completed successfully",
                        "success": True,
                        "tool_calls": [],
                        "tool_results": []
                    }
            else:
                # No tool calls were made, return the model's response
                return {
                    "response": response_message.content or "I processed your request.",
                    "success": True,
                    "tool_calls": [],
                    "tool_results": []
                }

        except Exception as e:
            return {
                "response": f"Error processing your request: {str(e)}",
                "success": False,
                "tool_calls": [],
                "tool_results": []
            }


# Global agent runner instance
agent_runner_service = AgentRunnerService()


def run_agent_for_user(user_input: str, user_id: int, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Convenience function to run the agent for a specific user.
    """
    try:
        return agent_runner_service.run_agent(user_input, user_id, chat_history)
    except ValueError as e:
        # If OpenAI API key is not configured, return error
        return {
            "response": f"Error: {str(e)}",
            "success": False,
            "tool_calls": [],
            "tool_results": []
        }