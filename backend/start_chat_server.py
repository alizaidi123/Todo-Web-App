#!/usr/bin/env python
"""
Start the FastAPI server with chat functionality.
"""
import uvicorn
import os
from app.main import create_app

def main():
    # Set default values if not in environment
    if not os.getenv("JWT_SECRET_KEY"):
        print("Warning: JWT_SECRET_KEY not set in environment. Using default for development.")
        os.environ["JWT_SECRET_KEY"] = "dev-secret-key-change-in-production"

    app = create_app()

    print("Starting AI Todo Chatbot server...")
    print("Available endpoints:")
    print("  - GET /chat/health - Health check for chat service")
    print("  - POST /chat/message - Chat message endpoint")
    print("  - Other existing task/auth endpoints")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )

if __name__ == "__main__":
    main()