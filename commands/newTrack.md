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
  - AskUserQuestion
  - Agent
  - EnterPlanMode
  - ExitPlanMode
  - Skill
---

# Context

<!-- No upfront context injection needed - all CLI calls are action-oriented -->

<system_directive>

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to guide the user through the creation of a new "Track" (a feature or bug fix), generate the necessary specification (`spec.md`) and plan (`plan.md`) files, and organize them within a dedicated track directory.

This command uses a **two-phase workflow** powered by Claude Code's Plan Mode:
- **Phase A (Plan Mode):** Research, compose spec + plan content in read-only mode, write to CC plan file for review
- **Phase B (Normal Mode):** After user approval, create branch, scaffold directory, write files, register, commit

<note type="critical">
You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.
</note>

</system_directive>

---

<cli_reference>

## Action CLI Commands

The following CLI commands are used for write operations during track creation:

```bash
# Generate track ID from description
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack generate-id "DESCRIPTION"

# Validate and enforce metadata.json for the track
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack register TRACK_ID --description "DESC"
```

### Track Types

Valid types: `feature` (default), `bugfix`, `refactor`, `docs`, `chore`

### Fallback Instructions

1. **For `generate-id` failure:** Generate manually using format `shortname_YYYYMMDD`
2. **For `register` failure:** Edit `conductor/tracks/<track_id>/metadata.json` directly

</cli_reference>

---

<protocol name="askuserquestion">

## AskUserQuestion Tool Protocol

**PROTOCOL: Use the AskUserQuestion tool for all interactive user prompts.**

**Full Pattern Reference:** `templates/askuserquestion-patterns.md`

<constraints>

### Quick Reference

| Rule | Constraint |
|------|------------|
| Header | Max 12 characters |
| Options | 2-4 per question |
| Sequential | One question at a time |
| multiSelect | `true` for additive, `false` for exclusive |

### Question Types

| Type | multiSelect | Use Case |
|------|-------------|----------|
| Additive | `true` | Multiple valid answers (capabilities, features) |
| Exclusive | `false` | Single answer (interaction type, approach) |
| Approval | `false` | Confirm/change decisions |

</constraints>

### Auto-Generate Behavior

When user selects "Auto-generate": stop asking questions, use context to infer remaining details, generate document, present for approval.

</protocol>

---

<protocol name="cc_plan_file">

## CC Plan File Format

During Phase A, composed content is written to the CC plan file for user review. Use this exact structure:

```markdown
# New Track: <description>

## Track Configuration
- **Type**: <feature|bugfix|refactor|docs|chore>
- **Branch**: <prefix>/<shortname>

---

## Specification

<full spec.md content — Overview, Background, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Out of Scope>

---

## Implementation Plan

<full plan.md content — Phases → Tasks → Sub-tasks with [ ] markers, verification tasks per phase>

---

## Phase B — Execution Steps (follow in order after approval)

After exiting plan mode, execute these steps in order. Use the Conductor CLI at `${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py`.

1. **Create git branch**: `git checkout -b <prefix>/<shortname>`
2. **Generate track ID**: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack generate-id "<description>"`
3. **Create directory**: `mkdir -p conductor/tracks/<TRACK_ID>`
4. **Write all track files** using the Write tool (no scaffold — write directly):
   - `spec.md` — approved Specification content above
   - `plan.md` — approved Implementation Plan content above
   - `index.md` — track index linking to spec, plan, decisions, metadata
   - `decisions.md` — empty ADR template
   - `metadata.json` — `{"track_id":"<ID>","type":"<type>","status":"pending","description":"<desc>","created_at":"<ISO>","updated_at":"<ISO>"}`
5. **Register track**: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack register <TRACK_ID> --description "<description>"`
6. **Commit**: Stage with `git add conductor/tracks/<TRACK_ID>/metadata.json && git add conductor/tracks/<TRACK_ID>/*`, then commit with type-appropriate prefix
7. **Start implementation**: Call the Skill tool with `skill: "conductor:implement", args: "<TRACK_ID>"` — do NOT implement the track yourself

**CRITICAL**: Step 7 is mandatory. You MUST invoke `conductor:implement` via the Skill tool with the track ID as args. Do NOT read the plan and start coding — the implement skill has its own protocol, CLI commands, and workflow.
```

</protocol>

---

# PHASE A — PLAN MODE (read-only, system-enforced)

<phase name="enter_plan_mode">

## 1.0 ENTER PLAN MODE

<instructions>

**Call `EnterPlanMode` to activate read-only mode.**

- If already in plan mode, skip this step
- If `EnterPlanMode` is unavailable or fails, instruct the user: "Please press `Shift+Tab` to enter Plan Mode, then re-invoke the command."
- Do NOT proceed to Phase A steps until plan mode is active

</instructions>

</phase>

---

<phase name="setup_check">

## 1.1 SETUP CHECK

<instructions>

**PROTOCOL: Follow the Verify Setup Protocol in `protocols/verify-setup.md`.**

This step only reads files — fully compatible with plan mode.

**Explicit file resolution steps:**
1. Read `conductor/index.md` to find the actual paths for Product Definition, Tech Stack, and Workflow
2. If `conductor/index.md` doesn't exist, use default paths: `conductor/product.md`, `conductor/tech-stack.md`, `conductor/workflow.md`
3. Verify each file exists. If any are missing, HALT and tell the user to run `/conductor:setup`
4. Store the resolved paths — they will be passed to the context research agent in Step 1.3

After setup verification passes, proceed to **Section 1.2**.

</instructions>

</phase>

---

<phase name="get_description">

## 1.2 GET TRACK DESCRIPTION AND DETERMINE TYPE

<instructions>

1. **Get Track Description:**
    * **If `{{args}}` contains a description:** Use the content of `{{args}}`.
    * **If `{{args}}` is empty:** Use AskUserQuestion to ask:
        > "Please provide a brief description of the track (feature, bug fix, chore, etc.) you wish to start."
        Await the user's response and use it as the track description.

2. **Infer Track Type:** Analyze the description to determine the track type. Do NOT ask the user to classify it. Use the valid types defined in `<cli_reference>`.

3. **Decide Branch Name:** (for use in Phase B — do NOT create the branch yet)
    - Extract shortname from the track description (3-4 key words, hyphen-separated, lowercase)
    - Map track type to branch prefix:

    | Track Type | Branch Prefix |
    |------------|---------------|
    | feature    | feature/      |
    | bugfix     | fix/          |
    | refactor   | refactor/     |
    | docs       | docs/         |
    | chore      | chore/        |

    - Store the decided branch name (e.g., `feature/my-new-feature`) for Phase B

</instructions>

</phase>

---

<phase name="context_research">

## 1.3 CONTEXT RESEARCH VIA SUBAGENT

<instructions>

<note type="critical">
You MUST launch the `conductor:track-context-researcher` agent in this step. Do NOT skip it or read project files yourself — the agent offloads context gathering to a cheaper model and keeps the parent context clean.
</note>

1. **Prepare input** for the agent:
    ```json
    {
      "description": "<track description>",
      "type": "<inferred track type>",
      "project_files": {
        "product_definition": "<resolved path to product.md>",
        "tech_stack": "<resolved path to tech-stack.md>",
        "workflow": "<resolved path to workflow.md>",
        "product_guidelines": "<resolved path to product-guidelines.md>"
      }
    }
    ```

2. **Launch agent** using the Agent tool with:
    - `subagent_type`: `"conductor:track-context-researcher"`
    - `prompt`: The JSON input above
    - `model`: `"haiku"` (cost-efficient for context gathering)

3. **Parse the agent's JSON response** and use it to inform:
    - Context-aware questions in Step 1.4
    - Relevant file references in the spec
    - Pattern adherence in the plan

4. **Fallback (ONLY if the Agent tool call returns an error):** Read project files directly:
    - Read **Product Definition**, **Tech Stack**, **Workflow**, **Product Guidelines** via Universal File Resolution Protocol
    - Reference `conductor/docs/` and `conductor/product-guidelines.md` for established codebase patterns

</instructions>

</phase>

---

<phase name="spec_generation">

## 1.4 INTERACTIVE SPECIFICATION GENERATION

<instructions>

**Pattern Examples:** See the patterns documented in `<protocol name="askuserquestion">` and `templates/askuserquestion-patterns.md` for full JSON examples.

1. **Announce Goal:** "I'll now guide you through questions to build a specification for this track."

2. **Questioning Phase:**
    - Ask questions **sequentially** using AskUserQuestion tool, following the constraints in `<protocol name="askuserquestion">`
    - Incorporate suggested questions from the context research agent (Step 1.3) where relevant
    - Refer to **Product Definition**, **Tech Stack** for context-aware questions
    - Always include "Auto-generate" as the last option
    - **FEATURE:** Ask 3-5 questions (interaction type, capabilities, data flow)
    - **BUG/OTHER:** Ask 2-3 questions (reproduction steps, success criteria)

3. **Compose `spec.md` content** (hold in context — do NOT write files yet):
    Include: Overview, Background, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Out of Scope

4. **Present draft inline** for the user to see. Do NOT use a formal Approval prompt here — the spec will be formally reviewed together with the plan via ExitPlanMode in Step 1.7. If the user volunteers feedback at this point, incorporate it before proceeding.

</instructions>

</phase>

---

<phase name="plan_generation">

## 1.5 INTERACTIVE PLAN GENERATION

<instructions>

1. **Announce Goal:** "Now I will create an implementation plan based on the specification."

2. **Compose `plan.md` content** (hold in context — do NOT write files yet):
    - Use confirmed spec content, **Workflow** file, and context research results
    - Generate hierarchical structure: Phases → Tasks → Sub-tasks
    - Include status markers `[ ]` for every task
    - **CRITICAL:** Adhere to **Workflow** methodology (TDD structure)
    - **CRITICAL:** Append verification task to each phase: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

3. **Present draft inline** for the user to see. Do NOT use a formal Approval prompt here — the plan will be formally reviewed together with the spec via ExitPlanMode in Step 1.7. If the user volunteers feedback at this point, incorporate it before proceeding.

</instructions>

</phase>

---

<phase name="write_plan_file">

## 1.7 WRITE TO CC PLAN FILE AND EXIT PLAN MODE

<instructions>

**This is the single formal approval gate for all composed content.**

1. **Compose the CC plan file** using the format defined in `<protocol name="cc_plan_file">`, combining:
    - Track configuration (type, branch name)
    - Composed spec content
    - Composed plan content
    - Execution preview

2. **Call `ExitPlanMode`** with the composed content as the plan.

<note type="critical">
**How to interpret the ExitPlanMode result:**
- After calling `ExitPlanMode`, the system will clear prior context and return a system reminder containing "Exited Plan Mode". This is **SUCCESS** — the user approved the plan.
- Do NOT interpret context clearing or the system reminder as a rejection or failure.
- Do NOT ask what to do next, offer retry options, or request additional feedback.
- **Read the CC plan file** at the path provided in the system reminder. The plan file contains the "Phase B — Execution Steps" section with all commands to run in order.
- **Follow those Phase B steps exactly** — they include creating the branch, scaffolding, writing files, registering, committing, and invoking `conductor:implement` via the Skill tool.
- Do NOT skip steps or implement the track yourself.
</note>

3. **If `ExitPlanMode` tool call itself errors** (tool not found, permission denied), instruct the user:
    > "Please press `Shift+Tab` to exit Plan Mode, then tell me to continue."
    When the user confirms, proceed immediately to Phase B.

</instructions>

</phase>

---

# PHASE B — NORMAL MODE (writes enabled, after user approval)

<phase name="create_branch">

## 2.1 CREATE GIT BRANCH

<instructions>

**PROTOCOL: Follow the Git Isolation Protocol in `protocols/git-isolation.md`.**

Use the branch name decided in Step 1.2. The branch name and prefix were already determined during Phase A — now execute the creation:

1. **Create and switch to the branch:** `git checkout -b <branch_name>`
2. If the branch already exists, ask the user whether to switch to it or choose a different name

<note>
**Note for newTrack:** Since the `track_id` does not exist yet, the branch name was derived from the track description in Step 1.2.
</note>

</instructions>

</phase>

---

<phase name="generate_and_scaffold">

## 2.2 GENERATE TRACK ID AND CREATE FILES

<instructions>

**PROTOCOL: Use the CLI commands defined in `<cli_reference>`.**

| Step | Action | Fallback |
|------|--------|----------|
| 1. Generate ID | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack generate-id "DESC"` | Manual: `shortname_YYYYMMDD` |
| 2. Create directory | `mkdir -p conductor/tracks/<TRACK_ID>` | — |

Then **Write all 5 track files directly** (no scaffold — avoids overwrite conflicts):

1. **Read back the approved content** from conversation context (or from the CC plan file if context was cleared)
2. **Write `spec.md`**: approved spec content
3. **Write `plan.md`**: approved plan content
4. **Write `index.md`**: track index with links to spec, plan, decisions, metadata
5. **Write `decisions.md`**: empty ADR template (read from `templates/decisions.md` if it exists, otherwise minimal template)
6. **Write `metadata.json`**: `{"track_id": "<ID>", "type": "<type>", "status": "pending", "description": "<desc>", "created_at": "<ISO>", "updated_at": "<ISO>"}`

</instructions>

</phase>

---

<phase name="register">

## 2.4 REGISTER TRACK

<instructions>

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json newtrack register TRACK_ID --description "DESC"
```

**Fallback:** Edit `conductor/tracks/<track_id>/metadata.json` directly if CLI fails.

</instructions>

</phase>

---

<phase name="commit">

## 2.5 COMMIT AND FINALIZE

<instructions>

1. **Confirm Commit:** Use AskUserQuestion with Commit pattern (Commit now/Skip commit), following constraints in `<protocol name="askuserquestion">`
2. **Stage metadata.json first** (per project feedback — metadata must be staged before committing):
   ```bash
   git add conductor/tracks/<track_id>/metadata.json
   git add conductor/tracks/<track_id>/*
   ```
3. **Commit (if confirmed):** Use commit type matching the track type:

   | Track Type | Commit Prefix |
   |------------|---------------|
   | feature    | feat          |
   | bugfix     | fix           |
   | refactor   | refactor      |
   | docs       | docs          |
   | chore      | chore         |

   ```bash
   git commit -m "<prefix>(conductor): Create track '<description>'"
   ```
4. **Announce:** Inform user track is created.
5. **Invoke implementation:** Call the Skill tool with `skill: "conductor:implement", args: "<TRACK_ID>"` to begin implementing the track. Do NOT attempt to implement the track yourself — the `conductor:implement` skill has its own protocol, CLI commands, and workflow that must be followed.

</instructions>

</phase>
