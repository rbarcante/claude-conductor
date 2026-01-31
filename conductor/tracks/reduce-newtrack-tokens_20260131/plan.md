# Implementation Plan: Reduce Token Usage in newTrack → implement Workflow

## Summary

This plan addresses token optimization through modularization and lazy loading strategies. The primary target is reducing `implement.md` (684 lines) which is loaded when user runs implement after clearing context.

**Key Insight**: User workflow is `newTrack → clean context → implement`. The implement command must reload everything from scratch.

---

# Phase 1: Modularize implement.md (HIGHEST PRIORITY)

**Goal**: Extract inline protocols from implement.md (684 lines → <250 lines)

- [x] Task: Extract Quality Gate Protocol to separate file
    - [x] Create `protocols/quality-gate.md` with full quality gate content (lines 248-459)
    - [x] Include parallel agent mode and inline mode instructions
    - [x] Include quality gate output format

- [x] Task: Refactor implement.md section 3.5 QUALITY GATE
    - [x] Replace ~211 lines of inline protocol with 15-line summary
    - [x] Add reference: "Follow protocol in `protocols/quality-gate.md`"
    - [x] Keep only essential trigger conditions and output format

- [x] Task: Refactor implement.md section 3.6 DECISION CAPTURE
    - [x] Protocol already exists at `protocols/decision-capture.md`
    - [x] Replace ~111 lines with 10-line summary + reference
    - [x] Keep only decision point triggers

- [x] Task: Condense implement.md sections 4.0 and 5.0
    - [x] Documentation Sync: reduce verbose examples (~58 lines → ~20 lines)
    - [x] Track Cleanup: reduce verbose prompts (~38 lines → ~15 lines)

- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

---

# Phase 2: Modularize CLAUDE.md

**Goal**: Extract verbose protocols to separate files, keeping CLAUDE.md as a lightweight pointer.

- [x] Task: Create protocols reference directory structure
    - [x] Create `protocols/skill-loading.md` with full Skill Loading Protocol
    - [x] Create `protocols/pattern-resolution.md` with full Pattern Resolution Protocol
    - [x] Verify protocols are valid standalone documents

- [x] Task: Refactor CLAUDE.md to use protocol references
    - [x] Replace Skill Loading Protocol with 10-line summary + reference
    - [x] Replace Pattern Resolution Protocol with 10-line summary + reference
    - [x] Keep Universal File Resolution Protocol (essential, 41 lines)
    - [x] Target: CLAUDE.md < 150 lines (achieved: 86 lines)

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

---

# Phase 3: Condense newTrack.md Command

**Goal**: Reduce repetitive content in the command definition.

- [x] Task: Create AskUserQuestion reference template
    - [x] Create `templates/askuserquestion-patterns.md` with all JSON examples
    - [x] Document question type patterns (Additive, Exclusive, Approval)
    - [x] Include header constraints and option rules

- [x] Task: Refactor newTrack.md to reference template
    - [x] Keep ONE example per question type in command file
    - [x] Reference template for additional patterns
    - [x] Remove repeated JSON structures (8+ occurrences → 1 reference)
    - [x] Target: newTrack.md < 300 lines (achieved: 176 lines)

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

---

# Phase 4: Optimize conductor-methodology Skill

**Goal**: Create lightweight summary for always-active loading.

- [x] Task: Create SKILL-SUMMARY.md pattern
    - [x] Define summary format (30-50 lines max)
    - [x] Include: Core philosophy, plan structure, status markers, key commands
    - [x] Exclude: Detailed TDD workflow, git notes, commit patterns

- [x] Task: Create conductor-methodology SKILL-SUMMARY.md
    - [x] Extract essential concepts from 283-line SKILL.md
    - [x] Target: 40 lines maximum (achieved: 44 lines)
    - [x] Ensure completeness for newTrack context needs

- [x] Task: Update Skill Loading Protocol for summaries
    - [x] Add "summary_available" field to skill manifest
    - [x] Load SKILL-SUMMARY.md by default for always-active skills
    - [x] Load full SKILL.md only when task requires detailed guidance

- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

---

# Phase 5: Verification and Documentation

**Goal**: Validate optimizations and document changes.

- [x] Task: Measure token reduction
    - [x] Calculate new line counts for all modified files
    - [x] Compare against baseline measurements
    - [x] Document achieved reduction percentage

- [ ] Task: Manual testing of workflows
    - [ ] Test newTrack command with feature description
    - [ ] Test implement command with generated track
    - [ ] Verify quality gates still work
    - [ ] Verify decision capture still works

- [ ] Task: Update documentation
    - [ ] Document new protocol reference pattern
    - [ ] Update conductor/index.md with new files

- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

---

## Metrics

| Metric | Baseline | Target | Actual | Reduction |
|--------|----------|--------|--------|-----------|
| **implement.md lines** | **684** | **< 250** | **348** | **49%** |
| CLAUDE.md lines | 339 | < 150 | **86** | **75%** |
| newTrack.md lines | 544 | < 300 | **176** | **68%** |
| conductor-methodology summary | 283 | < 50 | **44** | **84%** |
| **Total implement context** | **~2,500** | **~1,200** | **~654** | **~74%** |
