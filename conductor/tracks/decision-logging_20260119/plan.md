# Implementation Plan: Decision Logging

## Phase 1: Decision Template Creation [checkpoint: 843a915]

- [x] Task: Design ADR template structure [f44ff2f]
    - [x] Research ADR format best practices
    - [x] Define required sections (Context, Decision, Consequences)
    - [x] Define optional sections (Alternatives, Status)
    - [x] Document template design

- [x] Task: Create decisions.md template [6a2cfb2]
    - [x] Write tests to validate template structure
    - [x] Create `/templates/decisions.md`
    - [x] Include format explanation and example
    - [x] Include placeholder for first decision

- [x] Task: Conductor - User Manual Verification 'Phase 1: Decision Template Creation' (Protocol in workflow.md)

## Phase 2: Track Structure Enhancement [checkpoint: baa4075]

- [x] Task: Modify newTrack.md to create decisions.md [645d95a]
    - [x] Write tests for newTrack.md structure changes
    - [x] Add decisions.md creation step to Section 2.4
    - [x] Initialize with template content
    - [x] Include track-specific header

- [x] Task: Update track index template [645d95a]
    - [x] Modify track index.md to include decisions.md link
    - [x] Update newTrack.md to generate enhanced index

- [x] Task: Conductor - User Manual Verification 'Phase 2: Track Structure Enhancement' (Protocol in workflow.md)

## Phase 3: Decision Capture Protocol

- [x] Task: Design decision identification rules [60ab86d]
    - [x] Define what constitutes a "significant decision"
    - [x] Create decision trigger checklist (tech selection, pattern choice, etc.)
    - [x] Define when to prompt vs. when to skip
    - [x] Document decision identification rules

- [x] Task: Create Decision Capture Protocol document [60ab86d]
    - [x] Write tests for protocol documentation completeness
    - [x] Create protocol section in implement.md or separate doc
    - [x] Include trigger identification
    - [x] Include user prompt format (Context + Options A/B/C)
    - [x] Include recording format

- [x] Task: Design decision prompt format [60ab86d]
    - [x] Create standard template for presenting decisions
    - [x] Include context section
    - [x] Include alternatives with pros/cons
    - [x] Include recommendation with rationale

- [x] Task: Conductor - User Manual Verification 'Phase 3: Decision Capture Protocol' (Protocol in workflow.md)

## Phase 4: Implement Command Enhancement

- [ ] Task: Add decision capture to implement.md
    - [ ] Write tests for implement.md structure changes
    - [ ] Add decision capture invocation points during implementation
    - [ ] Include decision prompting logic
    - [ ] Include decision recording to decisions.md

- [ ] Task: Implement decision recording logic
    - [ ] Define ADR entry format
    - [ ] Define append mechanism to decisions.md
    - [ ] Include timestamp and status
    - [ ] Generate decision ID/title

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Implement Command Enhancement' (Protocol in workflow.md)

## Phase 5: Git Notes Enhancement

- [ ] Task: Design enhanced git note format
    - [ ] Add "Decisions Made" section
    - [ ] Add reference to decisions.md entries
    - [ ] Add "Why" section for overall rationale
    - [ ] Document enhanced format

- [ ] Task: Update workflow.md with enhanced git notes
    - [ ] Write tests for workflow.md structure changes
    - [ ] Update Section 9 (Attach Task Summary) with new format
    - [ ] Include example of enhanced git note
    - [ ] Update git notes command template

- [ ] Task: Conductor - User Manual Verification 'Phase 5: Git Notes Enhancement' (Protocol in workflow.md)

## Phase 6: Integration and Documentation

- [ ] Task: End-to-end integration testing
    - [ ] Test newTrack creates decisions.md correctly
    - [ ] Test decision capture during implementation
    - [ ] Test decisions.md format and readability
    - [ ] Test git note references to decisions

- [ ] Task: Update TESTING.md with decision logging scenarios
    - [ ] Add test scenario for decision capture
    - [ ] Add test scenario for decisions.md content
    - [ ] Add test scenario for git note enhancement

- [ ] Task: Update README.md with decision logging documentation
    - [ ] Document decision logging feature
    - [ ] Include ADR format explanation
    - [ ] Include example decision entry

- [ ] Task: Conductor - User Manual Verification 'Phase 6: Integration and Documentation' (Protocol in workflow.md)
