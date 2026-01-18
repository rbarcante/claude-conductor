---
name: conductor:skills
description: Manage and explore Conductor skills
argument-hint: "[list|info <skill>|enable <skill>|disable <skill>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to help users manage and explore skills in the Conductor ecosystem. This includes listing available skills, viewing skill details, and enabling/disabling skills for the current project.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the skill ecosystem exists.**

1.  **Verify Skill Registry:** Check for the existence of `skills/skill-registry.json`.

2.  **Handle Failure:**
    -   If the file is missing, announce: "Skill registry not found. The skills/skill-registry.json file is missing."
    -   Do NOT proceed to command execution.

---

## 2.0 COMMAND ROUTING
**PROTOCOL: Parse user input and route to appropriate subcommand.**

1.  **Parse Arguments:** Examine `{{args}}` to determine the subcommand:
    -   If `{{args}}` is empty or equals "list" → Execute **LIST PROTOCOL**
    -   If `{{args}}` starts with "info " → Extract skill name and execute **INFO PROTOCOL**
    -   If `{{args}}` starts with "enable " → Extract skill name and execute **ENABLE PROTOCOL**
    -   If `{{args}}` starts with "disable " → Extract skill name and execute **DISABLE PROTOCOL**
    -   Otherwise → Show usage help

2.  **Usage Help:** If arguments don't match any subcommand:
    ```
    **Usage:** /conductor:skills [subcommand]

    **Subcommands:**
    - `list` - List all available skills (default)
    - `info <skill>` - Show detailed information about a skill
    - `enable <skill>` - Enable a skill for the current project
    - `disable <skill>` - Disable a skill for the current project

    **Examples:**
    - /conductor:skills list
    - /conductor:skills info typescript-best-practices
    - /conductor:skills enable api-design
    - /conductor:skills disable testing-strategies
    ```

---

## 3.0 LIST PROTOCOL
**PROTOCOL: Display all available skills with their status.**

1.  **Read Registry:** Read and parse `skills/skill-registry.json`.

2.  **Read Project Settings:** Check if `conductor/settings.json` exists.
    -   If it exists, read and parse it to get the `disabledSkills` array.
    -   If it doesn't exist, assume no skills are disabled.

3.  **Build Skills Table:** For each skill in the registry:
    -   **Name:** From `skill.name`
    -   **Version:** From `skill.version`
    -   **Status:**
        -   "Always Active" if `skill.activation.always_active` is true
        -   "Disabled" if skill path is in `disabledSkills` array
        -   "Available" otherwise
    -   **Description:** From `skill.description`

4.  **Format Output:**
    ```
    🔧 **Available Skills**

    | Skill | Version | Status | Description |
    |-------|---------|--------|-------------|
    | conductor-methodology | 1.0.0 | Always Active | Core development methodology |
    | typescript-best-practices | 1.0.0 | Available | Type safety and async patterns |
    | api-design | 1.0.0 | Disabled | REST conventions and error handling |
    | ... | ... | ... | ... |

    **Total:** X skills available

    💡 Use `/conductor:skills info <skill-name>` to view details.
    💡 Use `/conductor:skills enable <skill>` or `disable <skill>` to manage skills.
    ```

---

## 4.0 INFO PROTOCOL
**PROTOCOL: Display detailed information about a specific skill.**

1.  **Extract Skill Name:** Get the skill identifier from `{{args}}` (everything after "info ").

2.  **Normalize Name:** Convert to lowercase, replace spaces with hyphens.

3.  **Find Skill in Registry:**
    -   Read `skills/skill-registry.json`
    -   Search for a skill where the path ends with the normalized name OR where the name matches (case-insensitive)
    -   If not found, execute **SKILL NOT FOUND** protocol

4.  **Read Skill Files:**
    -   Read the skill's `manifest.json` from `skills/<skill-path>/manifest.json`
    -   If `manifest.json` doesn't exist, use the registry entry data
    -   Read the skill's `SKILL.md` from `skills/<skill-path>/SKILL.md` (if exists)

5.  **Check Project Status:**
    -   Read `conductor/settings.json` if it exists
    -   Determine if skill is enabled or disabled for current project

6.  **Format Output:**
    ```
    📦 **Skill: <Skill Name>**
    *Version: <version> | Status: <Enabled/Disabled/Always Active>*

    ---

    **Description:**
    <skill description>

    ---

    **Activation Rules:**
    - **Keywords:** <comma-separated keywords or "None">
    - **File Patterns:** <comma-separated patterns or "None">
    - **Tech Stack:**
      - Languages: <languages or "Any">
      - Frameworks: <frameworks or "Any">
    - **Always Active:** <Yes/No>

    ---

    **Provides:**
    - **Guidance:** <topics or "None">
    - **Patterns:** <pattern IDs or "None">
    - **Templates:** <template paths or "None">
    - **Protocols:** <protocol IDs or "None">

    ---

    **Dependencies:** <skill dependencies or "None">

    ---

    **Skill File:** `skills/<skill-path>/SKILL.md`

    💡 Use `/conductor:skills enable <skill>` to enable this skill.
    ```

7.  **Skill Not Found:** If skill cannot be resolved:
    ```
    ❌ **Skill Not Found:** "<skill-name>"

    Available skills:
    - conductor-methodology
    - typescript-best-practices
    - api-design
    - testing-strategies

    💡 Use `/conductor:skills list` to see all available skills.
    ```

---

## 5.0 ENABLE PROTOCOL
**PROTOCOL: Enable a skill for the current project.**

1.  **Extract Skill Name:** Get the skill identifier from `{{args}}` (everything after "enable ").

2.  **Verify Skill Exists:**
    -   Read `skills/skill-registry.json`
    -   Find the skill by name or path
    -   If not found, execute **SKILL NOT FOUND** protocol from INFO PROTOCOL

3.  **Check if Already Active:**
    -   If `skill.activation.always_active` is true:
        ```
        ℹ️ **<Skill Name>** is always active and cannot be enabled/disabled.
        ```
    -   Return without changes

4.  **Load Project Settings:**
    -   Check if `conductor/settings.json` exists
    -   If it doesn't exist, create it with default structure:
        ```json
        {
          "version": "1.0.0",
          "disabledSkills": []
        }
        ```

5.  **Update Settings:**
    -   Remove the skill path from `disabledSkills` array if present
    -   Write updated settings to `conductor/settings.json`

6.  **Confirm Success:**
    ```
    ✅ **Enabled:** <Skill Name>

    The skill will now activate based on its activation rules:
    - Keywords: <keywords>
    - File Patterns: <patterns>
    - Tech Stack: <requirements>

    💡 The skill will be loaded during `/conductor:implement` when context matches.
    ```

---

## 6.0 DISABLE PROTOCOL
**PROTOCOL: Disable a skill for the current project.**

1.  **Extract Skill Name:** Get the skill identifier from `{{args}}` (everything after "disable ").

2.  **Verify Skill Exists:**
    -   Read `skills/skill-registry.json`
    -   Find the skill by name or path
    -   If not found, execute **SKILL NOT FOUND** protocol from INFO PROTOCOL

3.  **Check if Always Active:**
    -   If `skill.activation.always_active` is true:
        ```
        ⚠️ **<Skill Name>** is always active and cannot be disabled.

        Always-active skills provide core functionality and are loaded for every task.
        ```
    -   Return without changes

4.  **Load Project Settings:**
    -   Check if `conductor/settings.json` exists
    -   If it doesn't exist, create it with default structure:
        ```json
        {
          "version": "1.0.0",
          "disabledSkills": []
        }
        ```

5.  **Update Settings:**
    -   Add the skill path to `disabledSkills` array if not already present
    -   Write updated settings to `conductor/settings.json`

6.  **Confirm Success:**
    ```
    ✅ **Disabled:** <Skill Name>

    The skill will no longer activate for this project.

    💡 Use `/conductor:skills enable <skill>` to re-enable.
    ```

---

## 7.0 SETTINGS FILE FORMAT
**Reference: Structure of conductor/settings.json**

```json
{
  "version": "1.0.0",
  "disabledSkills": [
    "./typescript-best-practices",
    "./api-design"
  ]
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Settings schema version |
| `disabledSkills` | array | Skill paths that are disabled for this project |

### Behavior

- Skills not in `disabledSkills` are considered enabled
- Always-active skills cannot be added to `disabledSkills`
- Skill paths must match the `path` field from skill-registry.json
