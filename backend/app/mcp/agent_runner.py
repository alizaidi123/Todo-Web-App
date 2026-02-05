"""
Agent Runner for MCP Tools Integration.

This module implements an agent runner that can call MCP tools based on
natural language input, load history, run agent, store responses, and return results.
"""
import json
from typing import List, Dict, Any, Optional
from .tools import MCP_TOOLS
import re


class AgentRunner:
    """
    Agent runner that processes natural language and executes MCP tools.
    """

    def __init__(self):
        self.tools = MCP_TOOLS

    def parse_user_intent(self, user_input: str) -> tuple[Optional[str], Dict[str, Any]]:
        """
        Parse the user's input to determine which tool to call and with what parameters.
        This is a simple NLP parser for demonstration purposes.
        """
        user_input_lower = user_input.lower().strip()

        # Add task patterns
        if any(keyword in user_input_lower for keyword in ["add ", "create ", "new task", "make task"]):
            # Extract title and description
            title_match = re.search(r"(?:add|create|new)\s+(?:task|to-do|todo)?\s*[\"']([^\"']+)[\"']|(?:add|create|new)\s+(?:task|to-do|todo)?\s+(.+?)(?:\.|$)", user_input_lower)

            title = ""
            description = ""

            if title_match:
                title = title_match.group(1) or title_match.group(2) or ""
                # Remove the title from the original input to find description
                temp_input = user_input.replace(title_match.group(0), "", 1).lower()

                # Look for description patterns
                desc_match = re.search(r"(?:with\s+description|description:?)\s*[\"']([^\"']+)[\"']|(?:and\s+)?(.+)$", temp_input)
                if desc_match and desc_match.group(1):
                    description = desc_match.group(1)
                elif desc_match and desc_match.group(2):
                    description = desc_match.group(2).strip()

            # Clean up title if it's too generic
            title = title.strip("'\".,!? ").strip()
            if not title:
                # Try to extract title from the rest of the sentence
                parts = user_input.split(" ", 2)
                if len(parts) > 2:
                    title = " ".join(parts[2:])
                else:
                    title = "New Task"

            # Default user_id - in real implementation this would come from context
            return "add_task", {"title": title, "description": description, "user_id": 1}

        # List tasks patterns
        elif any(keyword in user_input_lower for keyword in ["list ", "show me", "show my", "what are", "view ", "display "]):
            # Check if user wants completed or active tasks
            completed = None
            if "completed" in user_input_lower or "done" in user_input_lower:
                completed = True
            elif "active" in user_input_lower or "incomplete" in user_input_lower:
                completed = False

            return "list_tasks", {"user_id": 1, "completed": completed}

        # Update task patterns
        elif any(keyword in user_input_lower for keyword in ["update ", "change ", "modify ", "edit "]) and ("task" in user_input_lower or re.search(r"\d+", user_input_lower)):
            # Extract task ID and what to update
            task_id_match = re.search(r"(\d+)", user_input)
            if task_id_match:
                task_id = int(task_id_match.group(1))

                # Look for title update
                title_match = re.search(r"(?:title|name):\s*[\"']([^\"']+)[\"']|(?:to|as)\s+[\"']([^\"']+)[\"']", user_input)
                title = title_match.group(1) if title_match and title_match.group(1) else (title_match.group(2) if title_match else None)

                # Look for description update
                desc_match = re.search(r"description:\s*[\"']([^\"']+)[\"']|described as\s+[\"']([^\"']+)[\"']", user_input)
                description = desc_match.group(1) if desc_match and desc_match.group(1) else (desc_match.group(2) if desc_match else None)

                return "update_task", {
                    "task_id": task_id,
                    "user_id": 1,
                    "title": title,
                    "description": description
                }

        # Delete task patterns
        elif any(keyword in user_input_lower for keyword in ["delete ", "remove ", "erase ", "kill "]) and ("task" in user_input_lower or re.search(r"\d+", user_input_lower)):
            task_id_match = re.search(r"(\d+)", user_input)
            if task_id_match:
                task_id = int(task_id_match.group(1))
                return "delete_task", {"task_id": task_id, "user_id": 1}

        # Complete/incomplete task patterns
        elif any(keyword in user_input_lower for keyword in ["complete ", "finish ", "mark done", "mark complete", "done ", "incomplete ", "undo complete"]):
            task_id_match = re.search(r"(\d+)", user_input)
            if task_id_match:
                task_id = int(task_id_match.group(1))
                completed = not any(keyword in user_input_lower for keyword in ["incomplete", "undo complete"])
                return "complete_task", {"task_id": task_id, "user_id": 1, "completed": completed}

        # Default to list if not sure
        return "list_tasks", {"user_id": 1}

    def run_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool with given parameters.
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }

        tool_func = self.tools[tool_name]["function"]

        try:
            # Validate parameters exist
            result = tool_func(params)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing tool {tool_name}: {str(e)}"
            }

    def run_agent(self, user_input: str, user_id: int, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent to process user input, execute tools, and return response.

        Args:
            user_input: Natural language input from user
            user_id: ID of the user making the request
            chat_history: Previous conversation history

        Returns:
            Dictionary containing response, success status, and tool calls
        """
        if chat_history is None:
            chat_history = []

        try:
            # Parse user intent to determine which tool to call
            tool_name, params = self.parse_user_intent(user_input)

            # Override user_id from context
            params["user_id"] = user_id

            # Execute the tool
            tool_result = self.run_tool(tool_name, params)

            # Format the response based on tool result
            if tool_result["success"]:
                if tool_name == "list_tasks":
                    tasks = tool_result.get("tasks", [])
                    if not tasks:
                        response = "You don't have any tasks."
                    else:
                        task_list_str = "\n".join([f"- {task['id']}: {task['title']} ({'completed' if task['completed'] else 'active'})" for task in tasks[:10]])  # Limit to first 10
                        response = f"You have {len(tasks)} tasks:\n{task_list_str}"
                        if len(tasks) > 10:
                            response += f"\n... and {len(tasks) - 10} more tasks."
                elif tool_name in ["add_task", "update_task", "delete_task", "complete_task"]:
                    response = tool_result.get("message", f"Operation completed successfully")
                else:
                    response = "Operation completed successfully"
            else:
                response = f"Error: {tool_result.get('error', 'Unknown error occurred')}"

            # Create tool call record for traceability
            tool_call = {
                "id": f"{tool_name}_{hash(str(params)) % 10000}",  # Simple ID generation
                "function": {
                    "name": tool_name,
                    "arguments": params
                }
            }

            return {
                "response": response,
                "success": tool_result["success"],
                "tool_calls": [tool_call],
                "tool_results": [tool_result]
            }
        except Exception as e:
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "success": False,
                "tool_calls": [],
                "tool_results": []
            }


# Global agent instance for use in endpoints
agent_runner = AgentRunner()


def run_agent_for_user(user_input: str, user_id: int, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Convenience function to run the agent for a specific user.
    """
    return agent_runner.run_agent(user_input, user_id, chat_history)