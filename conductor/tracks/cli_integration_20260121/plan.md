# Implementation Plan: Integrate Python CLI into Command Protocols

## Phase 1: Foundation & Pattern Establishment

- [ ] Task: Define the standard integration template
    - [ ] Create a reusable documentation section format for "CLI Operations"
    - [ ] Define the standard pattern for `!`command`` invocations in protocols
    - [ ] Document fallback instruction format

- [ ] Task: Integrate status.md with status.py
    - [ ] Read and analyze `scripts/commands/status.py` subcommands
    - [ ] Read current `commands/status.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use `!`python scripts/conductor_cli.py status <subcommand>`` for mechanical operations
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Pattern Establishment' (Protocol in workflow.md)

## Phase 2: Core Workflow Commands

- [ ] Task: Integrate setup.md with setup.py
    - [ ] Read and analyze `scripts/commands/setup.py` subcommands
    - [ ] Read current `commands/setup.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: tech stack detection, scaffolding, state management, template copying
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Integrate newTrack.md with newtrack.py
    - [ ] Read and analyze `scripts/commands/newtrack.py` subcommands
    - [ ] Read current `commands/newTrack.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: ID generation, scaffolding, track registration
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Integrate implement.md with implement.py
    - [ ] Read and analyze `scripts/commands/implement.py` subcommands
    - [ ] Read current `commands/implement.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: track parsing, status updates, coverage parsing, pattern matching
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Workflow Commands' (Protocol in workflow.md)

## Phase 3: Auxiliary Commands

- [ ] Task: Integrate patterns.md with patterns.py
    - [ ] Read and analyze `scripts/commands/patterns.py` subcommands
    - [ ] Read current `commands/patterns.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: pattern listing, display, searching
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Integrate snippet.md with snippets.py
    - [ ] Read and analyze `scripts/commands/snippets.py` subcommands
    - [ ] Read current `commands/snippet.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: snippet listing, display, searching
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Integrate skills.md with skills.py
    - [ ] Read and analyze `scripts/commands/skills.py` subcommands
    - [ ] Read current `commands/skills.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: skill listing, info display, enable/disable
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Auxiliary Commands' (Protocol in workflow.md)

## Phase 4: Advanced Commands

- [ ] Task: Integrate revert.md with revert.py
    - [ ] Read and analyze `scripts/commands/revert.py` subcommands
    - [ ] Read current `commands/revert.md` protocol
    - [ ] Add "CLI Operations" documentation section
    - [ ] Update protocol to use CLI for: commit finding, plan updates, revert list building, execution
    - [ ] Add fallback instructions
    - [ ] Verify CLI invocations work correctly

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Advanced Commands' (Protocol in workflow.md)

## Phase 5: Final Verification & Consistency Review

- [ ] Task: Cross-command consistency review
    - [ ] Verify all 8 commands follow the same documentation format
    - [ ] Verify all CLI invocation patterns are consistent
    - [ ] Verify all fallback instructions follow the same pattern
    - [ ] Fix any inconsistencies found

- [ ] Task: End-to-end verification
    - [ ] Test a complete workflow: setup → newTrack → implement → status
    - [ ] Verify CLI commands execute correctly in sequence
    - [ ] Document any issues or edge cases discovered

- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Verification & Consistency Review' (Protocol in workflow.md)
