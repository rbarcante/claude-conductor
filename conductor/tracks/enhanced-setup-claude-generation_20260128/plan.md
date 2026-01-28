# Implementation Plan: Enhanced Setup - CLAUDE.md Generation with Progressive Disclosure

> **Track ID:** `enhanced-setup-claude-generation_20260128`

## Overview

This plan implements the enhanced `/conductor:setup` command with comprehensive codebase analysis and Progressive Disclosure documentation generation. All functionality is implemented directly in the setup protocol. Analysis results are presented in a single consolidated review.

---

## Phase 1: Analysis Protocol Design

### Objective
Create the codebase analysis protocol document that defines how to detect patterns.

- [ ] Task: Create codebase analysis protocol
    - [ ] Create `protocols/codebase-analysis.md`
    - [ ] Define pattern detection algorithms using file reading and grep
    - [ ] Document code pattern detection rules (naming, imports, structure)
    - [ ] Document architecture pattern detection rules
    - [ ] Document testing pattern detection rules
    - [ ] Document annotation/decorator detection rules
    - [ ] Document API convention detection rules
    - [ ] Document configuration pattern detection rules
    - [ ] Add confidence scoring methodology

- [ ] Task: Create documentation templates
    - [ ] Create `templates/claude-md.md` template with Progressive Disclosure structure
    - [ ] Create `templates/docs/` folder with category templates (architecture.md, code-conventions.md, testing.md, api-patterns.md, configuration.md, annotations.md)
    - [ ] Define auto-generated section markers (`<!-- AUTO-GENERATED -->`)

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Analysis Protocol Design' (Protocol in workflow.md)

---

## Phase 2: Integration into Setup Command

### Objective
Integrate the analysis into the existing setup.md flow with a single consolidated review.

- [ ] Task: Add codebase analysis section to setup.md (Section 2.0.2)
    - [ ] Add analysis workflow after stack detection
    - [ ] Execute all pattern detection categories
    - [ ] Collect all detected patterns into a structured result
    - [ ] Calculate confidence levels for each category

- [ ] Task: Add single consolidated review step
    - [ ] Present all analysis results to user in formatted summary
    - [ ] Add single AskUserQuestion with multi-select for category approval
    - [ ] Options: Each detected category as a selectable option (e.g., "Code Conventions (8 patterns)", "Architecture (3 patterns)")
    - [ ] Allow user to approve all, select specific categories, or skip

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Integration into Setup Command' (Protocol in workflow.md)

---

## Phase 3: Documentation Generation

### Objective
Implement the documentation generation based on approved analysis results.

- [ ] Task: Define CLAUDE.md generation logic
    - [ ] Generate overview section from product.md context
    - [ ] Generate quick reference (5-10 key rules) from approved patterns
    - [ ] Generate links section to conductor/docs/
    - [ ] Define merge strategy for existing CLAUDE.md

- [ ] Task: Define conductor/docs/ generation logic
    - [ ] Generate only files for approved categories
    - [ ] Include code examples extracted during analysis
    - [ ] Add confidence indicators where applicable
    - [ ] Add cross-references between related files

- [ ] Task: Add documentation generation section to setup.md (Section 2.0.3)
    - [ ] Generate CLAUDE.md and conductor/docs/ based on approved categories
    - [ ] Handle CLAUDE.md merge if file exists
    - [ ] Present final documentation for user confirmation

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Documentation Generation' (Protocol in workflow.md)

---

## Phase 4: Finalization & Testing

### Objective
Final integration, testing, and project documentation updates.

- [ ] Task: Update setup finalization section
    - [ ] Add CLAUDE.md to committed files
    - [ ] Add conductor/docs/ to committed files
    - [ ] Update state machine with new steps (2.0.2_analysis, 2.0.3_docs)
    - [ ] Update commit message format

- [ ] Task: Manual testing
    - [ ] Test on existing brownfield project
    - [ ] Verify single-question review flow
    - [ ] Verify documentation generation quality
    - [ ] Test CLAUDE.md merge scenario

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
