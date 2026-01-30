# Implementation Plan: Specialist Sub-Agents for Claude Conductor

## Phase 1: Agent Directory Structure and First Agent [checkpoint: ]

- [ ] Task: Create agents directory structure
    - [ ] Create `agents/` directory at plugin root
    - [ ] Verify directory is created successfully

- [ ] Task: Implement code-quality-analyzer agent
    - [ ] Write agent definition with YAML frontmatter (name, description, model: inherit, color: blue)
    - [ ] Define allowed-tools: Read, Glob, Grep
    - [ ] Write system prompt specifying input/output JSON contract
    - [ ] Include code smell detection, style compliance, and maintainability analysis focus
    - [ ] Document skill injection placeholder (parent command injects relevant language skill based on detected stack)

- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Analysis Agents [checkpoint: ]

- [ ] Task: Implement security-scanner agent
    - [ ] Write agent definition with YAML frontmatter (name, description, model: inherit, color: red)
    - [ ] Define allowed-tools: Read, Glob, Grep
    - [ ] Write system prompt for security vulnerability detection
    - [ ] Include hardcoded secrets, injection risks, OWASP patterns
    - [ ] Specify JSON output contract with severity levels

- [ ] Task: Implement test-coverage-analyzer agent
    - [ ] Write agent definition with YAML frontmatter (name, description, model: haiku, color: green)
    - [ ] Define allowed-tools: Read, Glob, Grep
    - [ ] Write system prompt for test coverage analysis
    - [ ] Include test-to-source file mapping logic
    - [ ] Document skill injection placeholder (parent command may inject testing-strategies or other relevant skill)

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Utility Agents [checkpoint: ]

- [ ] Task: Implement git-history-analyst agent
    - [ ] Write agent definition with YAML frontmatter (name, description, model: haiku, color: cyan)
    - [ ] Define allowed-tools with pattern-based Bash constraints (git log:*, git show:*, git diff:*, git status:*, git branch:*, git rev-parse:*)
    - [ ] Write system prompt for commit analysis and revert list building
    - [ ] Include track/task ID pattern matching
    - [ ] Specify read-only git operations constraint

- [ ] Task: Implement codebase-pattern-detector agent
    - [ ] Write agent definition with YAML frontmatter (name, description, model: haiku, color: magenta)
    - [ ] Define allowed-tools: Read, Glob, Grep
    - [ ] Write system prompt for architecture and convention detection
    - [ ] Include naming conventions, testing patterns, API patterns analysis
    - [ ] Document skill injection placeholder (parent command may inject api-design or other relevant skill)

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Command Integration - codeReview [checkpoint: ]

- [ ] Task: Update codeReview.md to use parallel sub-agents
    - [ ] Read current codeReview.md implementation
    - [ ] Add parallel Task invocations for code-quality-analyzer
    - [ ] Add parallel Task invocations for security-scanner
    - [ ] Add parallel Task invocations for test-coverage-analyzer
    - [ ] Implement result aggregation from all three agents
    - [ ] Add error handling for agent failures with fallback

- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Command Integration - implement and revert [checkpoint: ]

- [ ] Task: Update implement.md with quality gate sub-agent calls
    - [ ] Read current implement.md implementation
    - [ ] Add quality gate checkpoint using analysis agents
    - [ ] Integrate git-history-analyst for commit tracking
    - [ ] Add error handling for agent failures

- [ ] Task: Update revert.md with git-history-analyst
    - [ ] Read current revert.md implementation
    - [ ] Add git-history-analyst Task invocation for commit identification
    - [ ] Integrate revert list building from agent output

- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Phase 6: Command Integration - setup and newTrack [checkpoint: ]

- [ ] Task: Update setup.md with parallel pattern detection
    - [ ] Read current setup.md implementation
    - [ ] Add parallel codebase-pattern-detector invocations for brownfield analysis
    - [ ] Integrate pattern detection results into context generation

- [ ] Task: Update newTrack.md with pattern detector for context
    - [ ] Read current newTrack.md implementation
    - [ ] Add codebase-pattern-detector Task invocation for context gathering
    - [ ] Use detected patterns to inform spec generation

- [ ] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)

## Phase 7: Verification and Documentation [checkpoint: ]

- [ ] Task: Verify agent discovery in Claude Code
    - [ ] Confirm all 5 agents appear in available Task subagent_types
    - [ ] Test each agent can be invoked via Task tool
    - [ ] Document any plugin.json updates if explicit registration required

- [ ] Task: End-to-end testing
    - [ ] Run /conductor:codeReview and verify parallel agent execution
    - [ ] Verify JSON output format matches contract
    - [ ] Test error handling by simulating agent failure
    - [ ] Verify graceful degradation to sequential execution

- [ ] Task: Conductor - User Manual Verification 'Phase 7' (Protocol in workflow.md)
