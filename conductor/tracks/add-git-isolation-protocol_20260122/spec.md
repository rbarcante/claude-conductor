# Specification: Add Git Isolation Protocol to newTrack Command

> **Type:** chore
> **Track ID:** `add-git-isolation-protocol_20260122`

## Overview

Extract the Git Isolation Setup logic from `implement.md` into a shared protocol file and integrate it into `newTrack.md` to prevent accidental commits to protected branches (`main`, `master`, `develop`) during track creation.

## Background

Currently, `implement.md` has a comprehensive "GIT ISOLATION SETUP" section (Section 2.1) that:
- Detects if the user is on a protected branch (`main`, `master`, or `develop`)
- Suggests appropriate branch names based on track type
- Offers options for branch creation, worktree creation, or custom naming
- Handles error scenarios gracefully

The `newTrack.md` command lacks this protection, allowing track files to be committed directly to protected branches.

## Requirements

### Functional Requirements

- [ ] **FR-1: Create Shared Protocol File** - Create `protocols/git-isolation.md` containing the complete Git Isolation Setup logic extracted from `implement.md` Section 2.1. Ensure the protocol is self-contained and reusable. Explicitly define protected branches: `main`, `master`, `develop`.

- [ ] **FR-2: Update implement.md** - Replace Section 2.1 content with a reference to the shared protocol using format: `**PROTOCOL: Follow the Git Isolation Protocol (`protocols/git-isolation.md`).**`. Maintain section numbering and flow.

- [ ] **FR-3: Update newTrack.md** - Add a new section "1.2 GIT ISOLATION SETUP" after the Setup Check (Section 1.1), referencing the shared protocol. Ensure branch enforcement occurs BEFORE track creation begins (before Section 2.0).

- [ ] **FR-4: CLI Integration** - The shared protocol must reference the existing CLI command: `suggest-branch`. The protocol should work with track IDs that don't exist yet (for newTrack). For newTrack, the suggested branch can be generated from the track description before the track_id is created.

### Non-Functional Requirements

- [ ] **NFR-1: No Duplication** - The Git Isolation logic must exist in only one location (the protocol file). Both commands reference the same source of truth.

- [ ] **NFR-2: Backward Compatibility** - The implement.md workflow must function identically after refactoring. No behavioral changes, only structural reorganization.

## Acceptance Criteria

- [ ] **AC-1**: Running `/conductor:newTrack` on `main`, `master`, or `develop` branch prompts the user to create/switch branches before proceeding
- [ ] **AC-2**: Running `/conductor:implement` continues to work exactly as before
- [ ] **AC-3**: The file `protocols/git-isolation.md` exists and contains the complete Git Isolation Setup logic with protected branches defined as `main`, `master`, `develop`
- [ ] **AC-4**: Both `implement.md` and `newTrack.md` reference `protocols/git-isolation.md` instead of containing duplicate logic
- [ ] **AC-5**: User can choose to create branch, create worktree, or type custom name in both commands

## Out of Scope

- Adding branch enforcement to other commands (setup, status, revert)
- Modifying the CLI's `suggest-branch` subcommand
- Adding new branch naming conventions beyond what exists in implement.md

## Dependencies

- Existing `implement.md` Section 2.1 content
- Existing CLI `suggest-branch` subcommand

## References

- `commands/implement.md` Section 2.1 (lines 127-307)
- `scripts/conductor_cli.py` suggest-branch subcommand
