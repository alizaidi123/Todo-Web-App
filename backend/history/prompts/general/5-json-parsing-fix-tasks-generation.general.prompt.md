---
id: 5
title: JSON Parsing Fix Tasks Generation
stage: tasks
date_iso: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: json-parsing-fix
branch: 1-ai-todo-chatbot
user: user
command: /sp.tasks
labels: ["tasks", "json", "parsing", "security", "agent", "tool-calls"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - D:\\todo-app\\backend\\specs\\2-json-parsing-fix\\tasks.md
tests_yaml: |
prompt_text: |

  We have a runtime error in Phase 3 chat tool execution:

  When user says: "mark task 1 as completed"
  Chat shows: "Error processing your request: name 'true' is not defined"

  This indicates backend is parsing tool-call arguments as Python code (eval/ast.literal_eval) and receiving JSON booleans like true/false/null.

  TASK:
  1) Find where agent tool calls are parsed/executed (likely app/services/agent_runner.py or tool execution helper).
  2) Replace unsafe parsing with JSON-first parsing:
     - If args is dict -> use directly.
     - If args is str -> try json.loads(args).
     - If json.loads fails -> fallback: normalize JSON booleans/null into Python equivalents and then ast.literal_eval, OR return a 400 with helpful error.
  3) Ensure tool execution receives proper Python bool (True/False) for fields like "completed".
  4) Add a small unit test or quick self-check function that proves:
     - parse_tool_args('{"completed": true}') returns {"completed": True}
     - parse_tool_args('{"completed": false}') returns {"completed

response_text: |

  Created comprehensive tasks.md file with 16 sequential tasks organized in 7 phases:

  ## Phase Breakdown:
  - Phase 1: Setup (no specific tasks needed)
  - Phase 2: Foundational Tasks (T001-T002) - Create safe parsing utilities
  - Phase 3: [US1] Secure Tool Argument Parsing (T003-T006) - Replace eval() with safe JSON parsing
  - Phase 4: [US2] Tool Execution Verification (T007-T008) - Verify boolean conversion
  - Phase 5: [US3] Unit Testing and Validation (T009-T011) - Create unit tests
  - Phase 6: [US4] Integration Testing (T012-T014) - End-to-end testing
  - Phase 7: Polish & Cross-Cutting Concerns (T015-T016) - Final cleanup

  ## Key Features:
  - All tasks follow the required checklist format with proper IDs and labels
  - Parallelizable tasks marked with [P] flag
  - User story phases clearly labeled with [US1], [US2], etc.
  - Independent test criteria defined for each user story phase
  - Dependencies properly organized with foundational tasks first
  - Addresses the specific error "name 'true' is not defined" by replacing eval() with safe JSON parsing

  ## Directly Addresses Original Requirements:
  - T001-T002: Create safe parsing utilities ✓
  - T003-T006: Replace eval() with JSON-first parsing ✓
  - T007-T008: Ensure proper Python bool conversion ✓
  - T009-T011: Unit tests for JSON boolean conversion ✓

outcome: Comprehensive tasks file created with 16 tasks in 7 phases
evaluation: All original requirements mapped to specific tasks with proper organization and sequencing. Tasks follow required format and enable systematic implementation of the JSON parsing fix.
---
