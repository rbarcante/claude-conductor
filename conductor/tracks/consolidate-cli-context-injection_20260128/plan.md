# Implementation Plan: Consolidate CLI Context Injection

> **Track ID:** `consolidate-cli-context-injection_20260128`

## Overview

This plan outlines the implementation tasks for consolidating CLI context injection across Conductor command files.

---

## Phase 1: Analysis and Design [checkpoint: 2d37e28]

- [x] Task: Analyze current CLI call patterns in each command file
    - [x] Document all CLI calls in setup.md with their purposes
    - [x] Document all CLI calls in newTrack.md with their purposes
    - [x] Document all CLI calls in implement.md with their purposes
    - [x] Document all CLI calls in status.md with their purposes
    - [x] Categorize calls as "read-only context" vs "action/write"

- [x] Task: Design consolidated context JSON structure
    - [x] Define expected JSON output format for setup context
    - [x] Define expected JSON output format for newTrack context
    - [x] Define expected JSON output format for implement context
    - [x] Define expected JSON output format for status context

- [x] Task: Conductor - User Manual Verification 'Analysis and Design' (Protocol in workflow.md)

## Phase 2: Update status.md [checkpoint: 0f7551f]

- [x] Task: Add Context section to status.md
    - [x] Add `# Context` section after frontmatter
    - [x] Add `!`backtick`` with `status full` CLI call
    - [x] Update CLI Operations section to reference injected context
    - [x] Update Section 1.1 to use context instead of separate verify call
    - [x] Update Section 2.1 to use context instead of separate full call

- [x] Task: Validate status.md changes
    - [x] Verify command syntax is correct
    - [x] Verify fallback instructions are preserved
    - [x] Test that `!`backtick`` syntax executes properly

- [x] Task: Conductor - User Manual Verification 'Update status.md' (Protocol in workflow.md)

## Phase 3: Update setup.md

- [x] Task: Add Context section to setup.md
    - [x] Add `# Context` section after frontmatter
    - [x] Add `!`backtick`` with chained detect + state get CLI calls
    - [x] Update CLI Operations section to reference injected context
    - [x] Update Section 1.1 to use context for state check
    - [x] Update Section 2.0 to use context for project detection

- [x] Task: Validate setup.md changes
    - [x] Verify command syntax is correct
    - [x] Verify fallback instructions are preserved
    - [x] Verify action CLI calls (scaffold, state set, copy-templates) remain as instructions

- [ ] Task: Conductor - User Manual Verification 'Update setup.md' (Protocol in workflow.md)

## Phase 4: Update newTrack.md

- [ ] Task: Add Context section to newTrack.md
    - [ ] Add `# Context` section after frontmatter
    - [ ] Determine which CLI calls can be consolidated for upfront context
    - [ ] Add `!`backtick`` with appropriate CLI calls
    - [ ] Update CLI Operations section to reference injected context

- [ ] Task: Validate newTrack.md changes
    - [ ] Verify command syntax is correct
    - [ ] Verify fallback instructions are preserved
    - [ ] Verify action CLI calls (generate-id, scaffold, register) remain as instructions

- [ ] Task: Conductor - User Manual Verification 'Update newTrack.md' (Protocol in workflow.md)

## Phase 5: Update implement.md

- [ ] Task: Add Context section to implement.md
    - [ ] Add `# Context` section after frontmatter
    - [ ] Add `!`backtick`` with parse-tracks CLI call
    - [ ] Update CLI Operations section to reference injected context
    - [ ] Update Section 2.0 to use context for track parsing

- [ ] Task: Validate implement.md changes
    - [ ] Verify command syntax is correct
    - [ ] Verify fallback instructions are preserved
    - [ ] Verify action CLI calls (update-status, archive) remain as instructions

- [ ] Task: Conductor - User Manual Verification 'Update implement.md' (Protocol in workflow.md)

## Phase 6: Final Validation and Documentation

- [ ] Task: Cross-command validation
    - [ ] Verify all four commands have consistent Context section structure
    - [ ] Verify no functionality is broken by the changes
    - [ ] Verify permission prompts are reduced as expected

- [ ] Task: Update any affected documentation
    - [ ] Update CLAUDE.md if needed
    - [ ] Update tech-stack.md if patterns changed

- [ ] Task: Conductor - User Manual Verification 'Final Validation and Documentation' (Protocol in workflow.md)

---

## Notes

<!-- Implementation notes, decisions made during development -->
