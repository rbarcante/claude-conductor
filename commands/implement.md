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

You are an AI agent for the Conductor spec-driven development framework. Your task is to implement a track. Follow this protocol precisely.

CRITICAL: Validate every tool call. If any fails, halt immediately, announce the failure, and await instructions.

---

## CLI Reference

```bash
# Status & archiving
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status TRACK_ID STATUS
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive TRACK_ID
# Consolidated context (replaces multiple Reads)
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json tracks read-context TRACK_ID
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement git-snapshot [--diff-stat-only]
# Batch operations (replaces per-task calls)
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement batch-match-patterns --plan TRACK_ID
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json codereview filtered-diff [--base BRANCH] [--exclude PATH...]
# Task-level operations
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py tracks update-task TRACK_ID PHASE_IDX TASK_IDX STATUS
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage --format FORMAT --path PATH
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path ADR_PATH
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement suggest-branch TRACK_ID
```

**Fallback:** If context injection fails, scan `conductor/tracks/*/metadata.json` directly.

---

## 1.1 SETUP CHECK

**PROTOCOL: Follow the Verify Setup Protocol in `protocols/verify-setup.md`.**

---

## 2.0 TRACK SELECTION

**PROTOCOL: Identify and select the track to be implemented.**

1. **Check for User Input:** If user provided a track name as argument, match it case-insensitively against track descriptions from the injected `# Context` JSON.
   - If unique match found, confirm: "I found track '<description>'. Is this correct?"
   - If no match or ambiguous, inform user and suggest the next available track.

2. **Auto-Select:** If no argument provided, find the first track where `status` is NOT `completed`.
   - Announce: "Automatically selecting the next incomplete track: '<description>'."
   - If no incomplete tracks: "All tasks are completed!" — halt.

3. **If no tracks found:** "The tracks file is empty or malformed." — halt.

4. After selection, proceed to **Section 2.1**.

---

## 2.1 GIT ISOLATION SETUP

**PROTOCOL: Follow the Git Isolation Protocol in `protocols/git-isolation.md`.**

### Fast Path Check

1. Get current branch: `git branch --show-current`
2. Extract track shortname from `track_id` (e.g., `dark-mode-toggle` from `dark-mode-toggle_20260122`)
3. **If current branch contains the track shortname:** Announce "Already on branch `<branch>`. Proceeding." — skip to **Section 2.2**
4. **Otherwise:** Execute the full Git Isolation Protocol.

---

## 2.2 BASE BRANCH DETECTION

**PROTOCOL: Detect the base branch via a single CLI call.**

Execute:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement git-snapshot --diff-stat-only
```

The response includes:
- `data.base_branch` — validated base branch name
- `data.current_branch` — current branch
- `data.uncommitted_changes` — staging status
- `data.diff_stats` — files changed, lines added/removed

Store `data.base_branch` as `BASE_BRANCH` for use in **Section 3.7**.

Announce: "Base branch detected: `<BASE_BRANCH>`."

**Fallback:** If CLI fails, follow the manual detection steps in `protocols/git-isolation.md` (reflog → remote tracking → default branch → `master`).

---

## 2.5 SKILL ACTIVATION (LAZY LOADING)

**PROTOCOL: Load skills incrementally to minimize upfront token usage.**

### Phase 1: Always-Active Skills (Upfront)

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json`
   - If missing, skip silently and proceed to **Section 3.0**
2. Identify skills with `activation.always_active: true`, read their SKILL.md files
3. Announce: `🔧 **Skills Activated:** conductor-methodology (always active)`

### Phase 2: Task-Specific Skills (Deferred)

Happens in Section 3.0 before each task:
1. Extract keywords from task description
2. Match against `activation.keywords`, `activation.tech_stack`, `activation.file_patterns`
3. Activate skills scoring >= 1.5 (max 3 per task, skip already-loaded)
4. Announce only if new skills activated: `🔧 **Task Skills:** [Name] activated`

---

## 3.0 TRACK IMPLEMENTATION

**PROTOCOL: Execute the selected track.**

### Step 1: Announce and Update Status

1. Announce which track you are implementing.
2. Execute: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> in-progress`
   - **Fallback:** Manually edit `conductor/tracks/<track_id>/metadata.json`, set `status` to `"in_progress"`.

### Step 2: Load Track Context (CACHE FOR SESSION)

Execute a single CLI call to load spec, plan, and metadata:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json tracks read-context <track_id>
```

The response includes:
- `data.spec` — full specification text
- `data.plan.parsed` — structured phases and tasks with indices
- `data.metadata` — track type, status, timestamps

Also read the **Workflow** file (`conductor/workflow.md`). Cache both in context — do NOT re-read during task execution.

**Error Handling:** If either read fails, stop and inform the user.

### Step 3: Surface Patterns (Batch — Single Upfront Call)

Execute once for the entire track:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement batch-match-patterns --plan <track_id>
```

The response returns a `task_matches` array mapping each task to its matched patterns. Cache the results. Before each task, check its matches:
- If any patterns score >= 1.0, announce (max 3, sorted by score):
  ```
  📚 **Relevant Patterns Detected:**
  1. **[Pattern Name]** (patterns/core/<name>.md)
     > <one-line description>
  [Apply patterns? (Y)es / (S)kip / (V)iew first]
  ```
- If no matches >= 1.0, continue silently.

### Step 4: Execute Tasks

Iterate through each task in the plan's `parsed` phases sequentially.

**For each task:**

a. **Mark In Progress:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py tracks update-task <track_id> <phase_idx> <task_idx> in-progress`

b. **Activate Task Skills** (Phase 2 from Section 2.5 — skip already-loaded skills)

c. **Check Cached Patterns** from Step 3 for this task

d. **Execute per Workflow (FROM CACHE):** Follow the Workflow's "Task Workflow" section — TDD cycle, implementation, testing, committing. The Workflow is the single source of truth.

e. **Capture Decisions** per Section 3.6 when significant decision points arise

f. **If this is the LAST task:** Before committing, run Step 5 (Finalize Track) first so that `metadata.json` is updated and staged with this commit.

g. **Mark Complete:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py tracks update-task <track_id> <phase_idx> <task_idx> completed`

### Step 5: Finalize Track

After all tasks complete:

1. **Run Auto Code Review** (Section 3.7)
2. **Update status BEFORE committing the last task:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement update-status <track_id> completed`
   - **Fallback:** Manually edit `conductor/tracks/<track_id>/metadata.json`, set `status` to `"completed"`.
   - **CRITICAL:** This MUST happen before the last task's commit so that `metadata.json` is staged and included in that commit. Do NOT create a separate commit for track completion.

---

## 3.5 QUALITY GATE VERIFICATION

**PROTOCOL: Run quality analysis after task implementation, before marking complete.**

**Full Reference:** `protocols/quality-analysis.md` and `protocols/coverage-intelligence.md`

1. **Get modified files:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement modified-files`
2. **Run agents in parallel:** Launch `code-quality-analyzer` and `security-scanner` via Task tool
3. **Run coverage:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement parse-coverage`
4. **Handle results:**
   - 🛑 Critical → must fix before proceeding
   - ⚠️ High/Medium → allow skip with documented reason
   - ✅ No issues → proceed

---

## 3.6 DECISION CAPTURE

**PROTOCOL: Capture significant implementation decisions.**

**Full Reference:** `protocols/decision-capture.md`

**Triggers:** Technology selection, pattern choice, API design, data modeling, error handling strategies, performance tradeoffs.

1. Detect when multiple reasonable alternatives exist
2. Present options with pros/cons (A/B/skip)
3. Get ADR number: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement next-adr-number --path conductor/tracks/<track_id>`
4. Append entry to `conductor/tracks/<track_id>/decisions.md`

**Skip when:** approach dictated by spec, only one option, or easily reversible.

---

## 3.7 AUTO CODE REVIEW

**PROTOCOL: Run automated code review when track reaches completion.**

### 3.7.1 Prompt User

Ask via AskUserQuestion: "All tasks complete. Run automated code review before finalizing?"
- Options: "Run code review (Recommended)" / "Skip"
- If Skip: return to finalization.

### 3.7.2 Generate Diff via CLI

Execute a single call to generate the filtered diff:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json codereview filtered-diff --base <BASE_BRANCH> --exclude "conductor/tracks/*"
```

The response includes:
- `data.stats` — files_changed, lines_added, lines_removed, truncated flag
- `data.language_breakdown` — per-language file counts and line counts
- `data.file_stats` — per-file breakdown with language detection
- `data.diff_content` — the full diff (filtered, size-capped)

**Uncommitted changes check:** If `git status --porcelain` shows changes, ask user:
- "All changes" → use `--base <BASE_BRANCH>` (includes working tree)
- "Committed only" → default three-dot diff
- "Skip review" → return to finalization

**Empty diff handling:** If no reviewable product files changed, announce and proceed to finalization.

### 3.7.3 Run Analysis (Parallel)

Prepare agent input from the CLI response:
```json
{
  "diff_content": "<data.diff_content>",
  "file_list": ["<from data.file_stats[].file>"],
  "project_context": {
    "tech_stack": "<from conductor/tech-stack.md>",
    "language_breakdown": "<from data.language_breakdown>",
    "styleguide_path": "conductor/code_styleguides/<language>.md",
    "product_guidelines_path": "conductor/product-guidelines.md"
  }
}
```

**Launch all three agents simultaneously** in a single message:
- `subagent_type: "code-quality-analyzer"`
- `subagent_type: "security-scanner"`
- `subagent_type: "test-coverage-analyzer"`

**Failures:** 1 agent fails → note in report, proceed with others. 2+ fail → skip review.

### 3.7.4 Generate and Save Report

1. Aggregate findings from all agents (merge `findings` arrays, sum severity counts)
2. Generate report using the template from `codeReview.md` Section 7.2 (Summary table, Code Quality, Security, Test Coverage, Recommendations sections). Add `**Track:** <description>` to header.
3. Save to `conductor/tracks/<track_id>/review.md`
4. Update track `index.md` with link to review
5. Display report: High severity → "⚠️ Review before merging." / No high → "✅ No blocking issues."
6. Return to finalization (review is non-blocking)

---

## 4.0 SYNCHRONIZE PROJECT DOCUMENTATION

**Trigger:** Only when track status reaches `[x]` (completed).

1. Read track Specification, Product Definition, Tech Stack, Product Guidelines
2. Identify new features, functionality changes, or tech updates
3. For each document needing changes, present diff to user for approval
4. Apply only after explicit confirmation
5. **Note:** Documentation updates should be bundled into the last code commit or left as uncommitted changes for the user to include in their next commit. Do NOT create a separate conductor-specific commit for docs sync.

| Document | Update When | Confirmation |
|----------|-------------|-------------|
| Product Definition | Feature significantly impacts product description | Yes |
| Tech Stack | Technology changes detected | Yes |
| Product Guidelines | **Rare** — branding/strategic shifts only | Yes (with warning) |

---

## 5.0 TRACK CLEANUP

**Trigger:** After track completion and documentation sync.

| Choice | Action | Command |
|--------|--------|---------|
| A. Archive | Move to `conductor/tracks/archive/` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py implement archive <track_id>` |
| B. Delete | Permanently remove | Manual (requires "yes" confirmation) |
| C. Skip | Leave in tracks file | None |

1. Prompt user with A/B/C
2. Archive: Run CLI, commit `chore: Archive track '<description>'`
3. Delete: Require explicit confirmation, delete folder
4. Commit changes
