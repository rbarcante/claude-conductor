# Architecture Decisions

## ADR-001: Remove tracks.md in favor of directory scan

**Status:** Accepted
**Date:** 2026-02-20

### Context
`conductor/tracks.md` is a shared central registry that all parallel development branches must modify when creating or updating tracks. This causes merge conflicts during simultaneous track development, blocking productive parallel work (Issue #41).

### Decision
Replace `tracks.md` with directory scanning of `conductor/tracks/*/metadata.json`. All the data stored in `tracks.md` (track ID, description, status, path) is fully redundant with each track's individual `metadata.json`. The `archive/` subdirectory convention already exists and distinguishes active from archived tracks.

### Why keep `newtrack register`?
Rather than removing the `register` subcommand, repurpose it as a **metadata quality gate**. The LLM may create track directories with missing or malformed `metadata.json` fields. The `register` command validates, normalizes, and backfills `metadata.json` to ensure consistent, canonical data — preventing status string inconsistencies (`"in-progress"` vs `"in_progress"` vs `"new"`) from causing downstream parse failures.

### Consequences
- Merge conflicts during parallel development are eliminated (each track only modifies its own directory)
- `tracks.md` is deleted permanently
- Major version bump required (breaking change for any tooling that reads `tracks.md` directly)
- Migration script provided to backfill any `metadata.json` files that may be missing from older environments
- `status verify` now checks for `conductor/tracks/` directory existence instead of `tracks.md` file existence
