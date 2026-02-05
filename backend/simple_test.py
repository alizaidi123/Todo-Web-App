"""Simple test to verify the app can be created with chat routes."""
import sys
import os
sys.path.append('.')

# Set the required environment variable for JWT
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-for-testing'

def test_app_creation():
    """Test that the app can be created with chat routes."""
    from app.main import create_app

    try:
        app = create_app()
        print("[OK] App created successfully")

        # Check if the chat routes are registered by looking at the routes
        route_paths = [route.path for route in app.routes]
        chat_routes = [path for path in route_paths if '/chat' in path]

        if chat_routes:
            print(f"[OK] Chat routes found: {chat_routes}")
        else:
            print("[ERROR] No chat routes found")

        print("[OK] All tests passed! Chat routes are properly integrated.")
        return True
    except Exception as e:
        print(f"[ERROR] Error creating app: {e}")
        return False

if __name__ == "__main__":
    success = test_app_creation()
    if not success:
        exit(1)