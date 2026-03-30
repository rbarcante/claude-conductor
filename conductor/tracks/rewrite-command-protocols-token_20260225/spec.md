# Specification: Rewrite Command Protocols for Token Optimization

## Overview

Rewrite the three highest-token-consuming command protocols (`implement.md`, `codeReview.md`, `setup.md`) to use the batch CLI commands built in Phase 1 of the PTC plan. Each command becomes a thin wrapper that delegates bulk operations to CLI calls and focuses only on LLM-essential tasks (reasoning, generation, user interaction).

## Functional Requirements

### 1. `implement.md` Rewrite (634 -> ~300 lines)

- Replace Section 2.2 Base Branch Detection (58 lines of bash instructions) with single `implement git-snapshot` call
- Replace Section 3.0 Load Track Context (3 separate Reads) with single `tracks read-context` call
- Replace per-task `match-patterns` calls with single upfront `implement batch-match-patterns --plan <track_id>`
- Replace manual `plan.md` Edit operations with `tracks update-task` calls
- Replace Section 3.7 Auto Code Review (~220 lines) with delegation to `codereview filtered-diff` for diff generation, keep agent orchestration compact

### 2. `codeReview.md` Rewrite (538 -> ~250 lines)

- Replace Sections 2.2-2.4 (branch update, diff generation, stats parsing) with single `codereview filtered-diff` call
- Compress Sections 4.0/5.0/6.0 (inline analysis fallbacks, ~120 lines) into compact reference
- Use `filtered-diff` response's `languages` field instead of manual file-extension detection

### 3. `setup.md` Rewrite (527 -> ~350 lines)

- Compress verbose phase sections (2.0-2.5) — tighten prose, remove redundant protocol references
- Consolidate Section 3.0 track generation artifacts into more compact instructions

## Non-Functional Requirements

- Each rewritten command must produce identical outcomes (same files written, same git operations, same user interactions)
- No behavioral regressions — all existing protocol steps must still execute
- Commands must remain self-contained (no cross-command dependencies at runtime)

## Acceptance Criteria

- `implement.md` reduced to <=350 lines
- `codeReview.md` reduced to <=280 lines
- `setup.md` reduced to <=400 lines
- All CLI commands referenced use correct argument syntax
- Tool call count targets: implement 10-15, codeReview 8-12, setup 15-22

## Out of Scope

- Phase 3 PTC exploration (separate track)
- Changes to the Python CLI commands themselves (Phase 1 complete)
- Rewriting other commands (status, revert, patterns, etc.)
