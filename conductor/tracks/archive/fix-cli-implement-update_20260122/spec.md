# Specification: Fix CLI implement update-status track detection

> **Type:** bugfix
> **Track ID:** `fix-cli-implement-update_20260122`

## Overview

The `conductor_cli.py implement update-status` command fails for tracks registered via CLI due to incorrect path format in `newtrack register`.

## Problem Analysis

**Root Cause:** `newtrack.py:493` generates `./tracks/{track_id}/` but `update_status` expects `./conductor/tracks/{track_id}/`.

| Component | Format Used |
|-----------|-------------|
| `newtrack.py:493` (register) | `./tracks/{track_id}/` |
| Existing tracks.md entries | `./conductor/tracks/{track_id}/` |
| `implement.py:213` (fallback search) | `conductor/tracks/{track_id}` |

## Functional Requirements

1. **FR-1**: Fix `newtrack register` to use path format `./conductor/tracks/{track_id}/`

## Acceptance Criteria

- [ ] `newtrack register` creates links with `./conductor/tracks/{track_id}/` format
- [ ] `update-status` works for newly registered tracks
- [ ] Existing tests pass

## Out of Scope

- Backward compatibility for incorrect `./tracks/` format
- Fixing existing tracks.md entries (they already use correct format)

## References

- Bug report: `implement update-status` returns "Could not find track" for `git-branch-worktree-integration_20260122`
- Root cause file: `scripts/commands/newtrack.py` line 493
