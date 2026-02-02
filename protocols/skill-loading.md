# Skill Loading Protocol

**Version:** 1.0.0
**Purpose:** Activate relevant skills during implementation based on task context
**Scope:** Conductor commands, task execution workflow

---

## Overview

This protocol defines how to identify and load relevant skills from the Skill Registry. Skills provide domain-specific guidance, patterns, and protocols that enhance implementation quality.

---

## 1. Load Skill Registry

Read `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json` to get the list of available skills with their manifests.

**Registry Structure:**
```json
{
  "version": "1.0.0",
  "skills": [
    {
      "name": "conductor-methodology",
      "version": "1.0.0",
      "path": "./conductor-methodology",
      "description": "Core development methodology",
      "activation": {
        "always_active": true,
        "keywords": ["conductor", "track", "plan"],
        "file_patterns": ["conductor/**/*"],
        "tech_stack": {}
      },
      "provides": {
        "guidance": ["conductor-concepts", "track-lifecycle"]
      }
    }
  ]
}
```

---

## 2. Check Project Settings

Before loading skills, check for project-level skill configuration:

1. Read `conductor/settings.json` if it exists
2. Check the `disabledSkills` array for skills that are disabled
3. Exclude disabled skills from activation (except always-active skills)

**Settings Structure:**
```json
{
  "version": "1.0.0",
  "disabledSkills": ["./api-design", "./testing-strategies"]
}
```

---

## 3. Validate Skill Manifests

For each skill in the registry, validate the manifest before processing:

**Required Fields:**
- `name`: Non-empty string
- `version`: Valid semver (X.Y.Z)
- `path`: Valid relative path starting with `./`
- `description`: Non-empty string

**Validation Rules:**
1. Skip skills with missing required fields (log warning)
2. Skip skills where `SKILL.md` file doesn't exist (log warning)
3. Skip skills with malformed activation rules (log warning)
4. Continue processing valid skills

**Error Handling:**
```
⚠️ Skipping skill '<name>': Missing required field 'version'
⚠️ Skipping skill '<name>': SKILL.md not found at <path>
```

---

## 4. Identify Always-Active Skills

Load all skills with `activation.always_active: true` immediately. These skills provide foundational guidance that applies to all tasks.

**Always-Active Loading:**
1. Check if `summary_available: true` in skill manifest
2. If summary available: Read `SKILL-SUMMARY.md` instead of full `SKILL.md`
3. If no summary: Read the skill's `SKILL.md` file from its path
4. Add skill guidance to implementation context
5. Mark skill as loaded (no score needed)
6. Always-active skills CANNOT be disabled via settings

**Summary Loading Rationale:** Summaries (~40 lines) provide essential concepts for context without the full detail (~280 lines). Full skill is loaded on-demand when detailed guidance is needed.

---

## 5. Resolve Dependencies

Before scoring remaining skills, resolve any dependencies:

1. For each skill, check its `dependencies` array
2. If a skill depends on another skill, the dependency must be loaded first
3. If a dependency is missing or disabled, log warning and skip the dependent skill

**Dependency Resolution Order:**
1. Build dependency graph from all potentially-activatable skills
2. Detect circular dependencies (skip all skills in cycle with warning)
3. Load skills in topological order (dependencies before dependents)

**Example:**
```
Skill A depends on [B, C]
Skill B depends on [C]
Skill C has no dependencies

Load order: C → B → A
```

---

## 6. Score Remaining Skills

For each non-always-active skill (not disabled, dependencies resolved), calculate activation score.

### 6.1 Keyword Extraction from Task

From the current task description:
1. **Tokenize**: Split into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter**: Remove stop words (a, an, the, in, on, for, with, is, are, etc.)
4. **Match**: Compare against skill's `activation.keywords`

### 6.2 File Pattern Matching

1. Get list of files to be modified in task (from plan or context)
2. Match against skill's `activation.file_patterns` globs
3. Any matching file contributes to score

### 6.3 Tech Stack Matching

1. Read project's detected stack from `conductor/tech-stack.md`
2. Match against skill's `activation.tech_stack` requirements:
   - `languages`: Array of language identifiers (e.g., `["typescript", "python"]`)
   - `frameworks`: Array of framework names (e.g., `["react", "nextjs"]`)
   - `tools`: Array of tool names (e.g., `["docker", "kubernetes"]`)

### 6.4 Scoring Table

| Match Type | Condition | Score |
|------------|-----------|-------|
| **Keyword match** | Task keyword matches activation keyword | +1.0 |
| **File pattern** | Modified file matches skill's file_pattern | +1.5 |
| **Language match** | Project language matches skill's tech_stack.languages | +2.0 |
| **Framework match** | Project framework matches skill's tech_stack.frameworks | +1.5 |
| **Tool match** | Project tool matches skill's tech_stack.tools | +1.0 |

---

## 7. Activation Decision

| Total Score | Action |
|-------------|--------|
| **>= 3.0** | Activate with high confidence |
| **1.5 - 2.9** | Activate with medium confidence |
| **< 1.5** | Do not activate |

**Constraints:**
- Maximum 5 skills per task (excluding always-active)
- Sort by score descending
- If no skills score >= 1.5, continue with only always-active skills

---

## 8. Skill Loading Priority

When multiple skills could apply, use this priority order:

1. **Always-active skills**: Loaded first, regardless of score
2. **Dependency order**: Skills load after their dependencies
3. **Score (descending)**: Higher scoring skills take priority
4. **Match specificity**:
   - File pattern matches > Tech stack matches > Keyword matches
   - Language + Framework match > Single match
5. **Limit enforcement**: If more than 5 scored skills qualify, take top 5

**Conflict Resolution:**
- If two skills provide conflicting guidance, the higher-scoring skill takes precedence
- If scores are equal, the skill listed first in the registry wins
- Skills should be designed to complement, not conflict

---

## 9. Load Skill Context

For each activated skill:
1. Read the skill's `SKILL.md` file from `<skill_path>/SKILL.md`
2. Parse YAML frontmatter for metadata
3. Add skill guidance to implementation context
4. Track which skills are active for the current task

---

## 10. Skill Announcement Format

When skills are activated, announce at the start of task execution:

```
🔧 **Skills Activated:**

1. **conductor-methodology** (always active)
   > Core methodology guidance for TDD and verification protocols

2. **typescript-best-practices** (score: 3.5)
   > Type safety, async patterns, and null handling guidance

[Proceed with implementation using activated skills]
```

**Announcement Rules:**
- List always-active skills first
- Show score for scored skills
- Include brief description from skill manifest
- Do not announce if only always-active skills are loaded (keep output clean)

---

## 11. Error Handling

**Registry Errors:**
- **Registry missing**: Log warning, continue without skill loading
- **Registry malformed**: Log error with details, continue without skills

**Skill Errors:**
- **Skill file missing**: Log warning, skip skill, continue with others
- **Invalid manifest**: Skip skill with warning, continue with others
- **SKILL.md parse error**: Skip skill with warning, continue with others

**Dependency Errors:**
- **Missing dependency**: Skip dependent skill with warning
- **Circular dependency**: Skip all skills in cycle with warning
- **Disabled dependency**: Skip dependent skill (dependency requirement not met)

**Error Format:**
```
⚠️ Skill Loading Warning: <message>
   Skill: <skill-name>
   Reason: <detailed reason>
   Action: Skipping skill, continuing with others
```

---

## Default Paths

- **Skill Registry**: `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json`
- **Skill Directory**: `${CLAUDE_PLUGIN_ROOT}/skills/`
- **Skill Definition**: `${CLAUDE_PLUGIN_ROOT}/skills/<skill_id>/SKILL.md`
- **Skill Manifest**: `${CLAUDE_PLUGIN_ROOT}/skills/<skill_id>/manifest.json`
- **Project Settings**: `conductor/settings.json` (project file, not plugin file)
