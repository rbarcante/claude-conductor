# Implementation Plan: Automate integration between implement and codeReview commands

## Phase 1: Base Branch Detection Utility

- [x] Task: Add base branch detection logic to `implement.md`
  - [x] Sub-task: Research git commands for reliably detecting the originating branch (`git merge-base`, `git log --all --oneline`)
  - [x] Sub-task: Define the detection algorithm in a reusable protocol section or inline in implement.md
  - [x] Sub-task: Add fallback logic (default branch detection) when originating branch cannot be determined
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Auto-trigger Code Review on Track Completion

- [x] Task: Modify `implement.md` Section 3.0 Step 6 (Finalize Track) to add code review trigger
  - [x] Sub-task: Add a new step between task completion and track status update that invokes the code review pipeline
  - [x] Sub-task: Add user prompt to skip/proceed with the review (using AskUserQuestion pattern)
  - [x] Sub-task: Integrate the three specialist agents (code-quality-analyzer, security-scanner, test-coverage-analyzer) following codeReview.md's parallel execution pattern
  - [x] Sub-task: Add fallback to sequential execution if parallel fails
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Report Generation and Persistence

- [x] Task: Add review report generation logic to `implement.md`
  - [x] Sub-task: Define the report format (reuse codeReview.md Section 7.0 format)
  - [x] Sub-task: Add logic to write the report as `conductor/tracks/<track_id>/review.md`
  - [x] Sub-task: Add logic to update the track's `index.md` with a link to `review.md`
  - [x] Sub-task: Display the report to the user inline before proceeding with track finalization
- [x] Task: Add `review.md` to track template documentation in relevant places (tech-stack.md track artifacts table, etc.)
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
