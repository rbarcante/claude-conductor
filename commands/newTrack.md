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

## AskUserQuestion Tool Protocol

**PROTOCOL: Use the AskUserQuestion tool for all interactive user prompts.**

All questions to the user during track creation MUST be asked using the `AskUserQuestion` tool. This provides a structured, consistent user experience with clickable options.

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

1. **Header Constraint:** Maximum 12 characters (e.g., "Interaction", "Data", "Scope")
2. **Options Constraint:** Minimum 2, maximum 4 options per question
3. **multiSelect:** Set to `true` for "Additive" questions where multiple selections are valid; `false` for "Exclusive Choice" questions
4. **Sequential Questions:** Ask one question at a time. Wait for user response before asking the next question
5. **"Other" Option:** Users can always select "Other" to provide custom text input - do NOT add this as an explicit option
6. **Recommendations:** When recommending an option, add "(Recommended)" to the label and make it the first option

### Question Type Mapping

| Question Type | multiSelect | Example Use Case |
|--------------|-------------|------------------|
| **Additive** (multiple valid answers) | `true` | "Which capabilities should this feature include?" |
| **Exclusive Choice** (single answer) | `false` | "How should users interact with this feature?" |
| **Approval** (approve/change) | `false` | "Does this specification capture the requirements?" |

### Standard Option Patterns for newTrack

**Approval Questions (Spec/Plan Review):**
```json
{
  "question": "Does this specification accurately capture the requirements?",
  "header": "Review",
  "options": [
    {"label": "Approve", "description": "The document is correct, proceed to next step"},
    {"label": "Suggest changes", "description": "I want to modify some parts"}
  ],
  "multiSelect": false
}
```

**Feature Interaction Type (Exclusive):**
```json
{
  "question": "How will users primarily interact with this feature?",
  "header": "Interaction",
  "options": [
    {"label": "UI component", "description": "Visual interface element (button, form, page)"},
    {"label": "API endpoint", "description": "Backend service or REST/GraphQL endpoint"},
    {"label": "CLI command", "description": "Command-line interface operation"},
    {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
  ],
  "multiSelect": false
}
```

**Feature Capabilities (Additive):**
```json
{
  "question": "Which capabilities should this feature include?",
  "header": "Capabilities",
  "options": [
    {"label": "Create/Add", "description": "Ability to create new items"},
    {"label": "Read/View", "description": "Ability to view existing items"},
    {"label": "Update/Edit", "description": "Ability to modify existing items"},
    {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
  ],
  "multiSelect": true
}
```

**Bug Reproduction (Additive):**
```json
{
  "question": "Which details are available for this bug?",
  "header": "Bug Info",
  "options": [
    {"label": "Steps to reproduce", "description": "I can provide exact reproduction steps"},
    {"label": "Error message", "description": "I have the error message or stack trace"},
    {"label": "Expected behavior", "description": "I know what should happen instead"},
    {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
  ],
  "multiSelect": true
}
```

### Auto-Generate Option

For interactive specification and plan generation, always include an auto-generate option as the last choice:

```json
{"label": "Auto-generate", "description": "Infer from context and generate the document"}
```

When user selects this option:
1. Stop asking questions immediately
2. Use gathered answers and project context to infer remaining details
3. Generate the complete document (spec or plan)
4. Present for review using an Approval question

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
    -   Do NOT proceed.

3.  **Continue:** After setup verification passes, proceed to **Section 1.2 GIT ISOLATION SETUP**.

---

## 1.2 GIT ISOLATION SETUP

**PROTOCOL: Follow the Git Isolation Protocol in `protocols/git-isolation.md`.**

This section ensures track work is properly isolated from the main codebase. Execute the Git Isolation Protocol to create or switch to a dedicated git branch before track creation begins.

**Note for newTrack:** Since the `track_id` does not exist yet, use the track description to generate the branch name:
1. Extract shortname from the track description (3-4 key words, hyphen-separated, lowercase)
2. Use the inferred track type to determine the branch prefix
3. Present branch options to the user following the protocol

After completing the protocol, proceed to **Section 2.0 NEW TRACK INITIALIZATION**.

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

2.  **Questioning Phase:** Ask a series of questions to gather details for the `spec.md`. Tailor questions based on the track type (Feature or Other). **All questions MUST use the AskUserQuestion tool** as defined in the **AskUserQuestion Tool Protocol** section above.

    *   **General Guidelines:**
        *   **CRITICAL:** You MUST ask questions sequentially (one by one) using the AskUserQuestion tool. Do not ask multiple questions in a single turn. Wait for the user's response after each question.
        *   Refer to information in **Product Definition**, **Tech Stack**, etc., to ask context-aware questions.
        *   Before formulating each question, classify its purpose:
            *   **Additive** (`multiSelect: true`): For scope definition (capabilities, features, requirements)
            *   **Exclusive Choice** (`multiSelect: false`): For singular decisions (interaction type, primary approach)
        *   **Always include "Auto-generate" as the last option** - when selected, stop asking questions and generate the spec from gathered context.
        *   Follow the key rules from the AskUserQuestion Tool Protocol (header max 12 chars, 2-4 options).

    *   **If FEATURE:**
        *   **Ask 3-5 relevant questions** to clarify the feature request.
        *   Tailor questions to what's missing from the description (UI, logic, data flow, etc.).

        **Example: Interaction Type Question (Exclusive):**
        ```json
        {
          "questions": [{
            "question": "How will users primarily interact with this feature?",
            "header": "Interaction",
            "options": [
              {"label": "UI component", "description": "Visual interface element (button, form, page)"},
              {"label": "API endpoint", "description": "Backend service or REST/GraphQL endpoint"},
              {"label": "CLI command", "description": "Command-line interface operation"},
              {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
            ],
            "multiSelect": false
          }]
        }
        ```

        **Example: Capability Selection Question (Additive):**
        ```json
        {
          "questions": [{
            "question": "Which capabilities should this feature include?",
            "header": "Capabilities",
            "options": [
              {"label": "Create/Add", "description": "Ability to create new items"},
              {"label": "Read/View", "description": "Ability to view existing items"},
              {"label": "Update/Edit", "description": "Ability to modify existing items"},
              {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
            ],
            "multiSelect": true
          }]
        }
        ```

        **Example: Data/Input Question (Additive):**
        ```json
        {
          "questions": [{
            "question": "What data or inputs does this feature need to handle?",
            "header": "Data",
            "options": [
              {"label": "User input", "description": "Form fields, text entry, selections"},
              {"label": "External API", "description": "Data from third-party services"},
              {"label": "Database", "description": "Stored records and relationships"},
              {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
            ],
            "multiSelect": true
          }]
        }
        ```

    *   **If SOMETHING ELSE (Bug, Chore, etc.):**
        *   **Ask 2-3 relevant questions** to obtain necessary details.

        **Example: Bug Information Question (Additive):**
        ```json
        {
          "questions": [{
            "question": "Which details are available for this bug?",
            "header": "Bug Info",
            "options": [
              {"label": "Steps to reproduce", "description": "I can provide exact reproduction steps"},
              {"label": "Error message", "description": "I have the error message or stack trace"},
              {"label": "Expected behavior", "description": "I know what should happen instead"},
              {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
            ],
            "multiSelect": true
          }]
        }
        ```

        **Example: Scope/Success Criteria Question (Additive):**
        ```json
        {
          "questions": [{
            "question": "What defines success for this task?",
            "header": "Success",
            "options": [
              {"label": "Specific files changed", "description": "I know exactly which files need modification"},
              {"label": "Test passes", "description": "Existing or new tests should pass"},
              {"label": "Behavior change", "description": "Observable change in application behavior"},
              {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
            ],
            "multiSelect": true
          }]
        }
        ```

    *   **Auto-Generate Behavior:** If the user selects "Auto-generate" at any point:
        1. Stop asking questions immediately
        2. Use all gathered answers plus project context (**Product Definition**, **Tech Stack**) to infer remaining details
        3. Generate the complete `spec.md` document
        4. Present for review using the Approval pattern (step 4)

3.  **Draft `spec.md`:** Once sufficient information is gathered (or auto-generate selected), draft the content for the track's `spec.md` file, including sections like Overview, Functional Requirements, Non-Functional Requirements (if any), Acceptance Criteria, and Out of Scope.

4.  **User Confirmation:** Present the drafted `spec.md` content to the user and use the AskUserQuestion tool for approval:

    > "I've drafted the specification for this track. Please review:"
    >
    > ```markdown
    > [Drafted spec.md content here]
    > ```

    **Use AskUserQuestion for approval:**
    ```json
    {
      "questions": [{
        "question": "Does this specification accurately capture the requirements?",
        "header": "Review",
        "options": [
          {"label": "Approve", "description": "The specification is correct, proceed to plan generation"},
          {"label": "Suggest changes", "description": "I want to modify some parts before proceeding"}
        ],
        "multiSelect": false
      }]
    }
    ```

    **Handle Response:**
    *   **If "Approve":** Proceed to Section 2.3 (Interactive Plan Generation)
    *   **If "Suggest changes":** Ask the user what changes they want, revise the spec, and present for approval again

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

3.  **User Confirmation:** Present the drafted `plan.md` to the user and use the AskUserQuestion tool for approval:

    > "I've drafted the implementation plan. Please review:"
    >
    > ```markdown
    > [Drafted plan.md content here]
    > ```

    **Use AskUserQuestion for approval:**
    ```json
    {
      "questions": [{
        "question": "Does this plan accurately reflect the implementation steps?",
        "header": "Review",
        "options": [
          {"label": "Approve", "description": "The plan is correct, proceed to create the track"},
          {"label": "Suggest changes", "description": "I want to modify some parts before proceeding"}
        ],
        "multiSelect": false
      }]
    }
    ```

    **Handle Response:**
    *   **If "Approve":** Proceed to Section 2.4 (Create and Register Track)
    *   **If "Suggest changes":** Ask the user what changes they want, revise the plan, and present for approval again

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
