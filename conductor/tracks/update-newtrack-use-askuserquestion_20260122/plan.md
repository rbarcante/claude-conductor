# Implementation Plan: Update newTrack.md to Use AskUserQuestion Tool

> **Track ID:** `update-newtrack-use-askuserquestion_20260122`

## Overview

This plan outlines the implementation tasks for updating `commands/newTrack.md` to use the `AskUserQuestion` tool for all interactive user prompts.

---

## Phase 1: Add AskUserQuestion Tool Protocol Section

- [ ] Task: Add AskUserQuestion Tool Protocol section after CLI Operations
    - [ ] Create new section header "## AskUserQuestion Tool Protocol"
    - [ ] Add JSON structure documentation (questions array, header, options, multiSelect)
    - [ ] Add key constraints (header max 12 chars, 2-4 options per question)
    - [ ] Add question type mapping (Additive vs Exclusive Choice)
    - [ ] Add standard option patterns (Confirmation, Approval, Selection)
    - [ ] Add Auto-generate option pattern documentation
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Update Section 2.2 (Interactive Specification Generation)

- [ ] Task: Update General Guidelines subsection
    - [ ] Replace text-based question guidelines with AskUserQuestion-based instructions
    - [ ] Add JSON template examples for Additive questions (multiSelect: true)
    - [ ] Add JSON template examples for Exclusive Choice questions (multiSelect: false)
    - [ ] Document the Auto-generate option behavior
- [ ] Task: Add FEATURE track question examples
    - [ ] Add JSON example for interaction type question (UI/API/CLI)
    - [ ] Add JSON example for capability selection question (CRUD operations)
    - [ ] Include Auto-generate option in all examples
- [ ] Task: Add OTHER track question examples (Bug, Chore, etc.)
    - [ ] Add JSON example for bug reproduction steps question
    - [ ] Add JSON example for scope/success criteria question
    - [ ] Include Auto-generate option in all examples
- [ ] Task: Update User Confirmation subsection
    - [ ] Replace text-based confirmation with AskUserQuestion approval pattern
    - [ ] Add JSON example for spec review approval question
    - [ ] Document response handling (Approve → proceed, Suggest changes → revise)
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Update Section 2.3 (Interactive Plan Generation)

- [ ] Task: Update User Confirmation subsection
    - [ ] Replace text-based confirmation with AskUserQuestion approval pattern
    - [ ] Add JSON example for plan review approval question
    - [ ] Document response handling (Approve → proceed, Suggest changes → revise)
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Review and Commit

- [ ] Task: Verify all AskUserQuestion patterns are consistent
    - [ ] Cross-check JSON examples with setup.md patterns
    - [ ] Verify header lengths don't exceed 12 characters
    - [ ] Ensure all options have both label and description
- [ ] Task: Commit changes to newTrack.md
    - [ ] Stage newTrack.md
    - [ ] Commit with message: "feat(newTrack): Add AskUserQuestion tool support for interactive prompts"
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

---

## Notes

<!-- Implementation notes, decisions made during development -->
