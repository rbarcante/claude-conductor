# Implementation Plan: Reduce Token Usage in setup.md

## Phase 1: Analysis and Template Preparation

- [x] Task: Analyze current setup.md structure and identify extraction targets
    - [x] Map all inline AskUserQuestion JSON examples
    - [x] Map all inline protocol explanations (git, codebase analysis, stack detection)
    - [x] Map all verbose explanations that can become tables
    - [x] Document current line count by section

- [x] Task: Verify external protocol/template files exist and are complete
    - [x] Confirm `templates/askuserquestion-patterns.md` covers all setup.md patterns
    - [x] Confirm `protocols/git-isolation.md` is complete
    - [x] Confirm `protocols/codebase-analysis.md` exists and covers parallel agents
    - [x] Confirm `protocols/stack-detection.md` is complete

## Phase 2: Core Refactoring

- [x] Task: Create consolidated CLI Commands section
    - [x] Extract all CLI commands to top-level section
    - [x] Add fallback instructions in table format
    - [x] Remove inline CLI explanations from protocol sections

- [x] Task: Refactor AskUserQuestion content
    - [x] Replace all inline JSON examples with protocol references
    - [x] Create quick reference table for question types
    - [x] Keep only the minimal constraint summary inline

- [x] Task: Refactor Setup Check and Resume sections
    - [x] Convert verbose resume logic to concise table format
    - [x] Simplify state check instructions with CLI reference

- [x] Task: Refactor Greenfield/Brownfield detection sections
    - [x] Reference `protocols/stack-detection.md` for detection logic
    - [x] Keep only summary and user interaction flow inline
    - [x] Preserve brownfield indicators in concise list format

- [x] Task: Refactor Codebase Analysis section (preserve parallel agents)
    - [x] Reference `protocols/codebase-analysis.md` for full protocol
    - [x] Keep agent launch instructions with Task tool syntax
    - [x] Maintain 4-agent parallel launch pattern
    - [x] Keep inline fallback mode reference

- [x] Task: Refactor Interactive Document Generation sections (2.1-2.3)
    - [x] Consolidate product guide, guidelines, and tech stack sections
    - [x] Use consistent pattern: announce → questions → draft → confirm → write
    - [x] Reference AskUserQuestion patterns template for examples

- [x] Task: Refactor Style Guide and Workflow selection sections (2.4-2.5)
    - [x] Consolidate with quick reference tables
    - [x] Remove verbose example JSON

- [x] Task: Refactor Documentation Generation section (2.5.1)
    - [x] Reference protocol for detailed steps
    - [x] Keep high-level flow inline

- [x] Task: Refactor Initial Track Generation section (3.0)
    - [x] Align with newTrack.md patterns
    - [x] Reference shared track creation protocols

- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Refactoring' (Protocol in workflow.md)

## Phase 3: Validation and Finalization

- [x] Task: Validate refactored setup.md functionality
    - [x] Test greenfield project setup flow
    - [x] Test brownfield project detection flow
    - [x] Verify parallel agent launch syntax is correct
    - [x] Confirm state resume logic works

- [x] Task: Measure and document token reduction
    - [x] Count final line count
    - [x] Calculate percentage reduction
    - [x] Document any sections that could not be reduced

- [x] Task: Final cleanup and consistency check
    - [x] Ensure all section references are correct
    - [x] Verify protocol file paths use ${CLAUDE_PLUGIN_ROOT}
    - [x] Check for orphaned content

- [x] Task: Conductor - User Manual Verification 'Phase 3: Validation and Finalization' (Protocol in workflow.md)
