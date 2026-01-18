---
name: conductor:newTrack
description: Plans a track, generates track-specific spec documents and updates the tracks file
argument-hint: "[optional: track description]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to guide the user through the creation of a new "Track" (a feature or bug fix), generate the necessary specification (`spec.md`) and plan (`plan.md`) files, and organize them within a dedicated track directory.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## CLI Operations

**PROTOCOL: Token-efficient CLI commands for mechanical operations.**

The Python CLI provides scriptable operations that reduce token usage by offloading mechanical tasks (ID generation, file scaffolding, registry updates) to deterministic Python code.

### Available Subcommands

| Subcommand | Purpose | Output Format |
|------------|---------|---------------|
| `generate-id DESCRIPTION` | Generate track ID from description | JSON: `{track_id, shortname, date, description}` |
| `scaffold TRACK_ID --type TYPE --description DESC` | Create track directory structure with template files | JSON: `{track_id, track_dir, created_files, metadata}` |
| `register TRACK_ID --description DESC` | Register track in conductor/tracks.md | JSON: `{track_id, tracks_file, entry}` |

### Usage Examples

**Generate Track ID:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack generate-id "Add dark mode toggle"
```
Output:
```json
{
  "success": true,
  "data": {
    "track_id": "dark-mode-toggle_20260121",
    "shortname": "dark-mode-toggle",
    "date": "20260121",
    "description": "Add dark mode toggle"
  }
}
```

**Scaffold Track Directory:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack scaffold dark-mode-toggle_20260121 --type feature --description "Add dark mode toggle"
```
Output:
```json
{
  "success": true,
  "data": {
    "track_id": "dark-mode-toggle_20260121",
    "track_type": "feature",
    "track_dir": "conductor/tracks/dark-mode-toggle_20260121",
    "created_files": [
      "conductor/tracks/dark-mode-toggle_20260121/index.md",
      "conductor/tracks/dark-mode-toggle_20260121/metadata.json",
      "conductor/tracks/dark-mode-toggle_20260121/spec.md",
      "conductor/tracks/dark-mode-toggle_20260121/plan.md",
      "conductor/tracks/dark-mode-toggle_20260121/decisions.md"
    ]
  }
}
```

**Register Track:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack register dark-mode-toggle_20260121 --description "Add dark mode toggle"
```

### Track Types

Valid track types for `--type`:
- `feature` (default) - New functionality
- `bugfix` - Bug fixes
- `refactor` - Code refactoring
- `docs` - Documentation changes
- `chore` - Maintenance tasks

### When to Use CLI vs Direct Tool Calls

| Operation | Use CLI | Use Direct Tool Calls |
|-----------|---------|----------------------|
| Generate track ID | Yes - `generate-id` | No |
| Create directory structure | Yes - `scaffold` | Fallback only |
| Write template files (index, metadata, decisions) | Yes - `scaffold` | Fallback only |
| Write spec.md with generated content | No | Yes - use Write tool to overwrite template |
| Write plan.md with generated content | No | Yes - use Write tool to overwrite template |
| Register track in tracks.md | Yes - `register` | Fallback only |
| Interactive spec/plan generation | N/A | LLM generates content through conversation |

### Fallback Instructions

If any CLI command fails:

1. **For `generate-id` failure:** Generate manually using format `shortname_YYYYMMDD`:
   - Extract 3-4 key words from description (skip stop words)
   - Join with hyphens, lowercase
   - Append underscore and today's date (YYYYMMDD)

2. **For `scaffold` failure:** Create files manually using Write tool:
   - Create directory: `conductor/tracks/<track_id>/`
   - Create `index.md`, `metadata.json`, `spec.md`, `plan.md`, `decisions.md`
   - Follow the content structures defined in Section 2.4

3. **For `register` failure:** Use Edit tool on `conductor/tracks.md`:
   - Find "## Active Tracks" section
   - Append entry: `- [ ] **Track: <description>**\n  *Link: [<track_id>](./tracks/<track_id>/)*`

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol**, resolve and verify the existence of:
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:**
    -   If ANY of these files are missing, you MUST halt the operation immediately.
    -   Announce: "Conductor is not set up. Please run `/conductor:setup` to set up the environment."
    -   Do NOT proceed to New Track Initialization.

---

## 2.0 NEW TRACK INITIALIZATION
**PROTOCOL: Follow this sequence precisely.**

### 2.1 Get Track Description and Determine Type

1.  **Load Project Context:** Read and understand the content of the project documents (**Product Definition**, **Tech Stack**, etc.) resolved via the **Universal File Resolution Protocol**.
2.  **Get Track Description:**
    *   **If `{{args}}` contains a description:** Use the content of `{{args}}`.
    *   **If `{{args}}` is empty:** Ask the user:
        > "Please provide a brief description of the track (feature, bug fix, chore, etc.) you wish to start."
        Await the user's response and use it as the track description.
3.  **Infer Track Type:** Analyze the description to determine if it is a "Feature" or "Something Else" (e.g., Bug, Chore, Refactor). Do NOT ask the user to classify it.

### 2.2 Interactive Specification Generation (`spec.md`)

1.  **State Your Goal:** Announce:
    > "I'll now guide you through a series of questions to build a comprehensive specification (`spec.md`) for this track."

2.  **Questioning Phase:** Ask a series of questions to gather details for the `spec.md`. Tailor questions based on the track type (Feature or Other).
    *   **CRITICAL:** You MUST ask these questions sequentially (one by one). Do not ask multiple questions in a single turn. Wait for the user's response after each question.
    *   **General Guidelines:**
        *   Refer to information in **Product Definition**, **Tech Stack**, etc., to ask context-aware questions.
        *   Provide a brief explanation and clear examples for each question.
        *   **Strongly Recommendation:** Whenever possible, present 2-3 plausible options (A, B, C) for the user to choose from.
        *   **Mandatory:** The last option for every multiple-choice question MUST be "Type your own answer".

        *   **1. Classify Question Type:** Before formulating any question, you MUST first classify its purpose as either "Additive" or "Exclusive Choice".
            *   Use **Additive** for brainstorming and defining scope (e.g., users, goals, features, project guidelines). These questions allow for multiple answers.
            *   Use **Exclusive Choice** for foundational, singular commitments (e.g., selecting a primary technology, a specific workflow rule). These questions require a single answer.

        *   **2. Formulate the Question:** Based on the classification, you MUST adhere to the following:
            *   **Strongly Recommended:** Whenever possible, present 2-3 plausible options (A, B, C) for the user to choose from.
            *   **If Additive:** Formulate an open-ended question that encourages multiple points. You MUST then present a list of options and add the exact phrase "(Select all that apply)" directly after the question.
            *   **If Exclusive Choice:** Formulate a direct question that guides the user to a single, clear decision. You MUST NOT add "(Select all that apply)".

        *   **3. Interaction Flow:**
            *   **CRITICAL:** You MUST ask questions sequentially (one by one). Do not ask multiple questions in a single turn. Wait for the user's response after each question.
            *   The last option for every multiple-choice question MUST be "Type your own answer".
            *   Confirm your understanding by summarizing before moving on to the next question or section..

    *   **If FEATURE:**
        *   **Ask 3-5 relevant questions** to clarify the feature request.
        *   Examples include clarifying questions about the feature, how it should be implemented, interactions, inputs/outputs, etc.
        *   Tailor the questions to the specific feature request (e.g., if the user didn't specify the UI, ask about it; if they didn't specify the logic, ask about it).

    *   **If SOMETHING ELSE (Bug, Chore, etc.):**
        *   **Ask 2-3 relevant questions** to obtain necessary details.
        *   Examples include reproduction steps for bugs, specific scope for chores, or success criteria.
        *   Tailor the questions to the specific request.

3.  **Draft `spec.md`:** Once sufficient information is gathered, draft the content for the track's `spec.md` file, including sections like Overview, Functional Requirements, Non-Functional Requirements (if any), Acceptance Criteria, and Out of Scope.

4.  **User Confirmation:** Present the drafted `spec.md` content to the user for review and approval.
    > "I've drafted the specification for this track. Please review the following:"
    >
    > ```markdown
    > [Drafted spec.md content here]
    > ```
    >
    > "Does this accurately capture the requirements? Please suggest any changes or confirm."
    Await user feedback and revise the `spec.md` content until confirmed.

### 2.3 Interactive Plan Generation (`plan.md`)

1.  **State Your Goal:** Once `spec.md` is approved, announce:
    > "Now I will create an implementation plan (plan.md) based on the specification."

2.  **Generate Plan:**
    *   Read the confirmed `spec.md` content for this track.
    *   Resolve and read the **Workflow** file (via the **Universal File Resolution Protocol** using the project's index file).
    *   Generate a `plan.md` with a hierarchical list of Phases, Tasks, and Sub-tasks.
    *   **CRITICAL:** The plan structure MUST adhere to the methodology in the **Workflow** file (e.g., TDD tasks for "Write Tests" and "Implement").
    *   Include status markers `[ ]` for **EVERY** task and sub-task. The format must be:
        - Parent Task: `- [ ] Task: ...`
        - Sub-task: `    - [ ] ...`
    *   **CRITICAL: Inject Phase Completion Tasks.** Determine if a "Phase Completion Verification and Checkpointing Protocol" is defined in the **Workflow**. If this protocol exists, then for each **Phase** that you generate in `plan.md`, you MUST append a final meta-task to that phase. The format for this meta-task is: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`.

3.  **User Confirmation:** Present the drafted `plan.md` to the user for review and approval.
    > "I've drafted the implementation plan. Please review the following:"
    >
    > ```markdown
    > [Drafted plan.md content here]
    > ```
    >
    > "Does this plan accurately reflect the implementation steps? Please suggest any changes or confirm."
    Await user feedback and revise the `plan.md` content until confirmed.

### 2.4 Create and Register Track

**PROTOCOL: Use CLI commands for mechanical operations. Fall back to direct tool calls only if CLI fails.**

#### Step 1: Generate Track ID (CLI)

Execute the CLI command to generate a unique track ID:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack generate-id "<track description>"
```

Parse the JSON response to extract:
- `track_id`: The generated identifier (format: `shortname_YYYYMMDD`)
- `shortname`: The base name derived from description
- `date`: Today's date (YYYYMMDD)

**Fallback:** If CLI fails, manually create ID:
- Extract 3-4 significant words from description (skip stop words like "a", "the", "and")
- Join with hyphens, convert to lowercase
- Append `_` and today's date in YYYYMMDD format
- Example: "Add dark mode toggle" -> `dark-mode-toggle_20260121`

#### Step 2: Scaffold Track Directory (CLI)

Execute the CLI command to create directory structure and template files:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack scaffold <track_id> --type <track_type> --description "<track description>"
```

Where `<track_type>` is one of: `feature`, `bugfix`, `refactor`, `docs`, `chore`

This creates:
- `conductor/tracks/<track_id>/index.md` - Track context links
- `conductor/tracks/<track_id>/metadata.json` - Track metadata
- `conductor/tracks/<track_id>/spec.md` - Template (will be overwritten)
- `conductor/tracks/<track_id>/plan.md` - Template (will be overwritten)
- `conductor/tracks/<track_id>/decisions.md` - ADR log

**Fallback:** If CLI fails, manually create using Write tool:

1. Create `conductor/tracks/<track_id>/index.md`:
   ```markdown
   # Track: <track description>

   > Track ID: `<track_id>`

   ## Contents

   - [Specification](./spec.md) - Requirements and acceptance criteria
   - [Implementation Plan](./plan.md) - Task breakdown and progress
   - [Decisions](./decisions.md) - Architecture Decision Records (ADRs)
   - [Metadata](./metadata.json) - Track metadata and status
   ```

2. Create `conductor/tracks/<track_id>/metadata.json`:
   ```json
   {
     "track_id": "<track_id>",
     "type": "<feature|bugfix|refactor|docs|chore>",
     "status": "new",
     "created_at": "<ISO timestamp>",
     "updated_at": "<ISO timestamp>",
     "description": "<track description>"
   }
   ```

3. Create `conductor/tracks/<track_id>/decisions.md`:
   - Read template from `${CLAUDE_PLUGIN_ROOT}/templates/decisions.md` if available
   - Otherwise create with header: `# Decisions Log: <Track Description>`

#### Step 3: Write Generated Content

Use the Write tool to overwrite the template files with the user-confirmed content:

1. Write the confirmed `spec.md` content to `conductor/tracks/<track_id>/spec.md`
2. Write the confirmed `plan.md` content to `conductor/tracks/<track_id>/plan.md`

**Note:** The CLI scaffold creates templates; this step replaces them with the actual generated content from Sections 2.2 and 2.3.

#### Step 4: Register Track (CLI)

Execute the CLI command to register the track in the tracks registry:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack register <track_id> --description "<track description>"
```

This appends the track entry to `conductor/tracks.md` in the Active Tracks section.

**Fallback:** If CLI fails, manually edit `conductor/tracks.md`:
1. Read current content
2. Find "## Active Tracks" section
3. Append entry:
   ```markdown
   - [ ] **Track: <Track Description>**
     *Link: [<track_id>](./tracks/<track_id>/)*
   ```
4. Write updated content back

#### Step 5: Commit Changes

Stage all the new files and commit:
```bash
git add conductor/tracks/<track_id>/spec.md \
        conductor/tracks/<track_id>/plan.md \
        conductor/tracks/<track_id>/decisions.md \
        conductor/tracks/<track_id>/metadata.json \
        conductor/tracks/<track_id>/index.md \
        conductor/tracks.md && \
git commit -m "conductor(track): Create track '<track description>'"
```

#### Step 6: Final Announcement

Announce successful creation:
> "Track '<track description>' has been created successfully. You can now begin implementation with `/conductor:implement` or review the plan at `conductor/tracks/<track_id>/plan.md`."
