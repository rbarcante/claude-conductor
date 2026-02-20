# Spec: Fix tracks.md Format Inconsistency

**Track ID:** fix-tracks-format-inconsistency_20260220
**Type:** bugfix
**Issue:** https://github.com/rbarcante/claude-conductor/issues/46

---

## Overview

There is a format mismatch between what `conductor setup` / `conductor newtrack register`
write to `conductor/tracks.md` and what `TracksParser.parse_tracks_registry()` can read.
This causes `conductor status` to return an empty tracks list even after tracks are registered.

The fix has two sides:
1. **Writer fix:** Ensure `newtrack register` and `setup scaffold` always write the canonical checkbox format
2. **Reader fix:** Update `TracksParser` to also parse Markdown table format for backward compatibility with any existing files that contain table entries

---

## Functional Requirements

### FR-1: Writer produces correct checkbox format

- `newtrack register` MUST write track entries in the canonical checkbox format:
  ```
  - [ ] **Track: {description}**
    *Link: [{track_id}](./conductor/tracks/{track_id}/)*
  ```
- `setup scaffold` MUST initialize `tracks.md` with a checkbox-compatible structure
- No table-row format shall be written by any command going forward

### FR-2: Reader parses both formats (backward compatibility)

- `TracksParser.parse_tracks_registry()` MUST parse the existing checkbox format (unchanged behavior)
- `TracksParser.parse_tracks_registry()` MUST ALSO parse the Markdown table format:
  ```
  | ID | Title | Status | Created |
  |----|-------|--------|---------|
  | my-track_20260220 | My Track Title | in-progress | 2026-02-20 |
  ```
- Table rows are mapped to `Track` objects with correct `track_id`, `description`, and `status`
- Status column values (e.g., `in-progress`, `pending`, `completed`) are mapped to internal status types
- Separator rows (`|---|...|`) are skipped

---

## Non-Functional Requirements

- NFR-1: No breaking changes to existing `Track` data model or downstream consumers
- NFR-2: All existing checkbox-format `tracks.md` files must continue to parse identically
- NFR-3: Fix is covered by unit tests for both writer and reader paths
- NFR-4: Code coverage ≥ 80% for all modified files

---

## Acceptance Criteria

1. Running `conductor setup` → `conductor newtrack` → `conductor --json status` returns a non-empty `"tracks"` list
2. A `tracks.md` using table format is fully parsed by `TracksParser` with correct `track_id`, `description`, and `status`
3. A `tracks.md` using checkbox format continues to parse with no regression
4. A `tracks.md` using mixed formats (both checkbox and table entries) is parsed correctly
5. Unit tests cover: writing a track entry, parsing checkbox format, parsing table format, and mixed-format files

---

## Out of Scope

- Migrating existing `tracks.md` files (parser backward compatibility handles them at read time)
- Changes to the `Track` data model fields
- Changes to any conductor commands beyond `setup scaffold`, `newtrack register`, and `TracksParser`
