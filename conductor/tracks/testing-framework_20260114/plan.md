# Implementation Plan: Testing Framework for Claude Conductor

## Phase 1: Testing Framework Setup

**Goal:** Establish the testing infrastructure and choose appropriate testing approaches for markdown-based protocol definitions.

### Tasks

- [ ] Task: Research and select testing approach
    - [ ] Evaluate Claude Code's built-in testing capabilities (if available)
    - [ ] Research testing frameworks for markdown-based projects
    - [ ] Assess snapshot testing options (e.g., expect, similar frameworks)
    - [ ] Document testing approach decision with rationale

- [ ] Task: Initialize testing infrastructure
    - [ ] Create tests/ directory structure
    - [ ] Set up test configuration files
    - [ ] Install testing dependencies (if applicable)
    - [ ] Create test helpers and utilities

- [ ] Task: Establish test data fixtures
    - [ ] Create sample protocol definitions for testing
    - [ ] Create sample JSON artifacts (metadata.json, setup_state.json)
    - [ ] Create sample conductor context files
    - [ ] Document fixture organization and usage

- [ ] Task: Create test utilities
    - [ ] Implement file system helpers (create temp dirs, cleanup)
    - [ ] Implement markdown validation helpers
    - [ ] Implement JSON schema validation helpers
    - [ ] Implement assertion helpers for Conductor-specific artifacts

- [ ] Task: Conductor - User Manual Verification 'Testing Framework Setup' (Protocol in workflow.md)

## Phase 2: Core Protocol Validation Tests

**Goal:** Implement validation tests for Conductor protocol definitions and JSON artifacts.

### Tasks

- [ ] Task: Test command protocol structure validation
    - [ ] Write tests for setup.md protocol structure
    - [ ] Write tests for newTrack.md protocol structure
    - [ ] Write tests for implement.md protocol structure
    - [ ] Write tests for status.md protocol structure
    - [ ] Write tests for revert.md protocol structure
    - [ ] Implement protocol structure validator

- [ ] Task: Test JSON schema validation
    - [ ] Write tests for metadata.json schema validation
    - [ ] Write tests for setup_state.json schema validation
    - [ ] Implement JSON schema validator
    - [ ] Test invalid schema rejection

- [ ] Task: Test template file validation
    - [ ] Write tests for workflow.md template validation
    - [ ] Write tests for code styleguide template validation
    - [ ] Implement template validator
    - [ ] Test template completeness and required fields

- [ ] Task: Test track ID generation
    - [ ] Write tests for track ID format (shortname_YYYYMMDD)
    - [ ] Test track ID uniqueness
    - [ ] Test track ID from various descriptions
    - [ ] Implement track ID generator

- [ ] Task: Conductor - User Manual Verification 'Core Protocol Validation Tests' (Protocol in workflow.md)

## Phase 3: Setup Command Tests

**Goal:** Test the `/conductor:setup` command workflow across various scenarios.

### Tasks

- [ ] Task: Test brownfield project detection
    - [ ] Write tests for detecting existing git repository
    - [ ] Write tests for detecting dependency manifests
    - [ ] Write tests for detecting source code directories
    - [ ] Implement brownfield detection logic

- [ ] Task: Test greenfield project detection
    - [ ] Write tests for detecting empty directory
    - [ ] Write tests for detecting directory with only README.md
    - [ ] Implement greenfield detection logic

- [ ] Task: Test state file management
    - [ ] Write tests for state file creation
    - [ ] Write tests for state file reading
    - [ ] Write tests for state file updates
    - [ ] Write tests for resume capability from state file
    - [ ] Implement state file manager

- [ ] Task: Test context file generation
    - [ ] Write tests for product.md generation
    - [ ] Write tests for product-guidelines.md generation
    - [ ] Write tests for tech-stack.md generation
    - [ ] Write tests for workflow.md copying
    - [ ] Implement context file generators

- [ ] Task: Test code styleguide selection
    - [ ] Write tests for styleguide directory creation
    - [ ] Write tests for styleguide file copying
    - [ ] Write tests for recommended styleguide logic
    - [ ] Implement styleguide manager

- [ ] Task: Conductor - User Manual Verification 'Setup Command Tests' (Protocol in workflow.md)

## Phase 4: New Track Command Tests

**Goal:** Test the `/conductor:newTrack` command workflow.

### Tasks

- [ ] Task: Test track creation workflow
    - [ ] Write tests for track directory creation
    - [ ] Write tests for track ID generation
    - [ ] Write tests for initial metadata.json creation
    - [ ] Implement track creation workflow

- [ ] Task: Test spec.md generation
    - [ ] Write tests for spec document structure
    - [ ] Write tests for spec content from user input
    - [ ] Write tests for spec section completeness
    - [ ] Implement spec generator

- [ ] Task: Test plan.md generation
    - [ ] Write tests for plan document structure
    - [ ] Write tests for phase generation
    - [ ] Write tests for task and sub-task generation
    - [ ] Write tests for status markers ([ ], [~], [x])
    - [ ] Implement plan generator

- [ ] Task: Test tracks.md file update
    - [ ] Write tests for appending new track to tracks.md
    - [ ] Write tests for tracks.md formatting
    - [ ] Implement tracks.md updater

- [ ] Task: Test metadata.json validation
    - [ ] Write tests for required fields in metadata
    - [ ] Write tests for timestamp format validation
    - [ ] Write tests for status enum validation
    - [ ] Implement metadata validator

- [ ] Task: Conductor - User Manual Verification 'New Track Command Tests' (Protocol in workflow.md)

## Phase 5: Implement Command Tests

**Goal:** Test the `/conductor:implement` command workflow.

### Tasks

- [ ] Task: Test task selection and workflow
    - [ ] Write tests for selecting next pending task
    - [ ] Write tests for marking task as in-progress [~]
    - [ ] Write tests for sequential task execution order
    - [ ] Implement task selector

- [ ] Task: Test plan.md status updates
    - [ ] Write tests for updating task status to [x]
    - [ ] Write tests for appending commit SHA to completed tasks
    - [ ] Write tests for plan file persistence
    - [ ] Implement plan status updater

- [ ] Task: Test git commit creation
    - [ ] Write tests for commit message formatting
    - [ ] Write tests for commit message types (feat, fix, conductor)
    - [ ] Write tests for proper git staging
    - [ ] Implement git commit handler

- [ ] Task: Test git notes attachment
    - [ ] Write tests for git notes creation
    - [ ] Write tests for note content formatting
    - [ ] Write tests for note attachment to correct commit
    - [ ] Implement git notes handler

- [ ] Task: Test phase completion verification
    - [ ] Write tests for detecting phase completion
    - [ ] Write tests for triggering verification protocol
    - [ ] Write tests for checkpoint commit creation
    - [ ] Implement phase completion detector

- [ ] Task: Conductor - User Manual Verification 'Implement Command Tests' (Protocol in workflow.md)

## Phase 6: Status Command Tests

**Goal:** Test the `/conductor:status` command workflow.

### Tasks

- [ ] Task: Test tracks.md parsing
    - [ ] Write tests for parsing track entries
    - [ ] Write tests for extracting track links
    - [ ] Write tests for reading track status checkboxes
    - [ ] Implement tracks.md parser

- [ ] Task: Test status calculation
    - [ ] Write tests for counting tracks by status
    - [ ] Write tests for calculating progress percentage
    - [ ] Write tests for handling empty tracks list
    - [ ] Implement status calculator

- [ ] Task: Test status output formatting
    - [ ] Write tests for formatted status display
    - [ ] Write tests for progress bar visualization
    - [ ] Write tests for track listing
    - [ ] Implement status formatter

- [ ] Task: Conductor - User Manual Verification 'Status Command Tests' (Protocol in workflow.md)

## Phase 7: Revert Command Tests

**Goal:** Test the `/conductor:revert` command workflow.

### Tasks

- [ ] Task: Test git history analysis
    - [ ] Write tests for parsing git log
    - [ ] Write tests for identifying track-related commits
    - [ ] Write tests for identifying phase commits
    - [ ] Write tests for identifying task commits
    - [ ] Implement git history analyzer

- [ ] Task: Test track-level revert
    - [ ] Write tests for selecting commits to revert for a track
    - [ ] Write tests for executing revert operation
    - [ ] Write tests for updating tracks.md after revert
    - [ ] Implement track revert logic

- [ ] Task: Test phase-level revert
    - [ ] Write tests for selecting commits to revert for a phase
    - [ ] Write tests for updating plan.md checkpoint SHA
    - [ ] Implement phase revert logic

- [ ] Task: Test task-level revert
    - [ ] Write tests for identifying task-specific commits
    - [ ] Write tests for resetting task status in plan.md
    - [ ] Implement task revert logic

- [ ] Task: Test confirmation prompts
    - [ ] Write tests for displaying changes to be reverted
    - [ ] Write tests for user confirmation handling
    - [ ] Implement confirmation handler

- [ ] Task: Conductor - User Manual Verification 'Revert Command Tests' (Protocol in workflow.md)

## Phase 8: Coverage Reporting and CI/CD Integration

**Goal:** Set up coverage reporting and integrate tests into CI/CD pipeline.

### Tasks

- [ ] Task: Implement coverage reporting
    - [ ] Write tests for coverage measurement
    - [ ] Set up coverage report generation
    - [ ] Configure coverage threshold enforcement (>80%)
    - [ ] Implement coverage reporter

- [ ] Task: Create CI/CD configuration
    - [ ] Write tests for CI/CD pipeline execution
    - [ ] Create GitHub Actions workflow (or equivalent)
    - [ ] Configure automated test triggers
    - [ ] Set up test result reporting

- [ ] Task: Optimize test performance
    - [ ] Write tests for test execution time
    - [ ] Profile slow tests
    - [ ] Implement test parallelization where possible
    - [ ] Optimize file I/O operations

- [ ] Task: Conductor - User Manual Verification 'Coverage Reporting and CI/CD Integration' (Protocol in workflow.md)

## Phase 9: Documentation and Finalization

**Goal:** Document testing patterns and complete the testing framework implementation.

### Tasks

- [ ] Task: Write testing documentation
    - [ ] Create TESTING.md with overview
    - [ ] Document how to run tests locally
    - [ ] Document test organization and structure
    - [ ] Document how to write new tests
    - [ ] Document testing best practices

- [ ] Task: Document testing patterns
    - [ ] Create examples of protocol validation tests
    - [ ] Create examples of workflow integration tests
    - [ ] Create examples of fixture usage
    - [ ] Document common testing scenarios

- [ ] Task: Update project documentation
    - [ ] Update README.md with testing section
    - [ ] Update product.md with testing capabilities
    - [ ] Add testing contribution guidelines

- [ ] Task: Final verification and cleanup
    - [ ] Run full test suite and verify >80% coverage
    - [ ] Review and refactor test code
    - [ ] Remove any temporary test artifacts
    - [ ] Ensure all tests pass consistently

- [ ] Task: Conductor - User Manual Verification 'Documentation and Finalization' (Protocol in workflow.md)
