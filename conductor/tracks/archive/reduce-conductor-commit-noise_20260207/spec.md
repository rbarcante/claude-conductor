# Specification: Reduce Conductor Commit Noise

> **Type:** refactor
> **Track ID:** `reduce-conductor-commit-noise_20260207`

## Overview

The conductor workflow currently generates excessive housekeeping commits (plan updates, status markers, phase checkpoints) that pollute the git log and make it difficult to read meaningful project history. For a typical track with 2 phases and 3 tasks each, ~11 conductor commits are created alongside only 6 actual code commits.

This refactor consolidates conductor housekeeping commits by batching plan/status updates and making git notes optional, resulting in a cleaner git history where conductor commits are the exception, not the norm.

## Background

The current workflow creates separate commits for:
- Plan status updates after each task (`conductor(plan): Mark task '...' as complete`)
- Phase checkpoint commits (`conductor(checkpoint): Checkpoint end of Phase X`)
- Plan updates after each phase checkpoint (`conductor(plan): Mark phase '...' as complete`)
- Track completion status (`chore(conductor): Mark track '...' as complete`)

This results in nearly 2x the number of commits needed, making `git log` difficult to read and obscuring the actual development work.

## Requirements

### Functional Requirements

- [x] **FR-1: Batch plan updates to phase end** - After each task completes, update `plan.md` in the working tree (mark `[~]` → `[x]`, append commit SHA) but do not commit the plan change separately. At phase completion, the phase checkpoint commit includes all accumulated plan.md changes.
- [x] **FR-2: Consolidate phase checkpoint commits** - The phase checkpoint commit includes all accumulated plan.md task status updates and the phase heading checkpoint SHA annotation (2 commits → 1).
- [x] **FR-3: Remove separate track completion commit** - The final phase checkpoint commit also includes the track status update in `tracks.md`.
- [x] **FR-4: Make git notes optional** - Git notes become opt-in rather than mandatory. Add "Optional" label to git notes steps in both workflow files.
- [x] **FR-5: Confirm Commit step remains per-task** - The user is still asked to confirm each task's code commit (the actual work). Only conductor metadata commits are batched/eliminated.

### Non-Functional Requirements

- [x] **NFR-1:** Changes must be applied consistently across all 4 files: `commands/implement.md`, `commands/newTrack.md`, `conductor/workflow.md`, `templates/workflow.md`
- [x] **NFR-2:** The newTrack creation commit remains unchanged (single useful commit)
- [x] **NFR-3:** Plan.md must always reflect current state on disk (even if uncommitted) so `/conductor:status` works correctly
- [x] **NFR-4:** No changes to the CLI scripts - this is purely a protocol/workflow change

## Acceptance Criteria

- [x] A typical track (2 phases, 3 tasks each) produces at most: 6 code commits + 2 phase checkpoints + 1 track creation = 9 commits (down from ~17)
- [x] `plan.md` is updated on disk after each task (status command still works)
- [x] Git notes steps are clearly marked as optional in all workflow files
- [x] No separate `conductor(plan):` commits exist in the workflow
- [x] Phase checkpoint commit message clearly indicates it includes plan updates

## Out of Scope

- Changes to the CLI scripts (`conductor_cli.py`)
- Changes to the `/conductor:setup` command
- Changes to the `/conductor:revert` command (may need separate track if checkpoint format changes)
- Removing git notes entirely (they remain available as opt-in)

## Dependencies

- None identified

## References

- `commands/implement.md` - Implementation command protocol
- `commands/newTrack.md` - Track creation command protocol
- `conductor/workflow.md` - Project workflow (active)
- `templates/workflow.md` - Workflow template (for new projects)
