# Implementation Plan: Specialist Sub-Agents for Claude Conductor

## Phase 1: Agent Directory Structure and First Agent [checkpoint: 7285f00]

- [x] Task: Create agents directory structure
    - [x] Create `agents/` directory at plugin root
    - [x] Verify directory is created successfully

- [x] Task: Implement code-quality-analyzer agent
    - [x] Write agent definition with YAML frontmatter (name, description, model: inherit, color: blue)
    - [x] Define allowed-tools: Read, Glob, Grep
    - [x] Write system prompt specifying input/output JSON contract
    - [x] Include code smell detection, style compliance, and maintainability analysis focus
    - [x] Document skill injection placeholder (parent command injects relevant language skill based on detected stack)

- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Analysis Agents [checkpoint: 5bbe874]

- [x] Task: Implement security-scanner agent
    - [x] Write agent definition with YAML frontmatter (name, description, model: inherit, color: red)
    - [x] Define allowed-tools: Read, Glob, Grep
    - [x] Write system prompt for security vulnerability detection
    - [x] Include hardcoded secrets, injection risks, OWASP patterns
    - [x] Specify JSON output contract with severity levels

- [x] Task: Implement test-coverage-analyzer agent
    - [x] Write agent definition with YAML frontmatter (name, description, model: haiku, color: green)
    - [x] Define allowed-tools: Read, Glob, Grep
    - [x] Write system prompt for test coverage analysis
    - [x] Include test-to-source file mapping logic
    - [x] Document skill injection placeholder (parent command may inject testing-strategies or other relevant skill)

- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

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
