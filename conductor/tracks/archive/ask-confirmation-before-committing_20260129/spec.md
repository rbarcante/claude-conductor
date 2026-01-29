# Specification: Ask Confirmation Before Committing

> **Type:** bugfix
> **Track ID:** `ask-confirmation-before-committing_20260129`

## Overview

The `/conductor:newTrack` and `/conductor:implement` commands currently commit files automatically at various points without explicitly asking the user for confirmation before the commit. This behavior is problematic because:

1. Users lose control over when commits are made
2. No opportunity to review or cancel before committing
3. Committing is a distinct action from content/task approval and should require explicit confirmation

## Problem Statement

### `/conductor:newTrack` (Section 2.4, Step 5)

**Current Behavior:**
- User approves `spec.md` content
- User approves `plan.md` content
- Track files are written to disk
- Track is registered
- **Files are committed without asking**

**Expected Behavior:**
- After track registration, **ask user to confirm before committing**
- User can approve or skip the commit

### `/conductor:implement` (Multiple locations)

**Current Behavior (via workflow.md Task Workflow):**
- Task implementation completes
- Tests pass
- **Code changes are committed without asking** (Step 8)
- **Plan update is committed without asking** (Step 11)

**Expected Behavior:**
- After task implementation, **ask user to confirm before committing**
- User can approve or skip the commit

## Requirements

### Functional Requirements

- [ ] FR-1: Add Commit Confirmation to newTrack - Before executing the git commit in newTrack Section 2.4 Step 5, ask the user for confirmation
- [ ] FR-2: Add Commit Confirmation to implement Task Workflow - Before executing git commit in workflow.md Task Workflow Step 8, ask the user for confirmation
- [ ] FR-3: Commit Confirmation Question Format - Use a consistent approval pattern across all commit points
- [ ] FR-4: Handle User Response - If "Commit now" execute git commands, if "Skip commit" skip and announce

### Non-Functional Requirements

- [ ] Consistency: Use the same AskUserQuestion format across all commit confirmation points
- [ ] User Experience: Clear messaging about what happens when commit is skipped

## Files to Modify

1. `commands/newTrack.md` - Add confirmation step before Step 5 commit
2. `conductor/workflow.md` - Add confirmation step before Task Workflow Step 8 commit

## Acceptance Criteria

- [ ] AC-1: `/conductor:newTrack` asks for user confirmation before committing track files
- [ ] AC-2: `/conductor:implement` asks for user confirmation before committing task changes
- [ ] AC-3: User can choose to commit or skip at each commit point
- [ ] AC-4: If user skips, files remain on disk but uncommitted
- [ ] AC-5: Announcements reflect whether commit was made or skipped

## Out of Scope

- Changes to the spec or plan approval flow
- Changes to the git branch creation flow
- Changes to phase checkpoint commits (these already have user verification)
- Changes to track archive/delete commits

## Dependencies

- None identified

## References

- commands/newTrack.md Section 2.4
- conductor/workflow.md Task Workflow section
