---
id: 4
title: generate-chat-user-id-fix-tasks
stage: tasks
date_iso: 2026-01-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 1-ai-todo-chatbot
user: Claude
command: /sp.tasks "Phase 3 chat route uses /api/{user_id}/chat. Frontend is incorrectly calling /api/2/chat, causing "not authorized for user 2". We now have (or will have) backend GET /auth/me that returns { user_id } using the existing token system."
labels: ["chat", "authentication", "user-id", "api-integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - D:/todo-app/frontend/specs/ai-todo-chatbot/tasks.md
tests_yaml:
  - D:/todo-app/frontend/specs/ai-todo-chatbot/tasks.md
---

# Generate Chat User ID Fix Tasks

## Prompt Text
Phase 3 chat route uses /api/{user_id}/chat. Frontend is incorrectly calling /api/2/chat, causing "not authorized for user 2".

We now have (or will have) backend GET /auth/me that returns { user_id } using the existing token system.

TASKS:
1) Update app/chat/page.tsx (or the chat client flow) so it:
   - Reads token from existing getToken()
   - Calls GET `${NEXT_PUBLIC_API_URL || http://127.0.0.1:8000}/auth/me` with Authorization Bearer token
   - Extracts user_id from response
   - Uses that user_id when calling POST /api/{user_id}/chat
2) Remove any hardcoded user id logic.
3) If /auth/me fails (401), redirect to /login (existing behavior).
4) Ensure existing Phase 2 tasks UI remains unchanged.

Acceptance:
- Clicking "Chat with AI" keeps user logged in
- Chat requests go to /api/<real_user_id>/chat not /api/2/chat
- "mark task 1 as completed" no longer returns authorization error

## Response Text
Generated new tasks.md file with updated tasks for fixing the user ID retrieval issue in the chat functionality. The new tasks include updating the chat page to use the /auth/me endpoint instead of decoding JWT tokens directly, implementing proper error handling, and ensuring the correct user ID is passed to the chat API endpoint.

## Outcome
Created a comprehensive task list organized in phases to address the user ID retrieval issue in the chat functionality. The tasks are designed to update the frontend to use the backend /auth/me endpoint for obtaining the user ID, replace the current JWT token decoding approach, and ensure proper error handling and redirects.