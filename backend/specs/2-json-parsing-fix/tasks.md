# Tasks: Fix JSON Parsing in Agent Tool Arguments

## Feature Overview
Fix the unsafe JSON parsing in agent tool execution that causes runtime errors when processing JSON booleans (true/false/null) by replacing eval() with proper JSON parsing.

## Implementation Strategy
This feature will be implemented in phases, focusing on safely parsing tool call arguments while maintaining compatibility with existing functionality. The approach ensures secure and reliable tool execution.

## Dependencies
- User Story 1 (Security Fix) must complete first to ensure safe parsing before any other changes

## Parallel Execution Opportunities
- Within User Story 1: Parsing function implementation and error handling can run in parallel

## Phase 1: Setup
No specific setup tasks needed beyond existing project structure.

## Phase 2: Foundational Tasks
Tasks that must complete before user stories can begin.

- [X] T001 [P] Create safe_parse_arguments utility function to replace eval() with JSON-first parsing
- [X] T002 [P] Implement JSON normalization function to convert JSON booleans/null to Python equivalents

## Phase 3: [US1] Secure Tool Argument Parsing
Replace unsafe eval() with safe JSON parsing in agent runner to handle JSON booleans correctly.

**Goal**: Agent runner safely parses tool call arguments without using eval().

**Independent Test Criteria**:
- Running "mark task 1 as completed" no longer produces "name 'true' is not defined" error
- JSON booleans (true/false/null) are properly converted to Python equivalents (True/False/None)

- [X] T003 [US1] Replace eval() with safe JSON parsing in app/services/agent_runner.py
- [X] T004 [US1] Handle case where arguments are already dict (pass through directly)
- [X] T005 [US1] Handle case where arguments are string (try json.loads first)
- [X] T006 [US1] Handle case where json.loads fails (normalize JSON literals and use ast.literal_eval as fallback)

## Phase 4: [US2] Tool Execution Verification
Ensure tool execution receives proper Python boolean values for fields like "completed".

**Goal**: Tools receive proper Python boolean values instead of JSON booleans.

**Independent Test Criteria**:
- Tools receive True/False instead of true/false for boolean fields
- Task completion works properly when user says "mark task 1 as completed"

- [X] T007 [US2] Verify boolean fields are properly converted in tool arguments
- [X] T008 [US2] Test that completed: true becomes completed: True in tool execution

## Phase 5: [US3] Unit Testing and Validation
Add unit tests to verify the fix works correctly.

**Goal**: Comprehensive test coverage for the JSON parsing fix.

**Independent Test Criteria**:
- parse_tool_args('{"completed": true}') returns {"completed": True}
- parse_tool_args('{"completed": false}') returns {"completed": False}

- [X] T009 [US3] Create unit test for JSON boolean conversion
- [X] T010 [US3] Create unit test for mixed data types in JSON
- [X] T011 [US3] Create unit test for error handling scenarios

## Phase 6: [US4] Integration Testing
Test the complete flow with actual tool calls.

**Goal**: End-to-end functionality works with safe JSON parsing.

**Independent Test Criteria**:
- User can say "mark task 1 as completed" without error
- All existing tool functionality continues to work

- [X] T012 [US4] Test "mark task 1 as completed" scenario
- [X] T013 [US4] Test other tool calls to ensure no regression
- [X] T014 [US4] Verify all boolean parameters work correctly

## Phase 7: Polish & Cross-Cutting Concerns
Final validation and documentation.

- [X] T015 Update any related documentation to reflect the safe parsing implementation
- [X] T016 Clean up temporary files or test data created during implementation