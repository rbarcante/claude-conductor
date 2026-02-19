# Implementation Plan: Fix task-specific skill activation in implement.md

## Phase 1: Update implement.md Section 2.5 (Consolidated Skill Activation)

- [ ] Task 1.1: Rewrite Section 2.5 to perform full skill scoring upfront — extract keywords from track spec/plan, match against tech stack from `conductor/tech-stack.md`, score all non-always-active skills, and load SKILL.md for skills scoring >= 1.5
- [ ] Task 1.2: Remove Phase 2 deferred loading instructions from Section 2.5, replacing with a single consolidated phase
- [ ] Task 1.3: Update Section 3.0 Step 5.c.i — replace per-task skill activation with a reference to pre-loaded skills from Section 2.5
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Update Skill Loading Protocol

- [ ] Task 2.1: Update `protocols/skill-loading.md` to describe consolidated upfront activation — remove per-task scoring model, clarify that all scoring happens before task execution begins
- [ ] Task 2.2: Update CLAUDE.md Skill Loading Protocol quick reference if it references per-task activation
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Final Review

- [ ] Task 3.1: Cross-reference all changes for consistency — verify Section 2.5, Step 5.c.i, protocol, and CLAUDE.md all align
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
