# Implementation Plan: Update setup.md to use XML tags following newTrack.md pattern

## Phase 1: Analysis and Tag Mapping

- [ ] Task: Read and compare both files
  - [ ] Sub-task: Read current `commands/setup.md` in full
  - [ ] Sub-task: Confirm tag schema from `commands/newTrack.md`
  - [ ] Sub-task: Map every setup.md section to its XML tag equivalent
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Apply XML Tags to setup.md

- [ ] Task: Wrap Section 1.0 SYSTEM DIRECTIVE in `<system_directive>` with `<note type="critical">`
- [ ] Task: Wrap Action CLI Commands + Fallback in `<cli_reference>`
- [ ] Task: Wrap AskUserQuestion Protocol in `<protocol name="askuserquestion">` with `<constraints>`
- [ ] Task: Wrap Section 1.1 RESUME CHECK in `<phase name="resume_check">`
- [ ] Task: Wrap Section 1.2 PRE-INITIALIZATION OVERVIEW in `<phase name="pre_init">`
- [ ] Task: Wrap Section 2.0 PROJECT INCEPTION in `<phase name="inception">` with `<instructions>` per sub-section (2.0.1, 2.0.2, 2.0.3)
- [ ] Task: Wrap Sections 2.1–2.5 each in individual `<phase>` with `<instructions>`
- [ ] Task: Wrap Section 2.5.1 Documentation Generation in `<phase name="docs_generation">` with brownfield `<note>`
- [ ] Task: Wrap Section 2.6 Finalization in `<phase name="finalization">`
- [ ] Task: Wrap Section 3.0–3.4 Initial Track Generation in `<phase name="track_generation">` with `<instructions>` per sub-section
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
