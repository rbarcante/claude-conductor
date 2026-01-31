# Implementation Plan: Reduce Token Usage in newTrack → implement Workflow

## Summary

This plan addresses token optimization through modularization and lazy loading strategies. The primary target is reducing `implement.md` (684 lines) which is loaded when user runs implement after clearing context.

**Key Insight**: User workflow is `newTrack → clean context → implement`. The implement command must reload everything from scratch.

---

# Phase 1: Modularize implement.md (HIGHEST PRIORITY)

**Goal**: Extract inline protocols from implement.md (684 lines → <250 lines)

- [ ] Task: Extract Quality Gate Protocol to separate file
    - [ ] Create `protocols/quality-gate.md` with full quality gate content (lines 248-459)
    - [ ] Include parallel agent mode and inline mode instructions
    - [ ] Include quality gate output format

- [ ] Task: Refactor implement.md section 3.5 QUALITY GATE
    - [ ] Replace ~211 lines of inline protocol with 15-line summary
    - [ ] Add reference: "Follow protocol in `protocols/quality-gate.md`"
    - [ ] Keep only essential trigger conditions and output format

- [ ] Task: Refactor implement.md section 3.6 DECISION CAPTURE
    - [ ] Protocol already exists at `protocols/decision-capture.md`
    - [ ] Replace ~111 lines with 10-line summary + reference
    - [ ] Keep only decision point triggers

- [ ] Task: Condense implement.md sections 4.0 and 5.0
    - [ ] Documentation Sync: reduce verbose examples (~58 lines → ~20 lines)
    - [ ] Track Cleanup: reduce verbose prompts (~38 lines → ~15 lines)

- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

---

# Phase 2: Modularize CLAUDE.md

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

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

---

# Phase 3: Condense newTrack.md Command

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

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

---

# Phase 4: Optimize conductor-methodology Skill

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
    - [ ] Test implement command with generated track
    - [ ] Verify quality gates still work
    - [ ] Verify decision capture still works

- [ ] Task: Update documentation
    - [ ] Document new protocol reference pattern
    - [ ] Update conductor/index.md with new files

- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

---

## Metrics

| Metric | Baseline | Target | Actual |
|--------|----------|--------|--------|
| **implement.md lines** | **684** | **< 250** | TBD |
| CLAUDE.md lines | 339 | < 150 | TBD |
| newTrack.md lines | 544 | < 300 | TBD |
| conductor-methodology summary | 283 | < 50 | TBD |
| **Total implement context** | **~2,500** | **~1,200** | TBD |
