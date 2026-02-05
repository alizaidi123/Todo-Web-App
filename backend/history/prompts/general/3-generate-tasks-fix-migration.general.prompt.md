---
id: 3
title: "generate-tasks-fix-migration"
stage: "tasks"
date_iso: "2026-01-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "fix-migration"
branch: "1-ai-todo-chatbot"
user: "user"
command: "sp.tasks"
labels: ["migration", "postgresql", "bug-fix", "database"]
link_spec: "null"
link_ticket: "null"
link_adr: "null"
link_pr: "null"
files_yaml: |
  - tasks_fix_migration.md
tests_yaml: |
  - null
---

# Prompt History Record: Generate Tasks for Migration Fix

## Original Prompt
```
/sp.tasks

Alembic upgrade fails on revision 87833a57b8d1_priority_string_conversion.py:

psycopg2.errors.DatatypeMismatch: column "priority" is of type integer but expression is of type text
The failing SQL is:
UPDATE task
SET priority = CASE WHEN priority=1 THEN 'low' ... END

The migration is updating priority to TEXT values while the column is still INTEGER.
Fix the migration so it works on Postgres/Neon.

Requirements:
- Do NOT reimplement app features.
- Only modify migration(s) and any small supporting code if required.
- The correct approach should convert INTEGER->TEXT safely:
  Prefer a single ALTER statement using USING CASE mapping:
    ALTER TABLE task ALTER COLUMN priority TYPE TEXT USING (
      CASE
        WHEN priority = 1 THEN 'low'
        WHEN priority = 2 THEN 'medium'
        WHEN priority = 3 THEN 'high'
        ELSE 'medium'
      END
    )
- Ensure the migration is idempotent-safe enough for typical runs.
- Provide downgrade that converts back to INTEGER using reverse mapping:
    'l
```

## Response Summary
Generated tasks_fix_migration.md file to address the PostgreSQL/Neon compatibility issue with the priority column migration. The tasks include updating the migration to use the USING clause for atomic type conversion, ensuring it works correctly on PostgreSQL/Neon databases, and maintaining data integrity during the conversion.

## Outcome
Successfully created tasks_fix_migration.md with 9 tasks organized in phases to systematically fix the migration issue while maintaining functionality.