# Implementation Plan: Reduce Conductor Commit Noise

> **Track ID:** `reduce-conductor-commit-noise_20260207`

## Overview

This plan refactors the conductor workflow to reduce commit noise by batching plan/status updates into phase checkpoints and making git notes optional.

---

## Phase 1: Core Workflow Refactor

- [x] Task: Update `templates/workflow.md` - Remove separate plan update commits (steps 10-11), batch plan.md updates into phase checkpoint, mark git notes as optional [uncommitted]
- [x] Task: Update `conductor/workflow.md` - Apply identical changes as templates/workflow.md to keep project workflow in sync [uncommitted]
- [x] Task: Update `commands/implement.md` - Remove separate track completion commit (section 3.0 step 6), consolidate into final phase checkpoint [uncommitted]
- [x] Task: Update `commands/newTrack.md` - Verify no changes needed (track creation commit stays), ensure consistency with updated workflow references [no-change]
- [x] Task: Conductor - User Manual Verification 'Core Workflow Refactor' (Protocol in workflow.md) [verified]

## Phase 2: Validation and Documentation

- [ ] Task: Audit all commit-related instructions across the 4 files to ensure no orphaned references to removed commit steps
- [ ] Task: Update step numbering and cross-references in all modified files to maintain internal consistency
- [ ] Task: Conductor - User Manual Verification 'Validation and Documentation' (Protocol in workflow.md)

---

## Notes

<!-- Implementation notes, decisions made during development -->
