---
id: 0001
title: Phase 3 Deployment Fix Specification
stage: spec
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-deployment-fix
branch: 002-deployment-fix
user: alizaidi123
command: /sp.specify
labels: ["deployment", "vercel", "huggingface", "cors", "environment-variables", "production-fix"]
links:
  spec: specs/002-deployment-fix/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-deployment-fix/spec.md
 - specs/002-deployment-fix/checklists/requirements.md
 - history/prompts/002-deployment-fix/ (directory created)
tests:
 - none
---

## Prompt

# Project: Phase 3 Deployment Fix (Vercel frontend + HF backend)

## Context
Next.js frontend is deployed on Vercel. FastAPI backend is deployed on Hugging Face Spaces (Docker).
Locally works. On Vercel, clicking "Chat with AI" redirects to /login. DevTools shows API calls going to http://127.0.0.1:8000/auth/me and CORS/PNA errors.

Vercel env vars (All Environments) are set:
- NEXT_PUBLIC_API_BASE_URL=https://alisaboor3-todo-app.hf.space
- NEXT_PUBLIC_API_URL=https://alisaboor3-todo-app.hf.space

But production bundle still falls back to localhost due to fallback logic.

## Goal
1) Frontend must never fall back to localhost in production build
2) Frontend must always call backend using NEXT_PUBLIC_* env vars in prod
3) Backend must allow CORS from local dev and the Vercel deploy origin
4) Auth remains intact so /chat stays logged in (no redirect to /login due to failed /auth/me)

## Constraints
- Minimal changes
- No new dependencies
- Keep local dev behavior intact
- Do not change auth flows besides fix

## Response snapshot

Created comprehensive feature specification for deployment fix issue. Generated branch name "deployment-fix", created feature branch 002-deployment-fix, wrote detailed specification covering user scenarios (production API connectivity P1, local dev preservation P2), functional requirements (FR-001 through FR-010), success criteria (measurable, technology-agnostic), scope, assumptions, dependencies, and constraints. Created requirements checklist validating spec quality. All validation items pass.

## Outcome

- ✅ Impact: Created complete feature specification ready for planning phase, with clear user scenarios, testable requirements, and measurable success criteria
- 🧪 Tests: Validation checklist confirms all quality criteria pass
- 📁 Files: specs/002-deployment-fix/spec.md (156 lines), specs/002-deployment-fix/checklists/requirements.md
- 🔁 Next prompts: Run `/sp.plan` to create architectural plan, or `/sp.clarify` if any requirements need refinement
- 🧠 Reflection: Spec successfully avoids implementation details while providing clear, testable requirements - distinguishes WHAT (env vars must be used) from HOW (specific Next.js or FastAPI code)

## Evaluation notes (flywheel)

- Failure modes observed: Initial PowerShell script execution failed due to multiline description argument parsing. Recovered by verifying branch/spec creation had succeeded despite error. No template placeholders left unfilled.
- Graders run and results (PASS/FAIL): PASS - All checklist items validated: no implementation details, technology-agnostic success criteria, testable requirements, zero [NEEDS CLARIFICATION] markers
- Prompt variant (if applicable): base-variant
- Next experiment (smallest change to try): Specification is complete and ready for planning. Consider testing plan generation with this spec to validate requirement clarity.
