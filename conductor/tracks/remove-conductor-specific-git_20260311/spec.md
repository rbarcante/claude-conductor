# Specification: Remove Conductor-Specific Git Commits

> **Type:** feature
> **Track ID:** `remove-conductor-specific-git_20260311`

## Overview

Conductor currently produces its own git commits with conductor-specific prefixes (`conductor(track):`, `conductor(checkpoint):`, `chore(conductor):`, `docs(conductor):`). These add noise to git history and don't carry meaningful code changes. This track removes all conductor-specific commits by bundling conductor artifact changes (plan.md, metadata.json, etc.) into the actual feature/code commits they relate to.

## Background

After the prior `reduce-conductor-commit-noise` refactor, the remaining conductor-specific commits are:
- **Track creation:** `conductor(track): Create track '<description>'` — commits spec.md, plan.md, metadata.json, etc.
- **Phase checkpoints:** `conductor(checkpoint): Checkpoint end of Phase X` — commits accumulated plan.md updates
- **Track completion:** `chore(conductor): Mark track '<description>' as complete`
- **Docs sync:** `docs(conductor): Synchronize docs for track '<description>'`

## Requirements

### Functional Requirements

- **FR-1: Remove phase checkpoint commits** — Plan.md updates and phase status changes are bundled into the next task's code commit, or into the final task commit of the phase. Plan.md remains updated on disk after each task for status tracking.
- **FR-2: Remove track completion commits** — Track completion status update is bundled into the last code commit of the track.
- **FR-3: Remove docs sync commits** — Documentation synchronization is bundled into the relevant code commit.
- **FR-4: Ask user about track creation commit** — At track creation time, ask the user whether to commit track files (spec.md, plan.md, metadata.json, etc.) as a separate commit or leave them uncommitted to be bundled with the first task commit.
- **FR-5: Update git-history-analyst** — Update the git history analysis agent to no longer rely on conductor-specific commit prefixes for identifying track-related commits.
- **FR-6: Update conductor-methodology skill** — Remove conductor-specific commit patterns from the skill's commit message documentation.

### Non-Functional Requirements

- **NFR-1:** Changes must be applied consistently across: `commands/implement.md`, `commands/newTrack.md`, `conductor/workflow.md`, `templates/workflow.md`, `skills/conductor-methodology/SKILL.md`, `agents/git-history-analyst.md`
- **NFR-2:** `plan.md` must always reflect current state on disk so `/conductor:status` works correctly
- **NFR-3:** No changes to CLI scripts — this is purely a protocol/workflow change
- **NFR-4:** The `/conductor:revert` command logic should still work (may need updated heuristics)

## Acceptance Criteria

- No commits with `conductor(` prefix appear in the workflow protocols
- Track creation offers a user choice: commit separately (with standard commit type like `chore:`) or defer
- Phase checkpoint verification still happens but doesn't create its own commit — plan updates ride along with code commits
- `git-history-analyst` uses alternative strategies (track metadata, plan.md references) instead of conductor commit prefixes
- CONTRIBUTING.md warning about conductor commit types is updated/removed
- TESTING.md examples are updated to reflect new commit patterns

## Out of Scope

- Changes to CLI scripts (`conductor_cli.py`)
- Changes to `/conductor:setup` (setup commit stays — it's a one-time project init)
- Changes to `/conductor:revert` internals (separate track if needed)
- Removing git notes (they remain opt-in)

## Dependencies

- None identified

## References

- `commands/implement.md` - Implementation command protocol
- `commands/newTrack.md` - Track creation command protocol
- `conductor/workflow.md` - Project workflow (active)
- `templates/workflow.md` - Workflow template (for new projects)
- `skills/conductor-methodology/SKILL.md` - Conductor methodology skill
- `agents/git-history-analyst.md` - Git history analysis agent
- `conductor/tracks/archive/reduce-conductor-commit-noise_20260207/spec.md` - Prior related refactor
