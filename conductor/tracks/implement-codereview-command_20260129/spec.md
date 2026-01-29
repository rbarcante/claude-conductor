# Specification: Code Review Command

## Overview

Implement a new `/conductor:codeReview` command for the Claude Conductor plugin that performs comprehensive code review of changes in the current branch compared to a base branch (default: `origin/HEAD`). The command provides structured feedback covering code quality, security, and test coverage.

## Functional Requirements

### FR1: Context Injection
- The command MUST inject the git diff output directly into the command context via the `# Context` section
- Default comparison: current branch vs `origin/HEAD`
- Use `git diff origin/HEAD` to capture all changes
- Context injection happens automatically without requiring additional tool calls

### FR2: Comprehensive Analysis
The command SHALL analyze code changes across three dimensions:

1. **Code Quality**
   - Identify code smells and anti-patterns
   - Check adherence to project's code styleguides (from `conductor/code_styleguides/`)
   - Verify naming conventions and code organization
   - Assess maintainability and readability
   - Check for proper documentation (docstrings, comments)

2. **Security Analysis**
   - Detect common vulnerabilities (SQL injection, XSS, command injection, etc.)
   - Identify hardcoded secrets or credentials
   - Check for insecure dependencies or imports
   - Verify input validation and sanitization
   - Assess authentication and authorization patterns

3. **Test Coverage**
   - Verify that changed code has corresponding tests
   - Check if tests follow project's testing patterns (from `workflow.md`)
   - Identify untested edge cases
   - Assess test quality and completeness

### FR3: Structured Report Output
- Generate a markdown-formatted report with the following structure:
  ```
  # Code Review Report

  ## Summary
  - Files changed: X
  - Lines added: Y / Lines removed: Z
  - Findings: High (N) | Medium (N) | Low (N)

  ## Code Quality
  [Findings organized by file]

  ## Security Analysis
  [Security findings with severity levels]

  ## Test Coverage
  [Test coverage analysis]

  ## Recommendations
  [Prioritized action items]
  ```

### FR4: No Changes Fallback
- When `git diff origin/HEAD` returns no changes:
  1. Detect the empty diff
  2. Use `AskUserQuestion` tool to prompt user for alternative comparison branch
  3. Options should include: common branches (main, master, develop) and "Specify custom branch"
  4. Re-run analysis with user-selected branch

### FR5: Project Context Awareness
- Reference project's `product-guidelines.md` for style and messaging standards
- Use `tech-stack.md` to understand project's technology choices
- Apply standards from `workflow.md` (TDD requirements, coverage thresholds)
- Check against applicable code styleguides

## Non-Functional Requirements

### NFR1: Performance
- Command should complete within reasonable time for diffs up to 5000 lines
- For larger diffs, provide progress indication or summary analysis

### NFR2: Usability
- Clear, actionable feedback
- Findings should reference specific file paths and line numbers where applicable
- Severity levels (High/Medium/Low) to help prioritize fixes

### NFR3: Integration
- Follow Conductor command conventions (frontmatter, structure)
- Use standard Claude Code tools (Read, Bash, AskUserQuestion)
- Maintain consistency with other Conductor commands

## Acceptance Criteria

1. Command file created at `commands/codeReview.md` with proper frontmatter
2. Context section successfully injects git diff output
3. Analysis covers all three dimensions: code quality, security, test coverage
4. Report generated in structured markdown format
5. When no changes detected, command prompts user for alternative branch
6. Command references and applies project context files
7. Manual testing confirms command works on sample code changes

## Out of Scope

- Automated code fixing or refactoring
- Integration with external code analysis tools (SonarQube, ESLint, etc.)
- Persistent storage of review reports
- Comparison of more than two branches simultaneously
- Line-by-line interactive review mode
