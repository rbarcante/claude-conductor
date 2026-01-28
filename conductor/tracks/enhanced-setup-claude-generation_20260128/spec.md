# Specification: Enhanced Setup - CLAUDE.md Generation with Progressive Disclosure

> **Type:** feature
> **Track ID:** `enhanced-setup-claude-generation_20260128`

## Overview

Enhance the `/conductor:setup` command to perform comprehensive codebase analysis for brownfield projects and generate structured documentation using **Progressive Disclosure**. Instead of placing all context in a single CLAUDE.md file, the system will generate:

1. **CLAUDE.md** - High-level project overview with links to detailed documentation
2. **conductor/docs/** - Task-specific documentation files organized by category

This approach ensures Claude only loads context when needed, reducing token consumption and improving response quality.

## Background

Currently, `/conductor:setup` detects the technology stack but doesn't analyze or document existing code patterns, architecture decisions, or conventions. Users who run setup on brownfield projects miss out on having their existing practices documented for AI consumption. This leads to inconsistent AI-generated code that doesn't follow established patterns.

## Requirements

### Functional Requirements

#### FR-1: Codebase Analysis Engine

The setup command must analyze existing codebases to detect:

**FR-1.1: Code Patterns**
- [x] File and directory naming conventions (kebab-case, PascalCase, etc.)
- [x] Module organization patterns (barrel exports, index files)
- [x] Import patterns (absolute vs relative, path aliases)
- [x] Common file structures (components/, services/, utils/, etc.)

**FR-1.2: Architecture Patterns**
- [x] Design patterns in use (Repository, Factory, Singleton, Observer, etc.)
- [x] Layer organization (MVC, Clean Architecture, Hexagonal, etc.)
- [x] Dependency injection patterns
- [x] State management patterns (for frontend)

**FR-1.3: Testing Patterns**
- [x] Test file naming conventions (*.test.ts, *.spec.ts, __tests__/)
- [x] Test framework identification (Jest, Pytest, Go testing, etc.)
- [x] Mocking patterns and utilities
- [x] Test organization (unit, integration, e2e)

**FR-1.4: Annotations and Decorators**
- [x] Custom decorators/annotations and their purposes
- [x] Framework-specific decorators (e.g., @Injectable, @Entity, @Route)
- [x] Documentation annotations (JSDoc, docstrings, GoDoc)

**FR-1.5: Configuration Patterns**
- [x] Configuration file formats and locations
- [x] Environment variable patterns
- [x] Build tool configurations (webpack, vite, rollup, etc.)
- [x] CI/CD pipeline patterns

**FR-1.6: API Conventions**
- [x] REST endpoint naming patterns
- [x] GraphQL schema conventions
- [x] Request/Response format patterns
- [x] Error handling conventions

#### FR-2: Progressive Disclosure Documentation Structure

**FR-2.1: CLAUDE.md Generation**
Generate a high-level CLAUDE.md containing:
- [x] Project summary (one paragraph)
- [x] Quick reference: Core coding rules (5-10 bullet points)
- [x] Directory structure overview
- [x] Links to detailed documentation in conductor/docs/

**FR-2.2: conductor/docs/ Generation**
Create organized documentation files:

| File | Content |
|------|---------|
| `architecture.md` | Architecture patterns, layer organization, design patterns |
| `code-conventions.md` | Naming conventions, import patterns, file organization |
| `testing.md` | Test patterns, framework usage, mocking conventions |
| `api-patterns.md` | REST/GraphQL conventions, error handling, response formats |
| `configuration.md` | Config files, env vars, build setup |
| `annotations.md` | Decorators, annotations, and their usage |

**FR-2.3: Cross-referencing**
Each documentation file must:
- [x] Include a header linking back to CLAUDE.md
- [x] Reference related documentation files where relevant
- [x] Include concrete code examples from the actual codebase

#### FR-3: Integration with Existing Setup Flow

**FR-3.1: Brownfield Enhancement**
- [x] Execute after existing brownfield analysis (Section 2.0)
- [x] Use already-detected stack information as input
- [x] Run before product definition generation

**FR-3.2: CLAUDE.md Handling**
- [x] If CLAUDE.md exists: Merge new content, preserve user sections
- [x] If CLAUDE.md doesn't exist: Create new file
- [x] Mark auto-generated sections with comments for easy identification

**FR-3.3: conductor/docs/ Handling**
- [x] Create directory if it doesn't exist
- [x] Overwrite existing auto-generated docs (marked sections only)
- [x] Preserve any user-added documentation files

#### FR-4: Analysis Configuration

**FR-4.1: Single Consolidated Review**
- [x] Present all detected patterns in a single formatted summary
- [x] Use single AskUserQuestion with multi-select for category approval
- [x] Allow user to approve all, select specific categories, or skip

### Non-Functional Requirements

- [x] **NFR-1: Performance** - Analysis must complete within 60 seconds for codebases up to 10,000 files
- [x] **NFR-2: File Sampling** - Use sampling for large files (first 100 + last 50 lines)
- [x] **NFR-3: Ignore Patterns** - Respect .gitignore and .claudeignore patterns
- [x] **NFR-4: Confidence Levels** - Pattern detection with HIGH/MEDIUM/LOW confidence
- [x] **NFR-5: Timestamps** - Generated documentation includes "last analyzed" timestamp
- [x] **NFR-6: Auto-generated Markers** - Clearly mark auto-generated vs user-added sections

## Acceptance Criteria

- [x] Running `/conductor:setup` on a brownfield project generates CLAUDE.md with project overview
- [x] Running `/conductor:setup` creates conductor/docs/ with categorized documentation
- [x] Generated documentation includes actual code examples from the codebase
- [x] Analysis results are presented in a single consolidated review question
- [x] Existing CLAUDE.md content is preserved during merge
- [x] Auto-generated sections are clearly marked for future updates
- [x] Documentation includes confidence levels for detected patterns

## Out of Scope

- Real-time documentation updates during development
- Language-specific AST parsing (use heuristics instead)
- Automatic documentation for private/internal APIs
- Integration with external documentation tools (Confluence, Notion)
- CLI commands for analysis (all handled in setup protocol)

## Dependencies

- Existing brownfield detection in setup.md (Section 2.0)
- Stack detection protocol (protocols/stack-detection.md)

## References

- [Claude Code Progressive Disclosure](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#progressive-disclosure)
- [Conductor Setup Command](../../../commands/setup.md)
