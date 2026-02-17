# Specification: Automate integration between implement and codeReview commands

## Overview

Add an automated code review step to the `/conductor:implement` command that triggers a full code review (using the `/conductor:codeReview` protocol) when a track reaches completion. The review report is saved as `review.md` in the track folder for traceability.

## Functional Requirements

### 1. Auto-trigger on Track Completion

When all tasks in a track's `plan.md` are marked complete (Section 3.0, Step 6 "Finalize Track"), the system automatically invokes the codeReview analysis pipeline before marking the track as completed.

### 2. Full Code Review Execution

The auto-triggered review follows the codeReview protocol:
- Generates a diff between the track's branch and the originating branch (the branch from which the track branch was created)
- Runs all three specialist agents in parallel: `code-quality-analyzer`, `security-scanner`, `test-coverage-analyzer`
- Falls back to sequential analysis if parallel execution fails

### 3. Report Generation and Persistence

- Generate a structured Code Review Report following the existing codeReview report format (Section 7.0 of codeReview.md)
- Save the report as `conductor/tracks/<track_id>/review.md`
- Add the report file to the track's `index.md`

### 4. Non-Blocking Behavior

The review is informational only:
- The report is displayed to the user and saved
- Track completion proceeds regardless of findings
- High-severity findings are highlighted with a warning but do not block

### 5. Base Branch Detection

Determine the base branch by finding the branch the current track branch was created from:
- Use `git merge-base --fork-point` or `git log --oneline --decorate` to identify the originating branch
- This is the branch used for the `git diff` comparison in the code review
- If detection fails, fall back to the project's default branch (master/main/develop) and inform the user

## Non-Functional Requirements

- The integration should not significantly increase the token cost of a typical `/conductor:implement` session (the review happens once at the end)
- The review step should be skippable via user prompt (in case they want to run it separately)
- Must work with both parallel and sequential agent execution modes

## Acceptance Criteria

- [ ] When a track's last task is completed, a code review is automatically triggered
- [ ] The review uses all three specialist agents (code-quality, security, test-coverage)
- [ ] A `review.md` file is generated and saved in the track folder
- [ ] The track's `index.md` is updated to link to `review.md`
- [ ] The user is shown the review report before track finalization
- [ ] Track completion proceeds regardless of review findings (non-blocking)
- [ ] The user can skip the review step when prompted
- [ ] The base branch is automatically detected as the originating branch of the track's feature branch

## Out of Scope

- Modifying the per-task quality gate in implement.md (Section 3.5)
- Changing the standalone `/conductor:codeReview` command behavior
- Adding new specialist agents
- PR creation integration (could be a future track)
