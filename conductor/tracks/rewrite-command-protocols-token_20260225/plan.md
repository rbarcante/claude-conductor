# Implementation Plan: Rewrite Command Protocols for Token Optimization

## Phase 1: Rewrite implement.md

- [ ] Task: Replace Section 2.2 Base Branch Detection with `implement git-snapshot` call — remove 58 lines of bash instructions, replace with single CLI call that returns base_branch in JSON
- [ ] Task: Replace Section 3.0 Load Track Context with `tracks read-context <track_id>` — consolidate 3 separate Read instructions into single CLI call
- [ ] Task: Replace per-task pattern matching (Section 3.0 Step 4) with `implement batch-match-patterns --plan <track_id>` — single upfront call, cache results
- [ ] Task: Replace manual plan.md Edit instructions with `tracks update-task` calls for task status updates
- [ ] Task: Replace Section 3.7 Auto Code Review (~220 lines) with delegation to `codereview filtered-diff` for diff generation, keep agent orchestration compact
- [ ] Task: Review and compress remaining sections (Skill Activation, Quality Gate, Decision Capture) for consistency
- [ ] Task: Verify all CLI command references use correct syntax and argument names

## Phase 2: Rewrite codeReview.md

- [ ] Task: Replace Sections 2.2-2.4 (branch update, diff generation, stats parsing) with single `codereview filtered-diff` call
- [ ] Task: Compress Sections 4.0/5.0/6.0 (inline analysis checklists, ~120 lines) into compact fallback reference
- [ ] Task: Simplify Section 3.0 execution strategy using `filtered-diff` language detection
- [ ] Task: Compress Section 7.0 report generation — keep template, remove redundant instructions
- [ ] Task: Verify all CLI command references and agent orchestration remain correct

## Phase 3: Rewrite setup.md

- [ ] Task: Compress verbose phase sections (2.0-2.5) — tighten prose, remove redundant protocol references
- [ ] Task: Consolidate Section 3.0 track generation artifacts into more compact instructions
- [ ] Task: Verify all CLI command references and state management remain correct
- [ ] Task: Conductor - User Manual Verification 'Rewrite setup.md' (Protocol in workflow.md)
