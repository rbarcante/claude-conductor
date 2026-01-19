# Implementation Plan: Add suggest-branch subcommand to implement CLI

> **Track ID:** `add-suggest-branch-subcommand_20260122`

## Overview

Add the missing `suggest-branch` subcommand to the implement CLI command, providing branch name suggestions based on track type and ID.

---

## Phase 1: Implementation [checkpoint: 95f2fef]

- [x] Task: Write failing tests for suggest-branch subcommand [69b1a7c]
    - [x] Test: suggest_branch returns correct prefix for feature track
    - [x] Test: suggest_branch returns correct prefix for bugfix track
    - [x] Test: suggest_branch extracts shortname from track_id
    - [x] Test: suggest_branch returns error for missing track
    - [x] Test: suggest_branch returns current branch name
    - [x] Run tests and confirm they fail

- [x] Task: Add suggest-branch subcommand to CLI parser [7e8040b]
    - [x] Add subparser in conductor_cli.py for suggest-branch
    - [x] Add track_id positional argument
    - [x] Wire to implement.handle()

- [x] Task: Implement suggest_branch function [cbd8a79]
    - [x] Add TRACK_TYPE_TO_BRANCH_PREFIX mapping
    - [x] Implement suggest_branch() function in implement.py
    - [x] Handle track not found error
    - [x] Get current branch from git
    - [x] Generate worktree path suggestion
    - [x] Run tests and confirm they pass

- [x] Task: Conductor - User Manual Verification 'Phase 1: Implementation' (Protocol in workflow.md)

---

## Phase 2: Integration and Polish [checkpoint: 8b509c3]

- [x] Task: Verify full test suite passes
    - [x] Run all existing tests to ensure no regressions
    - [x] Verify CLI help shows new subcommand

- [x] Task: Test CLI integration manually
    - [x] Test with existing track
    - [x] Test with non-existent track
    - [x] Verify JSON output format matches protocol

- [x] Task: Conductor - User Manual Verification 'Phase 2: Integration and Polish' (Protocol in workflow.md)

---

## Notes

**Implementation Location:**
- Parser: `scripts/conductor_cli.py` (add subcommand)
- Handler: `scripts/commands/implement.py` (add function)
- Tests: `scripts/tests/test_commands.py`

**Branch Prefix Mapping:**
| Track Type | Branch Prefix |
|------------|---------------|
| `feature` | `feature/` |
| `bugfix` | `fix/` |
| `bug` | `fix/` |
| `refactor` | `refactor/` |
| `docs` | `docs/` |
| `chore` | `chore/` |
| (default) | `feature/` |
