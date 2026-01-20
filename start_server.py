#!/usr/bin/env python
"""
Script to start the FastAPI server with environment variables loaded from .env
"""

import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Verify that the required environment variable is set
secret = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY")
if not secret:
    raise RuntimeError("Either BETTER_AUTH_SECRET or JWT_SECRET_KEY environment variable must be set for JWT verification")

print("Environment variables loaded successfully!")
print(f"Database URL: {os.getenv('DATABASE_URL', os.getenv('NEON_DATABASE_URL', 'Not set'))}")

# Start the server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=False)