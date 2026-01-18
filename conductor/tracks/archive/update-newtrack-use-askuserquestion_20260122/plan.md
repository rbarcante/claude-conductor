# Implementation Plan: Update newTrack.md to Use AskUserQuestion Tool

> **Track ID:** `update-newtrack-use-askuserquestion_20260122`

## Overview

This plan outlines the implementation tasks for updating `commands/newTrack.md` to use the `AskUserQuestion` tool for all interactive user prompts.

---

## Phase 1: Add AskUserQuestion Tool Protocol Section

- [x] Task: Add AskUserQuestion Tool Protocol section after CLI Operations
    - [x] Create new section header "## AskUserQuestion Tool Protocol"
    - [x] Add JSON structure documentation (questions array, header, options, multiSelect)
    - [x] Add key constraints (header max 12 chars, 2-4 options per question)
    - [x] Add question type mapping (Additive vs Exclusive Choice)
    - [x] Add standard option patterns (Confirmation, Approval, Selection)
    - [x] Add Auto-generate option pattern documentation
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Update Section 2.2 (Interactive Specification Generation)

- [x] Task: Update General Guidelines subsection
    - [x] Replace text-based question guidelines with AskUserQuestion-based instructions
    - [x] Add JSON template examples for Additive questions (multiSelect: true)
    - [x] Add JSON template examples for Exclusive Choice questions (multiSelect: false)
    - [x] Document the Auto-generate option behavior
- [x] Task: Add FEATURE track question examples
    - [x] Add JSON example for interaction type question (UI/API/CLI)
    - [x] Add JSON example for capability selection question (CRUD operations)
    - [x] Include Auto-generate option in all examples
- [x] Task: Add OTHER track question examples (Bug, Chore, etc.)
    - [x] Add JSON example for bug reproduction steps question
    - [x] Add JSON example for scope/success criteria question
    - [x] Include Auto-generate option in all examples
- [x] Task: Update User Confirmation subsection
    - [x] Replace text-based confirmation with AskUserQuestion approval pattern
    - [x] Add JSON example for spec review approval question
    - [x] Document response handling (Approve → proceed, Suggest changes → revise)
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Update Section 2.3 (Interactive Plan Generation)

- [x] Task: Update User Confirmation subsection
    - [x] Replace text-based confirmation with AskUserQuestion approval pattern
    - [x] Add JSON example for plan review approval question
    - [x] Document response handling (Approve → proceed, Suggest changes → revise)
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Review and Commit

- [x] Task: Verify all AskUserQuestion patterns are consistent
    - [x] Cross-check JSON examples with setup.md patterns
    - [x] Verify header lengths don't exceed 12 characters
    - [x] Ensure all options have both label and description
- [x] Task: Commit changes to newTrack.md `a0c6dc9`
    - [x] Stage newTrack.md
    - [x] Commit with message: "feat(newTrack): Add AskUserQuestion tool support for interactive prompts"
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

---

## Notes

<!-- Implementation notes, decisions made during development -->
