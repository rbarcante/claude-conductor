## Specification

### Overview
Refactor `commands/codeReview.md` to remove the parallel vs. sequential user prompt (Section 3.1) and make parallel execution the only path. Sequential/inline analysis is retained solely as an internal fallback for agent failures.

### Background
Section 3.1 currently asks users to choose between "Parallel (Recommended)" and "Sequential" via AskUserQuestion. In practice, parallel is always preferred. The sequential option adds unnecessary friction and an inferior code path that shouldn't be a user choice.

### Functional Requirements
1. **FR-1:** Remove Section 3.1 (the AskUserQuestion prompt) — parallel execution starts immediately after diff generation
2. **FR-2:** Rename Section 3.2 from "Parallel Execution (Preferred)" to the main execution path, remove "(Preferred)" qualifier
3. **FR-3:** Rename Section 3.3 from "Sequential Execution (Fallback)" to "Inline Fallback (Agent Failure Only)" — make clear this is not a user choice
4. **FR-4:** Update Section 4.0 error handling to remove references to "user selects Sequential"
5. **FR-5:** Verify `commands/implement.md` Section 3.7.3 is already consistent (runs parallel by default)

### Non-Functional Requirements
- No structural changes to the report format or agent definitions
- Keep inline checklists intact for error fallback use

### Acceptance Criteria
- No AskUserQuestion prompt for execution strategy exists in codeReview.md
- Parallel execution is the sole execution path
- Inline analysis remains available only as agent failure fallback
- Error handling in Section 4.0 reflects the removal of user choice

### Out of Scope
- Changes to agent definitions
- Changes to implement.md (already runs parallel)
- Report format changes
