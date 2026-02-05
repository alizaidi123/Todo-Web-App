"""
Final integration test for the AI Chatbot functionality.
"""
import os
import sys
sys.path.append('backend')

# Set the required environment variable for JWT
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-for-testing'

def test_integration():
    print("Testing AI Chatbot Integration...")

    # Test 1: Check that the main app can be created with chat routes
    from app.main import create_app
    app = create_app()
    print("[OK] Main app created successfully with chat routes")

    # Test 2: Check that all required modules can be imported without errors
    from app.routes.chat import router as chat_router
    from app.agents.task_agent import process_chat_message
    from app.tools.task_tools import add_task, list_tasks, update_task, delete_task, complete_task
    print("[OK] All modules imported successfully")

    # Test 3: Test the NLP parsing functionality
    from app.agents.task_agent import parse_user_intent, TaskOperation

    # Test adding a task
    op, params = parse_user_intent("Add a task to buy groceries")
    assert op == TaskOperation.ADD
    assert "buy groceries" in params.get("title", "").lower()
    print("[OK] NLP parsing works for adding tasks")

    # Test listing tasks
    op, params = parse_user_intent("Show me my tasks")
    assert op == TaskOperation.LIST
    print("[OK] NLP parsing works for listing tasks")

    # Test completing a task
    op, params = parse_user_intent("Complete task 1")
    assert op == TaskOperation.COMPLETE
    assert params.get("task_id") == 1
    print("[OK] NLP parsing works for completing tasks")

    # Test 4: Test the message processing function
    result = process_chat_message("Add a task to test the chatbot")
    assert "response" in result
    assert "success" in result
    print("[OK] Message processing works")

    # Test 5: Check that the routes are registered
    route_paths = [route.path for route in app.routes]
    chat_routes = [path for path in route_paths if '/chat' in path]
    assert len(chat_routes) >= 2  # Should have at least /chat/message and /chat/health
    print(f"[OK] Chat routes properly registered: {chat_routes}")

    print("\n*** All integration tests passed! ***")
    print("AI Chatbot is successfully integrated with the Todo application!")

if __name__ == "__main__":
    test_integration()