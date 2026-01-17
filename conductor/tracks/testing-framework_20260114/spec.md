# Specification: Testing Framework for Conductor Plugin

## Overview

This specification defines the requirements for adding a comprehensive testing framework to the Conductor plugin. Currently, the Conductor plugin lacks automated testing, which poses risks for maintaining code quality and detecting regressions as the plugin evolves.

## Problem Statement

The Conductor plugin is a documentation and protocol-driven plugin for Claude Code that implements context-driven development methodology. Key challenges:

1. **No Test Coverage**: The plugin has no automated tests to verify protocol logic
2. **Manual Testing Required**: All testing is currently manual, which is time-consuming and error-prone
3. **Regression Risk**: Changes to protocol definitions may inadvertently break existing functionality
4. **Quality Gate Missing**: No automated validation before committing changes

## Goals

### Primary Goals

1. **Establish Testing Infrastructure**: Set up a testing framework suitable for markdown-based protocol definitions
2. **Test Core Workflows**: Create tests for key Conductor workflows (setup, newTrack, implement, status, revert)
3. **Achieve High Coverage**: Target >80% test coverage for protocol logic
4. **Documentation**: Document testing patterns for protocol-driven plugins

### Secondary Goals

1. **CI/CD Integration**: Set up automated testing in CI/CD pipeline
2. **Performance Testing**: Ensure tests run efficiently
3. **Developer Experience**: Make tests easy to run and understand

## Non-Goals

1. **Rewriting Protocols**: Not changing the existing protocol definitions, only testing them
2. **Language Changes**: Not introducing new programming languages to the plugin itself
3. **External Service Testing**: Not testing external Claude Code CLI behavior

## Requirements

### Functional Requirements

#### FR1: Testing Framework Setup

**ID:** FR1
**Priority:** High
**Description:** Establish a testing framework that can validate markdown-based protocol definitions

**Acceptance Criteria:**
- Testing framework is installed and configured
- Tests can be run with a single command
- Test results are clearly reported
- Framework supports test organization and categorization

**Notes:**
Since the Conductor plugin is markdown-based and executed within Claude Code, traditional unit testing approaches may not apply. Consider:
- Protocol validation tests (markdown structure, required fields)
- Integration tests using Claude Code's testing capabilities
- Snapshot tests for protocol outputs
- Schema validation for JSON artifacts

#### FR2: Setup Command Testing

**ID:** FR2
**Priority:** High
**Description:** Test the `/conductor:setup` command workflow

**Acceptance Criteria:**
- Test brownfield project detection (existing git repo, dependencies)
- Test greenfield project detection (empty directory)
- Test state file creation and management
- Test context file generation (product.md, product-guidelines.md, tech-stack.md, workflow.md)
- Test code styleguide selection
- Test resumption from incomplete setup

**Test Scenarios:**
1. Fresh setup in empty directory
2. Setup detection of existing project
3. Setup resume from incomplete state
4. State file persistence and recovery

#### FR3: New Track Command Testing

**ID:** FR3
**Priority:** High
**Description:** Test the `/conductor:newTrack` command workflow

**Acceptance Criteria:**
- Test track creation with user description
- Test spec.md generation with required sections
- Test plan.md generation with proper structure
- Test metadata.json creation with valid schema
- Test tracks.md file update
- Test track ID generation (shortname_YYYYMMDD format)

**Test Scenarios:**
1. Create new feature track
2. Create new bug track
3. Generate spec from user input
4. Generate plan with phases and tasks
5. Validate metadata structure

#### FR4: Implement Command Testing

**ID:** FR4
**Priority:** High
**Description:** Test the `/conductor:implement` command workflow

**Acceptance Criteria:**
- Test task selection and marking in-progress
- Test TDD workflow (Red-Green-Refactor)
- Test plan.md status updates
- Test git commit creation
- Test git notes attachment
- Test phase completion verification protocol

**Test Scenarios:**
1. Select and execute first task
2. Update task status in plan.md
3. Create git commit with proper message
4. Attach git note with task summary
5. Mark task complete with commit SHA
6. Execute phase completion verification

#### FR5: Status Command Testing

**ID:** FR5
**Priority:** Medium
**Description:** Test the `/conductor:status` command workflow

**Acceptance Criteria:**
- Test tracks.md parsing and display
- Test track status identification (new, in_progress, completed)
- Test progress calculation
- Test formatted output

**Test Scenarios:**
1. Display status with no tracks
2. Display status with single track
3. Display status with multiple tracks
4. Display status with mixed track states

#### FR6: Revert Command Testing

**ID:** FR6
**Priority:** Medium
**Description:** Test the `/conductor:revert` command workflow

**Acceptance Criteria:**
- Test git history analysis for track identification
- Test track-level revert
- Test phase-level revert
- Test task-level revert
- Test confirmation prompts

**Test Scenarios:**
1. Revert entire track
2. Revert specific phase
3. Revert specific task
4. Handle revert conflicts

### Non-Functional Requirements

#### NFR1: Test Performance

**ID:** NFR1
**Priority:** Medium
**Description:** Tests should execute efficiently

**Acceptance Criteria:**
- Full test suite completes in under 5 minutes
- Individual test files complete in under 30 seconds
- No unnecessary file I/O operations

#### NFR2: Test Maintainability

**ID:** NFR2
**Priority:** High
**Description:** Tests should be easy to understand and maintain

**Acceptance Criteria:**
- Clear test names that describe what is being tested
- Well-organized test structure
- Minimal test duplication
- Clear setup and teardown procedures

#### NFR3: Coverage Reporting

**ID:** NFR3
**Priority:** Medium
**Description:** Test coverage should be measurable and reported

**Acceptance Criteria:**
- Coverage reports are generated
- Coverage metrics are visible in CI/CD
- Coverage threshold is enforced (>80%)

## Design Considerations

### Testing Approach

Given the unique nature of the Conductor plugin (markdown-based protocol definitions executed by Claude Code), several testing approaches should be considered:

1. **Protocol Validation Tests**
   - Validate markdown file structure
   - Check for required sections and fields
   - Verify markdown formatting consistency

2. **Schema Validation Tests**
   - Validate JSON artifacts (metadata.json, setup_state.json)
   - Check data types and required fields
   - Verify timestamp formats

3. **Snapshot Tests**
   - Capture expected outputs for given inputs
   - Compare generated files against snapshots
   - Easy to review and update when behavior changes intentionally

4. **Integration Tests**
   - Test end-to-end workflows using Claude Code's testing framework
   - Verify command execution from user perspective
   - Validate file system changes

### Test Organization

```
tests/
├── unit/              # Protocol validation, schema tests
├── integration/       # End-to-end workflow tests
├── fixtures/          # Sample files for testing
└── helpers/           # Test utilities and assertions
```

### Test Data Management

- Use fixture files for sample protocols and artifacts
- Create temporary directories for file system tests
- Clean up test artifacts after test execution

## Success Criteria

The testing framework is considered successful when:

1. **Infrastructure Established**: Testing framework is set up and documented
2. **Core Workflows Tested**: Setup, newTrack, implement, status, and revert have test coverage
3. **Coverage Target Met**: >80% of protocol logic is covered by tests
4. **CI/CD Integrated**: Tests run automatically on changes
5. **Documentation Complete**: Testing patterns and practices are documented
6. **All Tests Passing**: Test suite executes successfully with no failures

## Dependencies

### External Dependencies

- Claude Code CLI testing framework (if available)
- Node.js / Python / Other runtime (to be determined based on testing approach)

### Internal Dependencies

- Protocol definition files in `commands/` directory
- Template files in `templates/` directory
- Existing conductor artifacts for test scenarios

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Claude Code lacks testing framework | High | Medium | Develop custom validation scripts, use snapshot testing |
| Markdown protocols are hard to test | Medium | High | Focus on schema validation and structure checks |
| Tests become brittle | Medium | Medium | Use fixtures and helpers to reduce duplication |
| Slow test execution | Low | Low | Optimize file I/O, parallelize independent tests |

## Open Questions

1. **Testing Framework Choice**: What testing framework is best suited for markdown-based protocols?
   - Options: Custom validation scripts, Node.js with Jest, Python with pytest
   - Recommendation: Evaluate Claude Code's built-in testing capabilities first

2. **Test Execution Environment**: Where and how should tests be run?
   - Options: Local development only, CI/CD pipeline, both
   - Recommendation: Support both for developer convenience and CI/CD quality gates

3. **Coverage Measurement**: How do we measure coverage for markdown protocols?
   - Options: Line-based coverage, section-based coverage, scenario coverage
   - Recommendation: Use scenario-based coverage (what workflows are tested)

## Timeline Estimate

- Phase 1: Framework Setup (1-2 days)
- Phase 2: Core Workflow Tests (3-5 days)
- Phase 3: Coverage Expansion (2-3 days)
- Phase 4: Documentation and Refinement (1-2 days)

Total estimated effort: 7-12 days

## References

- Conductor Plugin README.md
- Conductor Product Documentation (conductor/product.md)
- Conductor Workflow (conductor/workflow.md)
- Claude Code Documentation (if available)
