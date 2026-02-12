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
   - **SKIP the full Git Isolation Protocol** and proceed directly to **Section 2.5 SKILL ACTIVATION**

4. **Otherwise:** Execute the full Git Isolation Protocol to create or switch to a dedicated git branch.

After completing (or skipping) the protocol, proceed to **Section 2.5 SKILL ACTIVATION**.

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

6.  **Finalize Track:**
    -   After all tasks in the track's local **Implementation Plan** are completed, you MUST update the track's status.
    -   **Update via CLI:** Execute `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> completed`
    -   **If CLI fails:** Fall back to manually editing the **Tracks Registry**, finding the specific line (e.g., `- [~] **Track: <Description>**`) and replacing it with `- [x] **Track: <Description>**`.
    -   **Commit Changes:** Stage the **Tracks Registry** file along with any uncommitted `plan.md` changes (checkpoint SHA annotations). Commit with the message `chore(conductor): Mark track '<track_description>' as complete`.
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
