# Implementation Plan: Implement AskUserQuestion Tool Standardization

## Phase 1: Add Protocol Documentation

- [x] Task: Add AskUserQuestion Tool Protocol section to implement.md
    - [x] Copy the protocol section from newTrack.md as reference
    - [x] Place after the "Fallback Instructions" section
    - [x] Include Tool Structure, Key Rules, and Standard Option Patterns
    - [x] Adapt examples for implement.md use cases (track selection, quality gate, etc.)

- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Convert Track Selection (Section 2.0)

- [x] Task: Convert track confirmation prompt to AskUserQuestion
    - [x] Replace "Is this correct?" text prompt with AskUserQuestion call
    - [x] Use header "Confirm" (7 chars)
    - [x] Options: "Yes, proceed" / "No, let me clarify"

- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Convert Pattern Surfacing (Section 3.0)

- [x] Task: Convert pattern application prompt to AskUserQuestion
    - [x] Replace "Apply patterns? (Y)es / (S)kip / (V)iew first" with AskUserQuestion
    - [x] Use header "Patterns" (8 chars)
    - [x] Options: "Apply patterns" / "View first" / "Skip"

- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Convert Quality Gate (Section 3.5)

- [x] Task: Convert quality gate options prompt to AskUserQuestion
    - [x] Replace "Enter choice (1/2/3)" with AskUserQuestion
    - [x] Use header "Action" (6 chars)
    - [x] Options: "Fix issues" / "Skip with reasons" / "View details"

- [x] Task: Convert skip reason prompt to AskUserQuestion
    - [x] Replace text prompt for reasons with AskUserQuestion
    - [x] Use header "Skip Reason" (11 chars)
    - [x] Options: common reasons (Intentional, Deferred, False positive)
    - [x] multiSelect: true to allow multiple reasons

- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Convert Decision Capture (Section 3.6)

- [ ] Task: Convert decision point prompt to AskUserQuestion
    - [ ] Replace "Select an option (A/B/skip)" with AskUserQuestion
    - [ ] Use header "Decision" (8 chars)
    - [ ] Dynamically generate options from decision context
    - [ ] Include "Skip recording" as final option

- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Phase 6: Convert Doc Synchronization (Section 4.0)

- [ ] Task: Convert Product Definition approval to AskUserQuestion
    - [ ] Replace "yes/no" with AskUserQuestion
    - [ ] Use header "Approve" (7 chars)
    - [ ] Options: "Approve changes" / "Reject changes"

- [ ] Task: Convert Tech Stack approval to AskUserQuestion
    - [ ] Same pattern as Product Definition

- [ ] Task: Convert Product Guidelines approval to AskUserQuestion
    - [ ] Same pattern but include warning in question text
    - [ ] Options: "Approve critical changes" / "Reject changes"

- [ ] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)

## Phase 7: Convert Track Cleanup (Section 5.0)

- [ ] Task: Convert cleanup options prompt to AskUserQuestion
    - [ ] Replace "A/B/C" text prompt with AskUserQuestion
    - [ ] Use header "Cleanup" (7 chars)
    - [ ] Options: "Archive" / "Delete" / "Skip cleanup"
    - [ ] Include descriptions for each option

- [ ] Task: Convert delete confirmation to AskUserQuestion
    - [ ] Replace "yes/no" with AskUserQuestion
    - [ ] Use header "Confirm" (7 chars)
    - [ ] Include WARNING in question text
    - [ ] Options: "Yes, delete permanently" / "Cancel deletion"

- [ ] Task: Conductor - User Manual Verification 'Phase 7' (Protocol in workflow.md)

## Phase 8: Final Verification

- [ ] Task: Verify no text-based prompts remain
    - [ ] Search for patterns: "yes/no", "Enter choice", "A/B/C", "(Y)es"
    - [ ] Confirm all user interactions use AskUserQuestion

- [ ] Task: Verify all headers are ≤12 characters
    - [ ] Review all header values in AskUserQuestion calls

- [ ] Task: Conductor - User Manual Verification 'Phase 8' (Protocol in workflow.md)
