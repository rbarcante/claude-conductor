# Specification: Wiki Comprehensive Audit & Update

## Overview

Perform a comprehensive audit and update of the Claude Conductor wiki (`.wiki` repo) to fully reflect the current state of the conductor plugin. This includes adding missing documentation pages, updating outdated content, and ensuring all features, commands, and systems are accurately represented.

## Functional Requirements

### FR1: Create Commands-CodeReview.md
- Add a new wiki page documenting the `/conductor:codeReview` command
- Cover command purpose, usage, analysis dimensions (Code Quality, Security, Test Coverage), execution strategies (parallel vs sequential), and output format

### FR2: Update Navigation & Index Pages
- Update `_Sidebar.md` to include Code Review link
- Update `Commands.md` to reference 9 commands (not 8) and add codeReview entry to all tables
- Update `Home.md` commands table and features section

### FR3: Update Architecture.md
- Add `agents/` directory to plugin structure
- Document the 5 specialist sub-agents
- Add `codeReview.md` to commands listing
- Add mention of parallel analysis architecture

### FR4: Update Protocols.md
- Document 4 missing protocols: codebase-analysis, pattern-resolution, skill-loading, verify-setup

### FR5: Update Patterns-System.md
- List the 5 specific anti-patterns (god-object, mutable-defaults, spaghetti-code, magic-numbers, deep-nesting) with descriptions

### FR6: Feature Visibility in Home.md
- Add Specialist Sub-Agents to the features section
- Enhance Quality Intelligence description to reference parallel analysis

## Non-Functional Requirements

- All changes are wiki-only (conductor repo is read-only reference)
- Maintain existing wiki style, formatting, and link conventions
- Use `[[wiki-link|Page]]` syntax consistently
- Keep pages concise and scannable

## Acceptance Criteria

- [ ] All 9 commands are documented with dedicated pages
- [ ] _Sidebar.md links to all pages including CodeReview
- [ ] Architecture.md reflects agents/ directory and all components
- [ ] Protocols.md documents all 10+ protocols
- [ ] Patterns-System.md lists all anti-patterns
- [ ] Home.md accurately represents all features and commands

## Out of Scope

- Changes to the conductor repo itself
- Creating a separate Agents-System.md deep-dive page
- Documenting marketplace.json (infrastructure, not user-facing)
