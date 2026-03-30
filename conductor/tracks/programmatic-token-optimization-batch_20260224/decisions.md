# Decisions: Programmatic Token Optimization — Batch CLI Commands

> Architecture Decision Records for this track.

## ADR-001: Standalone Command Modules Over Extending Existing

**Date:** 2026-02-24
**Status:** Accepted

**Context:** Several proposed CLI commands overlap with existing utilities (TracksParser already has parse_plan, GitOps has get_current_branch/show_diff). The question was whether to extend existing modules or create standalone ones.

**Decision:** Create standalone command modules (`git_snapshot.py`, `codereview.py`, `tracks.py`) with minimal coupling to existing libs.

**Consequences:**
- (+) Clear ownership and boundaries per module
- (+) Easier to test in isolation
- (+) No risk of breaking existing commands
- (-) Some code duplication with existing utilities
- (-) Larger total codebase

## ADR-002: Phase 1 Scope — CLI Commands Only

**Date:** 2026-02-24
**Status:** Accepted

**Context:** The full optimization plan has 3 phases: CLI commands, command markdown rewrites, and PTC exploration. Implementing all at once risks scope creep.

**Decision:** Scope this track to Phase 1 only (new CLI batch commands). Command rewrites and PTC exploration deferred to future tracks.

**Consequences:**
- (+) Focused, deliverable scope
- (+) Commands can be tested independently before rewriting protocols
- (+) Lower risk of breaking existing workflows
- (-) Full token savings not realized until Phase 2 track completes
