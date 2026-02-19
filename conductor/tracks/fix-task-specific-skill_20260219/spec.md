# Specification: Fix task-specific skill activation in implement.md

## Overview

Task-specific skills (e.g., `typescript-best-practices`, `api-design`) are never activated during `/conductor:implement` execution. Only the always-active skill (`conductor-methodology`) loads. The root cause is that Phase 2 of the lazy skill loading approach (Section 2.5 of `implement.md`) defers scoring to a sub-step inside the task loop, but the model never re-executes the scoring logic per-task in practice.

**GitHub Issue:** #42

## Functional Requirements

1. **Consolidate skill activation upfront** — Move all skill scoring and activation to Section 2.5 (before task execution begins), using the full tech stack context from `conductor/tech-stack.md` and the track's spec/plan for keyword extraction.
2. **Remove Phase 2 per-task activation** — Eliminate the deferred lazy-loading instruction from Section 3.0 Step 5.c.i, replacing it with a reference to already-loaded skills.
3. **Update skill-loading.md protocol** — Align the Skill Loading Protocol to describe the consolidated upfront approach, removing the per-task scoring model.
4. **Preserve scoring logic** — The scoring algorithm (keywords +1.0, file patterns +1.5, language +2.0, framework +1.5, tools +1.0) and activation threshold (>= 1.5) remain unchanged.
5. **Update CLAUDE.md** — If the Skill Loading Protocol quick reference in CLAUDE.md references per-task activation, update it to reflect the consolidated approach.

## Non-Functional Requirements

- The fix must not increase upfront token usage significantly (skill SKILL.md files are only loaded for activated skills).
- The announcement format for activated skills must remain consistent with existing format.

## Acceptance Criteria

- [ ] When running `/conductor:implement` on a TypeScript project, `typescript-best-practices` skill is announced as activated during Section 2.5
- [ ] The per-task skill activation instruction (Step 5.c.i) is replaced with a reference to pre-loaded skills
- [ ] `protocols/skill-loading.md` describes a consolidated upfront approach
- [ ] Scoring table and thresholds remain unchanged
- [ ] Always-active skills continue to load as before

## Out of Scope

- Adding new skills to the registry
- Changing the scoring algorithm weights or thresholds
- CLI-based skill matching (skills use the in-protocol scoring, unlike patterns which use CLI)
