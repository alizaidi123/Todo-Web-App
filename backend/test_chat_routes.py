"""Test script to verify the chat routes are properly integrated."""
import asyncio
import sys
import os
sys.path.append('.')

# Set the required environment variable for JWT
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-for-testing'

from fastapi.testclient import TestClient
from app.main import create_app

def test_chat_routes():
    """Test that chat routes are accessible."""
    app = create_app()
    client = TestClient(app)

    # Test the health endpoint
    response = client.get("/chat/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    print("✓ Chat health endpoint is working")

    # Test the main API endpoint
    response = client.get("/")
    assert response.status_code == 200

    print("✓ Main API endpoint is working")

    # Test that the chat message endpoint exists (will fail due to auth, but should return 401, not 404)
    response = client.post("/chat/message", json={"message": "hello"})
    # Should return 401 (Unauthorized) rather than 404 (Not Found)
    assert response.status_code in [401, 422]  # 422 if validation fails but route exists

    print("✓ Chat message endpoint exists")

    print("\nAll tests passed! Chat routes are properly integrated.")

if __name__ == "__main__":
    test_chat_routes()