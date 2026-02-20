# Code Review Report

**Branch:** `refactor/remove-tracks-registry` vs `origin/master`
**Generated:** 2026-02-20
**Track:** Remove tracks.md registry, use directory scan via conductor_cli.py

---

## Summary

| Metric | Value |
|--------|-------|
| Files Changed | 20 |
| Lines Added | +845 |
| Lines Removed | -484 |
| **Findings** | 🔴 High: 1 | 🟡 Medium: 11 | 🟢 Low: 11 |

---

## Code Quality

### High Severity

- **`status.py:209` — `calculate_progress()` iterates archive/ without filtering**
  The function calls `tracks_dir.iterdir()` which includes the `archive/` directory. While the `plan_file.exists()` guard means archived sub-tracks are not double-counted (only `archive/` itself is visited, not `archive/<track_id>/`), this is architecturally inconsistent with all other functions that explicitly skip `archive/`. Add `if track_dir.name == "archive": continue` for clarity and future safety.

### Medium Severity

- **`tracks_parser.py` — Duplicate scan loop**: active-track and archive-track scan loops are ~25 lines of near-identical code. Extract a private `_scan_directory()` helper.
- **`tracks_parser.py:116` — `import json as _json` inside method**: Move to top-level imports.
- **`tracks_parser.py:133` — Bare `except Exception: continue`**: Silently swallows all JSON parse errors. Log a warning or collect errors for user visibility.
- **`status.py` / `implement.py` — Duplicate `parse_tracks()` enrichment logic**: Both functions scan tracks, extract metadata, resolve plans, and build track data with near-identical structure. Extract a shared helper.
- **Status normalization fragmented** across `tracks_parser.py`, `implement.py`, `newtrack.py` with slightly different mapping tables. Centralize in `TracksParser._string_to_status()`.
- **`newtrack.py:301` — Dead setdefault**: `metadata.setdefault("track_id", track_id)` is immediately overwritten by `metadata["track_id"] = track_id` 8 lines later. Remove the setdefault.

### Low Severity

- **`datetime.utcnow()` deprecated** (Python 3.12+) in `implement.py`, `newtrack.py`, `migrate_remove_tracks_md.py`, `json_manager.py`. Use `datetime.now(timezone.utc)`.
- **`Track.raw_line` field** is now always `""` — ideal candidate for removal in this major version.
- **Inline `from datetime import datetime` imports** in `update_status()` and `register()`. Move to file top.

---

## Security Analysis

### Critical/High Severity

No critical or high severity security vulnerabilities detected. The codebase is a local CLI tool operating on the user's own project files.

### Medium Severity

- **Path traversal via unsanitized `track_id`** (3 locations): `json_manager.py`, `migrate_remove_tracks_md.py`, `newtrack.py` all interpolate `track_id` directly into filesystem paths without validation. A `track_id` like `../../malicious` could escape the `conductor/tracks/` boundary. Risk is limited to local use but recommend a shared validation function:
  ```python
  def validate_track_id(track_id: str) -> bool:
      return bool(re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,100}', track_id))
  ```

- **`newtrack.py:319` — Pass-through of unrecognized status values**: `status_map.get(status_raw, status_raw)` stores unknown strings as-is. Default unknown values to `"pending"` instead.

### Low Severity

- **`json_manager.py:79` — `mkdir(parents=True)`** without path containment check. Add `assert full_path.resolve().is_relative_to(self.project_root)` after resolving.
- **Silent skip of corrupt `metadata.json`**: No audit trail when a file fails to parse.
- **Exception message in migration warnings**: `str(e)` could expose partial file content in error messages.

---

## Test Coverage

### Missing Tests (High Priority)

- **`revert.py:parse_registry()`** — Completely rewritten, zero dedicated unit tests. Add: priority sorting test, excludes-archived test, empty-directory test.
- **Corrupt `metadata.json` skip** — `scan_tracks_directory()` silently skips corrupt files; no test verifies this behavior.
- **`update_status()` with no existing metadata.json** — New code path in `implement.py` creates minimal metadata when file absent; not tested.

### Insufficient Coverage

- **`implement.py:parse_tracks()` filters** — `track_id_filter` and `status_filter` paths untested.
- **`update_status()` invalid status rejection** — No test for `status="invalid"` path.
- **Migration table-format parsing** — `parse_tracks_md()` table branch has zero test coverage.
- **Migration `dry_run=True`** — Not tested; could silently write files.
- **`register()` missing track directory error** — `success=False` path untested.

### Files With Tests

All 6 changed source files have corresponding test files.

---

## Recommendations

**Priority Actions (address before merging):**
1. Fix `calculate_progress()` to explicitly skip `archive/` directory
2. Add `track_id` validation against allowlist pattern at CLI entry points
3. Add dedicated tests for `revert.py:parse_registry()`
4. Add test for corrupt `metadata.json` graceful skip

**Suggested Improvements:**
1. Move `datetime.utcnow()` to `datetime.now(timezone.utc)` (deprecation fix)
2. Extract duplicate `_scan_directory()` helper in `TracksParser`
3. Centralize status normalization into one function
4. Add migration table-format test

---

*Auto-review generated by `/conductor:implement` on track completion*
