## Specification

### Overview
Add a global enforcement directive to `templates/askuserquestion-patterns.md` — the single source of truth for the AskUserQuestion protocol — mandating that all interactive questions across all Conductor commands MUST use the AskUserQuestion tool, with no plain text questions allowed. Remove the per-section enforcement note from `commands/newTrack.md` since it will be covered globally.

### Background
Currently, enforcement is inconsistent:
- `commands/newTrack.md` Section 2.5 has a `<note type="critical">` enforcing AskUserQuestion for that one section
- All other question points across all commands lack explicit enforcement
- `templates/askuserquestion-patterns.md` is the shared reference for the AskUserQuestion protocol, referenced by all commands — the ideal place for a global enforcement rule

### Functional Requirements
1. **FR-1:** Add a prominent enforcement section to `templates/askuserquestion-patterns.md` stating: all interactive questions in any Conductor command MUST use the AskUserQuestion tool — no plain text questions, without exception.
2. **FR-2:** Remove the per-section `<note type="critical">` from `commands/newTrack.md` Section 2.5 (line 475-477) since the global directive covers it.

### Non-Functional Requirements
- Single source of truth for the enforcement rule
- No structural changes to command phases or logic in any command file

### Acceptance Criteria
- `templates/askuserquestion-patterns.md` contains a clear, prominent enforcement directive
- No per-section AskUserQuestion enforcement notes remain in any command file
- Existing command logic and flow remain unchanged across all commands

### Out of Scope
- Adding JSON examples or templates inline to commands
- Changing the question flow or count in any command
- Refactoring how commands reference the patterns template
