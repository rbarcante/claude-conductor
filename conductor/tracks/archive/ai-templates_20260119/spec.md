# Specification: AI-Optimized Templates

## Overview

Optimize patterns and templates specifically for AI assistant consumption by creating dual-format standards, enhancing code styleguides with AI Quick Reference sections, building a snippet library, and adding snippet search/insertion command. This maximizes AI effectiveness by providing condensed, structured lookup formats alongside human-readable documentation.

## Background

Current patterns and templates are optimized for human readability but not for AI context windows. AI assistants benefit from condensed, structured formats that can be quickly parsed. This feature creates AI-optimized sections in all patterns, enhances styleguides, and builds a library of ready-to-use code snippets that follow project patterns.

## Functional Requirements

### FR1: Dual-Format Pattern Standard
- Define standard dual-format structure for all patterns
- AI Quick Reference: Max 50 lines, structured with clear sections (PATTERN, USE WHEN, STRUCTURE, EXAMPLE, AVOID)
- Human Documentation: Detailed explanation with multiple examples
- Update Pattern Reference Layer patterns to use dual format

### FR2: Code Styleguide Enhancement
- Add AI Quick Reference sections to all templates/code_styleguides/*.md
- Condensed format with key rules (max 30 lines)
- Structured format (LANGUAGE RULES, TYPE PATTERNS, AVOID)
- Keep existing detailed sections

### FR3: Snippet Library
Create `/snippets/` directory structure with:
- snippets/index.md - Snippet registry
- snippets/typescript/ - TypeScript snippets (5+ files)
- snippets/python/ - Python snippets (5+ files)
- snippets/patterns/ - Pattern-based snippets (5+ files)

Each snippet includes:
- AI-optimized comment header (USE, REQUIRES, PATTERN)
- Complete working code example
- Key assumptions and customization points

### FR4: Snippet File Format
Standard format for all snippets:
- Language-appropriate comment block with metadata
- Complete, runnable code
- Inline comments for customization points
- No placeholders (actual working implementation)

### FR5: Snippet Command
- Create `/commands/snippet.md` command
- Support subcommands: list, search <query>, show <snippet>
- Search matches against snippet metadata and content
- Show displays full snippet with usage notes

### FR6: AI Template Generation Protocol
- Create protocol for generating AI-optimized content during setup
- Apply to code styleguides generation
- Apply to pattern creation
- Document in setup.md

## Non-Functional Requirements

### NFR1: AI Context Efficiency
- AI Quick Reference sections must be <50 lines
- Structured format for easy parsing
- No redundant information

### NFR2: Code Quality
- All snippets must be production-quality code
- Follow best practices for respective languages
- Include error handling where appropriate

### NFR3: Maintainability
- Dual format maintains single source of truth
- Snippets are self-contained (no external dependencies)

## Acceptance Criteria

- [ ] Dual-format standard documented
- [ ] All code styleguides enhanced with AI Quick Reference
- [ ] Snippet library created with 15+ snippets
- [ ] /conductor:snippet command functional
- [ ] AI Template Generation Protocol documented
- [ ] Setup generates AI-optimized styleguides
- [ ] Existing patterns updated to dual format

## Out of Scope

- Snippet generation from existing code (manual curation only)
- Language-specific snippet validation/linting
- Snippet versioning and updates
- Snippet marketplace

## Dependencies

- Pattern Reference Layer (Track 1) - patterns use dual format
- Skill Ecosystem (Track 5) - skills may provide snippets
