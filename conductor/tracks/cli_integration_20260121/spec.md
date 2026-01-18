# Specification: Integrate Python CLI into Command Protocols

## Overview

This track integrates the Python CLI (`scripts/conductor_cli.py`) into the respective markdown command protocols (`commands/*.md`). The goal is to leverage the token-efficient Python operations for mechanical tasks while maintaining the markdown protocols as the authoritative instruction source for Claude Code.

## Background

The Conductor plugin currently has two parallel systems:
1. **Markdown command protocols** (`commands/`) - Define the step-by-step instructions Claude Code follows
2. **Python CLI** (`scripts/`) - Provides token-efficient operations for file parsing, JSON manipulation, and git operations

These systems are not currently connected. The markdown protocols perform mechanical operations through direct tool calls, consuming tokens for deterministic tasks that could be offloaded to Python.

## Technical Approach

### CLI Invocation Syntax

Markdown command files support a special syntax for invoking shell commands and injecting their output into the context:

```
!`python scripts/conductor_cli.py <command> <subcommand> [options]`
```

This syntax executes the command and injects the result directly into the markdown context, enabling token-efficient operations without manual tool calls.

## Functional Requirements

### FR-1: CLI Documentation in Commands
Each markdown command file must include a "CLI Operations" section that documents:
- Available subcommands and their purpose
- Command syntax with examples using the `!`command`` invocation syntax
- Expected output format (JSON vs human-readable)
- When to use CLI vs direct tool calls

### FR-2: Protocol Integration
Markdown protocols must be updated to use the `!`command`` syntax to invoke CLI commands for mechanical operations:
- File parsing (plan.md, tracks.md, metadata.json)
- JSON manipulation (status updates, metadata creation)
- Git operations (find commits, build revert lists)
- Directory scaffolding (track creation, project setup)
- Pattern/snippet searching and retrieval

### FR-3: Fallback Instructions
Protocols must include fallback instructions for cases where the CLI is unavailable or fails, ensuring graceful degradation to direct tool calls.

### FR-4: Command Mapping
The following command pairs must be integrated:

| Python Script | Markdown Command |
|---------------|------------------|
| `implement.py` | `implement.md` |
| `newtrack.py` | `newTrack.md` |
| `patterns.py` | `patterns.md` |
| `revert.py` | `revert.md` |
| `setup.py` | `setup.md` |
| `skills.py` | `skills.md` |
| `snippets.py` | `snippet.md` |
| `status.py` | `status.md` |

## Non-Functional Requirements

### NFR-1: Consistency
All integrated commands must follow a consistent documentation format and integration pattern.

### NFR-2: Backward Compatibility
Existing functionality must be preserved. The CLI integration should enhance, not replace, the core protocol logic.

### NFR-3: Discoverability
CLI operations should be clearly documented so users and Claude Code can easily understand when and how to use them.

## Acceptance Criteria

- [ ] All 8 markdown command files contain a "CLI Operations" section with documented subcommands
- [ ] Protocols use `!`command`` syntax to invoke CLI for mechanical operations
- [ ] Fallback instructions exist for CLI failures
- [ ] CLI commands execute successfully when invoked via `!`command`` syntax
- [ ] Documentation includes usage examples with expected output
- [ ] Integration follows consistent patterns across all commands

## Out of Scope

- Modifying the Python CLI implementation itself
- Adding new CLI subcommands
- Changing the CLI's output format
- Creating automated tests for the CLI (already exists in `scripts/tests/`)
- Modifying the core protocol logic (only the mechanical operation invocations)
