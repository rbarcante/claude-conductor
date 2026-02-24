# Implementation Plan: Programmatic Token Optimization — Batch CLI Commands

## Phase 1: Git Snapshot Command (`git-snapshot`)

- [ ] Task: Create `scripts/commands/git_snapshot.py` module with base branch detection via git reflog, current branch, uncommitted changes summary, diff stats, and filtered diff content
- [ ] Task: Add `--exclude` and `--diff-stat-only` argument support with path filtering logic
- [ ] Task: Register `git-snapshot` subcommand under `implement` in `conductor_cli.py` with argparse definitions
- [ ] Task: Write unit tests for git-snapshot (branch detection, exclude filtering, diff-stat-only mode, edge cases: detached HEAD, no upstream)
- [ ] Task: Conductor - User Manual Verification 'Git Snapshot Command' (Protocol in workflow.md)

## Phase 2: Filtered Diff Command (`filtered-diff`)

- [ ] Task: Create `scripts/commands/codereview.py` module with filtered diff generation, language detection from file extensions, and per-file stats
- [ ] Task: Add `--exclude`, `--max-lines` argument support with diff truncation logic and truncation indicator
- [ ] Task: Register `codereview filtered-diff` subcommand in `conductor_cli.py`
- [ ] Task: Write unit tests for filtered-diff (language stats, max-lines truncation, exclude paths, empty diff, large diff handling)
- [ ] Task: Conductor - User Manual Verification 'Filtered Diff Command' (Protocol in workflow.md)

## Phase 3: Track Operations Commands (`parse-plan`, `update-task`, `read-context`)

- [ ] Task: Create `scripts/commands/tracks.py` module with `parse-plan` subcommand — parse plan.md into phases/tasks/status JSON with line numbers and summary counts
- [ ] Task: Add `update-task` subcommand — modify task status markers in plan.md by phase index and task index, return old/new status
- [ ] Task: Add `read-context` subcommand — consolidate spec.md, plan.md (pre-parsed), and metadata.json into single JSON response with `--include` filter
- [ ] Task: Register all three subcommands under `tracks` in `conductor_cli.py`
- [ ] Task: Write unit tests for all three track commands (parse accuracy, status update correctness, context consolidation, missing file handling)
- [ ] Task: Conductor - User Manual Verification 'Track Operations Commands' (Protocol in workflow.md)

## Phase 4: Batch Match Patterns Command

- [ ] Task: Add `batch-match-patterns` subcommand to `scripts/commands/implement.py` — extract keywords from all plan tasks and match patterns in bulk, returning per-task results
- [ ] Task: Register `batch-match-patterns` subcommand in `conductor_cli.py` under `implement`
- [ ] Task: Write unit tests for batch-match-patterns (multi-task extraction, scoring aggregation, empty plan handling)
- [ ] Task: Conductor - User Manual Verification 'Batch Match Patterns Command' (Protocol in workflow.md)
