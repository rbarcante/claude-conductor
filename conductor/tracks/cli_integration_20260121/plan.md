# Implementation Plan: Integrate Python CLI into Command Protocols

## Phase 1: Foundation & Pattern Establishment

- [x] Task: Define the standard integration template
    - [x] Create a reusable documentation section format for "CLI Operations"
    - [x] Define the standard pattern for ``command`` invocations in protocols
    - [x] Document fallback instruction format

- [x] Task: Integrate status.md with status.py
    - [ ] Read and analyze `scripts/commands/status.py` subcommands
    - [ ] Read current `commands/status.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use `!`python scripts/conductor_cli.py status <subcommand>`` for mechanical operations
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Pattern Establishment' (Protocol in workflow.md)

## Phase 2: Core Workflow Commands

- [x] Task: Integrate setup.md with setup.py
    - [x] Read and analyze `scripts/commands/setup.py` subcommands
    - [x] Read current `commands/setup.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: tech stack detection, scaffolding, state management, template copying
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [x] Task: Integrate newTrack.md with newtrack.py
    - [x] Read and analyze `scripts/commands/newtrack.py` subcommands
    - [x] Read current `commands/newTrack.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: ID generation, scaffolding, track registration
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [x] Task: Integrate implement.md with implement.py
    - [x] Read and analyze `scripts/commands/implement.py` subcommands
    - [x] Read current `commands/implement.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: track parsing, status updates, coverage parsing, pattern matching
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Workflow Commands' (Protocol in workflow.md)

## Phase 3: Auxiliary Commands

- [x] Task: Integrate patterns.md with patterns.py
    - [x] Read and analyze `scripts/commands/patterns.py` subcommands
    - [x] Read current `commands/patterns.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: pattern listing, display, searching
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [x] Task: Integrate snippet.md with snippets.py
    - [x] Read and analyze `scripts/commands/snippets.py` subcommands
    - [x] Read current `commands/snippet.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: snippet listing, display, searching
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [x] Task: Integrate skills.md with skills.py
    - [x] Read and analyze `scripts/commands/skills.py` subcommands
    - [x] Read current `commands/skills.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: skill listing, info display, enable/disable
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Auxiliary Commands' (Protocol in workflow.md)

## Phase 4: Advanced Commands

- [x] Task: Integrate revert.md with revert.py
    - [x] Read and analyze `scripts/commands/revert.py` subcommands
    - [x] Read current `commands/revert.md` protocol
    - [x] Add "CLI Operations" documentation section
    - [x] Update protocol to use CLI for: commit finding, plan updates, revert list building, execution
    - [x] Add fallback instructions
    - [x] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Advanced Commands' (Protocol in workflow.md)

## Phase 5: Final Verification & Consistency Review

- [x] Task: Cross-command consistency review
    - [x] Verify all 8 commands follow the same documentation format
    - [x] Verify all CLI invocation patterns are consistent
    - [x] Verify all fallback instructions follow the same pattern
    - [x] Fix any inconsistencies found

- [x] Task: End-to-end verification
    - [x] Test a complete workflow: setup → newTrack → implement → status
    - [x] Verify CLI commands execute correctly in sequence
    - [x] Document any issues or edge cases discovered

- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Verification & Consistency Review' (Protocol in workflow.md)
