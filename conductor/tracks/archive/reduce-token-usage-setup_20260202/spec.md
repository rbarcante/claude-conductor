# Specification: Reduce Token Usage in setup.md

## Overview

Refactor `commands/setup.md` to achieve feature parity with the token-optimized versions of `commands/implement.md` and `commands/newTrack.md`. The goal is to reduce the file size and token consumption while maintaining full functionality, including parallel multi-agent support for brownfield codebase analysis.

## Background

The `implement.md` and `newTrack.md` commands were recently optimized to reduce token usage by:
1. Extracting inline content to external protocol/template references
2. Using quick reference tables instead of verbose explanations
3. Consolidating CLI commands in a dedicated section
4. Removing redundant inline JSON examples in favor of template references

The `setup.md` command (~1440 lines) has not yet been optimized and represents the largest command file in the plugin.

## Functional Requirements

### FR-1: External Protocol References
- Replace inline AskUserQuestion JSON examples with references to `templates/askuserquestion-patterns.md`
- Reference `protocols/git-isolation.md` instead of inline git setup instructions
- Reference `protocols/codebase-analysis.md` for brownfield analysis workflow
- Reference `protocols/stack-detection.md` for technology detection

### FR-2: Quick Reference Tables
- Convert verbose protocol instructions into concise tables
- Use tabular format for CLI commands with fallback instructions
- Summarize question type mappings in table format

### FR-3: Consolidated CLI Section
- Create a unified "Action CLI Commands" section at the top (matching implement.md pattern)
- Group all CLI commands with brief descriptions
- Include fallback instructions inline

### FR-4: Preserve Parallel Multi-Agent Support
- Maintain ability to launch 4 pattern detector agents concurrently
- Keep agent-based codebase analysis workflow intact
- Preserve inline fallback mode for when agents fail

### FR-5: Remove Redundant Content
- Remove duplicate protocol explanations that exist in referenced files
- Remove verbose example scenarios that can be inferred
- Remove inline JSON examples that duplicate template content

## Non-Functional Requirements

### NFR-1: Token Reduction
- Target: Achieve comparable line count reduction to implement.md (~350 lines) and newTrack.md (~177 lines)
- Expected final size: 300-500 lines (from current ~1440 lines)

### NFR-2: Maintain Readability
- Preserve logical section flow (setup check → greenfield/brownfield → product guide → tech stack → workflow → finalization)
- Keep critical directives clearly marked
- Maintain clear resume/checkpoint handling

### NFR-3: Backward Compatibility
- All existing functionality must work identically
- State file format unchanged
- CLI commands unchanged

## Acceptance Criteria

1. **AC-1**: setup.md references external protocols instead of inline content for:
   - AskUserQuestion patterns → `templates/askuserquestion-patterns.md`
   - Git isolation → `protocols/git-isolation.md`
   - Codebase analysis → `protocols/codebase-analysis.md`
   - Stack detection → `protocols/stack-detection.md`

2. **AC-2**: CLI commands are consolidated in a single section at the top with fallback instructions

3. **AC-3**: Verbose explanations replaced with quick reference tables

4. **AC-4**: Parallel multi-agent codebase analysis preserved with same agent types

5. **AC-5**: File size reduced by at least 60% (target: <600 lines)

6. **AC-6**: Setup command executes successfully for both greenfield and brownfield projects

## Out of Scope

- Changes to CLI implementation (`conductor_cli.py`)
- New protocol files (use existing ones)
- Changes to setup workflow logic or order
- Modifications to state file format
- Changes to other command files
