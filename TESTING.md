# Testing Guide for Conductor Plugin

This guide provides instructions for testing the Conductor plugin after installation.

## Prerequisites

- Claude Code CLI installed
- Git configured on your system
- A test project directory (can be new or existing)

## Installation for Testing

### Option 1: Local Plugin Directory

```bash
# Copy plugin to Claude Code plugins directory
cp -r conductor-plugin ~/.claude/plugins/conductor

# Or create a symlink for development
ln -s /path/to/conductor-plugin ~/.claude/plugins/conductor
```

### Option 2: Use Plugin Directory Flag

```bash
# Test without installing
cc --plugin-dir /path/to/conductor-plugin
```

## Test Scenarios

### Test 1: Plugin Loading

**Objective:** Verify the plugin loads correctly in Claude Code

**Steps:**
1. Start Claude Code: `cc`
2. Type `/help` and verify conductor commands appear:
   - `/conductor:setup`
   - `/conductor:newTrack`
   - `/conductor:implement`
   - `/conductor:status`
   - `/conductor:revert`

**Expected Result:** All 5 commands should be listed in help output

---

### Test 2: Greenfield Setup (New Project)

**Objective:** Test setup workflow for a new project

**Steps:**
1. Create empty test directory: `mkdir test-greenfield && cd test-greenfield`
2. Start Claude Code: `cc`
3. Run `/conductor:setup`
4. Follow the prompts:
   - Should ask "What do you want to build?"
   - Should walk through product guide questions
   - Should walk through product guidelines questions
   - Should walk through tech stack questions
   - Should ask about code style guides
   - Should ask about workflow customization
   - Should propose an initial track

**Expected Results:**
- `conductor/` directory created
- `conductor/product.md` created
- `conductor/product-guidelines.md` created
- `conductor/tech-stack.md` created
- `conductor/workflow.md` created
- `conductor/code_styleguides/` directory with selected guides
- `conductor/tracks.md` created
- `conductor/tracks/<track_id>/` directory created
- `conductor/tracks/<track_id>/spec.md` created
- `conductor/tracks/<track_id>/plan.md` created
- `conductor/tracks/<track_id>/metadata.json` created
- Git commit created: `conductor(setup): Add conductor setup files`

**Validation:**
```bash
# Check structure
ls -la conductor/
ls -la conductor/tracks/
cat conductor/tracks.md
```

---

### Test 3: Brownfield Setup (Existing Project)

**Objective:** Test setup workflow for existing project

**Steps:**
1. Navigate to existing project with code
2. Ensure git repository exists and is clean
3. Start Claude Code: `cc`
4. Run `/conductor:setup`
5. Should detect brownfield project
6. Should ask permission for code analysis
7. Should analyze existing code
8. Should infer tech stack

**Expected Results:**
- Code analysis summary provided
- Inferred tech stack presented for confirmation
- Setup completes with conductor/ structure
- Existing code remains untouched

---

### Test 4: Resume Setup

**Objective:** Test resume functionality if setup is interrupted

**Steps:**
1. Start `/conductor:setup`
2. Complete product guide section
3. Interrupt (Ctrl+C) before completing
4. Check `conductor/setup_state.json` exists
5. Run `/conductor:setup` again
6. Should resume from last completed step

**Expected Results:**
- Setup resumes without re-asking completed questions
- State file tracks progress correctly

---

### Test 5: Create New Track

**Objective:** Test track creation workflow

**Steps:**
1. After setup is complete
2. Run `/conductor:newTrack "Add user login feature"`
3. Answer specification questions
4. Review and approve spec
5. Review and approve plan

**Expected Results:**
- New track directory created: `conductor/tracks/<new_track_id>/`
- `spec.md` contains requirements
- `plan.md` contains phased task list with TDD structure
- `metadata.json` created with correct type
- `conductor/tracks.md` updated with new track
- Git commit created: `conductor(track): Create track 'Add user login feature'`

**Validation:**
```bash
cat conductor/tracks.md
cat conductor/tracks/<track_id>/spec.md
cat conductor/tracks/<track_id>/plan.md
```

---

### Test 6: Status Check

**Objective:** Test status reporting

**Steps:**
1. After creating tracks
2. Run `/conductor:status`

**Expected Results:**
- Summary of all tracks
- Status of each track (pending/in progress/completed)
- Overall progress percentage
- Current task if any in progress

---

### Test 7: Implement Track

**Objective:** Test track implementation workflow

**Steps:**
1. Run `/conductor:implement`
2. Should select first pending track
3. Should load plan and begin implementing tasks
4. Follow TDD workflow for at least one task:
   - Write failing tests
   - Implement feature
   - Verify tests pass
   - Commit with task note

**Expected Results:**
- Track status changes to `[~]` in tracks.md
- Tasks marked `[~]` then `[x]` in plan.md
- Code commits created for each task
- Plan commits created for each task completion
- Git notes attached to commits
- Phase checkpoints created if phase completes

**Validation:**
```bash
git log --oneline
git notes show <commit-sha>
cat conductor/tracks/<track_id>/plan.md
```

---

### Test 8: Revert Work

**Objective:** Test git-aware revert functionality

**Steps:**
1. After implementing some tasks
2. Run `/conductor:revert`
3. Select a task/phase to revert
4. Confirm the revert plan

**Expected Results:**
- Shows list of in-progress or completed items
- Identifies all related commits (implementation + plan updates)
- Presents revert plan
- Executes revert after confirmation
- Reverts code and plan changes

**Validation:**
```bash
git log --oneline
cat conductor/tracks/<track_id>/plan.md
```

---

### Test 9: Track Completion & Sync

**Objective:** Test track completion and documentation sync

**Steps:**
1. Complete all tasks in a track
2. Implementation should finish track
3. Should prompt for documentation sync
4. Approve/reject proposed updates to product.md and tech-stack.md
5. Should offer archive/delete/skip options

**Expected Results:**
- Track marked `[x]` in tracks.md
- Sync commit created if docs updated
- Track archived/deleted/kept based on choice
- Git history clean and logical

---

### Test 10: Skill Activation

**Objective:** Test skill is activated appropriately

**Steps:**
1. Ask questions about Conductor:
   - "How do track IDs work in Conductor?"
   - "What's the TDD workflow in Conductor?"
   - "How do I use git notes in Conductor?"

**Expected Results:**
- Skill should activate and provide informed answers
- Should reference workflow.md and plan structure
- Should explain concepts accurately

---

### Test 11: Pattern Surfacing During Implementation

**Objective:** Test automatic pattern surfacing during task implementation

**Steps:**
1. Create a track with tasks that contain pattern keywords:
   - "Add error handling for API endpoints"
   - "Implement input validation for user forms"
   - "Add logging for debugging"
2. Run `/conductor:implement`
3. Observe pattern surfacing announcements

**Expected Results:**
- Patterns should be detected based on task keywords
- Announcement should appear: `📚 **Relevant Patterns Detected:**`
- User should be prompted with `[Apply patterns? (Y)es / (S)kip / (V)iew first]`
- Selecting "View" should display the AI Quick Reference section
- Selecting "Skip" should continue without applying patterns
- Tasks with no matching keywords should continue silently

---

### Test 12: Patterns Command - List

**Objective:** Test `/conductor:patterns list` command

**Steps:**
1. Run `/conductor:patterns` or `/conductor:patterns list`

**Expected Results:**
- Table of all available patterns displayed
- Pattern name, category, and description shown
- Total count displayed
- Tip for using show command included

---

### Test 13: Patterns Command - Search

**Objective:** Test `/conductor:patterns search` command

**Steps:**
1. Run `/conductor:patterns search error`
2. Run `/conductor:patterns search validation`
3. Run `/conductor:patterns search nonexistent`

**Expected Results:**
- Search "error" should return Error Handling pattern with high relevance
- Search "validation" should return Validation pattern
- Search "nonexistent" should return "No patterns found" message
- Results should show relevance ranking

---

### Test 14: Patterns Command - Show

**Objective:** Test `/conductor:patterns show` command

**Steps:**
1. Run `/conductor:patterns show error-handling`
2. Run `/conductor:patterns show logging`
3. Run `/conductor:patterns show nonexistent-pattern`

**Expected Results:**
- Show "error-handling" should display full pattern content
- AI Quick Reference section should be prominently displayed
- Show "nonexistent-pattern" should show "Pattern Not Found" with suggestions

---

### Test 15: Edge Case - No Matching Patterns

**Objective:** Test pattern surfacing with tasks that have no matching keywords

**Steps:**
1. Create a track with generic tasks:
   - "Update README documentation"
   - "Refactor file structure"
2. Run `/conductor:implement`

**Expected Results:**
- Implementation should proceed silently without pattern announcements
- No "No patterns found" noise should be displayed
- User can manually search with `/conductor:patterns search`

---

## Edge Cases to Test

### Edge Case 1: Empty Tracks File
- Delete conductor/tracks.md
- Run `/conductor:status`
- Should handle gracefully with error message

### Edge Case 2: Corrupted State File
- Modify conductor/setup_state.json with invalid JSON
- Run `/conductor:setup`
- Should handle gracefully

### Edge Case 3: No Git Repository
- Create new directory without git init
- Run `/conductor:setup` for greenfield
- Should initialize git repository

### Edge Case 4: Uncommitted Changes
- Make changes without committing
- Run `/conductor:setup` for brownfield
- Should warn about uncommitted changes

### Edge Case 5: Multiple Tracks
- Create 3-4 tracks
- Run `/conductor:implement` without argument
- Should select first incomplete track

---

## Performance Testing

### Large Plan Test
1. Create track with 20+ tasks
2. Implement several tasks
3. Run `/conductor:status`
4. Should handle large plans efficiently

### Multiple Tracks Test
1. Create 5+ tracks
2. Check tracks.md parsing
3. Verify status command handles multiple tracks

---

## Validation Checklist

After testing, verify:

- [ ] All commands load and execute
- [ ] Greenfield setup completes end-to-end
- [ ] Brownfield setup analyzes code correctly
- [ ] Resume functionality works
- [ ] Track creation generates all files
- [ ] Status command provides accurate overview
- [ ] Implementation follows TDD workflow
- [ ] Git commits are properly formatted
- [ ] Git notes are attached correctly
- [ ] Revert identifies correct commits
- [ ] Documentation sync works
- [ ] Track cleanup (archive/delete) works
- [ ] Skill activates on relevant questions
- [ ] Error handling is graceful
- [ ] File permissions are correct
- [ ] Templates copy correctly from $CLAUDE_PLUGIN_ROOT
- [ ] Pattern surfacing works during implementation
- [ ] `/conductor:patterns list` displays all patterns
- [ ] `/conductor:patterns search` finds relevant patterns
- [ ] `/conductor:patterns show` displays pattern content
- [ ] No patterns silently skipped (no noise)

---

## Reporting Issues

If you find issues during testing:

1. Note the exact command run
2. Capture the error message
3. Check the git log for unexpected commits
4. Verify file contents in conductor/
5. Review `conductor/setup_state.json` if relevant
6. Note the Claude Code version

---

## Clean Up After Testing

```bash
# Remove conductor directory
rm -rf conductor/

# Remove test commits
git log --oneline
git reset --hard <commit-before-testing>

# Remove plugin
rm -rf ~/.claude/plugins/conductor
```
