# Implementation Plan: Git Branch/Worktree Integration for Implement Command

## Phase 1: Update Command Configuration [checkpoint: 5ac679f]

- [x] Task: Add AskUserQuestion to allowed-tools in implement.md frontmatter [37172b4]
    - [x] Read the frontmatter section of implement.md
    - [x] Add `- AskUserQuestion` to the allowed-tools list
    - [x] Verify the YAML frontmatter remains valid

- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Implement Git Isolation Protocol Section

- [x] Task: Create Section 2.1 GIT ISOLATION SETUP structure [c76e29a]
    - [x] Insert new section between 2.0 TRACK SELECTION and 2.5 SKILL ACTIVATION
    - [x] Add section header and protocol description
    - [x] Define the step-by-step protocol structure

- [x] Task: Implement Step 1 - Current Branch Detection [c752bd9]
    - [x] Document the git command to get current branch (`git branch --show-current`)
    - [x] Document the git command to get current commit/status
    - [x] Add logic to detect if on main/master vs feature branch
    - [x] Add pattern matching logic for track-related branch names

- [x] Task: Implement Step 2 - Branch Name Generation [5e4bb70]
    - [x] Document reading track type from metadata.json
    - [x] Define prefix mapping table (feature→feature/, bugfix→fix/, etc.)
    - [x] Document branch name format: `<prefix><track_shortname>`
    - [x] Add worktree path generation logic

- [x] Task: Implement Step 3 - AskUserQuestion Integration [38229a6]
    - [x] Document the AskUserQuestion tool call structure
    - [x] Define options for existing branch detection scenario
    - [x] Define options for new branch creation scenario
    - [x] Include worktree option in choices
    - [x] Ensure "Type your own name" option is included

- [x] Task: Implement Step 4 - Git Operations Execution [36d4a68]
    - [x] Document branch creation command (`git checkout -b`)
    - [x] Document worktree creation command (`git worktree add`)
    - [x] Add verification step to confirm operation succeeded
    - [x] Add error handling for common failures (dirty working tree, branch exists)

- [x] Task: Implement Step 5 - Fallback Instructions [f2a2c09]
    - [x] Add fallback for when git operations fail
    - [x] Document manual recovery steps
    - [x] Add clear error messages for users

- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Add CLI Support for Branch Operations

- [ ] Task: Add CLI command reference for branch operations
    - [ ] Add entry to CLI Command Reference table for branch suggestion
    - [ ] Document JSON output format for branch suggestions
    - [ ] Add fallback instructions for CLI failures

- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Documentation and Testing

- [ ] Task: Update section cross-references
    - [ ] Ensure Section 3.0 references the new git isolation step
    - [ ] Update any "proceed to next section" language
    - [ ] Verify section numbering is consistent

- [ ] Task: Add example scenarios to documentation
    - [ ] Add example for feature track branch creation
    - [ ] Add example for bugfix track branch creation
    - [ ] Add example for worktree creation
    - [ ] Add example for continuing on existing branch

- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
