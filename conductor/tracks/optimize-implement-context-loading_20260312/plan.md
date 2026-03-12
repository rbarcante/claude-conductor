# Implementation Plan: Optimize implement.md context loading after newTrack flow

## Phase 1: Add Warm Start Detection to implement.md

- [ ] Task: Add Section 1.0.1 "WARM START DETECTION" after Section 1.0 in `commands/implement.md`
  - Parse args for `--warm-start` flag
  - If detected: announce warm start mode, skip to Section 2.2 (base branch detection)
  - If not detected: proceed normally through Section 1.1
- [ ] Task: Modify Section 3.0 Step 2 to use conditional context loading
  - Add warm start conditional: use `read-context --include plan,metadata` (skip spec)
  - Add warm start conditional: skip workflow.md re-read (use "FROM CONTEXT" note)
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Update newTrack to pass warm start signal

- [ ] Task: Modify `commands/newTrack.md` Phase B Section 2.5 to pass `--warm-start` flag
  - Change Skill invocation from `args: "<TRACK_ID>"` to `args: "<TRACK_ID> --warm-start"`
  - Also update the CC Plan File template (protocol section) to reflect the new args format
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
