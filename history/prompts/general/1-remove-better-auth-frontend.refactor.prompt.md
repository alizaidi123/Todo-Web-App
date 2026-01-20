---
id: 1
title: Remove-Better-Auth-Frontend
stage: refactor
date: 2026-01-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: alizaidi123
command: /sp.phr
labels: ["auth", "frontend", "refactoring", "dependency-removal"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/components/AuthProvider.tsx
 - frontend/lib/auth.ts
 - frontend/package.json
tests:
 - none
---

## Prompt

Frontend is failing because it imports non-existent exports from "better-auth/react" (BaseProvider, createAuth).

Goal: remove Better Auth usage entirely to avoid auth-related issues and allow the UI to run.

Make these changes:
1) components/AuthProvider.tsx
   - Remove all imports from "better-auth/react"
   - Export AuthContextProvider that simply returns children (a no-op wrapper).
   - Keep the same component name and signature so other files don't break.

2) lib/auth.ts
   - Remove all imports from "better-auth/react"
   - Replace its exports with minimal placeholders (or delete the file if unused).
   - Ensure no file imports "better-auth/react" anywhere in the frontend.

3) Remove "better-auth" from package.json dependencies if present.

After changes: `npm run dev` must compile and load http://localhost:3000 without 500 errors.
No manual coding by human.

## Response snapshot

Successfully removed Better Auth from the frontend by modifying components/AuthProvider.tsx to be a no-op wrapper, replacing auth.ts exports with minimal placeholders, and removing better-auth from package.json. The development server now starts successfully.

## Outcome

- ✅ Impact: Removed Better Auth dependency and replaced with no-op implementations to prevent import errors
- 🧪 Tests: none
- 📁 Files: frontend/components/AuthProvider.tsx, frontend/lib/auth.ts, frontend/package.json
- 🔁 Next prompts: none
- 🧠 Reflection: Removing problematic dependencies requires careful replacement with compatible interfaces to avoid breaking existing code.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):