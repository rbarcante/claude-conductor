# Implementation Plan: Reduce Token Usage in setup.md

## Phase 1: Analysis and Template Preparation

- [ ] Task: Analyze current setup.md structure and identify extraction targets
    - [ ] Map all inline AskUserQuestion JSON examples
    - [ ] Map all inline protocol explanations (git, codebase analysis, stack detection)
    - [ ] Map all verbose explanations that can become tables
    - [ ] Document current line count by section

- [ ] Task: Verify external protocol/template files exist and are complete
    - [ ] Confirm `templates/askuserquestion-patterns.md` covers all setup.md patterns
    - [ ] Confirm `protocols/git-isolation.md` is complete
    - [ ] Confirm `protocols/codebase-analysis.md` exists and covers parallel agents
    - [ ] Confirm `protocols/stack-detection.md` is complete

## Phase 2: Core Refactoring

- [ ] Task: Create consolidated CLI Commands section
    - [ ] Extract all CLI commands to top-level section
    - [ ] Add fallback instructions in table format
    - [ ] Remove inline CLI explanations from protocol sections

- [ ] Task: Refactor AskUserQuestion content
    - [ ] Replace all inline JSON examples with protocol references
    - [ ] Create quick reference table for question types
    - [ ] Keep only the minimal constraint summary inline

- [ ] Task: Refactor Setup Check and Resume sections
    - [ ] Convert verbose resume logic to concise table format
    - [ ] Simplify state check instructions with CLI reference

- [ ] Task: Refactor Greenfield/Brownfield detection sections
    - [ ] Reference `protocols/stack-detection.md` for detection logic
    - [ ] Keep only summary and user interaction flow inline
    - [ ] Preserve brownfield indicators in concise list format

- [ ] Task: Refactor Codebase Analysis section (preserve parallel agents)
    - [ ] Reference `protocols/codebase-analysis.md` for full protocol
    - [ ] Keep agent launch instructions with Task tool syntax
    - [ ] Maintain 4-agent parallel launch pattern
    - [ ] Keep inline fallback mode reference

- [ ] Task: Refactor Interactive Document Generation sections (2.1-2.3)
    - [ ] Consolidate product guide, guidelines, and tech stack sections
    - [ ] Use consistent pattern: announce → questions → draft → confirm → write
    - [ ] Reference AskUserQuestion patterns template for examples

- [ ] Task: Refactor Style Guide and Workflow selection sections (2.4-2.5)
    - [ ] Consolidate with quick reference tables
    - [ ] Remove verbose example JSON

- [ ] Task: Refactor Documentation Generation section (2.5.1)
    - [ ] Reference protocol for detailed steps
    - [ ] Keep high-level flow inline

- [ ] Task: Refactor Initial Track Generation section (3.0)
    - [ ] Align with newTrack.md patterns
    - [ ] Reference shared track creation protocols

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Refactoring' (Protocol in workflow.md)

## Phase 3: Validation and Finalization

- [ ] Task: Validate refactored setup.md functionality
    - [ ] Test greenfield project setup flow
    - [ ] Test brownfield project detection flow
    - [ ] Verify parallel agent launch syntax is correct
    - [ ] Confirm state resume logic works

- [ ] Task: Measure and document token reduction
    - [ ] Count final line count
    - [ ] Calculate percentage reduction
    - [ ] Document any sections that could not be reduced

- [ ] Task: Final cleanup and consistency check
    - [ ] Ensure all section references are correct
    - [ ] Verify protocol file paths use ${CLAUDE_PLUGIN_ROOT}
    - [ ] Check for orphaned content

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Validation and Finalization' (Protocol in workflow.md)
