# Implementation Plan: CodeReview save prompt — deduplicate with implement

## Phase 1: Add Save Section to codeReview.md

- [ ] Task 1.1: Add Section 5.4 "Save Review" to `commands/codeReview.md`
  - [ ] Sub-task 1.1.1: Add track detection — scan `conductor/tracks/*/metadata.json` to match current git branch to a registered track
  - [ ] Sub-task 1.1.2: Add AskUserQuestion prompt:
    - If track detected: "Save to track" / "Save to file" / "Skip"
    - If no track: "Save to file" / "Skip"
  - [ ] Sub-task 1.1.3: Save-to-track: write report to `conductor/tracks/<track_id>/review.md`, update track `index.md`
  - [ ] Sub-task 1.1.4: Standalone save: ensure `conductor/reviews/` exists, write to `conductor/reviews/<branch_name>_<YYYY-MM-DD>.md`
  - [ ] Sub-task 1.1.5: Skip: display "Review not saved." and end
- [ ] Task 1.2: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Replace implement.md Section 3.7

- [ ] Task 2.1: Replace Sections 3.7.1–3.7.4 in `commands/implement.md` with:
  - [ ] Sub-task 2.1.1: Keep the prompt asking "All tasks complete. Run automated code review before finalizing?" with options "Run code review (Recommended)" / "Skip"
  - [ ] Sub-task 2.1.2: If user selects review: invoke `/conductor:codeReview` via the Skill tool (passing the base branch)
  - [ ] Sub-task 2.1.3: After codeReview completes (which now includes save prompt): return to finalization
  - [ ] Sub-task 2.1.4: Remove all inline diff generation (3.7.2), parallel agent launch (3.7.3), and report save (3.7.4) logic
- [ ] Task 2.2: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
