# Implementation Plan: Reduce Token Usage in newTrack → implement Workflow

## Summary

This plan addresses token optimization through modularization, consolidation, and lazy loading strategies. The goal is a 50% reduction in context tokens for the newTrack workflow.

---

# Phase 1: Modularize CLAUDE.md

**Goal**: Extract verbose protocols to separate files, keeping CLAUDE.md as a lightweight pointer.

- [ ] Task: Create protocols reference directory structure
    - [ ] Create `protocols/skill-loading.md` with full Skill Loading Protocol
    - [ ] Create `protocols/pattern-resolution.md` with full Pattern Resolution Protocol
    - [ ] Verify protocols are valid standalone documents

- [ ] Task: Refactor CLAUDE.md to use protocol references
    - [ ] Replace Skill Loading Protocol with 10-line summary + reference
    - [ ] Replace Pattern Resolution Protocol with 10-line summary + reference
    - [ ] Keep Universal File Resolution Protocol (essential, 41 lines)
    - [ ] Target: CLAUDE.md < 150 lines

- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

---

# Phase 2: Condense newTrack.md Command

**Goal**: Reduce repetitive content in the command definition.

- [ ] Task: Create AskUserQuestion reference template
    - [ ] Create `templates/askuserquestion-patterns.md` with all JSON examples
    - [ ] Document question type patterns (Additive, Exclusive, Approval)
    - [ ] Include header constraints and option rules

- [ ] Task: Refactor newTrack.md to reference template
    - [ ] Keep ONE example per question type in command file
    - [ ] Reference template for additional patterns
    - [ ] Remove repeated JSON structures (8+ occurrences → 1 reference)
    - [ ] Target: newTrack.md < 300 lines

- [ ] Task: Consolidate setup check with context loading
    - [ ] Combine sections 1.1 and 2.1 to avoid duplicate file reads
    - [ ] Pass resolved context to subsequent phases
    - [ ] Document which files are read once vs repeatedly

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

---

# Phase 3: Optimize conductor-methodology Skill

**Goal**: Create lightweight summary for always-active loading.

- [ ] Task: Create SKILL-SUMMARY.md pattern
    - [ ] Define summary format (30-50 lines max)
    - [ ] Include: Core philosophy, plan structure, status markers, key commands
    - [ ] Exclude: Detailed TDD workflow, git notes, commit patterns

- [ ] Task: Create conductor-methodology SKILL-SUMMARY.md
    - [ ] Extract essential concepts from 283-line SKILL.md
    - [ ] Target: 40 lines maximum
    - [ ] Ensure completeness for newTrack context needs

- [ ] Task: Update Skill Loading Protocol for summaries
    - [ ] Add "summary_available" field to skill manifest
    - [ ] Load SKILL-SUMMARY.md by default for always-active skills
    - [ ] Load full SKILL.md only when task requires detailed guidance

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

---

# Phase 4: Reduce Redundant File Reads

**Goal**: Ensure each context file is read only once per workflow.

- [ ] Task: Audit newTrack.md for redundant reads
    - [ ] Map all file read operations in the workflow
    - [ ] Identify files read multiple times (workflow.md, product.md, etc.)
    - [ ] Document actual read count vs necessary read count

- [ ] Task: Refactor workflow.md read pattern
    - [ ] Read workflow.md once during setup check
    - [ ] Extract "Phase Completion Protocol exists" flag
    - [ ] Pass flag to plan generation (avoid re-read)

- [ ] Task: Document context passing strategy
    - [ ] Add section to newTrack.md explaining context reuse
    - [ ] Specify which values should be cached between phases
    - [ ] Update protocol to pass context explicitly

- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

---

# Phase 5: Verification and Documentation

**Goal**: Validate optimizations and document changes.

- [ ] Task: Measure token reduction
    - [ ] Calculate new line counts for all modified files
    - [ ] Compare against baseline measurements
    - [ ] Document achieved reduction percentage

- [ ] Task: Manual testing of workflows
    - [ ] Test newTrack command with feature description
    - [ ] Test newTrack command with bug description
    - [ ] Verify spec and plan generation quality unchanged
    - [ ] Test implement command with generated track

- [ ] Task: Update documentation
    - [ ] Add optimization notes to CLAUDE.md header
    - [ ] Document new file structure in conductor/index.md
    - [ ] Create summary of changes for maintainers

- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

---

## Metrics

| Metric | Baseline | Target | Actual |
|--------|----------|--------|--------|
| CLAUDE.md lines | 339 | < 150 | TBD |
| newTrack.md lines | 544 | < 300 | TBD |
| conductor-methodology summary | 283 | < 50 | TBD |
| workflow.md reads per newTrack | 2+ | 1 | TBD |
| Total context lines (newTrack) | ~3,000 | ~1,500 | TBD |
