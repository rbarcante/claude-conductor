# Implementation Plan: Ask Confirmation Before Committing

> **Track ID:** `ask-confirmation-before-committing_20260129`

## Overview

This plan implements commit confirmation prompts in the `/conductor:newTrack` and `/conductor:implement` commands to give users control over when commits are made.

---

## Phase 1: Update newTrack Command

- [x] Task: Add commit confirmation step to newTrack.md [f93885c]
    - [x] Read current Section 2.4 structure in commands/newTrack.md
    - [x] Insert new Step 5 "Confirm Commit" between Step 4 (Register Track) and Commit Changes
    - [x] Add AskUserQuestion tool call with commit approval options
    - [x] Add conditional logic: if "Commit now" proceed to Step 6, if "Skip commit" skip to Step 7
    - [x] Update Step 7 announcement to reflect commit status (committed vs uncommitted)

- [~] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Update Workflow Task Lifecycle

- [ ] Task: Add commit confirmation step to workflow.md Task Workflow
    - [ ] Read current Task Workflow structure in conductor/workflow.md
    - [ ] Insert new Step 7.5 "Confirm Commit" between Step 7 (Document Deviations) and Step 8 (Commit Code Changes)
    - [ ] Add instruction to use AskUserQuestion tool with commit approval options
    - [ ] Add conditional logic: if "Commit now" proceed to Step 8, if "Skip commit" skip to Step 9
    - [ ] Ensure task completion flow works correctly when commit is skipped (plan update should still happen but may not be committed)

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Verification and Documentation

- [ ] Task: End-to-end verification of newTrack command
    - [ ] Create a test track using /conductor:newTrack
    - [ ] Verify confirmation prompt appears before commit
    - [ ] Test both "Commit now" and "Skip commit" paths
    - [ ] Verify announcements correctly reflect commit status

- [ ] Task: End-to-end verification of implement command
    - [ ] Start implementing a test task using /conductor:implement
    - [ ] Verify confirmation prompt appears before task commit
    - [ ] Test both "Commit now" and "Skip commit" paths
    - [ ] Verify task workflow continues correctly in both cases

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

---

## Notes

<!-- Implementation notes, decisions made during development -->
