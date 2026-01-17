# Specification: Pattern Reference Layer

## Overview

Add a Pattern Reference Layer to Conductor, enabling contextual pattern storage, retrieval, and automatic surfacing during implementation. This transforms Conductor from a pure process manager into a system that provides both "how to work" (process) and "how to build" (patterns).

## Background

Currently, Conductor excels at managing development workflow (Context → Spec & Plan → Implement) but lacks a reference layer for implementation patterns. Developers need quick access to proven patterns for common challenges like error handling, logging, and testing. This feature bridges that gap by creating a pattern library that integrates seamlessly with the existing implementation workflow.

## Functional Requirements

### FR1: Pattern Storage Structure
- Create `/patterns/` directory in plugin root
- Create `/patterns/index.md` as the pattern registry
- Create `/patterns/core/` subdirectory for language-agnostic patterns
- Support future expansion with `/patterns/stack/` for technology-specific patterns

### FR2: Core Pattern Library
Create 5 initial core patterns with dual-format structure:
1. `error-handling.md` - Exception handling, error propagation, user-friendly messages
2. `logging.md` - Log levels, structured logging, context inclusion
3. `configuration.md` - Config management, environment variables, secrets handling
4. `validation.md` - Input validation, schema validation, error messages
5. `testing.md` - Test structure, mocking, assertions, coverage strategies

### FR3: Pattern File Format
Each pattern file must include:
- **YAML Frontmatter**: name, category, tags, activation keywords/file patterns
- **AI Quick Reference**: Max 50 lines, structured lookup format for AI context
- **Human Documentation**: Detailed explanation with examples
- **Anti-Patterns to Avoid**: Common mistakes and why to avoid them

### FR4: Pattern Resolution Protocol
- Add Pattern Resolution Protocol to `CLAUDE.md`
- Protocol extracts keywords from current task description
- Matches keywords against pattern activation rules
- Returns list of relevant patterns with paths

### FR5: Automatic Pattern Surfacing in Implement
- Modify `commands/implement.md` to surface patterns before each task
- Present matched patterns with brief descriptions
- Allow user to skip or acknowledge patterns
- Reference patterns during implementation

### FR6: Patterns Command
- Create new `commands/patterns.md` command
- Support listing all available patterns
- Support searching patterns by keyword
- Display pattern content on request

## Non-Functional Requirements

### NFR1: Backward Compatibility
- All changes must be additive (no breaking changes)
- Existing Conductor projects must continue to work
- Pattern surfacing can be skipped without blocking workflow

### NFR2: Zero Dependencies
- Patterns are pure Markdown files
- No runtime dependencies introduced
- Follows Conductor's markdown-first philosophy

### NFR3: Extensibility
- Structure must support future stack-specific patterns
- Pattern format must be documented for community contributions

## Acceptance Criteria

- [ ] `/patterns/` directory exists with `index.md` and `core/` subdirectory
- [ ] All 5 core patterns created with complete dual-format structure
- [ ] Pattern Resolution Protocol documented in `CLAUDE.md`
- [ ] `implement.md` surfaces relevant patterns before task execution
- [ ] `/conductor:patterns` command lists and searches patterns
- [ ] Existing Conductor functionality unchanged
- [ ] Patterns can be skipped during implementation without errors

## Out of Scope

- Technology-specific patterns (TypeScript, Python, etc.) - future tracks
- Anti-pattern detection/warning system - Phase 3
- Skill ecosystem integration - Phase 5
- Snippet library - Phase 6
- Coverage intelligence - Phase 3
