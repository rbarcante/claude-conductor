# Specification: Add suggest-branch subcommand to implement CLI

> **Type:** feature
> **Track ID:** `add-suggest-branch-subcommand_20260122`

## Overview

The `implement.md` protocol references a `suggest-branch` CLI subcommand (Section 2.1 GIT ISOLATION SETUP) that does not exist in the actual CLI implementation. This track adds the missing subcommand to provide branch name suggestions based on track type and ID.

## Problem Analysis

**Root Cause:** The protocol document (`commands/implement.md`) was written with a `suggest-branch` subcommand specification, but the actual implementation in `scripts/commands/implement.py` and `scripts/conductor_cli.py` was never added.

**Current Behavior:**
```bash
python conductor_cli.py --json implement suggest-branch track_id
# Error: invalid choice: 'suggest-branch'
```

**Expected Behavior:**
```bash
python conductor_cli.py --json implement suggest-branch track_id
# Returns: {"branch_name": "feature/track-shortname", ...}
```

## Functional Requirements

1. **FR-1**: Add `suggest-branch` subcommand to the implement command parser in `conductor_cli.py`
   - Accept `track_id` as required positional argument
   - Follow existing CLI patterns

2. **FR-2**: Implement `suggest_branch()` function in `scripts/commands/implement.py`
   - Read track metadata to determine track type
   - Map track type to branch prefix:
     - `feature` → `feature/`
     - `bugfix` / `bug` → `fix/`
     - `refactor` → `refactor/`
     - `docs` → `docs/`
     - `chore` → `chore/`
   - Extract shortname from track_id (remove date suffix)
   - Generate suggested branch name: `<prefix><shortname>`
   - Generate suggested worktree path: `../<project>-<shortname>`

3. **FR-3**: Return structured JSON response matching protocol expectations:
   ```json
   {
     "success": true,
     "data": {
       "track_id": "dark-mode-toggle_20260122",
       "track_type": "feature",
       "branch_prefix": "feature/",
       "branch_name": "feature/dark-mode-toggle",
       "worktree_path": "../project-dark-mode-toggle",
       "current_branch": "main"
     }
   }
   ```

## Acceptance Criteria

- [ ] `implement suggest-branch <track_id>` subcommand exists and is documented
- [ ] Returns correct branch prefix based on track type from metadata
- [ ] Returns shortname extracted from track_id (without date suffix)
- [ ] Returns suggested worktree path based on project directory name
- [ ] Returns current branch name for context
- [ ] Handles missing track gracefully with error message
- [ ] JSON output matches protocol specification
- [ ] Unit tests cover all track type mappings

## Out of Scope

- Actually creating the branch (that's the protocol's job)
- Git worktree creation
- Interactive prompts

## References

- Protocol: `commands/implement.md` Section 2.1 GIT ISOLATION SETUP
- CLI: `scripts/conductor_cli.py` lines 170-193
- Handler: `scripts/commands/implement.py`
