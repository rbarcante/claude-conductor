# Specification: Optimize implement.md context loading after newTrack flow

## Overview

When `/conductor:implement` is invoked immediately after `/conductor:newTrack` (via the "Start implementation" option), it redundantly reloads context that was just created in the same session — spec content, plan content, workflow file, and setup verification. This adds ~15%+ unnecessary tokens to the session context before any actual implementation work begins.

## Background

The `newTrack` → `implement` flow works as follows:
1. **newTrack Phase A** reads product.md, tech-stack.md, workflow.md, product-guidelines.md, composes spec + plan
2. **newTrack Phase B** creates the branch, writes spec.md + plan.md + metadata.json, commits
3. **newTrack Phase B step 7** invokes `conductor:implement` via Skill tool with the track ID

Then `implement` starts and:
- **Section 1.1**: Re-verifies setup (product.md, tech-stack.md, workflow.md exist) — already verified
- **Section 2.1**: Runs git isolation protocol — branch was just created, fast path catches this but still executes protocol steps
- **Section 3.0 Step 2**: Calls `read-context` which reloads the **entire spec + plan text** — just written seconds ago, still in conversation context
- **Section 3.0 Step 2**: Re-reads workflow.md — already read during newTrack
- **Section 3.0 Step 3**: `batch-match-patterns` re-parses the plan — just created

The spec and plan reload via `read-context` is the **largest single redundancy**, as these are full text documents loaded back into an already-populated context window.

## Functional Requirements

1. **FR-1: Warm Start Signal** — When `newTrack` invokes `implement`, it passes a `--warm-start` flag in the args (e.g., `skill: "conductor:implement", args: "<TRACK_ID> --warm-start"`)

2. **FR-2: Warm Start Detection** — `implement.md` detects the `--warm-start` flag in its arguments and activates a streamlined startup path

3. **FR-3: Streamlined Startup** — In warm start mode, implement skips or reduces:
   - Setup verification (Section 1.1) — skip entirely
   - Git isolation (Section 2.1) — skip entirely (branch just created)
   - Full spec reload — use `read-context --include plan,metadata` instead of loading all 3
   - ~~Workflow re-read~~ — **kept**: workflow.md is read during newTrack Phase A but lost when ExitPlanMode clears context, so it must be re-read

4. **FR-4: Preserve Essential Steps** — Warm start does NOT skip:
   - Base branch detection (Section 2.2) — still needed
   - Skill activation (Section 2.5) — new work, not done in newTrack
   - Pattern matching (Section 3.0 Step 3) — new work (matching logic)
   - Track status update to in-progress
   - Task iteration loop
   - Workflow re-read — lost after ExitPlanMode context clearing

## Non-Functional Requirements

- **NFR-1**: Reduce context overhead by ~10-15% when using warm start
- **NFR-2**: No behavior change when implement is invoked standalone (without --warm-start)
- **NFR-3**: Warm start is purely a prompt optimization — no CLI code changes needed

## Acceptance Criteria

- [ ] `newTrack` Phase B step 7 passes `--warm-start` when invoking implement
- [ ] `implement.md` has a warm start detection section after Section 1.0
- [ ] In warm start mode, setup check (1.1) is skipped
- [ ] In warm start mode, git isolation (2.1) is skipped
- [ ] In warm start mode, `read-context` uses `--include plan,metadata` (no spec)
- [ ] In warm start mode, workflow.md is still re-read (lost after ExitPlanMode context clearing)
- [ ] Standalone invocation (no --warm-start) behaves identically to current behavior

## Out of Scope

- CLI code changes (all changes are in the prompt files)
- Optimizing the `parse-tracks` context injection (line 19 of implement.md) — this is a lightweight scan
- Optimizing skill loading or pattern matching — these are new work, not redundant
