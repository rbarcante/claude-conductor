## Implementation Plan

### Phase 1: Global enforcement refactor

- [x] Task 1.1: Add enforcement section to `templates/askuserquestion-patterns.md` — add a `## Mandatory Usage` section near the top (after the Key Rules section) with clear directive that AskUserQuestion is mandatory for all interactive prompts, no exceptions
- [x] Task 1.2: Remove the `<note type="critical">` block from `commands/newTrack.md` Section 2.5 (lines 475-477) — the global directive now covers this
- [x] Task: Conductor - User Manual Verification 'Global enforcement refactor' (Protocol in workflow.md)

### Critical files
- `templates/askuserquestion-patterns.md` — add global enforcement section
- `commands/newTrack.md` — remove per-section enforcement note
