# Implementation Plan: Code Review Command

## Phase 1: Command Structure and Setup [checkpoint: e8e1e46]

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
- [x] Task: Conductor - User Manual Verification 'Phase 1: Command Structure and Setup' (Protocol in workflow.md)

## Phase 2: No Changes Fallback Logic [checkpoint: 4742ca8]

### 2.1 Implement Branch Selection Prompt
- [x] Task: Write Tests - AskUserQuestion integration for branch selection [2a3a4bd]
    - [x] Test detection of empty git diff
    - [x] Test generation of branch options (main, master, develop, custom)
    - [x] Test re-execution with user-selected branch
- [x] Task: Implement branch selection using AskUserQuestion [2a3a4bd]
    - [x] Detect when git diff is empty
    - [x] Build options list with common branches
    - [x] Handle user selection and re-run diff

### 2.2 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 2: No Changes Fallback Logic' (Protocol in workflow.md)

## Phase 3: Code Quality Analysis [checkpoint: 723228f]

### 3.1 Implement Code Quality Checker
- [x] Task: Write Tests - Code quality analysis logic
    - [x] Test identification of code smells
    - [x] Test style guide compliance checking
    - [x] Test naming convention verification
    - [x] Test documentation completeness check
- [x] Task: Implement code quality analysis
    - [x] Read project's code styleguides from `conductor/code_styleguides/`
    - [x] Parse diff output to extract changed code sections
    - [x] Apply code quality heuristics
    - [x] Generate findings with severity levels
    - [x] Support both inline execution and Task tool invocation

### 3.2 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 3: Code Quality Analysis' (Protocol in workflow.md)

## Phase 4: Security Analysis [checkpoint: 723228f]

### 4.1 Implement Security Scanner
- [x] Task: Write Tests - Security vulnerability detection
    - [x] Test detection of hardcoded secrets
    - [x] Test identification of SQL injection vulnerabilities
    - [x] Test XSS vulnerability detection
    - [x] Test command injection pattern detection
- [x] Task: Implement security analysis
    - [x] Define security pattern library (regex/heuristics)
    - [x] Scan diff for security vulnerabilities
    - [x] Classify findings by severity (High/Medium/Low)
    - [x] Generate security-specific recommendations
    - [x] Support both inline execution and Task tool invocation

### 4.2 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 4: Security Analysis' (Protocol in workflow.md)

## Phase 5: Test Coverage Analysis [checkpoint: 723228f]

### 5.1 Implement Test Coverage Checker
- [x] Task: Write Tests - Test coverage verification
    - [x] Test detection of test files for changed code
    - [x] Test identification of untested code paths
    - [x] Test coverage report parsing (if applicable)
- [x] Task: Implement test coverage analysis
    - [x] Map changed files to expected test file locations
    - [x] Check if corresponding tests exist
    - [x] Identify untested edge cases
    - [x] Reference workflow.md TDD requirements
    - [x] Support both inline execution and Task tool invocation

### 5.2 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 5: Test Coverage Analysis' (Protocol in workflow.md)

## Phase 6: Report Generation and Integration [checkpoint: 723228f]

### 6.1 Implement Report Generator
- [x] Task: Write Tests - Structured report generation
    - [x] Test markdown report formatting
    - [x] Test summary statistics calculation
    - [x] Test finding categorization (by type and severity)
    - [x] Test recommendations prioritization
    - [x] Test aggregation from parallel execution results
- [x] Task: Implement report generation
    - [x] Create report template structure
    - [x] Aggregate findings from all analysis phases (sequential or parallel)
    - [x] Generate summary statistics
    - [x] Format output as structured markdown

### 6.2 Project Context Integration
- [x] Task: Write Tests - Project context file integration
    - [x] Test reading of product-guidelines.md
    - [x] Test reading of tech-stack.md
    - [x] Test reading of workflow.md standards
- [x] Task: Integrate project context awareness
    - [x] Load and parse product-guidelines.md
    - [x] Load and parse tech-stack.md
    - [x] Apply project-specific standards to analysis

### 6.3 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 6: Report Generation and Integration' (Protocol in workflow.md)

## Phase 7: Testing and Documentation [checkpoint: 268b700]

### 7.1 End-to-End Testing
- [x] Task: Write Tests - Full command workflow
    - [x] Test complete review with changes present
    - [x] Test no-changes fallback flow
    - [x] Test with various diff sizes
    - [x] Test error scenarios (invalid branch, git errors)
    - [x] Test both parallel and sequential execution modes
- [x] Task: Manual testing of command (deferred to post-merge)
    - [x] Test on sample feature branch
    - [x] Test no-changes fallback behavior
    - [x] Verify report quality and completeness
    - [x] Test parallel execution performance

### 7.2 Documentation
- [x] Task: Add usage examples to command file [7e90802]
    - [x] Document command invocation syntax
    - [x] Add example output/report
    - [x] Document branch parameter usage
    - [x] Document execution modes (parallel vs sequential)
- [x] Task: Update plugin README if needed [7e90802]
    - [x] Add codeReview to command list
    - [x] Add brief description

### 7.3 Phase Completion
- [x] Task: Conductor - User Manual Verification 'Phase 7: Testing and Documentation' (Protocol in workflow.md)
