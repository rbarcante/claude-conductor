# Implementation Plan: Technology-Aware Intelligence

## Phase 1: Stack Detection Protocol

- [x] Task: Design stack detection algorithm
    - [x] Define manifest file signatures (package.json, pom.xml, requirements.txt, etc.)
    - [x] Define file extension to language mapping
    - [x] Define framework detection patterns
    - [x] Document confidence scoring methodology

- [x] Task: Create Stack Detection Protocol document
    - [x] Write tests to validate protocol document structure
    - [x] Create `/protocols/stack-detection.md`
    - [x] Include step-by-step detection process
    - [x] Include output format (JSON stack profile)
    - [x] Include confidence thresholds and fallback behavior

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Stack Detection Protocol' (Protocol in workflow.md)

## Phase 2: Enhanced Setup Command

- [x] Task: Add brownfield detection enhancement to setup.md
    - [x] Write tests for setup.md structure changes
    - [x] Modify Section 2 (Project Inception) to invoke stack detection
    - [x] Add stack presentation step with confidence display
    - [x] Add user confirmation/correction flow

- [x] Task: Integrate auto-detection with tech-stack generation
    - [x] Pre-populate tech-stack.md with detected information
    - [x] Mark auto-detected items with confidence indicators
    - [x] Allow user to modify before finalizing

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Enhanced Setup Command' (Protocol in workflow.md)

## Phase 3: Skill Registry System

- [x] Task: Design skill manifest schema
    - [x] Define required fields (name, version, path)
    - [x] Define activation rules schema (keywords, file_patterns, tech_stack)
    - [x] Define provides schema (patterns, templates, protocols)
    - [x] Document schema in `/docs/skill-manifest-schema.md`

- [x] Task: Create skill registry
    - [x] Write tests for registry JSON structure
    - [x] Create `/skills/skill-registry.json`
    - [x] Add existing conductor-methodology skill to registry
    - [x] Include activation rules for methodology skill

- [x] Task: Add manifest.json to conductor-methodology skill
    - [x] Create `/skills/conductor-methodology/manifest.json`
    - [x] Define activation rules (always active as base methodology)

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Skill Registry System' (Protocol in workflow.md)

## Phase 4: Skill Loading Protocol

- [x] Task: Design skill activation algorithm
    - [x] Define keyword extraction from task descriptions
    - [x] Define file pattern matching for modified files
    - [x] Define tech stack matching logic
    - [x] Document priority and conflict resolution

- [x] Task: Document Skill Loading Protocol in CLAUDE.md
    - [x] Write tests for protocol documentation completeness
    - [x] Add "Skill Loading Protocol" section to CLAUDE.md
    - [x] Include activation index building process
    - [x] Include skill loading on task start
    - [x] Include skill context injection

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Skill Loading Protocol' (Protocol in workflow.md)

## Phase 5: Implement Command Enhancement

- [x] Task: Add skill activation step to implement.md
    - [x] Write tests for implement.md structure changes
    - [x] Add new section "Activate Relevant Skills" before task execution
    - [x] Include skill registry loading
    - [x] Include task-to-skill matching
    - [x] Include skill context loading

- [x] Task: Define skill activation output format
    - [x] Create standard announcement format for activated skills
    - [x] Include skill name and brief description
    - [x] Include what guidance is now available

- [ ] Task: Conductor - User Manual Verification 'Phase 5: Implement Command Enhancement' (Protocol in workflow.md)

## Phase 6: Integration and Documentation

- [ ] Task: End-to-end integration testing
    - [ ] Test stack detection on sample projects (Node.js, Python, Go)
    - [ ] Test skill activation during implementation
    - [ ] Verify brownfield setup flow works correctly

- [ ] Task: Update TESTING.md with technology intelligence scenarios
    - [ ] Add test scenario for stack detection
    - [ ] Add test scenario for skill activation
    - [ ] Add edge case: unknown stack type

- [ ] Task: Update README.md with technology intelligence documentation
    - [ ] Document stack detection feature
    - [ ] Document skill activation behavior
    - [ ] Include examples of detected stacks

- [ ] Task: Conductor - User Manual Verification 'Phase 6: Integration and Documentation' (Protocol in workflow.md)
