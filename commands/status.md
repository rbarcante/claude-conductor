---
name: conductor:status
description: Displays the current progress of the project
argument-hint: (no arguments)
allowed-tools:
  - Read
  - Bash
---

# Context

!`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status full`

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to provide a status overview of the current tracks file. This involves reading the `conductor/tracks.md` file, parsing its content, and summarizing the progress of tasks.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## CLI Operations

**PROTOCOL: Token-efficient CLI commands for mechanical operations.**

The Python CLI provides token-efficient alternatives for mechanical tasks. Use these commands when performing deterministic operations like file parsing, status aggregation, and progress calculation.

**Note:** The `status full` command has been executed via the `# Context` section above. The injected JSON contains all data needed for this command. The documentation below is preserved for fallback scenarios.

### Available Subcommands

| Subcommand | Purpose | Output Format |
|------------|---------|---------------|
| `status verify` | Verify conductor setup is valid | JSON |
| `status tracks` | Parse all tracks with metadata and task counts | JSON |
| `status progress` | Calculate aggregate project progress | JSON |
| `status full` | Complete status report (verify + tracks + progress + git) | JSON |

### Usage Examples

**Verify Setup:**
```
`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status verify`
```

Expected output:
```json
{
  "is_valid": true,
  "setup_complete": true,
  "missing_required": [],
  "checks": {
    "required": {"product": {"path": "conductor/product.md", "exists": true}, ...}
  }
}
```

**Get Full Status (Recommended for this command):**
```
`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status full`
```

Expected output:
```json
{
  "setup": {"is_valid": true, ...},
  "tracks": [{"description": "...", "status": "in_progress", "tasks": {...}}, ...],
  "progress": {"overall": {"total": 10, "completed": 5, "progress_percent": 50.0}},
  "git": {"branch": "main", "has_changes": false}
}
```

**Parse Tracks Only:**
```
`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status tracks`
```

**Calculate Progress Only:**
```
`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status progress`
```

### When to Use CLI vs Direct Tool Calls

| Operation | Use CLI | Use Direct Tool Calls |
|-----------|---------|----------------------|
| Verify setup files exist | ✓ | |
| Parse tracks.md and extract track metadata | ✓ | |
| Count task status markers in plan.md files | ✓ | |
| Calculate progress percentages | ✓ | |
| Format output for display | | ✓ (use JSON data) |
| Handle errors and user communication | | ✓ |

### Fallback Instructions

If the CLI command fails or is unavailable:
1. Announce: "CLI operation failed. Falling back to direct tool calls."
2. Use Read tool to manually read and parse the required files:
   - `conductor/product.md`, `conductor/tech-stack.md`, `conductor/workflow.md` for setup verification
   - `conductor/tracks.md` for track registry
   - `conductor/tracks/<track_id>/plan.md` for each track's task counts
3. Parse the markdown manually to extract status markers (`[ ]`, `[~]`, `[x]`)
4. Calculate totals and percentages
5. Continue with the protocol

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Use Injected Context:**
    -   The full status data has been injected via the `# Context` section above.
    -   Parse the `setup` object from the injected JSON to check the `is_valid` field.
    -   If `is_valid` is `false`, check `missing_required` array for missing files.
    -   **Fallback:** If context injection failed, execute the CLI command manually:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status verify
        ```

2.  **Handle Failure:**
    -   If setup is invalid (missing required files), you MUST halt the operation immediately.
    -   Announce: "Conductor is not set up. Please run `/conductor:setup` to set up the environment."
    -   List the missing files from `missing_required`.
    -   Do NOT proceed to Status Overview Protocol.

---

## 2.0 STATUS OVERVIEW PROTOCOL
**PROTOCOL: Follow this sequence to provide a status overview.**

### 2.1 Use Injected Context

1.  **Use Injected Context:**
    -   The full status data has been injected via the `# Context` section at the top of this document.
    -   The JSON contains all required data for status reporting.
    -   **Fallback:** If context injection failed, execute the CLI command manually:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json status full
        ```

2.  **Extract Data:** From the injected JSON (or fallback response), extract:
    -   `setup`: Verification status
    -   `tracks`: Array of track objects with description, status, path, and task counts
    -   `progress`: Overall and per-track progress metrics
    -   `git`: Current branch and uncommitted changes status

### 2.2 Parse and Summarize Status

1.  **Process Track Data:** For each track in the `tracks` array:
    -   Extract `description`, `status` (pending/in_progress/completed)
    -   Extract `tasks.total`, `tasks.completed`, `tasks.in_progress`, `tasks.pending`

2.  **Calculate Summary:** From the `progress.overall` object:
    -   Total phases/tracks
    -   Total tasks across all tracks
    -   Tasks completed, in progress, and pending
    -   Overall progress percentage

3.  **Identify Current Work:**
    -   Find tracks with `status: "in_progress"`
    -   Within those tracks, identify tasks marked as in-progress
    -   Identify next pending tasks

### 2.3 Present Status Overview

1.  **Output Summary:** Present the status to the user in a clear, readable format:

    ```
    📊 **Project Status Report**
    *Generated: <current timestamp>*

    ---

    **Overall Progress:** <completed>/<total> tasks (<percentage>%)

    ---

    **Tracks:**

    | Track | Status | Progress |
    |-------|--------|----------|
    | <description> | <status emoji> <status> | <completed>/<total> (<percent>%) |
    | ... | ... | ... |

    ---

    **Current Work:**
    - **Active Track:** <track description or "None">
    - **Current Task:** <task description or "None in progress">
    - **Next Action:** <next pending task or "All tasks completed">

    ---

    **Git Status:**
    - **Branch:** <branch name>
    - **Uncommitted Changes:** <Yes/No>

    ---

    💡 Use `/conductor:implement` to continue working on the active track.
    ```

2.  **Status Emoji Mapping:**
    -   Pending: ⏳
    -   In Progress: 🔄
    -   Completed: ✅

3.  **Blockers:** If any tracks have documented blockers in their metadata, list them in a separate "Blockers" section.
