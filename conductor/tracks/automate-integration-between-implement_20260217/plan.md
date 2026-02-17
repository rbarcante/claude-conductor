# Implementation Plan: Automate integration between implement and codeReview commands

## Phase 1: Base Branch Detection Utility

- [ ] Task: Add base branch detection logic to `implement.md`
  - [ ] Sub-task: Research git commands for reliably detecting the originating branch (`git merge-base`, `git log --all --oneline`)
  - [ ] Sub-task: Define the detection algorithm in a reusable protocol section or inline in implement.md
  - [ ] Sub-task: Add fallback logic (default branch detection) when originating branch cannot be determined
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Auto-trigger Code Review on Track Completion

- [ ] Task: Modify `implement.md` Section 3.0 Step 6 (Finalize Track) to add code review trigger
  - [ ] Sub-task: Add a new step between task completion and track status update that invokes the code review pipeline
  - [ ] Sub-task: Add user prompt to skip/proceed with the review (using AskUserQuestion pattern)
  - [ ] Sub-task: Integrate the three specialist agents (code-quality-analyzer, security-scanner, test-coverage-analyzer) following codeReview.md's parallel execution pattern
  - [ ] Sub-task: Add fallback to sequential execution if parallel fails
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Report Generation and Persistence

- [ ] Task: Add review report generation logic to `implement.md`
  - [ ] Sub-task: Define the report format (reuse codeReview.md Section 7.0 format)
  - [ ] Sub-task: Add logic to write the report as `conductor/tracks/<track_id>/review.md`
  - [ ] Sub-task: Add logic to update the track's `index.md` with a link to `review.md`
  - [ ] Sub-task: Display the report to the user inline before proceeding with track finalization
- [ ] Task: Add `review.md` to track template documentation in relevant places (tech-stack.md track artifacts table, etc.)
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
