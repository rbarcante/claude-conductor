# Implementation Plan: Remove tracks.md (Major Version)

## Phase 1: Migration Script & Tests

### 1.1 Create migration script
- [ ] Task: Create `scripts/migrate_remove_tracks_md.py`
  - Parse `conductor/tracks.md` entries (active + archived)
  - For each entry: verify `metadata.json` exists; backfill missing fields from tracks.md data
  - Output migration report (tracks verified, backfilled, warnings)
  - Idempotent — safe to run multiple times

### 1.2 Write migration script tests
- [ ] Task: Add `scripts/tests/test_migration.py`
  - Test backfill of missing `metadata.json` from `tracks.md` entry
  - Test idempotency (run twice = same result, no overwrites)
  - Test missing `tracks.md` (no-op / graceful exit)

- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Refactor Core Library

### 2.1 Update TracksParser
- [ ] Task: Add `scan_tracks_directory(include_archived=True)` to `TracksParser`
  - Scan `conductor/tracks/` subdirs; skip `archive/` dir itself
  - Read `metadata.json` per subdir; skip dirs without it (graceful)
  - Optionally scan `conductor/tracks/archive/` when `include_archived=True`
  - Map all status variants: `"new"` → PENDING, `"in-progress"` → IN_PROGRESS, `"in_progress"` → IN_PROGRESS, `"completed"` → COMPLETED
  - Set `raw_line=""` for backward compat with `Track` dataclass
- [ ] Task: Remove markdown-parsing methods from `TracksParser`
  - Remove: `parse_tracks_registry()`, `update_track_status()`, `get_in_progress_items()`
  - Remove: `STATUS_PATTERN`, `TRACK_PATTERN`, `LINK_PATTERN`, `TABLE_ROW_PATTERN`, `TABLE_SEPARATOR_PATTERN`
  - Keep all plan-parsing methods and patterns unchanged
- [ ] Task: Remove `tracks_registry` from `FileResolver.PROJECT_DEFAULTS`

### 2.2 Write library tests
- [ ] Task: Add `scan_tracks_directory` tests to `scripts/tests/test_lib.py`
  - `test_scan_basic` — two track dirs with `metadata.json` returned correctly
  - `test_scan_excludes_archive_by_default` — `archive/` dir not included by default
  - `test_scan_includes_archive` — `include_archived=True` returns archived tracks
  - `test_scan_skips_missing_metadata` — dirs without `metadata.json` silently skipped
  - `test_scan_status_mapping` — all variants (`"new"`, `"in-progress"`, `"pending"`, `"completed"`)
  - `test_scan_empty_dir` — empty tracks dir returns empty list
- [ ] Task: Remove obsolete tests: `test_parse_tracks_registry*`, `test_update_track_status()`

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Update CLI Commands

### 3.1 Update `scripts/commands/status.py`
- [ ] Task: Remove `tracks_registry` from `verify_setup()` required_files dict
- [ ] Task: Update `parse_tracks()` — replace `parse_tracks_registry()` with `scan_tracks_directory()`
- [ ] Task: Update error message: `"Tracks directory (conductor/tracks/) not found"`

### 3.2 Update `scripts/commands/implement.py`
- [ ] Task: Update `parse_tracks()` — replace `parse_tracks_registry()` with `scan_tracks_directory()`
- [ ] Task: Rewrite `update_status()` — use `json_mgr.read/write_track_metadata()` only
  - Verify track directory exists first
  - Normalize `"in-progress"` → `"in_progress"` before writing
  - Update `updated_at` timestamp
  - Remove all tracks.md string manipulation code
- [ ] Task: Verify `archive()` needs no changes (already directory-only operations)

### 3.3 Refactor `scripts/commands/newtrack.py` register subcommand
- [ ] Task: Change `register()` from tracks.md writer to metadata validator/enforcer
  - Verify track directory exists (return error if not)
  - Read `metadata.json`; create with defaults if file missing
  - Validate required fields: `track_id`, `type`, `status`, `created_at`, `updated_at`, `description`
  - Normalize `status` to canonical underscore form
  - Backfill any missing fields with defaults
  - Write validated `metadata.json` back
- [ ] Task: Remove `_create_tracks_header()`, `_create_track_entry()` helpers
- [ ] Task: Remove "Active Tracks" / "Archived Tracks" section manipulation code

### 3.4 Update `scripts/commands/revert.py`
- [ ] Task: Update `parse_registry()` — replace tracks.md read with `scan_tracks_directory(include_archived=False)`
- [ ] Task: Remove `tracks_registry` path resolution

### 3.5 Update command tests in `scripts/tests/test_commands.py`
- [ ] Task: Remove `tracks.md` creation from `conductor_project` fixture
- [ ] Task: Update `test_verify_setup()` — tracks_registry no longer in required files
- [ ] Task: Update `test_verify_missing_files()` — remove tracks_registry expectation
- [ ] Task: Update `test_update_status()` — add assertion that `metadata.json` status field updated
- [ ] Task: Update `test_register()` — assert `metadata.json` is validated/normalized (not tracks.md written)

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Documentation & Deletion

### 4.1 Update LLM command docs
- [ ] Task: Update `commands/implement.md`
  - Update fallback instructions from "read tracks.md" to "scan metadata.json"
  - Remove tracks.md from code review filter exclusion list
  - Remove "update Tracks Registry" from update-status step
  - Remove "remove from tracks.md" from archive/finalize steps
- [ ] Task: Update `commands/status.md`
  - Update fallback step 2: replace tracks.md reference with metadata.json scan
- [ ] Task: Update `commands/newTrack.md`
  - Update register step description to reflect new validator role

### 4.2 Update conductor metadata
- [ ] Task: Update `conductor/index.md` — remove "Tracks Registry (./tracks.md)" link
- [ ] Task: Update `CLAUDE.md` — remove `Tracks Registry: conductor/tracks.md` from Standard Default Paths

### 4.3 Run migration & delete tracks.md
- [ ] Task: Run `python scripts/migrate_remove_tracks_md.py` — verify all tracks have valid `metadata.json`
- [ ] Task: Delete `conductor/tracks.md`
- [ ] Task: Run `python scripts/conductor_cli.py --json status full` — verify correct output

### 4.4 Bump major version
- [ ] Task: Update version in `package.json` (or version file) to next major version

- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
