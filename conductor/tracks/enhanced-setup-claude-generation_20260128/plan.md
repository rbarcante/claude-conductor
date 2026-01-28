# Implementation Plan: Enhanced Setup - CLAUDE.md Generation with Progressive Disclosure

> **Track ID:** `enhanced-setup-claude-generation_20260128`

## Overview

This plan implements the enhanced `/conductor:setup` command with comprehensive codebase analysis and Progressive Disclosure documentation generation. All functionality is implemented directly in the setup protocol. Analysis results are presented in a single consolidated review.

---

## Phase 1: Analysis Protocol Design [checkpoint: 49e600a]

### Objective
Create the codebase analysis protocol document that defines how to detect patterns.

- [x] Task: Create codebase analysis protocol [078f2bd]
    - [x] Create `protocols/codebase-analysis.md`
    - [x] Define pattern detection algorithms using file reading and grep
    - [x] Document code pattern detection rules (naming, imports, structure)
    - [x] Document architecture pattern detection rules
    - [x] Document testing pattern detection rules
    - [x] Document annotation/decorator detection rules
    - [x] Document API convention detection rules
    - [x] Document configuration pattern detection rules
    - [x] Add confidence scoring methodology

- [x] Task: Create documentation templates [6ae5d56]
    - [x] Create `templates/claude-md.md` template with Progressive Disclosure structure
    - [x] Create `templates/docs/` folder with category templates (architecture.md, code-conventions.md, testing.md, api-patterns.md, configuration.md, annotations.md)
    - [x] Define auto-generated section markers (`<!-- AUTO-GENERATED -->`)

- [x] Task: Conductor - User Manual Verification 'Phase 1: Analysis Protocol Design' (Protocol in workflow.md) [49e600a]

---

## Phase 2: Integration into Setup Command [checkpoint: de25bcd]

### Objective
Integrate the analysis into the existing setup.md flow with a single consolidated review.

- [x] Task: Add codebase analysis section to setup.md (Section 2.0.2) [1abc467]
    - [x] Add analysis workflow after stack detection
    - [x] Execute all pattern detection categories
    - [x] Collect all detected patterns into a structured result
    - [x] Calculate confidence levels for each category

- [x] Task: Add single consolidated review step [1abc467]
    - [x] Present all analysis results to user in formatted summary
    - [x] Add single AskUserQuestion with multi-select for category approval
    - [x] Options: Each detected category as a selectable option (e.g., "Code Conventions (8 patterns)", "Architecture (3 patterns)")
    - [x] Allow user to approve all, select specific categories, or skip

- [x] Task: Conductor - User Manual Verification 'Phase 2: Integration into Setup Command' (Protocol in workflow.md) [de25bcd]

---

## Phase 3: Documentation Generation [checkpoint: aec3951]

### Objective
Implement the documentation generation based on approved analysis results.

- [x] Task: Define CLAUDE.md generation logic [9b13374]
    - [x] Generate overview section from product.md context
    - [x] Generate quick reference (5-10 key rules) from approved patterns
    - [x] Generate links section to conductor/docs/
    - [x] Define merge strategy for existing CLAUDE.md

- [x] Task: Define conductor/docs/ generation logic [9b13374]
    - [x] Generate only files for approved categories
    - [x] Include code examples extracted during analysis
    - [x] Add confidence indicators where applicable
    - [x] Add cross-references between related files

- [x] Task: Add documentation generation section to setup.md (Section 2.5.1) [9b13374]
    - [x] Generate CLAUDE.md and conductor/docs/ based on approved categories
    - [x] Handle CLAUDE.md merge if file exists
    - [x] Present final documentation for user confirmation

- [x] Task: Conductor - User Manual Verification 'Phase 3: Documentation Generation' (Protocol in workflow.md) [aec3951]

---

## Phase 4: Finalization & Testing

### Objective
Final integration, testing, and project documentation updates.

- [x] Task: Update setup finalization section [9b870ce]
    - [x] Add product-guidelines.md updates to committed files
    - [x] Add conductor/docs/ to committed files
    - [x] Update state machine with new steps (2.0.2_analysis, 2.5.1_docs_generated)
    - [x] Update resume handling for new states

- [ ] Task: Manual testing (deferred)
    - [ ] Test on existing brownfield project
    - [ ] Verify single-question review flow
    - [ ] Verify documentation generation quality
    - [ ] Test product-guidelines.md merge scenario

- [ ] Task: Update project documentation
    - [ ] Update README.md with new feature
    - [ ] Update product.md with new capability

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Finalization & Testing' (Protocol in workflow.md)

---

## Summary

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1 | 3 | Analysis Protocol & Templates |
| 2 | 3 | Setup Integration with Single Review |
| 3 | 4 | Documentation Generation |
| 4 | 4 | Finalization & Testing |

**Total Tasks:** 14

---

## Notes

<!-- Implementation notes, decisions made during development -->
