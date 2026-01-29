# Implementation Plan: Code Review Command

## Phase 1: Command Structure and Setup

### 1.1 Create Command File
- [x] Task: Create `commands/codeReview.md` with proper YAML frontmatter [61b5bf0]
    - [x] Add command name, description, and invocations
    - [x] Define command arguments structure (optional branch parameter)
    - [x] Set up command categories/tags

### 1.2 Implement Context Injection
- [x] Task: Write Tests - Context injection for git diff output
    - [x] Test that `# Context` section correctly invokes `git diff origin/HEAD`
    - [x] Test handling of empty diff (no changes)
    - [x] Test error handling when origin/HEAD doesn't exist
- [x] Task: Implement context injection in command file
    - [x] Add `# Context` section with git diff command
    - [x] Add git command to detect if diff is empty
    - [x] Implement fallback for missing origin/HEAD

### 1.3 Parallel Execution Architecture
- [x] Task: Write Tests - AskUserQuestion for parallel execution preference
    - [x] Test question prompts user for execution strategy
    - [x] Test handling of both parallel and sequential responses
- [x] Task: Implement execution strategy prompt
    - [x] Add AskUserQuestion at command start
    - [x] Ask: "Run analysis phases in parallel for faster results?"
    - [x] Options: "Parallel (Recommended)" vs "Sequential"
    - [x] Store user preference for conditional execution

### 1.4 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Command Structure and Setup' (Protocol in workflow.md)

## Phase 2: No Changes Fallback Logic

### 2.1 Implement Branch Selection Prompt
- [ ] Task: Write Tests - AskUserQuestion integration for branch selection
    - [ ] Test detection of empty git diff
    - [ ] Test generation of branch options (main, master, develop, custom)
    - [ ] Test re-execution with user-selected branch
- [ ] Task: Implement branch selection using AskUserQuestion
    - [ ] Detect when git diff is empty
    - [ ] Build options list with common branches
    - [ ] Handle user selection and re-run diff

### 2.2 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 2: No Changes Fallback Logic' (Protocol in workflow.md)

## Phase 3: Code Quality Analysis

### 3.1 Implement Code Quality Checker
- [ ] Task: Write Tests - Code quality analysis logic
    - [ ] Test identification of code smells
    - [ ] Test style guide compliance checking
    - [ ] Test naming convention verification
    - [ ] Test documentation completeness check
- [ ] Task: Implement code quality analysis
    - [ ] Read project's code styleguides from `conductor/code_styleguides/`
    - [ ] Parse diff output to extract changed code sections
    - [ ] Apply code quality heuristics
    - [ ] Generate findings with severity levels
    - [ ] Support both inline execution and Task tool invocation

### 3.2 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Code Quality Analysis' (Protocol in workflow.md)

## Phase 4: Security Analysis

### 4.1 Implement Security Scanner
- [ ] Task: Write Tests - Security vulnerability detection
    - [ ] Test detection of hardcoded secrets
    - [ ] Test identification of SQL injection vulnerabilities
    - [ ] Test XSS vulnerability detection
    - [ ] Test command injection pattern detection
- [ ] Task: Implement security analysis
    - [ ] Define security pattern library (regex/heuristics)
    - [ ] Scan diff for security vulnerabilities
    - [ ] Classify findings by severity (High/Medium/Low)
    - [ ] Generate security-specific recommendations
    - [ ] Support both inline execution and Task tool invocation

### 4.2 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Security Analysis' (Protocol in workflow.md)

## Phase 5: Test Coverage Analysis

### 5.1 Implement Test Coverage Checker
- [ ] Task: Write Tests - Test coverage verification
    - [ ] Test detection of test files for changed code
    - [ ] Test identification of untested code paths
    - [ ] Test coverage report parsing (if applicable)
- [ ] Task: Implement test coverage analysis
    - [ ] Map changed files to expected test file locations
    - [ ] Check if corresponding tests exist
    - [ ] Identify untested edge cases
    - [ ] Reference workflow.md TDD requirements
    - [ ] Support both inline execution and Task tool invocation

### 5.2 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Test Coverage Analysis' (Protocol in workflow.md)

## Phase 6: Report Generation and Integration

### 6.1 Implement Report Generator
- [ ] Task: Write Tests - Structured report generation
    - [ ] Test markdown report formatting
    - [ ] Test summary statistics calculation
    - [ ] Test finding categorization (by type and severity)
    - [ ] Test recommendations prioritization
    - [ ] Test aggregation from parallel execution results
- [ ] Task: Implement report generation
    - [ ] Create report template structure
    - [ ] Aggregate findings from all analysis phases (sequential or parallel)
    - [ ] Generate summary statistics
    - [ ] Format output as structured markdown

### 6.2 Project Context Integration
- [ ] Task: Write Tests - Project context file integration
    - [ ] Test reading of product-guidelines.md
    - [ ] Test reading of tech-stack.md
    - [ ] Test reading of workflow.md standards
- [ ] Task: Integrate project context awareness
    - [ ] Load and parse product-guidelines.md
    - [ ] Load and parse tech-stack.md
    - [ ] Apply project-specific standards to analysis

### 6.3 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Report Generation and Integration' (Protocol in workflow.md)

## Phase 7: Testing and Documentation

### 7.1 End-to-End Testing
- [ ] Task: Write Tests - Full command workflow
    - [ ] Test complete review with changes present
    - [ ] Test no-changes fallback flow
    - [ ] Test with various diff sizes
    - [ ] Test error scenarios (invalid branch, git errors)
    - [ ] Test both parallel and sequential execution modes
- [ ] Task: Manual testing of command
    - [ ] Test on sample feature branch
    - [ ] Test no-changes fallback behavior
    - [ ] Verify report quality and completeness
    - [ ] Test parallel execution performance

### 7.2 Documentation
- [ ] Task: Add usage examples to command file
    - [ ] Document command invocation syntax
    - [ ] Add example output/report
    - [ ] Document branch parameter usage
    - [ ] Document execution modes (parallel vs sequential)
- [ ] Task: Update plugin README if needed
    - [ ] Add codeReview to command list
    - [ ] Add brief description

### 7.3 Phase Completion
- [ ] Task: Conductor - User Manual Verification 'Phase 7: Testing and Documentation' (Protocol in workflow.md)
