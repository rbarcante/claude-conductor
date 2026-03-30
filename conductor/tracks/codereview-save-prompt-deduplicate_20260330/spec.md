# Specification: CodeReview save prompt — deduplicate with implement

## Overview

The `implement` command (Section 3.7) has its own inline code review flow that duplicates diff generation, agent launching, and report saving. The `codeReview` command has no save capability. This track:

1. Adds a "Save Review" section to `codeReview.md` so users can persist the report (track-aware or standalone).
2. Replaces `implement.md` Section 3.7 with a simple call to `/conductor:codeReview`, eliminating all duplicated logic. Since codeReview now includes the save prompt, implement gets it for free.

## Background

- **implement.md Section 3.7** (lines 267-327): Has its own diff generation, parallel agent launch, report generation, and save-to-track logic — all of which duplicates what `codeReview` already does (minus the save).
- **codeReview.md Section 5.3** (lines 228-232): Displays report and ends. No save.

## Functional Requirements

1. **FR-1: Save Prompt in codeReview** — After displaying the report, add Section 5.4 that asks the user via `AskUserQuestion` whether to save the review.
2. **FR-2: Track-Aware Save** — If a current track is detected (match current git branch to a registered track's metadata), save to `conductor/tracks/<track_id>/review.md` and update the track's `index.md`.
3. **FR-3: Standalone Save** — If no track detected, save to `conductor/reviews/<branch_name>_<date>.md`.
4. **FR-4: Skip Option** — User can decline saving.
5. **FR-5: Replace implement Section 3.7** — Replace the entire inline review (Sections 3.7.1–3.7.4) with: prompt user to run review → if yes, call `/conductor:codeReview` → return to finalization.

## Non-Functional Requirements

- `AskUserQuestion` constraints: 2-4 options, max 12-char header.
- Additive to codeReview sections 1.0–5.3 — no changes to report generation or display.

## Acceptance Criteria

- [ ] `codeReview` prompts to save after displaying the report
- [ ] Track-aware save writes to `conductor/tracks/<track_id>/review.md` and updates `index.md`
- [ ] Standalone save writes to `conductor/reviews/`
- [ ] User can skip saving
- [ ] `implement` Section 3.7 is replaced with a `/conductor:codeReview` invocation
- [ ] No duplicated diff generation, agent launching, or report logic in implement

## Out of Scope

- Review diffing or versioning
- Changing the report template format
