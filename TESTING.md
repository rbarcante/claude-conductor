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

## Technology Intelligence Test Scenarios

### Stack Detection Tests

**Scenario: Node.js/TypeScript Project Detection**

**Objective:** Verify stack detection correctly identifies a TypeScript/Node.js project

**Steps:**
1. Create a test directory with `package.json` containing React and Express dependencies
2. Add `tsconfig.json` with standard TypeScript configuration
3. Create several `.ts` and `.tsx` files
4. Run `/conductor:setup` and observe the stack detection step

**Expected Results:**
- Confidence: HIGH (score >= 85)
- Primary Language: TypeScript
- Languages Detected: TypeScript, JavaScript
- Frameworks: React (Frontend), Express.js (Backend)
- Build Tools: npm detected from package-lock.json or npm scripts
- Detection should be presented with the standard format:
  ```
  🔍 **Stack Detection Results** (Confidence: HIGH)
  ```

---

**Scenario: Python Project Detection**

**Objective:** Verify stack detection correctly identifies a Python Django project

**Steps:**
1. Create a test directory with `requirements.txt` containing Django and pytest
2. Add several `.py` files in a typical Django structure (views.py, models.py, etc.)
3. Run `/conductor:setup` and observe the stack detection step

**Expected Results:**
- Confidence: HIGH or MEDIUM
- Primary Language: Python
- Frameworks: Django (Backend)
- Testing: pytest detected
- Standard presentation format displayed

---

**Scenario: Go Project Detection**

**Objective:** Verify stack detection correctly identifies a Go project

**Steps:**
1. Create a test directory with `go.mod` containing Gin or Echo framework
2. Add several `.go` files
3. Run `/conductor:setup` and observe the stack detection step

**Expected Results:**
- Primary Language: Go
- Frameworks: Gin or Echo (Backend)
- Build Tools: Go modules
- Appropriate confidence level based on available signals

---

**Scenario: Unknown Stack Handling**

**Objective:** Verify graceful handling when stack cannot be confidently detected

**Steps:**
1. Create an empty directory with only a `README.md` file
2. Run `/conductor:setup` and observe the stack detection step

**Expected Results:**
- Confidence: UNCERTAIN (score < 30)
- Detection message should indicate minimal signals found
- User should be prompted for manual entry:
  ```
  🔍 **Stack Detection Results** (Confidence: UNCERTAIN)
  Minimal detection signals. Manual specification strongly recommended.
  ```
- Fallback to manual tech stack definition in Section 2.3

---

**Scenario: User Acceptance Flow**

**Objective:** Test the user confirmation flow after stack detection

**Steps:**
1. Run stack detection on a known project type
2. When prompted, select option A (Accept)
3. Verify tech-stack.md is populated correctly

**Expected Results:**
- Detected values should pre-populate tech-stack.md
- File should include detection metadata comment:
  ```markdown
  <!-- Auto-detected by Stack Detection Protocol -->
  <!-- Confidence: HIGH -->
  ```

---

**Scenario: User Edit Flow**

**Objective:** Test the user edit flow for correcting detected stack

**Steps:**
1. Run stack detection on a project
2. When prompted, select option B (Edit)
3. Modify one or more detected values
4. Verify corrections are applied

**Expected Results:**
- Each category should be presented for verification
- User corrections should override detected values
- Final tech-stack.md should reflect user modifications

---

### Skill Activation Tests

**Scenario: Always-Active Skill Loading**

**Objective:** Verify Conductor Methodology skill is always loaded

**Steps:**
1. Start implementation on any track: `/conductor:implement`
2. Observe the skill activation announcement

**Expected Results:**
- Conductor Methodology skill should be listed as "always active"
- Announcement format:
  ```
  🔧 **Skills Activated:** Conductor Methodology (always active)
  ```
- No score displayed for always-active skills

---

**Scenario: Context-Based Skill Activation**

**Objective:** Test skill activation based on task keywords

**Steps:**
1. Add a new skill to skill-registry.json with keywords `["authentication", "login"]`
2. Create a track with description containing "authentication"
3. Run `/conductor:implement`
4. Observe skill activation

**Expected Results:**
- New skill should be activated with a score displayed
- Announcement format should include:
  ```
  🔧 **Skills Activated for This Track:**

  **Always Active:**
  - Conductor Methodology: Core development workflow guidance

  **Context-Activated:** (based on track/task matching)
  - [Skill Name] (score: X.X): [Brief description]
  ```

---

**Scenario: Tech Stack Skill Matching**

**Objective:** Test skill activation based on project tech stack

**Steps:**
1. Set up a project with TypeScript/React in tech-stack.md
2. Add a skill with `tech_stack.languages: ["typescript"]` and `tech_stack.frameworks: ["react"]`
3. Run `/conductor:implement`

**Expected Results:**
- Skill should activate with high score due to tech stack match
- Language match: +2.0 points
- Framework match: +1.5 points
- Score should be >= 3.0 for high confidence activation

---

**Scenario: File Pattern Skill Matching**

**Objective:** Test skill activation based on file patterns

**Steps:**
1. Create a track that modifies files matching `conductor/**/*`
2. Run `/conductor:implement`

**Expected Results:**
- Conductor Methodology skill should match via file pattern
- File pattern contributes +1.5 to score
- Skill activates based on file pattern match

---

**Scenario: Maximum Skill Limit**

**Objective:** Verify maximum 5 skills (beyond always-active) are loaded

**Steps:**
1. Add 7+ skills to skill-registry.json with overlapping activation rules
2. Create a task that matches all skills
3. Run `/conductor:implement`

**Expected Results:**
- Maximum 5 scored skills should be activated
- Skills should be sorted by score descending
- Highest scoring skills should be selected
- Always-active skills are not counted toward the limit

---

**Scenario: Skill Registry Missing**

**Objective:** Test graceful handling when skill registry doesn't exist

**Steps:**
1. Rename or remove `skills/skill-registry.json`
2. Run `/conductor:implement`

**Expected Results:**
- Implementation should proceed without errors
- No skill activation announcement should appear
- Warning should be logged internally but not block execution

---

**Scenario: Skill File Missing**

**Objective:** Test handling when a registered skill's SKILL.md is missing

**Steps:**
1. Add a skill entry to registry pointing to non-existent path
2. Run `/conductor:implement`

**Expected Results:**
- Warning should be logged for missing skill
- Other skills should still load correctly
- Implementation should proceed

---

## Quality Intelligence Test Scenarios

### Anti-Pattern Detection Tests

**Scenario: Detect Mutable Defaults in Python**

**Objective:** Verify anti-pattern detection catches mutable default arguments

**Steps:**
1. Create a Python file with mutable default:
   ```python
   def process_items(items=[]):
       items.append("new")
       return items
   ```
2. Run `/conductor:implement` on a task modifying this file
3. Observe quality gate output

**Expected Results:**
- Quality gate should detect Mutable Defaults anti-pattern
- Finding should show:
  - Severity: High
  - File and line number
  - The problematic pattern
- User should be prompted to fix or skip with reason

---

**Scenario: Detect God Object**

**Objective:** Verify anti-pattern detection catches oversized classes

**Steps:**
1. Create a Python/JavaScript file with >500 lines and >20 methods
2. Run `/conductor:implement` on a task modifying this file
3. Observe quality gate output

**Expected Results:**
- Quality gate should detect God Object anti-pattern
- Severity: High
- Metrics shown: line count, method count
- Refactoring guidance available via "View details"

---

**Scenario: Detect Magic Numbers**

**Objective:** Verify anti-pattern detection catches unexplained numeric literals

**Steps:**
1. Create code with magic numbers:
   ```javascript
   if (retries > 3) { /* ... */ }
   const timeout = 86400;
   ```
2. Run quality gate

**Expected Results:**
- Quality gate should detect Magic Numbers
- Severity: Medium (informational)
- Line references for each occurrence

---

**Scenario: No Anti-Patterns Found**

**Objective:** Verify clean code passes quality gate

**Steps:**
1. Create well-structured code with no anti-patterns
2. Run quality gate

**Expected Results:**
- Quality gate should pass with:
  ```
  ✅ **Quality Gate Passed**
  No anti-patterns detected.
  ```
- Implementation should proceed without prompts

---

### Coverage Intelligence Tests

**Scenario: Parse LCOV Coverage Report**

**Objective:** Verify coverage parsing works with LCOV format

**Steps:**
1. Generate coverage report in LCOV format
2. Run quality gate after tests

**Expected Results:**
- Coverage percentage displayed
- Uncovered functions identified
- Priority suggestions generated with estimated gain

---

**Scenario: No Coverage Report Available**

**Objective:** Verify graceful handling when no coverage report exists

**Steps:**
1. Run quality gate without any coverage files present

**Expected Results:**
- Informational message displayed:
  ```
  ℹ️ No coverage report found. Skipping coverage analysis.
  ```
- Quality gate proceeds with anti-pattern detection only

---

**Scenario: Coverage Below Target**

**Objective:** Verify handling when coverage is below 80% target

**Steps:**
1. Generate coverage report showing 75% coverage
2. Run quality gate

**Expected Results:**
- Coverage gap highlighted:
  ```
  **Current Coverage:** 75% (Target: 80%)
  ```
- Top suggestions shown with estimated gain
- User can proceed or add tests

---

### Quality Gate Flow Tests

**Scenario: Skip High-Severity Issue with Reason**

**Objective:** Test the skip workflow for high-severity findings

**Steps:**
1. Trigger a high-severity anti-pattern
2. Choose option "2" (Skip with reason)
3. Enter reason for each finding
4. Verify documentation

**Expected Results:**
- Prompt appears for each high-severity item
- Skip reasons recorded in task documentation
- Implementation proceeds after all reasons provided

---

**Scenario: Critical Issue Blocks Completion**

**Objective:** Verify critical issues cannot be skipped

**Steps:**
1. Trigger a critical-severity anti-pattern (if any defined)
2. Attempt to proceed without fixing

**Expected Results:**
- Quality gate blocks with:
  ```
  🛑 **Quality Gate: BLOCKED**
  Critical issues must be resolved.
  ```
- No skip option available
- Must fix to proceed

---

**Scenario: View Anti-Pattern Details**

**Objective:** Test viewing anti-pattern guidance

**Steps:**
1. Trigger an anti-pattern
2. Choose option "3" (View guidance)

**Expected Results:**
- AI Quick Reference section displayed
- Refactoring steps shown
- Can return to main options after viewing

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
- [ ] Stack detection works for Node.js/TypeScript projects
- [ ] Stack detection works for Python projects
- [ ] Stack detection works for Go projects
- [ ] Unknown stack handled gracefully with manual fallback
- [ ] User can accept auto-detected stack
- [ ] User can edit auto-detected stack
- [ ] Always-active skills load on every implementation
- [ ] Context-activated skills match on keywords
- [ ] Tech stack matching contributes to skill scores
- [ ] File pattern matching contributes to skill scores
- [ ] Maximum skill limit (5) enforced
- [ ] Missing skill registry handled gracefully
- [ ] Missing skill files handled gracefully
- [ ] Anti-pattern detection identifies mutable defaults
- [ ] Anti-pattern detection identifies god objects
- [ ] Anti-pattern detection identifies magic numbers
- [ ] Anti-pattern detection identifies spaghetti code
- [ ] Anti-pattern detection identifies deep nesting
- [ ] Quality gate blocks on critical issues
- [ ] Quality gate warns on high-severity issues
- [ ] Quality gate allows skip with documented reason
- [ ] Coverage intelligence parses LCOV format
- [ ] Coverage intelligence handles missing reports gracefully
- [ ] Coverage suggestions prioritized by business impact

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
