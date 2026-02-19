---
name: conductor:implement
description: Executes the tasks defined in the specified track's plan
argument-hint: "[optional: track description]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
  - Task
---

# Context

!`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-tracks`

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to implement a track. You MUST follow this protocol precisely.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## Fallback Instructions

If the context injection fails:
- Read `conductor/tracks.md` directly and parse sections split by `---`

### Action CLI Commands (Used During Implementation)

```bash
# Update track status
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status TRACK_ID STATUS

# Archive completed track
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive TRACK_ID
```

### Task-Specific CLI Commands

Used during task execution (not injected upfront):

```bash
# Match patterns for task
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement match-patterns KEYWORD1 KEYWORD2

# Get modified files for quality gate
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files

# Parse coverage report
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage --format FORMAT --path PATH

# Get next ADR number
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path ADR_PATH

# Suggest branch name
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement suggest-branch TRACK_ID
```

---

## 1.1 SETUP CHECK

**PROTOCOL: Follow the Verify Setup Protocol in `protocols/verify-setup.md`.**

---

## 2.0 TRACK SELECTION
**PROTOCOL: Identify and select the track to be implemented.**

1.  **Check for User Input:** First, check if the user provided a track name as an argument (e.g., `/conductor:implement <track_description>`).

2.  **Use Injected Context:**
    -   The tracks data has been injected via the `# Context` section above.
    -   Parse the `tracks` array from the injected JSON to get track descriptions, statuses, and progress.
    -   **CRITICAL:** If no tracks are found, announce: "The tracks file is empty or malformed. No tracks to implement." and halt.

3.  **Continue:** Immediately proceed to the next step to select a track.

4.  **Select Track:**
    -   **If a track name was provided:**
        1.  Perform an exact, case-insensitive match for the provided name against the track descriptions from the parsed data.
        2.  If a unique match is found, confirm the selection with the user: "I found track '<track_description>'. Is this correct?"
        3.  If no match is found, or if the match is ambiguous, inform the user and ask for clarification. Suggest the next available track as below.
    -   **If no track name was provided (or if the previous step failed):**
        1.  **Identify Next Track:** From the parsed tracks, find the first track where `status` is NOT `completed`.
        2.  **If a next track is found:**
            -   Announce: "No track name provided. Automatically selecting the next incomplete track: '<track_description>'."
            -   Proceed with this track.
        3.  **If no incomplete tracks are found:**
            -   Announce: "No incomplete tracks found in the tracks file. All tasks are completed!"
            -   Halt the process and await further user instructions.

5.  **Handle No Selection:** If no track is selected, inform the user and await further instructions.

6.  **Continue:** After a track is selected, proceed to **Section 2.1 GIT ISOLATION SETUP** to create or switch to an isolated git branch.

---

## 2.1 GIT ISOLATION SETUP

**PROTOCOL: Follow the Git Isolation Protocol in `protocols/git-isolation.md`.**

This section ensures track work is properly isolated from the main codebase.

### Fast Path Check (Skip Protocol If Already On Track Branch)

Before executing the full protocol, perform a quick check:

1. **Get current branch:** `git branch --show-current`
2. **Extract track shortname** from the selected track's `track_id` (e.g., `dark-mode-toggle` from `dark-mode-toggle_20260122`)
3. **If current branch contains the track shortname** (e.g., `feature/dark-mode-toggle`):
   - Announce: "Already on branch `<branch>` for this track. Proceeding."
   - **SKIP the full Git Isolation Protocol** and proceed directly to **Section 2.2 BASE BRANCH DETECTION**

4. **Otherwise:** Execute the full Git Isolation Protocol to create or switch to a dedicated git branch.

After completing (or skipping) the protocol, proceed to **Section 2.2 BASE BRANCH DETECTION**.

---

## 2.2 BASE BRANCH DETECTION

**PROTOCOL: Detect the originating branch of the current track branch for later use in auto code review.**

Execute this once upfront and store the result for use in Section 3.7.

### Detection Algorithm

Execute the steps below in order, stopping as soon as a branch is successfully identified:

**Step 1: Check git reflog for branch creation event**

```bash
git reflog show HEAD | grep "branch: Created from" | head -1
```

- If output contains `Created from <branch>`, extract the branch name (strip any `refs/heads/` or `origin/` prefix).
- Store as `BASE_BRANCH`.

**Step 2: If Step 1 yields no result, inspect remote tracking information**

```bash
git log -1 --format="%D" HEAD | tr ',' '\n' | grep "origin/" | head -5
```

- Look for a remote-tracking ref that is NOT the current branch (e.g., `origin/master`, `origin/main`, `origin/develop`).
- Store the branch name (without `origin/` prefix) as `BASE_BRANCH`.
- Note: The `-1` flag limits inspection to HEAD's decoration only, preventing false matches from ancestors.

**Step 3: If Step 2 yields no result, detect default branch**

Try in order:
```bash
git rev-parse --verify origin/master 2>/dev/null && echo "master"
git rev-parse --verify origin/main 2>/dev/null && echo "main"
git rev-parse --verify origin/develop 2>/dev/null && echo "develop"
```

- Use the first branch that exists as `BASE_BRANCH`.
- Announce: "Base branch auto-detection fell back to `<BASE_BRANCH>`. Please verify this is correct."

**Step 4: If all steps fail**

- Set `BASE_BRANCH` to `master` as a last resort.
- Announce: "Could not automatically detect the base branch. Defaulting to `master`. You can override this during the code review step."

### Validation (Run After Any Step Yields a Result)

Before storing `BASE_BRANCH`, validate the extracted value:
- **Format check:** Verify it matches the pattern `^[a-zA-Z0-9._/-]+$` (only safe branch name characters).
- **Existence check:** Run `git rev-parse --verify origin/<BASE_BRANCH>` to confirm the branch exists remotely.
- If validation fails: treat the result as if the step yielded no output and proceed to the next step.
- If all steps fail validation: fall back to Step 4 (default `master`).

### Result

- Store the validated `BASE_BRANCH` in session context for use in **Section 3.7 AUTO CODE REVIEW**.
- Announce (only if detected successfully): "Base branch detected: `<BASE_BRANCH>`."

---

## 2.5 SKILL ACTIVATION (LAZY LOADING)
**PROTOCOL: Load skills incrementally to minimize upfront token usage.**

This section uses a two-phase approach: always-active skills are loaded once upfront, while task-specific skills are loaded lazily during task execution.

### Phase 1: Load Always-Active Skills (Upfront)

1.  **Load Skill Registry:**
    -   Read `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json` to get available skills
    -   If registry doesn't exist, skip skill activation silently and proceed to Track Implementation

2.  **Load Always-Active Skills Only:**
    -   Identify skills with `activation.always_active: true`
    -   Read their SKILL.md files and add guidance to implementation context
    -   Announce: `🔧 **Skills Activated:** conductor-methodology (always active)`

3.  **Continue:** Proceed to **Section 3.0 TRACK IMPLEMENTATION**

### Phase 2: Load Task-Specific Skills (Deferred to Task Loop)

Task-specific skill activation happens in Section 3.0, Step 5.c **before each task** executes:

1.  **Extract Keywords:** From the current task description
2.  **Match Skills:** Against `activation.keywords`, `activation.tech_stack`, and `activation.file_patterns`
3.  **Activate:** Load SKILL.md for skills scoring >= 1.5 (max 3 per task)
4.  **Announce:** Only if new skills are activated for this task

### Skill Announcement Format

**Upfront (always-active only):**
```
🔧 **Skills Activated:** conductor-methodology (always active)
```

**Per-task (if new skills activated):**
```
🔧 **Task Skills:** [Skill Name] activated for this task
```

If skill registry is missing or no always-active skills exist, proceed silently without announcement.

---

## 3.0 TRACK IMPLEMENTATION
**PROTOCOL: Execute the selected track.**

1.  **Announce Action:** Announce which track you are beginning to implement.

2.  **Update Status to 'In Progress' via CLI:**
    -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> in-progress`
    -   The CLI updates both:
        -   The track status marker in `conductor/tracks.md` (changes `[ ]` to `[~]`)
        -   The track's `metadata.json` with `status` and `updated_at` fields
    -   **If CLI fails:** Fall back to manually editing the **Tracks Registry** file, finding the specific line for the track (e.g., `- [ ] **Track: <Description>**`) and replacing it with `- [~] **Track: <Description>**`.

3.  **Load Track Context (CACHE FOR SESSION):**
    a. **Identify Track Folder:** From the tracks data, use the `track_id` to locate the track's folder.
    b. **Read Files:**
        -   **Track Context:** Using the **Universal File Resolution Protocol**, resolve and read the **Specification** and **Implementation Plan** for the selected track.
        -   **Workflow:** Resolve **Workflow** (via the **Universal File Resolution Protocol** using the project's index file).
    c. **Error Handling:** If you fail to read any of these files, you MUST stop and inform the user of the error.
    d. **IMPORTANT - Context Caching:** The Workflow file is now cached in your context window. DO NOT re-read it during task execution. Reference the content you just loaded for all subsequent tasks in this track.

4.  **Surface Relevant Patterns via CLI:**
    **PROTOCOL: Use CLI pattern matching before each task.**

    For each task you are about to execute:
    a. **Extract Keywords:** From the task description, extract normalized keywords (tokenize, lowercase, remove stop words).
    b. **Match Patterns via CLI:**
        -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement match-patterns <keyword1> <keyword2> ...`
        -   The CLI returns:
            ```json
            {
              "success": true,
              "data": {
                "keywords": ["authentication", "jwt", "token"],
                "matches": [
                  {
                    "name": "Authentication Pattern",
                    "path": "/path/to/patterns/core/authentication.md",
                    "score": 2.5,
                    "matched_keywords": ["authentication", "token"],
                    "description": "Secure authentication implementation..."
                  }
                ],
                "total_matches": 3
              }
            }
            ```
        -   **If CLI fails:** Fall back to reading `patterns/index.md` and manually matching keywords against pattern names and frontmatter.
    c. **Surface Decision:**
        -   If any patterns have `score >= 1.0`, announce them using this format:
          ```
          📚 **Relevant Patterns Detected:**

          1. **[Pattern Name]** (patterns/core/<name>.md)
             > <Pattern's one-line description>

          [Apply patterns? (Y)es / (S)kip / (V)iew first]
          ```
        -   Maximum 3 patterns per task, sorted by score descending
        -   If user chooses "View", display the AI Quick Reference section
        -   If user chooses "Skip", proceed without applying patterns
        -   If user chooses "Yes" or confirms, keep pattern guidance in mind during implementation
    d. **No Matches:** If no patterns score >= 1.0, continue silently without announcement.

5.  **Execute Tasks and Update Track Plan:**
    a. **Announce:** State that you will now execute the tasks from the track's **Implementation Plan** by following the procedures in the **Workflow**.
    b. **Iterate Through Tasks:** You MUST now loop through each task in the track's **Implementation Plan** one by one.
    c. **For Each Task, You MUST:**
        i. **Activate Task-Specific Skills (Lazy - Phase 2 from Section 2.5):**
            - Extract keywords from the current task description
            - Match against skill registry (skip skills already loaded)
            - For new matches scoring >= 1.5, load their SKILL.md (max 3 per task)
            - If new skills activated, announce: `🔧 **Task Skills:** [Name] activated`
        ii. **Defer to Workflow (FROM CACHE):** The **Workflow** file is the **single source of truth** for the entire task lifecycle. Reference the Workflow already loaded in Step 3 above—DO NOT re-read the file. Execute the procedures defined in the "Task Workflow" section. Follow its steps for implementation, testing, and committing precisely.
        iii. **Capture Decisions:** During implementation, invoke the **Decision Capture Protocol** (Section 3.6) when significant decision points are encountered. Record decisions to the track's `decisions.md` file.

---

## 3.5 QUALITY GATE VERIFICATION
**PROTOCOL: Run quality analysis before task completion.**

This section runs after task implementation but before the task is marked complete.

**Full Protocol Reference:** `protocols/quality-analysis.md` and `protocols/coverage-intelligence.md`

### Execution Steps

1.  **Choose Mode:** Use Parallel Agent Mode (preferred) or Inline Mode (fallback)
2.  **Identify Modified Files:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files`
3.  **Run Analysis:** Launch `code-quality-analyzer` and `security-scanner` agents in parallel
4.  **Run Coverage Intelligence:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage`
5.  **Handle Results:**
    - **Critical issues:** Block, must fix before proceeding
    - **High/Medium issues:** Allow skip with documented reason
    - **No issues:** Proceed with task completion

### Quick Reference: Output Format

| Status | Symbol | Action |
|--------|--------|--------|
| BLOCKED | 🛑 | Fix critical issues |
| Issues Detected | ⚠️ | Fix or skip with reason |
| Passed | ✅ | Proceed |

---

## 3.6 DECISION CAPTURE
**PROTOCOL: Capture significant implementation decisions.**

This section is invoked during task implementation when non-trivial choices are detected.

**Full Protocol Reference:** `protocols/decision-capture.md`

### Decision Triggers

Capture decisions when encountering: technology selection, pattern choice, API design, data modeling, error handling strategies, or performance tradeoffs.

### Execution Steps

1.  **Detect:** Identify when multiple reasonable alternatives exist with different tradeoffs
2.  **Present:** Show options with pros/cons to user (format: A/B/skip)
3.  **Record:** Get ADR number via `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path conductor/tracks/<track_id>`
4.  **Append:** Write ADR entry to `conductor/tracks/<track_id>/decisions.md`

**Skip capture when:** approach is dictated by spec, only one option exists, or choice is easily reversible.

---

## 3.7 AUTO CODE REVIEW
**PROTOCOL: Run automated code review when a track reaches completion.**

**Trigger:** This section is invoked from Step 6 (Finalize Track) when all tasks are complete.

### 3.7.1 Prompt User

Before running the review, ask the user:

```json
{
  "questions": [{
    "question": "All tasks are complete. Would you like to run an automated code review before finalizing the track?",
    "header": "Code Review",
    "options": [
      {"label": "Run code review (Recommended)", "description": "Analyze changes across code quality, security, and test coverage. Report saved to track folder."},
      {"label": "Skip", "description": "Finalize the track without running a code review"}
    ],
    "multiSelect": false
  }]
}
```

- **If "Skip":** Return to Step 6 and proceed with track finalization.
- **If "Run code review":** Continue with **Section 3.7.2**.

### 3.7.2 Generate Diff

**IMPORTANT: The review is scoped exclusively to code changed for this track.** The three-dot diff syntax ensures only commits on the current branch (not yet in the base branch) are analyzed.

**IMPORTANT: Only committed changes are included in the diff.** Uncommitted changes (staged or unstaged) are NOT captured by `git diff ...HEAD`. Before generating the diff, check for uncommitted changes.

**Step 0: Check for uncommitted changes**

```bash
git status --porcelain
```

- If output is **non-empty** (uncommitted staged or unstaged changes exist):
  - Offer the user a choice:
    ```json
    {
      "questions": [{
        "question": "Uncommitted changes were found. What should the review include?",
        "header": "Review Scope",
        "options": [
          {"label": "All changes (Recommended)", "description": "Review both committed and uncommitted changes in this track"},
          {"label": "Committed changes only", "description": "Review only committed changes (HEAD). Uncommitted work is excluded."},
          {"label": "Skip review", "description": "Skip the code review entirely"}
        ],
        "multiSelect": false
      }]
    }
    ```
  - **If "Skip review":** Return to Step 6 and proceed with track finalization.
  - **If "All changes":** Use `git diff origin/<BASE_BRANCH>` (two-dot, compares base branch against working tree including uncommitted changes) in Step 3 below.
  - **If "Committed changes only":** Use `git diff origin/<BASE_BRANCH>...HEAD` (three-dot) in Step 3 below.
- If output is **empty** (no uncommitted changes): Use `git diff origin/<BASE_BRANCH>...HEAD` (three-dot). Proceed directly.

1. **Use stored base branch** from **Section 2.2** (stored as `BASE_BRANCH`).

2. **Fetch latest:**
    ```bash
    git fetch origin
    ```
    - If `git fetch` fails (offline or no remote): Announce "Unable to fetch from remote. Proceeding with local branches." Use local branch names (e.g., `<BASE_BRANCH>` without `origin/` prefix) in the diff commands in Step 3. Continue with the review.

3. **Generate diff scoped to this track's changes (use the mode selected in Step 0):**

    - **All changes (committed + uncommitted):**
      ```bash
      git diff origin/<BASE_BRANCH>
      # If origin not available (fetch failed):
      git diff <BASE_BRANCH>
      ```
      Two-dot syntax compares the base branch against the current working tree. Note: includes all working-tree differences from the base, not only uncommitted files.

    - **Committed changes only:**
      ```bash
      git diff origin/<BASE_BRANCH>...HEAD
      # If origin not available (fetch failed):
      git diff <BASE_BRANCH>...HEAD
      ```
      Three-dot syntax uses the merge-base, capturing only committed changes on the current branch.

4. **Extract changed file list (product code only):**
    ```bash
    # For all changes (working tree):
    git diff --name-only origin/<BASE_BRANCH>
    # OR for committed changes only:
    git diff --name-only origin/<BASE_BRANCH>...HEAD
    ```
    **Filter out Conductor framework files** using path-based exclusion only — exclude files at these specific paths:
    - `conductor/tracks/**` (track management files: plan.md, metadata.json, decisions.md, index.md, review.md)
    - `conductor/tracks.md` (master track registry)
    - `conductor/index.md` (project index)

    **Include all other files** — this includes source code files (`.ts`, `.js`, `.py`, `.java`, etc.) AND documentation/protocol files that are part of the project's product (e.g., `commands/*.md`, `protocols/*.md`, `skills/**`, `patterns/**`, `templates/**`, `README.md`). For Conductor-type projects, markdown protocol files ARE the product code.

5. **Handle empty diff or no reviewable files:**
    - If only conductor/tracks/** files changed: Announce "Only track management files changed. No product code review needed." Proceed to finalization.
    - If no files remain after filtering: Announce "No reviewable changes detected for this track." Proceed to finalization.

6. **Parse diff statistics** (from full diff including all files):
    - Count files changed (lines starting with `diff --git`)
    - Count lines added (lines starting with `+` excluding `+++`)
    - Count lines removed (lines starting with `-` excluding `---`)

### 3.7.3 Run Analysis (Parallel)

Prepare the agent input using only the **product code diff** (filtered file list from Step 4 above):

```json
{
  "diff_content": "<diff output filtered to product code files only>",
  "file_list": ["<product code files changed in this track>"],
  "project_context": {
    "tech_stack": "<from conductor/tech-stack.md>",
    "styleguide_path": "conductor/code_styleguides/<language>.md",
    "product_guidelines_path": "conductor/product-guidelines.md",
    "workflow_path": "conductor/workflow.md"
  }
}
```

**Launch all three specialist agents simultaneously** in a single message with three Task tool calls:

- `subagent_type: "code-quality-analyzer"` with the agent input
- `subagent_type: "security-scanner"` with the agent input
- `subagent_type: "test-coverage-analyzer"` with the agent input

**Handle agent failures:**
- If exactly one agent fails: Note the failure in the report under the relevant section (e.g., "Security analysis unavailable: agent error"). Proceed with results from the remaining two agents. Do not attempt inline analysis for that dimension.
- If 2+ agents fail: announce "Multiple agents failed. Skipping auto code review." and return to Step 6.

### 3.7.4 Generate and Save Report

1. **Aggregate findings** from all agent results (parse JSON, merge `findings` arrays, sum severity counts).

2. **Generate report** following the structure from `codeReview.md` Section 7.2:

    ```markdown
    # Code Review Report

    **Branch:** `<current_branch>` vs `origin/<BASE_BRANCH>`
    **Generated:** <timestamp>
    **Track:** <track_description>

    ---

    ## Summary

    | Metric | Value |
    |--------|-------|
    | Files Changed | X |
    | Lines Added | +Y |
    | Lines Removed | -Z |
    | **Findings** | 🔴 High: N \| 🟡 Medium: N \| 🟢 Low: N |

    ---

    ## Code Quality

    ### High Severity
    [List findings or "No high severity issues found"]

    ### Medium Severity
    [List findings]

    ### Low Severity
    [List findings]

    ---

    ## Security Analysis

    ### Critical/High Severity
    [List security findings or "No security vulnerabilities detected"]

    ### Medium Severity
    [List findings]

    ---

    ## Test Coverage

    ### Missing Tests
    [List files without tests or "All changed files have corresponding tests"]

    ### Insufficient Coverage
    [List coverage gaps]

    ---

    ## Recommendations

    **Priority Actions (address before merging):**
    1. [High severity items that must be fixed]

    **Suggested Improvements:**
    1. [Medium/Low severity items to consider]

    ---

    *Auto-review generated by `/conductor:implement` on track completion*
    ```

3. **Save report to track folder:**
    - Write the generated report to `conductor/tracks/<track_id>/review.md`.

4. **Update track `index.md`:**
    - Add a link to the review file in the track's `index.md`:
      ```markdown
      - [Code Review Report](./review.md) - Auto-generated review on track completion
      ```

5. **Display report to user:**
    - Output the complete report inline.
    - If high severity findings exist: "⚠️ High severity findings detected. Review the report before merging."
    - If no high severity findings: "✅ Auto code review passed. No blocking issues found."

6. **Return to Step 6** to proceed with track finalization. The review is **non-blocking** — track completion proceeds regardless of findings.

---

6.  **Finalize Track:**
    -   After all tasks in the track's local **Implementation Plan** are completed, you MUST invoke **Section 3.7 AUTO CODE REVIEW** first.
    -   After the code review step completes (or is skipped), proceed with finalization:
    -   **Update via CLI:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> completed`
    -   **If CLI fails:** Fall back to manually editing the **Tracks Registry**, finding the specific line (e.g., `- [~] **Track: <Description>**`) and replacing it with `- [x] **Track: <Description>**`.
    -   **Commit Changes:** Stage the **Tracks Registry** file, any uncommitted `plan.md` changes (checkpoint SHA annotations), and if code review was run: both `review.md` and `index.md` from the track folder. Commit with the message `chore(conductor): Mark track '<track_description>' as complete`.
    -   Announce that the track is fully complete and the tracks file has been updated.

---

## 4.0 SYNCHRONIZE PROJECT DOCUMENTATION
**PROTOCOL: Update project-level documentation based on the completed track.**

**Trigger:** Only execute when track status reaches `[x]` (completed).

### Execution Steps

1.  **Load Context:** Read track Specification, Product Definition, Tech Stack, and Product Guidelines
2.  **Analyze:** Identify new features, functionality changes, or technology updates
3.  **Propose Updates:** For each document that needs changes, present diff to user for approval
4.  **Apply:** Only update files after explicit user confirmation
5.  **Commit:** Stage changed files with message `docs(conductor): Synchronize docs for track '<track_description>'`

### Update Priorities

| Document | Update When | Confirmation Required |
|----------|-------------|----------------------|
| Product Definition | Feature significantly impacts product description | Yes |
| Tech Stack | Technology changes detected | Yes |
| Product Guidelines | **Rare** - Only for branding/strategic shifts | Yes (with warning) |

---

## 5.0 TRACK CLEANUP
**PROTOCOL: Offer to archive or delete the completed track.**

**Trigger:** Execute after track completion and documentation sync.

### User Options

| Choice | Action | CLI Command |
|--------|--------|-------------|
| A. Archive | Move to `conductor/tracks/archive/` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive <track_id>` |
| B. Delete | Permanently remove (requires confirmation) | Manual deletion |
| C. Skip | Leave in tracks file | None |

### Execution

1.  Prompt user with options A/B/C
2.  For Archive: Run CLI, remove from tracks.md, commit with `chore(conductor): Archive track '<description>'`
3.  For Delete: Require explicit "yes" confirmation, then delete folder and update tracks.md
4.  Commit changes after archive or delete
