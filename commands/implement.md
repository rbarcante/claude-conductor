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
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to implement a track. You MUST follow this protocol precisely.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## CLI Operations

This protocol integrates with the Conductor Python CLI for token-efficient operations. The CLI handles mechanical tasks (file parsing, JSON manipulation, git operations) deterministically, reducing token usage.

### CLI Command Reference

| Operation | CLI Command | Output |
|-----------|-------------|--------|
| Parse tracks registry | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-tracks` | Tracks with status, progress % |
| Update track status | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status TRACK_ID STATUS` | Confirmation |
| Archive track | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive TRACK_ID` | Archive path |
| Get modified files | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files` | Staged, unstaged, untracked |
| Parse coverage | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage --format FORMAT --path PATH` | Coverage metrics |
| Get next ADR number | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path ADR_PATH` | Next number, padded |
| Match patterns | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement match-patterns KEYWORD1 KEYWORD2` | Scored pattern matches |
| Suggest branch name | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement suggest-branch TRACK_ID` | Branch name, prefix, worktree path |

### CLI Usage Guidelines

1. **Always use `--json` flag** when you need structured data for processing
2. **Check `success` field** in JSON output before proceeding
3. **Fallback to manual parsing** if CLI command fails (see Fallback Instructions below)
4. **Project root**: CLI uses current working directory; use `--project-root PATH` if needed

### Fallback Instructions

If CLI commands fail or are unavailable, use these manual alternatives:

| Operation | Manual Fallback |
|-----------|-----------------|
| Parse tracks | Read `conductor/tracks.md` and parse sections split by `---` |
| Update status | Edit tracks.md directly, changing `[ ]` to `[~]` or `[x]` |
| Get modified files | Run `git diff --name-only` and `git status --porcelain` |
| Parse coverage | Read coverage files directly (lcov.info, coverage.xml, etc.) |
| Next ADR number | List files in decisions dir matching `NNNN-*.md` pattern |
| Match patterns | Read `patterns/index.md` and match keywords manually |
| Archive track | Create `conductor/archive/` and use `mv` command |
| Suggest branch | Read `metadata.json` for track type, apply prefix mapping from Section 2.1 |

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol**, resolve and verify the existence of:
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:** If ANY of these are missing (or their resolved paths do not exist), Announce: "Conductor is not set up. Please run `/conductor:setup`." and HALT.

---

## 2.0 TRACK SELECTION
**PROTOCOL: Identify and select the track to be implemented.**

1.  **Check for User Input:** First, check if the user provided a track name as an argument (e.g., `/conductor:implement <track_description>`).

2.  **Parse Tracks Registry via CLI:**
    -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-tracks`
    -   The CLI returns structured JSON with:
        ```json
        {
          "success": true,
          "data": {
            "tracks": [
              {
                "description": "Track description",
                "status": "pending|in_progress|completed",
                "path": "./conductor/tracks/track-id",
                "track_id": "track-id",
                "progress_percent": 45.0,
                "tasks": {"completed": 3, "in_progress": 1, "pending": 2, "total": 6}
              }
            ],
            "summary": {"total": 5, "completed": 2, "in_progress": 1, "pending": 2}
          }
        }
        ```
    -   **If CLI fails:** Fall back to reading `conductor/tracks.md` directly. Parse by splitting content by `---` separator. Extract status (`[ ]`, `[~]`, `[x]`), description, and track folder link.
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
**PROTOCOL: Create or switch to an isolated git branch/worktree for track implementation.**

This section ensures track work is properly isolated from the main codebase by requiring a dedicated git branch or worktree before implementation begins.

1.  **Detect Current Branch:**
    -   Get the current branch name: `git branch --show-current`
    -   Get the current repository status: `git status --porcelain`
    -   **Determine Branch State:**
        -   If on `main`, `master`, or `develop`: User is on a protected branch and should create a new feature branch.
        -   If on a branch matching the pattern `<prefix>/<track_shortname>` where prefix is `feature/`, `fix/`, `refactor/`, `docs/`, or `chore/`: User may already be on a suitable branch for this track.
        -   Otherwise: User is on an unrelated branch.
    -   **Check for Matching Branch:**
        -   Extract the track's shortname from `track_id` (e.g., `dark-mode-toggle` from `dark-mode-toggle_20260122`)
        -   Check if current branch name contains the track shortname
        -   If match found, set `branch_matches_track = true`

2.  **Generate Branch Name Suggestion:**
    -   **Via CLI (preferred):** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement suggest-branch <track_id>`
        -   The CLI returns:
            ```json
            {
              "success": true,
              "data": {
                "track_id": "dark-mode-toggle_20260122",
                "track_type": "feature",
                "branch_prefix": "feature/",
                "branch_name": "feature/dark-mode-toggle",
                "worktree_path": "../project-dark-mode-toggle",
                "current_branch": "main"
              }
            }
            ```
        -   **If CLI fails:** Fall back to manual generation below.
    -   **Manual generation:** Read the track's `metadata.json` to get the track type.
    -   **Map track type to branch prefix:**

        | Track Type | Branch Prefix |
        |------------|---------------|
        | `feature` | `feature/` |
        | `bugfix` | `fix/` |
        | `bug` | `fix/` |
        | `refactor` | `refactor/` |
        | `docs` | `docs/` |
        | `chore` | `chore/` |
        | (other) | `feature/` |

    -   **Generate suggested branch name:** `<prefix><track_shortname>`
        -   Extract shortname: Remove date suffix from track_id (e.g., `dark-mode-toggle` from `dark-mode-toggle_20260122`)
    -   **Generate suggested worktree path:** `../<project_name>-<track_shortname>`
        -   Get project name from current directory name

3.  **Present Options to User:**
    Use the `AskUserQuestion` tool to present branch options based on the detection results.

    **Scenario A: Already on a matching branch** (when `branch_matches_track = true`)

    ```json
    {
      "questions": [{
        "question": "You're already on branch '<current_branch>' which matches this track. How would you like to proceed?",
        "header": "Branch",
        "options": [
          {"label": "Continue on current branch (Recommended)", "description": "Keep working on the existing branch"},
          {"label": "Create new branch", "description": "Create a fresh branch for this track"}
        ],
        "multiSelect": false
      }]
    }
    ```

    **Scenario B: On main/master/develop or unrelated branch**

    ```json
    {
      "questions": [{
        "question": "How would you like to isolate your work for this track?",
        "header": "Branch",
        "options": [
          {"label": "Create branch '<suggested_branch>' (Recommended)", "description": "Create a new feature branch from current HEAD"},
          {"label": "Create worktree at '<suggested_worktree_path>'", "description": "Create a separate working directory with its own branch"},
          {"label": "Type your own branch name", "description": "Specify a custom branch name"}
        ],
        "multiSelect": false
      }]
    }
    ```

    **Handle User Response:**
    -   If user selects "Continue on current branch": Proceed to Section 2.5 without git operations
    -   If user selects "Create branch": Execute git checkout -b with suggested name
    -   If user selects "Create worktree": Execute git worktree add
    -   If user selects "Type your own": Prompt for custom branch name, then execute git checkout -b

4.  **Execute Git Operations:**
    Based on the user's selection, execute the appropriate git command.

    **For branch creation:**
    ```bash
    git checkout -b <branch_name>
    ```

    **For worktree creation:**
    ```bash
    git worktree add <worktree_path> -b <branch_name>
    ```
    -   The worktree command creates both a new directory and a new branch.
    -   After creating a worktree, inform the user: "Worktree created at `<path>`. To work in it, open a new terminal and navigate to that directory."

    **Verification:**
    -   After executing the git command, verify success by running `git branch --show-current`.
    -   If the current branch matches the expected branch name, proceed to Section 2.5.
    -   If the command fails, proceed to Step 5 (Error Handling).

5.  **Handle Errors:**
    If git operations fail, provide clear error messages and recovery options.

    **Common Error Scenarios:**

    | Error | Cause | Recovery |
    |-------|-------|----------|
    | `error: Your local changes would be overwritten` | Uncommitted changes in working tree | Announce: "You have uncommitted changes. Please commit or stash them before creating a new branch." HALT. |
    | `fatal: A branch named '<name>' already exists` | Branch name already in use | Announce: "Branch `<name>` already exists. Would you like to switch to it or choose a different name?" Re-prompt with options. |
    | `fatal: '<path>' already exists` | Worktree path exists | Announce: "Directory `<path>` already exists. Choose a different location or remove the existing directory." Re-prompt with options. |
    | `fatal: not a git repository` | Not in a git repository | Announce: "This directory is not a git repository. Please initialize git first: `git init`" HALT. |

    **Fallback Option:**
    If git operations consistently fail, offer to skip branch isolation:
    -   Announce: "Git branch creation failed. You may continue on the current branch, but this is not recommended for track isolation."
    -   Use AskUserQuestion to ask: "Continue on current branch despite the error? (Not recommended)"
    -   If user confirms, proceed to Section 2.5 with a warning note in the track's implementation log.

### Example Scenarios

**Example 1: Feature track branch creation**
```
Track: dark-mode-toggle_20260122 (type: feature)
Current branch: main

→ Agent suggests: "Create branch 'feature/dark-mode-toggle' (Recommended)"
→ User selects option 1
→ Agent executes: git checkout -b feature/dark-mode-toggle
→ Agent verifies: git branch --show-current returns "feature/dark-mode-toggle"
→ Proceeds to Section 2.5
```

**Example 2: Bugfix track branch creation**
```
Track: login-validation_20260122 (type: bugfix)
Current branch: develop

→ Agent suggests: "Create branch 'fix/login-validation' (Recommended)"
→ User selects option 1
→ Agent executes: git checkout -b fix/login-validation
→ Proceeds to Section 2.5
```

**Example 3: Worktree creation**
```
Track: api-refactor_20260122 (type: refactor)
Current branch: main
Project directory: /home/user/myproject

→ Agent presents options including worktree
→ User selects: "Create worktree at '../myproject-api-refactor'"
→ Agent executes: git worktree add ../myproject-api-refactor -b refactor/api-refactor
→ Agent announces: "Worktree created. Navigate to ../myproject-api-refactor to work in it."
→ Proceeds to Section 2.5
```

**Example 4: Continuing on existing branch**
```
Track: dark-mode-toggle_20260122 (type: feature)
Current branch: feature/dark-mode-toggle

→ Agent detects branch matches track shortname
→ Agent asks: "You're already on branch 'feature/dark-mode-toggle'. Continue?"
→ User selects: "Continue on current branch (Recommended)"
→ No git operations needed
→ Proceeds to Section 2.5
```

---

## 2.5 SKILL ACTIVATION
**PROTOCOL: Load relevant skills before implementation begins.**

This section activates skills that provide domain-specific guidance for the selected track. Follow the **Skill Loading Protocol** defined in CLAUDE.md for detailed scoring rules.

1.  **Load Skill Registry:**
    -   Read `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json` to get available skills
    -   If registry doesn't exist, skip skill activation silently and proceed to Track Implementation

2.  **Load Always-Active Skills:**
    -   Identify skills with `activation.always_active: true`
    -   Read their SKILL.md files and add guidance to implementation context

3.  **Match Skills to Track Context:**
    -   Extract keywords from track description and current task
    -   Match against skill `activation.keywords`
    -   Match project tech stack against skill `activation.tech_stack`
    -   Match files to be modified against skill `activation.file_patterns`
    -   Calculate activation scores per Skill Loading Protocol in CLAUDE.md

4.  **Activate Matching Skills:**
    -   For skills scoring >= 1.5, load their SKILL.md files
    -   Maximum 5 additional skills (beyond always-active)
    -   Sort by score descending

5.  **Announce Activated Skills:**
    -   Use the standard skill announcement format (see below)
    -   List skill name, activation reason, and brief description
    -   Proceed to Track Implementation after announcement

### Skill Announcement Format

When skills are activated, announce to the user:

```
🔧 **Skills Activated for This Track:**

**Always Active:**
- conductor-methodology: Core development workflow guidance

**Context-Activated:** (based on track/task matching)
- [Skill Name] (score: X.X): [Brief description]

Proceeding with implementation using activated skill guidance.
```

If no additional skills are activated beyond always-active:
```
🔧 **Skills Activated:** conductor-methodology (always active)
```

If skill registry is missing or no always-active skills exist, proceed silently without announcement.

6.  **Continue:** After skill activation, proceed to **Section 3.0 TRACK IMPLEMENTATION**.

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

3.  **Load Track Context:**
    a. **Identify Track Folder:** From the tracks data, use the `track_id` to locate the track's folder.
    b. **Read Files:**
        -   **Track Context:** Using the **Universal File Resolution Protocol**, resolve and read the **Specification** and **Implementation Plan** for the selected track.
        -   **Workflow:** Resolve **Workflow** (via the **Universal File Resolution Protocol** using the project's index file).
    c. **Error Handling:** If you fail to read any of these files, you MUST stop and inform the user of the error.

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
        i. **Defer to Workflow:** The **Workflow** file is the **single source of truth** for the entire task lifecycle. You MUST now read and execute the procedures defined in the "Task Workflow" section of the **Workflow** file you have in your context. Follow its steps for implementation, testing, and committing precisely.
        ii. **Capture Decisions:** During implementation, invoke the **Decision Capture Protocol** (Section 3.6) when significant decision points are encountered. Record decisions to the track's `decisions.md` file.

---

## 3.5 QUALITY GATE VERIFICATION
**PROTOCOL: Run quality analysis before task completion.**

This section runs after task implementation but before the task is marked complete. Follow the **Quality Analysis Protocol** (`protocols/quality-analysis.md`) and **Coverage Intelligence Protocol** (`protocols/coverage-intelligence.md`).

### Step 1: Run Anti-Pattern Detection

1.  **Identify Modified Files via CLI:**
    -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files`
    -   The CLI returns:
        ```json
        {
          "success": true,
          "data": {
            "staged": ["src/service.py", "src/utils.py"],
            "unstaged": ["tests/test_service.py"],
            "untracked": ["src/new_feature.py"],
            "all_modified": ["src/service.py", "src/utils.py", "tests/test_service.py"],
            "counts": {"staged": 2, "unstaged": 1, "untracked": 1, "total": 4}
          }
        }
        ```
    -   **If CLI fails:** Fall back to `git diff --name-only HEAD~1` and `git status --porcelain`
    -   Filter to include only code files (exclude `.md`, `.json`, `.yaml`, etc.)

2.  **Load Applicable Anti-Patterns:**
    -   Read `patterns/anti-patterns/index.md` to get list of anti-patterns
    -   For each modified file, load anti-patterns matching the file extension

3.  **Execute Detection:**
    -   For each anti-pattern, check modified files against:
        - Regex patterns from `detection.patterns`
        - Metric thresholds from `detection.thresholds`
    -   Record findings with file path and line number

4.  **Report Findings:**
    -   Group findings by severity (critical, high, medium)
    -   Display using the Quality Gate Output Format (see below)

### Step 2: Run Coverage Intelligence (if coverage report exists)

1.  **Parse Coverage Report via CLI:**
    -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage`
    -   Optionally specify format and path: `--format lcov --path coverage/lcov.info`
    -   The CLI returns:
        ```json
        {
          "success": true,
          "data": {
            "format": "lcov",
            "path": "coverage/lcov.info",
            "metrics": {
              "lines_covered": 450,
              "lines_total": 600,
              "coverage_percent": 75.0,
              "uncovered_files": [
                {"file": "src/payment.py", "coverage": 45.2},
                {"file": "src/api.py", "coverage": 62.1}
              ]
            }
          }
        }
        ```
    -   **If CLI fails or no coverage found:** Skip coverage analysis with informational message
    -   Supported formats: `lcov`, `cobertura`, `json`

2.  **Analyze Results:**
    -   Calculate priority scores for uncovered code
    -   Generate test suggestions based on `uncovered_files` list

3.  **Report Suggestions:**
    -   Display top 3-5 suggestions with estimated coverage gain
    -   Show current vs target coverage percentage

### Step 3: Handle User Decision

Based on findings, present options to the user:

**If Critical Issues Found:**
```
🛑 **Quality Gate: BLOCKED**

Critical issues must be resolved before proceeding.

[Table of critical findings]

Action Required: Fix the issue(s) listed above, then the quality gate will re-run.
```
-   Do NOT allow skip for critical issues
-   Wait for user to fix issues

**If High/Medium Issues Found (no critical):**
```
⚠️ **Quality Gate: Issues Detected**

[Table of findings by severity]

Options:
1. Fix issues and re-run quality gate
2. Skip with documented reasons
3. View anti-pattern details for guidance

Enter choice (1/2/3):
```

**If User Chooses Skip:**
-   Prompt for reason for each high-severity item
-   Record skip decisions in the task completion documentation
-   Proceed with task completion

**If No Issues Found:**
```
✅ **Quality Gate Passed**

No anti-patterns detected. Coverage meets target.
Proceeding with task completion.
```

### Quality Gate Output Format

**Anti-Pattern Findings:**
```
### Anti-Pattern Findings

| Severity | File | Line | Anti-Pattern | Issue |
|----------|------|------|--------------|-------|
| 🔴 High | src/service.py | 45 | Mutable Defaults | `def process(items=[])` |
| 🟡 Medium | src/utils.py | 23 | Magic Numbers | Literal `86400` |
```

**Coverage Intelligence:**
```
### Coverage Intelligence

**Current Coverage:** 75% (Target: 80%)

**Top Suggestions:**
1. `process_payment()` in services/payment.py (+2.5% gain)
2. `validate_input()` in api/handlers.py (+1.8% gain)
```

**Skip Documentation Format:**
When issues are skipped, include in task documentation:
```
### Quality Gate Decisions

**Skipped Anti-Patterns:**
- **Mutable Defaults** at src/service.py:45
  - Reason: Intentional caching mechanism
  - Reviewed: YYYY-MM-DD
```

---

## 3.6 DECISION CAPTURE
**PROTOCOL: Capture significant implementation decisions.**

This section is invoked during task implementation when non-trivial choices are detected. Follow the **Decision Capture Protocol** (`protocols/decision-capture.md`) for detailed rules.

### Step 1: Detect Decision Points

During task implementation, identify decision points when encountering:
-   **Technology Selection:** Choosing libraries, frameworks, or tools
-   **Pattern Choice:** Selecting design patterns or architectural approaches
-   **API Design:** Defining endpoint structure, response formats
-   **Data Modeling:** Schema decisions, relationships, normalization
-   **Error Handling:** Exception strategies, retry policies
-   **Performance Tradeoffs:** Caching, lazy vs eager loading

### Step 2: Evaluate Significance

A decision is significant and should be captured when:
-   Multiple reasonable alternatives exist with different tradeoffs
-   The choice has long-term implications or affects architecture
-   The decision deviates from standard patterns or conventions
-   Future maintainers would benefit from understanding the rationale

**Skip capture when:**
-   The approach is dictated by the spec or tech stack
-   Only one reasonable option exists
-   The choice is easily reversible with no downstream impact
-   The decision follows an established project pattern

### Step 3: Present Decision (if significant)

When a significant decision is detected, present to the user:

```
---
**Decision Point: [Category]**

**Context:** [Brief description of the situation]

**Options:**
A. **[Option Name]** (Recommended)
   [Description]
   - Pros: [List]
   - Cons: [List]

B. **[Option Name]**
   [Description]
   - Pros: [List]
   - Cons: [List]

Select an option (A/B/skip):
---
```

### Step 4: Record Decision

If user selects an option (not skip):

1.  **Load decisions.md:** Read `conductor/tracks/<track_id>/decisions.md`

2.  **Determine ADR Number via CLI:**
    -   Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path conductor/tracks/<track_id>`
    -   The CLI returns:
        ```json
        {
          "success": true,
          "data": {
            "next_number": 3,
            "padded": "0003",
            "existing_count": 2,
            "path": "conductor/tracks/my-track"
          }
        }
        ```
    -   **If CLI fails:** Fall back to manually counting ADR entries in decisions.md (find highest `ADR-NNN` and increment)

3.  **Generate ADR Entry:**
    ```markdown
    ### ADR-[NNN]: [Decision Title]

    **Date:** [YYYY-MM-DD]
    **Status:** Accepted

    #### Context
    [The situation and constraints that led to this decision]

    #### Decision
    [The choice that was made, stated declaratively]

    #### Consequences
    **Positive:**
    - [Benefit 1]
    - [Benefit 2]

    **Negative:**
    - [Tradeoff 1]
    - [Tradeoff 2]

    #### Alternatives Considered
    - **[Option X]:** [Why not chosen]
    ```

4.  **Append to decisions.md:**
    -   Replace the placeholder `_No decisions recorded yet._` if present
    -   Append the new ADR entry at the end of the Decisions section

5.  **Announce:** "Decision recorded as ADR-[NNN] in decisions.md"

### Step 5: Continue Implementation

After recording (or skipping), continue with the task implementation.

---

6.  **Finalize Track:**
    -   After all tasks in the track's local **Implementation Plan** are completed, you MUST update the track's status.
    -   **Update via CLI:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> completed`
    -   **If CLI fails:** Fall back to manually editing the **Tracks Registry**, finding the specific line (e.g., `- [~] **Track: <Description>**`) and replacing it with `- [x] **Track: <Description>**`.
    -   **Commit Changes:** Stage the **Tracks Registry** file and commit with the message `chore(conductor): Mark track '<track_description>' as complete`.
    -   Announce that the track is fully complete and the tracks file has been updated.

---

## 4.0 SYNCHRONIZE PROJECT DOCUMENTATION
**PROTOCOL: Update project-level documentation based on the completed track.**

1.  **Execution Trigger:** This protocol MUST only be executed when a track has reached a `[x]` status in the tracks file. DO NOT execute this protocol for any other track status changes.

2.  **Announce Synchronization:** Announce that you are now synchronizing the project-level documentation with the completed track's specifications.

3.  **Load Track Specification:** Read the track's **Specification**.

4.  **Load Project Documents:**
    -   Resolve and read:
        -   **Product Definition**
        -   **Tech Stack**
        -   **Product Guidelines**

5.  **Analyze and Update:**
    a.  **Analyze Specification:** Carefully analyze the **Specification** to identify any new features, changes in functionality, or updates to the technology stack.
    b.  **Update Product Definition:**
        i. **Condition for Update:** Based on your analysis, you MUST determine if the completed feature or bug fix significantly impacts the description of the product itself.
        ii. **Propose and Confirm Changes:** If an update is needed, generate the proposed changes. Then, present them to the user for confirmation:
            > "Based on the completed track, I propose the following updates to the **Product Definition**:"
            > ```diff
            > [Proposed changes here, ideally in a diff format]
            > ```
            > "Do you approve these changes? (yes/no)"
        iii. **Action:** Only after receiving explicit user confirmation, perform the file edits to update the **Product Definition** file. Keep a record of whether this file was changed.
    c.  **Update Tech Stack:**
        i. **Condition for Update:** Similarly, you MUST determine if significant changes in the technology stack are detected as a result of the completed track.
        ii. **Propose and Confirm Changes:** If an update is needed, generate the proposed changes. Then, present them to the user for confirmation:
            > "Based on the completed track, I propose the following updates to the **Tech Stack**:"
            > ```diff
            > [Proposed changes here, ideally in a diff format]
            > ```
            > "Do you approve these changes? (yes/no)"
        iii. **Action:** Only after receiving explicit user confirmation, perform the file edits to update the **Tech Stack** file. Keep a record of whether this file was changed.
    d. **Update Product Guidelines (Strictly Controlled):**
        i. **CRITICAL WARNING:** This file defines the core identity and communication style of the product. It should be modified with extreme caution and ONLY in cases of significant strategic shifts, such as a product rebrand or a fundamental change in user engagement philosophy. Routine feature updates or bug fixes should NOT trigger changes to this file.
        ii. **Condition for Update:** You may ONLY propose an update to this file if the track's **Specification** explicitly describes a change that directly impacts branding, voice, tone, or other core product guidelines.
        iii. **Propose and Confirm Changes:** If the conditions are met, you MUST generate the proposed changes and present them to the user with a clear warning:
            > "WARNING: The completed track suggests a change to the core **Product Guidelines**. This is an unusual step. Please review carefully:"
            > ```diff
            > [Proposed changes here, ideally in a diff format]
            > ```
            > "Do you approve these critical changes to the **Product Guidelines**? (yes/no)"
        iv. **Action:** Only after receiving explicit user confirmation, perform the file edits. Keep a record of whether this file was changed.

6.  **Final Report:** Announce the completion of the synchronization process and provide a summary of the actions taken.
    - **Construct the Message:** Based on the records of which files were changed, construct a summary message.
    - **Commit Changes:**
        - If any files were changed (**Product Definition**, **Tech Stack**, or **Product Guidelines**), you MUST stage them and commit them.
        - **Commit Message:** `docs(conductor): Synchronize docs for track '<track_description>'`
    - **Example (if Product Definition was changed, but others were not):**
        > "Documentation synchronization is complete.
        > - **Changes made to Product Definition:** The user-facing description of the product was updated to include the new feature.
        > - **No changes needed for Tech Stack:** The technology stack was not affected.
        > - **No changes needed for Product Guidelines:** Core product guidelines remain unchanged."
    - **Example (if no files were changed):**
        > "Documentation synchronization is complete. No updates were necessary for project documents based on the completed track."

---

## 5.0 TRACK CLEANUP
**PROTOCOL: Offer to archive or delete the completed track.**

1.  **Execution Trigger:** This protocol MUST only be executed after the current track has been successfully implemented and the `SYNCHRONIZE PROJECT DOCUMENTATION` step is complete.

2.  **Ask for User Choice:** You MUST prompt the user with the available options for the completed track.
    > "Track '<track_description>' is now complete. What would you like to do?
    > A.  **Archive:** Move the track's folder to `conductor/tracks/archive/` and remove it from the tracks file.
    > B.  **Delete:** Permanently delete the track's folder and remove it from the tracks file.
    > C.  **Skip:** Do nothing and leave it in the tracks file.
    > Please enter the number of your choice (A, B, or C)."

3.  **Handle User Response:**
    *   **If user chooses "A" (Archive):**
        i.   **Archive via CLI:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive <track_id>`
        ii.  The CLI automatically:
             - Creates `conductor/tracks/archive/` if it doesn't exist
             - Moves the track folder to the archive directory
             - Returns the source and destination paths
        iii. **If CLI fails:** Fall back to manual archiving:
             - Check for existence of `conductor/tracks/archive/`. If not exists, create it.
             - Move the track's folder from `conductor/tracks/<track_id>` to `conductor/tracks/archive/<track_id>`.
        iv.  **Remove from Tracks File:** Read the content of `conductor/tracks.md`, remove the entire section for the completed track (the part that starts with `---` and contains the track description), and write the modified content back to the file.
        v.   **Commit Changes:** Stage `conductor/tracks.md` and `conductor/tracks/archive/`. Commit with the message `chore(conductor): Archive track '<track_description>'`.
        vi.  **Announce Success:** Announce: "Track '<track_description>' has been successfully archived."
    *   **If user chooses "B" (Delete):**
        i. **CRITICAL WARNING:** Before proceeding, you MUST ask for a final confirmation due to the irreversible nature of the action.
            > "WARNING: This will permanently delete the track folder and all its contents. This action cannot be undone. Are you sure you want to proceed? (yes/no)"
        ii. **Handle Confirmation:**
            - **If 'yes'**:
                a. **Delete Track Folder:** Permanently delete the track's folder from `conductor/tracks/<track_id>`.
                b. **Remove from Tracks File:** Read the content of `conductor/tracks.md`, remove the entire section for the completed track, and write the modified content back to the file.
                c. **Commit Changes:** Stage `conductor/tracks.md` and the deletion of `conductor/tracks/<track_id>`. Commit with the message `chore(conductor): Delete track '<track_description>'`.
                d. **Announce Success:** Announce: "Track '<track_description>' has been permanently deleted."
            - **If 'no' (or anything else)**:
                a. **Announce Cancellation:** Announce: "Deletion cancelled. The track has not been changed."
    *   **If user chooses "C" (Skip) or provides any other input:**
        *   Announce: "Okay, the completed track will remain in your tracks file for now."
