from typing import Dict, Any, List
import re
import os
from ..tools.task_tools import (
    add_task, list_tasks, update_task, delete_task, complete_task,
    AddTaskInput, ListTasksInput, UpdateTaskInput, DeleteTaskInput, CompleteTaskInput
)
import openai
from enum import Enum


class TaskOperation(Enum):
    ADD = "add"
    LIST = "list"
    UPDATE = "update"
    DELETE = "delete"
    COMPLETE = "complete"


def parse_user_intent(user_input: str) -> tuple[TaskOperation, dict]:
    """
    Parse the user's input to determine the intent and extract relevant parameters.
    This is a simplified parser that recognizes common patterns without using LangChain.
    """
    user_input_lower = user_input.lower().strip()

    # Add task patterns
    if any(keyword in user_input_lower for keyword in ["add ", "create ", "new task", "make task"]):
        # Extract title and description
        # Look for patterns like "add task 'title' with description 'desc'"
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

        return TaskOperation.ADD, {"title": title, "description": description}

    # List tasks patterns
    elif any(keyword in user_input_lower for keyword in ["list ", "show me", "show my", "what are", "view ", "display "]):
        # Check if user wants completed or active tasks
        completed = None
        if "completed" in user_input_lower or "done" in user_input_lower:
            completed = True
        elif "active" in user_input_lower or "incomplete" in user_input_lower:
            completed = False

        return TaskOperation.LIST, {"completed": completed}

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

            return TaskOperation.UPDATE, {
                "task_id": task_id,
                "title": title,
                "description": description
            }

    # Delete task patterns
    elif any(keyword in user_input_lower for keyword in ["delete ", "remove ", "erase ", "kill "]) and ("task" in user_input_lower or re.search(r"\d+", user_input_lower)):
        task_id_match = re.search(r"(\d+)", user_input)
        if task_id_match:
            task_id = int(task_id_match.group(1))
            return TaskOperation.DELETE, {"task_id": task_id}

    # Complete/incomplete task patterns
    elif any(keyword in user_input_lower for keyword in ["complete ", "finish ", "mark done", "mark complete", "done ", "incomplete ", "undo complete"]):
        task_id_match = re.search(r"(\d+)", user_input)
        if task_id_match:
            task_id = int(task_id_match.group(1))
            completed = not any(keyword in user_input_lower for keyword in ["incomplete", "undo complete"])
            return TaskOperation.COMPLETE, {"task_id": task_id, "completed": completed}

    # Default to list if not sure
    return TaskOperation.LIST, {}


def process_chat_message(user_input: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Process a chat message and convert it to appropriate task operations.

    Args:
        user_input: The user's message
        chat_history: List of previous chat messages (currently not used in this simple implementation)

    Returns:
        Dictionary containing the agent's response and any tool calls made
    """
    try:
        # Determine intent
        operation, params = parse_user_intent(user_input)

        # Track tool calls
        tool_calls = []

        # Execute the appropriate operation
        if operation == TaskOperation.ADD:
            input_data = AddTaskInput(title=params.get("title", ""), description=params.get("description", ""))
            result = add_task(input_data)
            response = result.get("message", f"Task added with ID: {result.get('task_id', 'unknown')}")

            # Log the tool call
            tool_calls.append({
                "id": f"add_task_{result.get('task_id', 'unknown')}",
                "function": {
                    "name": "add_task",
                    "arguments": {"title": input_data.title, "description": input_data.description}
                }
            })

        elif operation == TaskOperation.LIST:
            input_data = ListTasksInput(completed=params.get("completed"))
            result = list_tasks(input_data)
            tasks = result.get("tasks", [])

            if not tasks:
                response = "You don't have any tasks."
            else:
                task_list_str = "\n".join([f"- {task['id']}: {task['title']} ({'completed' if task['completed'] else 'active'})" for task in tasks[:10]])  # Limit to first 10
                response = f"You have {len(tasks)} tasks:\n{task_list_str}"
                if len(tasks) > 10:
                    response += f"\n... and {len(tasks) - 10} more tasks."

            # Log the tool call
            tool_calls.append({
                "id": "list_tasks",
                "function": {
                    "name": "list_tasks",
                    "arguments": {"completed": params.get("completed")}
                }
            })

        elif operation == TaskOperation.UPDATE:
            input_data = UpdateTaskInput(**params)
            result = update_task(input_data)
            response = result.get("message", "Task updated successfully")

            # Log the tool call
            tool_calls.append({
                "id": f"update_task_{params.get('task_id', 'unknown')}",
                "function": {
                    "name": "update_task",
                    "arguments": params
                }
            })

        elif operation == TaskOperation.DELETE:
            input_data = DeleteTaskInput(task_id=params.get("task_id"))
            result = delete_task(input_data)
            response = result.get("message", "Task deleted successfully")

            # Log the tool call
            tool_calls.append({
                "id": f"delete_task_{params.get('task_id', 'unknown')}",
                "function": {
                    "name": "delete_task",
                    "arguments": {"task_id": params.get("task_id")}
                }
            })

        elif operation == TaskOperation.COMPLETE:
            input_data = CompleteTaskInput(**params)
            result = complete_task(input_data)
            response = result.get("message", "Task status updated successfully")

            # Log the tool call
            tool_calls.append({
                "id": f"complete_task_{params.get('task_id', 'unknown')}",
                "function": {
                    "name": "complete_task",
                    "arguments": params
                }
            })

        else:
            response = "I didn't understand that command. You can ask me to add, list, update, delete, or complete tasks."

        return {
            "response": response,
            "success": True,
            "tool_calls": tool_calls
        }
    except Exception as e:
        return {
            "response": f"I encountered an error processing your request: {str(e)}",
            "success": False,
            "tool_calls": []
        }