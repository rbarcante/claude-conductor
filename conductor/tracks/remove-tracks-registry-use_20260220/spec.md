# Remove tracks.md: Replace with Directory-Scan Approach

## Overview
Eliminate `conductor/tracks.md` as the central track registry. All reads and writes
to this file are replaced by directory scanning of `conductor/tracks/*/metadata.json`.
This is a breaking change shipped as a major version bump.

## Problem
`tracks.md` is a shared file modified by all parallel branches, causing merge conflicts
during simultaneous track development (Issue #41).

## Functional Requirements

**FR-1: Directory-scan replaces tracks.md parsing**
`TracksParser.scan_tracks_directory()` reads all `conductor/tracks/*/metadata.json`
(active) and optionally `conductor/tracks/archive/*/metadata.json` (archived). Returns
`List[Track]` with the same interface as the removed `parse_tracks_registry()`.

**FR-2: Status updates write to metadata.json only**
`implement update-status` updates only `metadata.json` (status + updated_at).

**FR-3: `newtrack register` becomes metadata validator/enforcer**
`register` no longer touches `tracks.md`. Instead, it:
- Verifies the track directory exists (error if not)
- Reads `metadata.json`; creates with defaults if missing
- Validates all required fields: track_id, type, status, created_at, updated_at, description
- Normalizes status strings to canonical form (e.g. `"in-progress"` → `"in_progress"`)
- Backfills any missing fields with sensible defaults
- Writes validated `metadata.json` back

Acts as a post-scaffold quality gate to prevent LLM-generated malformed metadata.

**FR-4: verify-setup checks directory, not file**
`status verify` validates `conductor/tracks/` directory exists, not `tracks.md`.

**FR-5: Migration script provided**
A one-time `scripts/migrate_remove_tracks_md.py` script verifies all tracks in
`tracks.md` have corresponding `metadata.json` files, backfilling any missing ones
before `tracks.md` is deleted. Script is idempotent and safe to run multiple times.

## Non-Functional Requirements
- No data loss during migration
- All existing CLI commands continue to work post-migration
- Major version bump to signal breaking change

## Acceptance Criteria
- [ ] `conductor/tracks.md` is deleted
- [ ] `conductor status` shows correct track list via directory scan
- [ ] `implement update-status` updates metadata.json (not tracks.md)
- [ ] `newtrack register` validates/enforces metadata.json format
- [ ] Migration script validates/backfills metadata.json from tracks.md
- [ ] All unit tests pass
- [ ] Parallel branch development no longer modifies any shared file in conductor/

## Out of Scope
- Changing the metadata.json schema
- Changing how plan.md task status is tracked
