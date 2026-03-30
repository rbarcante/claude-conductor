## Implementation Plan

### Phase 1: Remove sequential option from codeReview.md

- [x] Task 1.1: Remove Section 3.1 (the AskUserQuestion prompt for parallel vs sequential)
- [x] Task 1.2: Update Section 3.2 — rename to main execution path, remove "(Preferred)" qualifier
- [x] Task 1.3: Update Section 3.3 — rename to "Inline Fallback (Agent Failure Only)", remove "If user selects Sequential" references, keep checklists as error-only fallback
- [x] Task 1.4: Update Section 4.0 — remove "Switch to full sequential mode" as a user-facing concept, keep as internal fallback only
- [x] Task 1.5: Verify `commands/implement.md` Section 3.7 is already consistent (no changes expected)
- [x] Task: Conductor - User Manual Verification 'Remove sequential option from codeReview.md' (Protocol in workflow.md)

### Critical files
- `commands/codeReview.md` — primary file being modified (Sections 3.0-4.0)
- `commands/implement.md` — verify consistency only (Section 3.7.3)
