# Project Constitution

## Version Information
- **Version**: 1.0.0
- **Ratification Date**: 2026-01-20
- **Last Amended Date**: 2026-01-20

## Project Identity
- **Project Name**: Todo App
- **Surface**: Next.js + FastAPI Todo Application
- **Mission**: Deliver a modern, responsive todo application with neon purple gen-z theme and glassmorphism design

## Core Principles

### 1. Auth Preservation
**Principle**: DO NOT change Better Auth configuration or auth logic.
**Rationale**: Maintain security integrity and existing authentication contracts.

### 2. Backend Stability
**Principle**: DO NOT change backend behavior or API contracts.
**Rationale**: Preserve existing API stability and prevent breaking changes to established interfaces.

### 3. CRUD Logic Preservation
**Principle**: DO NOT change task CRUD logic; UI/UX only.
**Rationale**: Maintain core business logic while allowing visual and interaction improvements.

### 4. No Manual Edits
**Principle**: No manual edits by the user; generate changes via Spec-Kit steps only.
**Rationale**: Ensure consistency and traceability of all changes through automated processes.

### 5. Functionality Preservation
**Principle**: Preserve existing routes and functionality; only redesign visuals and layout.
**Rationale**: Maintain application behavior while improving user experience and aesthetics.

## Technology Stack Principles

### 6. Tailwind CSS Adoption
**Principle**: Use Tailwind CSS for styling. If Tailwind is missing, add it safely (Next.js 14 compatible) without breaking existing pages.
**Rationale**: Enable consistent, utility-first styling approach aligned with modern UI practices.

### 7. Modern UI/UX Standards
**Principle**: Implement modern SaaS, Neon Purple gen-z theme, glassmorphism, responsive, accessible design.
**Rationale**: Create contemporary user experience that appeals to target demographic.

## Development Methodology

### 8. Spec-Driven Development (SDD)
**Principle**: Follow Spec-Kit Plus methodology with spec, plan, tasks, and implementation phases.
**Rationale**: Ensure systematic, well-documented development with clear requirements and testable outcomes.

### 9. Small, Testable Changes
**Principle**: Favor smallest viable diffs that are testable and reference code precisely.
**Rationale**: Reduce risk of introducing bugs and enable easier review and maintenance.

## Quality Assurance Principles

### 10. Authoritative Source Mandate
**Principle**: Prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.
**Rationale**: Ensure accuracy and reliability of all development activities.

### 11. Knowledge Capture
**Principle**: Record every user input verbatim in a Prompt History Record (PHR) after every user message. Follow PHR routing: Constitution → `history/prompts/constitution/`, Feature-specific → `history/prompts/<feature-name>/`, General → `history/prompts/general/`.
**Rationale**: Maintain complete audit trail and knowledge preservation for project continuity.

### 12. Architectural Decision Recording
**Principle**: When architecturally significant decisions are detected, suggest documentation: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto-create ADRs; require user consent.
**Rationale**: Preserve important architectural decisions for future reference and team alignment.

## Governance

### Amendment Procedure
Changes to this constitution require explicit user consent and must be documented with version increments following semantic versioning:
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
All development activities must be validated against these principles before implementation. Regular reviews ensure continued alignment with project goals.

### Versioning Policy
This constitution follows semantic versioning to track meaningful changes while maintaining backward compatibility where possible.