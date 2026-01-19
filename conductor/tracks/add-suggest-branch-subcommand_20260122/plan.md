# Implementation Plan: Add suggest-branch subcommand to implement CLI

> **Track ID:** `add-suggest-branch-subcommand_20260122`

## Overview

Add the missing `suggest-branch` subcommand to the implement CLI command, providing branch name suggestions based on track type and ID.

---

## Phase 1: Implementation

- [ ] Task: Write failing tests for suggest-branch subcommand
    - [ ] Test: suggest_branch returns correct prefix for feature track
    - [ ] Test: suggest_branch returns correct prefix for bugfix track
    - [ ] Test: suggest_branch extracts shortname from track_id
    - [ ] Test: suggest_branch returns error for missing track
    - [ ] Test: suggest_branch returns current branch name
    - [ ] Run tests and confirm they fail

- [ ] Task: Add suggest-branch subcommand to CLI parser
    - [ ] Add subparser in conductor_cli.py for suggest-branch
    - [ ] Add track_id positional argument
    - [ ] Wire to implement.handle()

- [ ] Task: Implement suggest_branch function
    - [ ] Add TRACK_TYPE_TO_BRANCH_PREFIX mapping
    - [ ] Implement suggest_branch() function in implement.py
    - [ ] Handle track not found error
    - [ ] Get current branch from git
    - [ ] Generate worktree path suggestion
    - [ ] Run tests and confirm they pass

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Implementation' (Protocol in workflow.md)

---

## Phase 2: Integration and Polish

- [ ] Task: Verify full test suite passes
    - [ ] Run all existing tests to ensure no regressions
    - [ ] Verify CLI help shows new subcommand

- [ ] Task: Test CLI integration manually
    - [ ] Test with existing track
    - [ ] Test with non-existent track
    - [ ] Verify JSON output format matches protocol

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Integration and Polish' (Protocol in workflow.md)

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
