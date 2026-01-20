"""
End-to-end tests for the Todo application
This file validates the complete functionality of the application
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


# Create a test client for the API
client = TestClient(app)


def test_api_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running!"}


def test_unauthorized_access_to_tasks():
    """Test that accessing tasks without authentication returns 401"""
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized


if __name__ == "__main__":
    # Run the basic tests
    test_api_root()
    test_unauthorized_access_to_tasks()
    print("Basic end-to-end tests passed!")