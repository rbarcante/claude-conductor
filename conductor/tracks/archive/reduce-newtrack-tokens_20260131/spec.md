# Specification: Reduce Token Usage in newTrack → implement Workflow

## Overview

The `newTrack → implement` workflow is consuming excessive tokens due to verbose protocol documentation, redundant file reads, and overly detailed context injection. This track addresses token optimization to reduce costs and improve response times.

## User Workflow Pain Point

The typical user workflow is:
1. Run `newTrack` command → loads all context
2. **Clear context** (start fresh session)
3. Run `implement` command → **reloads ALL context again**

The issue is that `implement` must reload everything from scratch, including the massive command protocol files.

## Problem Analysis

### Current Token Consumption Sources

| Source | Lines | Load Trigger | Impact |
|--------|-------|--------------|--------|
| CLAUDE.md (system context) | 339 | Every command | **Very High** |
| **implement.md** | **684** | On implement | **Very High** |
| conductor-methodology skill | 283 | Always-active | **Very High** |
| newTrack.md command | 544 | On newTrack | **High** |
| workflow.md | 359 | Read during implement | **High** |
| track spec.md + plan.md | ~200+ | On implement | **High** |
| tech-stack.md | 370 | Skill matching | **Medium** |

**Estimated Total Context for implement**: ~2,500+ lines before even reading the track

### Root Causes

1. **implement.md is massive (684 lines)**: Contains inline protocols that could be externalized:
   - Quality Gate Protocol (lines 248-459): ~211 lines
   - Decision Capture Protocol (lines 462-573): ~111 lines
   - Documentation Sync Protocol (lines 585-643): ~58 lines
   - Track Cleanup Protocol (lines 646-684): ~38 lines

2. **CLAUDE.md verbosity (339 lines)**: Contains full Skill Loading Protocol (231 lines) with detailed scoring tables, dependency resolution, error handling - loaded even when skills aren't used

3. **conductor-methodology skill always-active (283 lines)**: Loaded for every command, even when only ~50 lines are relevant

4. **Repeated examples in command files**: Same JSON structure patterns repeated multiple times

5. **Protocol files inlined instead of referenced**: Commands contain full protocol text instead of short references

## Functional Requirements

### FR-1: Modularize implement.md Command (HIGHEST PRIORITY)
- Extract Quality Gate Protocol (~211 lines) to `protocols/quality-gate.md`
- Extract Decision Capture Protocol (~111 lines) to `protocols/decision-capture.md` (already exists, just reference it)
- Keep only workflow skeleton and protocol references in command file
- Target: Reduce implement.md from 684 lines to ~250 lines

### FR-2: Modularize CLAUDE.md Protocols
- Extract Skill Loading Protocol to separate reference file
- Extract Pattern Resolution Protocol to separate reference file
- Keep only essential pointers in CLAUDE.md
- Load full protocols only when needed

### FR-4: Condense newTrack.md Command
- Replace repeated AskUserQuestion JSON examples with single reference
- Create `templates/askuserquestion-patterns.md` for full examples
- Keep only one example per question type in command file
- Target: Reduce from 544 lines to ~300 lines

### FR-5: Create Lightweight Skill Summaries
- Add optional `SKILL-SUMMARY.md` (30-50 lines) for always-active skills
- Load summary by default, full SKILL.md only on explicit reference
- Update Skill Loading Protocol to support this pattern

## Non-Functional Requirements

### NFR-1: Token Reduction Target
- Reduce implement.md from 684 lines to <250 lines (60% reduction)
- Reduce CLAUDE.md from 339 lines to <150 lines (55% reduction)
- Reduce newTrack.md from 544 lines to <300 lines (45% reduction)
- Reduce conductor-methodology always-active from 283 to <50 lines (80% reduction)

### NFR-2: Backward Compatibility
- Existing commands must continue to work
- No changes to user-facing workflow

### NFR-3: Maintainability
- Modular structure should be easy to extend
- Clear documentation for where each piece lives

## Acceptance Criteria

1. [ ] **implement.md reduced to <250 lines** (from 684) - HIGHEST IMPACT
2. [ ] CLAUDE.md reduced to <150 lines (from 339)
3. [ ] newTrack.md reduced to <300 lines (from 544)
4. [ ] conductor-methodology summary <50 lines
5. [ ] All existing commands pass manual testing
6. [ ] Protocol references work correctly (lazy loading)

## Out of Scope

- Changes to the actual workflow logic
- New features or commands
- Python CLI script changes (unless required for optimization)
