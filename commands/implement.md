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

## AskUserQuestion Tool Protocol

**PROTOCOL: Use the AskUserQuestion tool for all interactive user prompts.**

All questions to the user during implementation MUST be asked using the `AskUserQuestion` tool. This provides a structured, consistent user experience with clickable options.

### Tool Structure

```json
{
  "questions": [
    {
      "question": "The complete question text ending with ?",
      "header": "Short label",  // Max 12 characters
      "options": [
        {"label": "Option label", "description": "What this option means"},
        {"label": "Another option", "description": "Explanation of this choice"}
      ],
      "multiSelect": false  // true if user can select multiple options
    }
  ]
}
```

### Key Rules

1. **Header Constraint:** Maximum 12 characters (e.g., "Confirm", "Action", "Cleanup")
2. **Options Constraint:** Minimum 2, maximum 4 options per question
3. **multiSelect:** Set to `true` for "Additive" questions where multiple selections are valid; `false` for "Exclusive Choice" questions
4. **Sequential Questions:** Ask one question at a time. Wait for user response before asking the next question
5. **"Other" Option:** Users can always select "Other" to provide custom text input - do NOT add this as an explicit option
6. **Recommendations:** When recommending an option, add "(Recommended)" to the label and make it the first option

### Question Type Mapping

| Question Type | multiSelect | Example Use Case |
|--------------|-------------|------------------|
| **Additive** (multiple valid answers) | `true` | "Which reasons apply for skipping this issue?" |
| **Exclusive Choice** (single answer) | `false` | "How would you like to proceed?" |
| **Approval** (approve/reject) | `false` | "Do you approve these changes?" |
| **Confirmation** (yes/no with consequence) | `false` | "Are you sure you want to delete?" |

### Standard Option Patterns for implement

**Track Confirmation (Section 2.0):**
```json
{
  "question": "I found track '<track_description>'. Is this the correct track to implement?",
  "header": "Confirm",
  "options": [
    {"label": "Yes, proceed", "description": "Begin implementing this track"},
    {"label": "No, let me clarify", "description": "I want to select a different track"}
  ],
  "multiSelect": false
}
```

**Pattern Application (Section 3.0):**
```json
{
  "question": "Relevant patterns detected. How would you like to proceed?",
  "header": "Patterns",
  "options": [
    {"label": "Apply patterns (Recommended)", "description": "Use pattern guidance during implementation"},
    {"label": "View first", "description": "Show pattern details before deciding"},
    {"label": "Skip", "description": "Proceed without applying patterns"}
  ],
  "multiSelect": false
}
```

**Quality Gate Options (Section 3.5):**
```json
{
  "question": "Issues detected during quality analysis. How would you like to proceed?",
  "header": "Action",
  "options": [
    {"label": "Fix issues (Recommended)", "description": "Address the issues and re-run quality gate"},
    {"label": "Skip with reasons", "description": "Document reasons and proceed anyway"},
    {"label": "View details", "description": "See anti-pattern details for guidance"}
  ],
  "multiSelect": false
}
```

**Skip Reason Selection (Section 3.5):**
```json
{
  "question": "Why are you skipping these issues?",
  "header": "Skip Reason",
  "options": [
    {"label": "Intentional design", "description": "The pattern is used deliberately for a specific purpose"},
    {"label": "Deferred fix", "description": "Will be addressed in a future task or track"},
    {"label": "False positive", "description": "The detection is incorrect for this context"}
  ],
  "multiSelect": true
}
```

**Decision Capture (Section 3.6):**
```json
{
  "question": "A significant decision point was detected. Which approach would you like to take?",
  "header": "Decision",
  "options": [
    {"label": "Option A: <name>", "description": "<Brief description with key tradeoffs>"},
    {"label": "Option B: <name>", "description": "<Brief description with key tradeoffs>"},
    {"label": "Skip recording", "description": "Proceed without recording this decision"}
  ],
  "multiSelect": false
}
```

**Documentation Approval (Section 4.0):**
```json
{
  "question": "Do you approve the proposed updates to the <Document Name>?",
  "header": "Approve",
  "options": [
    {"label": "Approve changes", "description": "Apply the proposed updates to the document"},
    {"label": "Reject changes", "description": "Keep the document unchanged"}
  ],
  "multiSelect": false
}
```

**Track Cleanup (Section 5.0):**
```json
{
  "question": "Track '<track_description>' is complete. What would you like to do with it?",
  "header": "Cleanup",
  "options": [
    {"label": "Archive (Recommended)", "description": "Move to archive folder and remove from tracks file"},
    {"label": "Delete permanently", "description": "Permanently delete the track folder"},
    {"label": "Skip cleanup", "description": "Leave the track in the tracks file"}
  ],
  "multiSelect": false
}
```

**Delete Confirmation (Section 5.0):**
```json
{
  "question": "WARNING: This will permanently delete the track folder and all its contents. This action cannot be undone. Are you sure?",
  "header": "Confirm",
  "options": [
    {"label": "Yes, delete permanently", "description": "Proceed with irreversible deletion"},
    {"label": "Cancel deletion", "description": "Keep the track, do not delete"}
  ],
  "multiSelect": false
}
```

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

2.  **Use Injected Context:**
    -   The tracks data has been injected via the `# Context` section above.
    -   Parse the `tracks` array from the injected JSON to get track descriptions, statuses, and progress.
    -   **CRITICAL:** If no tracks are found, announce: "The tracks file is empty or malformed. No tracks to implement." and halt.

3.  **Continue:** Immediately proceed to the next step to select a track.

4.  **Select Track:**
    -   **If a track name was provided:**
        1.  Perform an exact, case-insensitive match for the provided name against the track descriptions from the parsed data.
        2.  If a unique match is found, confirm the selection using AskUserQuestion:
            ```json
            {
              "questions": [{
                "question": "I found track '<track_description>'. Is this the correct track to implement?",
                "header": "Confirm",
                "options": [
                  {"label": "Yes, proceed", "description": "Begin implementing this track"},
                  {"label": "No, let me clarify", "description": "I want to select a different track"}
                ],
                "multiSelect": false
              }]
            }
            ```
            - **If "Yes, proceed":** Continue with this track
            - **If "No, let me clarify":** Ask for clarification and suggest the next available track
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

This section ensures track work is properly isolated from the main codebase. Execute the Git Isolation Protocol to create or switch to a dedicated git branch before implementation begins.

After completing the protocol, proceed to **Section 2.5 SKILL ACTIVATION**.

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

### Step 0: Choose Execution Mode

For quality gate analysis, you may use either:
- **Parallel Agent Mode:** Launch specialist agents for faster concurrent analysis
- **Inline Mode:** Perform analysis directly (fallback if agents unavailable)

Default to **Parallel Agent Mode** for efficiency.

### Step 1: Run Quality Analysis

#### Parallel Agent Mode (Preferred)

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

2.  **Generate Diff Content:**
    -   Execute: `git diff HEAD` to get diff of all modified files
    -   Store for agent input

3.  **Prepare Agent Input:**
    ```json
    {
      "diff_content": "<diff output>",
      "file_list": ["<list of modified code files>"],
      "project_context": {
        "tech_stack": "<from conductor/tech-stack.md>",
        "styleguide_path": "conductor/code_styleguides/<language>.md",
        "product_guidelines_path": "conductor/product-guidelines.md"
      }
    }
    ```

4.  **Launch Analysis Agents in Parallel:**

    Send a single message with TWO Task tool calls:

    ```
    Task 1: code-quality-analyzer
    - subagent_type: "code-quality-analyzer"
    - prompt: <input JSON>

    Task 2: security-scanner
    - subagent_type: "security-scanner"
    - prompt: <input JSON>
    ```

5.  **Collect and Merge Results:**
    -   Parse JSON output from each agent
    -   Merge findings arrays
    -   Sum severity counts

6.  **Handle Agent Failures:**
    -   If an agent fails, fall back to inline detection for that category
    -   Code quality failure → Fall back to Step 1 (Inline Mode) subsection 2-4
    -   Security failure → Fall back to Step 1 (Inline Mode) subsection 5 (manual security check)

#### Inline Mode (Fallback)

1.  **Identify Modified Files via CLI:** (same as above)

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

5.  **Manual Security Check (if security agent failed):**
    -   Scan for hardcoded secrets patterns
    -   Check for injection vulnerability patterns
    -   Review authentication/authorization code

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
