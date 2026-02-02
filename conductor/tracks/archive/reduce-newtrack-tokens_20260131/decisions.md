# Decisions Log: Reduce Token Usage in newTrack → implement Workflow

This document records Architecture Decision Records (ADRs) for this track.

---

## ADR-001: Use Protocol References Instead of Inline Content

**Date**: 2026-01-31
**Status**: Proposed

### Context
CLAUDE.md contains the full Skill Loading Protocol (231 lines) and Pattern Resolution Protocol (68 lines) inline. This content is loaded as system context for every command, even when not needed.

### Decision
Extract protocols to separate files in `protocols/` directory and replace inline content with short summaries plus file references. The AI will lazy-load full protocols only when needed.

### Consequences
- **Positive**: Reduces CLAUDE.md from 339 to ~150 lines
- **Positive**: Protocols only loaded when actually used
- **Negative**: Requires additional file read when protocol is needed
- **Mitigated**: Protocol reads are rare (only during implement with skill activation)

---

## ADR-002: Create Skill Summary Pattern

**Date**: 2026-01-31
**Status**: Proposed

### Context
The `conductor-methodology` skill is always-active and loads 283 lines for every command. Most of this content is detailed implementation guidance not needed for newTrack.

### Decision
Create a `SKILL-SUMMARY.md` pattern for skills. Always-active skills will load the summary by default. Full skill content loaded only when detailed guidance is needed.

### Consequences
- **Positive**: Reduces always-active overhead from 283 to ~40 lines
- **Positive**: Pattern applicable to future skills
- **Negative**: Requires maintaining two files per skill
- **Mitigated**: Summary can reference sections of full SKILL.md

---

## ADR-003: Consolidate Context Reads

**Date**: 2026-01-31
**Status**: Proposed

### Context
During newTrack, workflow.md is read at least twice (setup check + plan generation). Context files (product.md, tech-stack.md) may be read multiple times across phases.

### Decision
Read each context file exactly once during setup/initialization phase. Cache relevant extracted values (e.g., "Phase Completion Protocol exists: true") and pass to subsequent phases.

### Consequences
- **Positive**: Eliminates redundant file reads
- **Positive**: Faster execution
- **Negative**: Requires explicit context passing between phases
- **Mitigated**: Context passing is a well-established pattern
