---
id: 1
title: "Create Project Constitution"
stage: constitution
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-create-project-constitution.constitution.prompt.md"
tests_yaml: []
---

# Create Project Constitution

## User Prompt
```
/sp.constitution

You are working on an existing Next.js + FastAPI Todo app.
Non-negotiables:
- DO NOT change Better Auth configuration or auth logic.
- DO NOT change backend behavior or API contracts.
- DO NOT change task CRUD logic; UI/UX only.
- No manual edits by the user; generate changes via Spec-Kit steps only.
- Preserve existing routes and functionality; only redesign visuals and layout.

UI goal: modern SaaS, Neon Purple gen-z theme, glassmorphism, responsive, accessible.
Use Tailwind CSS. If Tailwind is missing, add it safely (Next.js 14 compatible) without breaking existing pages.
```

## Response Summary
Created the project constitution file at `.specify/memory/constitution.md` based on the provided principles and requirements. The constitution includes:

- Core principles about preserving auth, backend behavior, and CRUD logic
- Technology stack principles for Tailwind CSS and modern UI/UX
- Development methodology principles for Spec-Driven Development
- Quality assurance principles for authoritative sources and knowledge capture
- Governance procedures for amendments and compliance

The constitution serves as the foundational document for the project, establishing non-negotiable constraints and guiding principles for all future development work.

## Outcome
Successfully created project constitution that captures all specified non-negotiables and principles. The constitution will guide all future development decisions and ensure adherence to the specified constraints.