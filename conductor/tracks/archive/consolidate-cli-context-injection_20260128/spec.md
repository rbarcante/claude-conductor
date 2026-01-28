# Specification: Consolidate CLI Context Injection

> **Type:** refactor
> **Track ID:** `consolidate-cli-context-injection_20260128`

## Overview

Refactor the Conductor command files (setup.md, newTrack.md, implement.md, status.md) to consolidate multiple Python CLI calls into a single upfront bash execution using the `!`backtick`` syntax. This uses existing CLI subcommands chained together, avoiding any Python code changes.

## Background

Currently, command files instruct the agent to make multiple separate Python CLI calls at various points during execution. Each call requires:
1. User permission approval (separate prompts)
2. Additional latency
3. Context switching during command execution

## Solution

Chain existing CLI subcommands into a single bash command executed once at command load time via the `!`backtick`` syntax under a `# Context` section. The combined output provides all needed data upfront.

### Commands Affected

| Command | Current CLI Calls | Consolidation Strategy |
|---------|------------------|----------------------|
| setup.md | detect, scaffold, state get/set, copy-templates | Chain detect + state get |
| newTrack.md | generate-id, scaffold, register | Chain relevant read-only calls |
| implement.md | parse-tracks, update-status, modified-files, parse-coverage, etc. | Chain parse-tracks + match-patterns |
| status.md | verify, tracks, progress, full | Use single `status full` call |

### Command File Structure

Each command file gains a `# Context` section at the top with chained CLI calls:

```markdown
# Context

!`<chained CLI calls returning combined JSON>`
```

## Requirements

### Functional Requirements

- [ ] FR-1: Add `# Context` section to each command file (after frontmatter, contains single `!`backtick`` bash execution)
- [ ] FR-2: Chain relevant CLI calls for each command (setup: detect + state get; newTrack: read-only context; implement: parse-tracks; status: status full)
- [ ] FR-3: Update command instructions to reference injected context instead of scattered CLI calls
- [ ] FR-4: Preserve fallback instructions for CLI failures

### Non-Functional Requirements

- [ ] No Python code changes required
- [ ] Existing functionality preserved
- [ ] Action-oriented CLI calls (writes/updates) remain as instructions

## Acceptance Criteria

- [ ] setup.md has `# Context` section with consolidated CLI call
- [ ] newTrack.md has `# Context` section with consolidated CLI call
- [ ] implement.md has `# Context` section with consolidated CLI call
- [ ] status.md has `# Context` section with consolidated CLI call
- [ ] Redundant CLI call instructions are replaced with context references
- [ ] No Python code changes required
- [ ] Existing functionality preserved
- [ ] Action-oriented CLI calls (writes/updates) remain as instructions

## Out of Scope

- Modifying conductor_cli.py
- Adding new CLI subcommands
- Changing command logic or protocols
- Consolidating action/write CLI calls (only read-only context calls)

## Dependencies

- None identified

## References

- None
