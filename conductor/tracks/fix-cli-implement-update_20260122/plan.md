# Implementation Plan: Fix CLI implement update-status track detection

> **Track ID:** `fix-cli-implement-update_20260122`

## Overview

Fix the path format mismatch in `newtrack.py` where the `register` command generates `./tracks/{track_id}/` but should generate `./conductor/tracks/{track_id}/`.

---

## Phase 1: Fix and Verification

- [x] Task: Write failing test for newtrack register path format [1bacd9e]
    - [x] Create test that verifies register generates `./conductor/tracks/` format
    - [x] Run test and confirm it fails

- [x] Task: Fix path format in newtrack.py [1bacd9e]
    - [x] Update `_create_track_entry()` at line 493 to use `./conductor/tracks/{track_id}/`
    - [x] Run tests and confirm they pass

- [x] Task: Verify fix with integration test [1bacd9e]
    - [x] Test full flow: register track, then update-status
    - [x] Confirm no errors

- [~] Task: Conductor - User Manual Verification 'Phase 1: Fix and Verification' (Protocol in workflow.md)

---

## Notes

**Root Cause:** `newtrack.py:493` creates `./tracks/{track_id}/` but `implement.py` expects `./conductor/tracks/{track_id}/`.

**Fix Location:** `scripts/commands/newtrack.py` line 493
