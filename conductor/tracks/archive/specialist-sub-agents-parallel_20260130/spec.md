# Specification: Specialist Sub-Agents for Claude Conductor

## Overview

Create 5 ultra-specialist sub-agents that can be reused across multiple Conductor commands to improve execution speed and reduce token usage through parallel execution. Each agent has a focused purpose, restricted tool access, and standardized input/output contracts.

## Functional Requirements

### FR-1: Agent Directory Structure

Create an `agents/` directory at the plugin root containing 5 agent definition files:

- `agents/code-quality-analyzer.md`
- `agents/security-scanner.md`
- `agents/test-coverage-analyzer.md`
- `agents/git-history-analyst.md`
- `agents/codebase-pattern-detector.md`

### FR-2: Agent Definitions

Each agent must have YAML frontmatter with:
- `name`: Agent identifier
- `description`: Trigger condition description
- `model`: `inherit` (Sonnet) or `haiku`
- `color`: Visual identifier (blue, red, green, cyan, magenta)
- `allowed-tools`: Restricted tool list

#### FR-2.1: code-quality-analyzer
- **Purpose**: Analyze code for smells, style compliance, and maintainability
- **Model**: inherit (Sonnet) - nuanced analysis needed
- **Color**: blue
- **Tools**: Read, Glob, Grep
- **Used by**: codeReview, implement (quality gate)

#### FR-2.2: security-scanner
- **Purpose**: Detect security vulnerabilities, hardcoded secrets, injection risks
- **Model**: inherit (Sonnet) - accuracy critical for security
- **Color**: red
- **Tools**: Read, Glob, Grep
- **Used by**: codeReview, implement (quality gate)

#### FR-2.3: test-coverage-analyzer
- **Purpose**: Map test files to source files, identify coverage gaps
- **Model**: haiku - mostly pattern matching
- **Color**: green
- **Tools**: Read, Glob, Grep
- **Used by**: codeReview, implement (quality gate)

#### FR-2.4: git-history-analyst
- **Purpose**: Find commits by track/task ID, build revert lists, analyze history
- **Model**: haiku - structured data parsing
- **Color**: cyan
- **Tools**: Read, Bash(git log:*), Bash(git show:*), Bash(git diff:*), Bash(git status:*), Bash(git branch:*), Bash(git rev-parse:*)
- **Used by**: revert, implement (commit tracking)

#### FR-2.5: codebase-pattern-detector
- **Purpose**: Detect patterns in existing codebase (architecture, conventions, testing)
- **Model**: haiku - pattern matching, low complexity
- **Color**: magenta
- **Tools**: Read, Glob, Grep
- **Used by**: setup (brownfield analysis), newTrack (context gathering)

### FR-3: Input/Output Contracts

All analysis agents must accept input via Task tool prompt parameter containing:
```json
{
  "diff_content": "Raw git diff output (for code analysis agents)",
  "file_list": ["array", "of", "file", "paths"],
  "project_context": {
    "tech_stack": "typescript|java|python|etc",
    "styleguide_path": "path/to/styleguide"
  }
}
```

All analysis agents must return JSON output:
```json
{
  "findings": [
    {
      "severity": "high|medium|low",
      "category": "code-smell|security|coverage",
      "file": "path/to/file.ts",
      "line": 42,
      "issue": "Brief description",
      "recommendation": "How to fix"
    }
  ],
  "summary": {
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

### FR-4: Dynamic Skill Injection

Skills are injected dynamically via Task prompt (not frontmatter) based on detected tech stack. The parent command decides which skill to inject based on the project context:
- `code-quality-analyzer`: Relevant language-specific best practices skill
- `test-coverage-analyzer`: Relevant testing skill
- `codebase-pattern-detector`: Relevant architecture/design skill
- `security-scanner`: No skill injection needed (universal patterns)
- `git-history-analyst`: No skill injection needed

### FR-5: Command Integration

Update existing commands to use sub-agents:
- `codeReview.md`: Add parallel Task invocations for quality/security/coverage
- `implement.md`: Add quality gate Task invocations
- `setup.md`: Add parallel codebase-pattern-detector invocations
- `revert.md`: Add git-history-analyst Task invocation
- `newTrack.md`: Add codebase-pattern-detector for context

## Non-Functional Requirements

### NFR-1: Parallel Execution
Commands must launch multiple agents simultaneously using parallel Task invocations where dependencies allow.

### NFR-2: Error Handling
When a sub-agent fails:
1. Log the failure with error details
2. Fall back to sequential/inline execution for that analysis type
3. Continue with remaining parallel agents
4. Include partial results in final report

### NFR-3: Token Usage Reduction
- Focused context: Each agent only receives relevant subset of data
- Structured output: Agents return JSON, not prose
- Haiku for simple tasks: Pattern matching agents use cheaper model
- Bounded scope: Agents cannot expand their own scope

## Acceptance Criteria

1. All 5 agent files exist in `agents/` directory with correct frontmatter
2. Agent discovery works (agents appear in Claude Code's available tools)
3. `/conductor:codeReview` executes 3 analysis agents in parallel
4. Agent output follows the defined JSON contract
5. Commands gracefully handle agent failures
6. Parallel execution reduces overall execution time compared to sequential

## Out of Scope

- Custom skill creation for agents
- Agent-to-agent communication
- Persistent agent state between invocations
- UI/visualization for agent results
