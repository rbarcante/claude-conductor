# Specification: Programmatic Token Optimization — Batch CLI Commands

## Overview

Add 6 new batch CLI commands to `conductor_cli.py` that consolidate multiple individual tool calls into single structured JSON responses. These commands target the execution-layer token consumption (22,500-86,000 tokens/session), which is 2-6x larger than instruction tokens. Each command replaces 3-8 individual tool calls with one CLI invocation returning filtered, summarized data.

## Functional Requirements

### FR-1: `implement git-snapshot` command

- Consolidate 6-8 git commands (branch detection, status, diff, reflog) into a single call
- Return structured JSON with: current branch, base branch (auto-detected via reflog), uncommitted changes summary, diff stats, changed file list, filtered diff content
- Support `--exclude <paths>` to filter out conductor paths from diff
- Support `--diff-stat-only` flag for lightweight queries
- **New standalone module:** `scripts/commands/git_snapshot.py`

### FR-2: `codereview filtered-diff` command

- Generate filtered, size-capped git diff between current branch and a base branch
- Return JSON with: stats, language breakdown, per-file stats, filtered diff content
- Support `--exclude <paths>` for path filtering
- Support `--max-lines <N>` to cap diff size (truncation with indicator)
- **New standalone module:** `scripts/commands/codereview.py`

### FR-3: `tracks parse-plan <track_id>` command

- Parse a track's `plan.md` into structured JSON with phases, tasks, status markers
- Return: phase hierarchy, task descriptions with status (pending/in_progress/completed), line numbers, summary counts, next pending task
- **New standalone module:** `scripts/commands/tracks.py`

### FR-4: `tracks update-task <track_id> <phase> <task_index> <status>` command

- Programmatically update task status markers (`[ ]`, `[~]`, `[x]`) in `plan.md` by phase index and task index
- Return confirmation with old/new status

### FR-5: `tracks read-context <track_id>` command

- Consolidate 3-5 separate file reads (spec.md, plan.md, metadata.json) into a single call
- Return JSON with all track context, plan already parsed (no need for separate parse-plan call)
- Support `--include spec,plan,metadata` filter

### FR-6: `implement batch-match-patterns --plan <track_id>` command

- Extract keywords from ALL tasks in a plan and match patterns in bulk
- Return per-task pattern matches in a single response (replaces N individual `match-patterns` calls)
- **Added as subcommand to existing:** `scripts/commands/implement.py`

## Non-Functional Requirements

- **NFR-1:** Each command returns structured JSON (`{"success": bool, "data": {...}, "message": str}`) following the existing CLI convention
- **NFR-2:** All commands must be registered in `conductor_cli.py` with proper argparse subparsers
- **NFR-3:** Commands are standalone modules — minimal coupling to existing libs (may import `FileResolver`, `GitOps` for utilities but not as hard dependencies)
- **NFR-4:** Unit tests required for each command (JSON output validation, edge cases)
- **NFR-5:** No breaking changes to existing CLI commands

## Acceptance Criteria

- [ ] All 6 commands registered and callable via `conductor_cli.py --json <command> <subcommand>`
- [ ] `git-snapshot` returns correct branch, base branch detection, and filtered diff
- [ ] `filtered-diff` respects `--max-lines` and `--exclude` flags, returns language stats
- [ ] `parse-plan` returns correct phase/task hierarchy matching TracksParser output
- [ ] `update-task` correctly modifies plan.md status markers
- [ ] `read-context` returns consolidated track files in single JSON response
- [ ] `batch-match-patterns` returns per-task pattern matches for all tasks in a plan
- [ ] Unit tests pass for all 6 commands
- [ ] Existing CLI commands remain unaffected

## Out of Scope

- Command markdown rewrites (implement.md, codeReview.md, setup.md) — deferred to Phase 2 track
- Programmatic Tool Calling (PTC) exploration — deferred to Phase 3 track
- Token measurement/benchmarking infrastructure
- Changes to existing command behavior
