# Specification: Reduce Token Usage in newTrack → implement Workflow

## Overview

The `newTrack → implement` workflow is consuming excessive tokens due to verbose protocol documentation, redundant file reads, and overly detailed context injection. This track addresses token optimization to reduce costs and improve response times.

## Problem Analysis

### Current Token Consumption Sources

| Source | Lines | Load Trigger | Impact |
|--------|-------|--------------|--------|
| CLAUDE.md (system context) | 339 | Every command | **Very High** |
| conductor-methodology skill | 283 | Always-active | **Very High** |
| newTrack.md command | 544 | On newTrack | **High** |
| workflow.md | 359 | Read 2x per newTrack | **High** |
| Conductor context files | 1,288 | Multiple reads | **High** |
| git-isolation.md protocol | 248 | newTrack section 1.2 | **Medium** |

**Estimated Total Context Loaded**: ~3,000+ lines per newTrack invocation

### Root Causes

1. **CLAUDE.md verbosity**: Contains full Skill Loading Protocol (231 lines) with detailed scoring tables, dependency resolution, error handling - loaded even when skills aren't used

2. **Repeated AskUserQuestion examples in newTrack.md**: The same JSON structure patterns are repeated 8+ times throughout the file

3. **conductor-methodology skill always-active**: 283 lines loaded for every command, even when only ~50 lines are relevant for newTrack

4. **Redundant file reads**: `workflow.md` read during setup check AND plan generation; context files potentially read multiple times

5. **Protocol files not modularized**: Full 248-line git-isolation.md loaded when only branch creation is needed

## Functional Requirements

### FR-1: Modularize CLAUDE.md Protocols
- Extract Skill Loading Protocol to separate reference file
- Extract Pattern Resolution Protocol to separate reference file
- Keep only essential pointers in CLAUDE.md
- Load full protocols only when needed

### FR-2: Condense newTrack.md Command
- Replace repeated AskUserQuestion JSON examples with single reference
- Create `templates/askuserquestion-patterns.md` for full examples
- Keep only one example per question type in command file
- Target: Reduce from 544 lines to ~300 lines

### FR-3: Create Lightweight Skill Summaries
- Add optional `SKILL-SUMMARY.md` (30-50 lines) for always-active skills
- Load summary by default, full SKILL.md only on explicit reference
- Update Skill Loading Protocol to support this pattern

### FR-4: Implement Context Caching Strategy
- Document which files should be read once per session
- Use file hash to detect changes vs re-reading full content
- Pass extracted context between workflow phases

### FR-5: Split conductor-methodology Skill
- Create separate "concepts" and "implementation" sections
- Load only "concepts" for newTrack
- Load full skill for implement command

## Non-Functional Requirements

### NFR-1: Token Reduction Target
- Reduce newTrack context from ~3,000 lines to ~1,500 lines (50% reduction)
- Reduce implement context by ~25%

### NFR-2: Backward Compatibility
- Existing commands must continue to work
- No changes to user-facing workflow

### NFR-3: Maintainability
- Modular structure should be easy to extend
- Clear documentation for where each piece lives

## Acceptance Criteria

1. [ ] CLAUDE.md reduced to <150 lines (from 339)
2. [ ] newTrack.md reduced to <300 lines (from 544)
3. [ ] conductor-methodology summary <50 lines
4. [ ] workflow.md read only once during newTrack
5. [ ] All existing commands pass manual testing
6. [ ] Protocol references work correctly (lazy loading)

## Out of Scope

- Changes to the actual newTrack workflow logic
- New features or commands
- Python CLI script changes (unless required for optimization)
- Pattern resolution changes (can be separate track)
