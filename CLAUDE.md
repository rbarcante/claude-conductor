# Conductor Context

If a user mentions a "plan" or asks about the plan, and they have used the conductor plugin in the current session, they are likely referring to the `conductor/tracks.md` file or one of the track plans (`conductor/tracks/<track_id>/plan.md`).

## Universal File Resolution Protocol

**PROTOCOL: How to locate files.**
To find a file (e.g., "**Product Definition**") within a specific context (Project Root or a specific Track):

1.  **Identify Index:** Determine the relevant index file:
    -   **Project Context:** `conductor/index.md`
    -   **Track Context:**
        a. Resolve and read the **Tracks Registry** (via Project Context).
        b. Find the entry for the specific `<track_id>`.
        c. Follow the link provided in the registry to locate the track's folder. The index file is `<track_folder>/index.md`.
        d. **Fallback:** If the track is not yet registered (e.g., during creation) or the link is broken:
            1. Resolve the **Tracks Directory** (via Project Context).
            2. The index file is `<Tracks Directory>/<track_id>/index.md`.

2.  **Check Index:** Read the index file and look for a link with a matching or semantically similar label.

3.  **Resolve Path:** If a link is found, resolve its path **relative to the directory containing the `index.md` file**.
    -   *Example:* If `conductor/index.md` links to `./workflow.md`, the full path is `conductor/workflow.md`.

4.  **Fallback:** If the index file is missing or the link is absent, use the **Default Path** keys below.

5.  **Verify:** You MUST verify the resolved file actually exists on the disk.

**Standard Default Paths (Project):**
- **Product Definition**: `conductor/product.md`
- **Tech Stack**: `conductor/tech-stack.md`
- **Workflow**: `conductor/workflow.md`
- **Product Guidelines**: `conductor/product-guidelines.md`
- **Tracks Registry**: `conductor/tracks.md`
- **Tracks Directory**: `conductor/tracks/`

**Standard Default Paths (Track):**
- **Specification**: `conductor/tracks/<track_id>/spec.md`
- **Implementation Plan**: `conductor/tracks/<track_id>/plan.md`
- **Metadata**: `conductor/tracks/<track_id>/metadata.json`

## Pattern Resolution Protocol

**PROTOCOL: How to surface relevant patterns during implementation.**

When beginning a task, follow this protocol to identify and surface relevant patterns from the Pattern Reference Layer.

### 1. Keyword Extraction

From the current task description:
1. **Tokenize**: Split into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter**: Remove stop words (a, an, the, in, on, for, with, is, are, etc.)
4. **Stem** (optional): Reduce to root form (e.g., "handling" → "handle")

### 2. Pattern Matching

For each pattern in `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`:
1. Read the pattern's `activation.keywords` from YAML frontmatter
2. Read the pattern's `activation.file_patterns` from YAML frontmatter
3. Calculate match score:

| Match Type | Condition | Score |
|------------|-----------|-------|
| **Exact keyword** | Extracted keyword equals activation keyword | +1.0 |
| **Stem match** | Extracted keyword stem matches activation keyword | +0.8 |
| **Partial match** | Keyword contains or is contained by activation keyword | +0.5 |
| **File pattern** | Any modified file matches a pattern's file_pattern | +1.5 |

### 3. Surfacing Decision

| Total Score | Action |
|-------------|--------|
| **>= 2.0** | Surface pattern with high confidence |
| **1.0 - 1.9** | Surface pattern with moderate confidence |
| **0.5 - 0.9** | Do not surface, but pattern available via search |
| **< 0.5** | No match, ignore pattern |

**Constraints:**
- Surface maximum 3 patterns per task
- Sort by score descending
- If no patterns score >= 1.0, continue silently (no announcement)

### 4. Surfacing Format

When patterns match (score >= 1.0), announce:

```
📚 **Relevant Patterns Detected:**

1. **[Pattern Name]** (${CLAUDE_PLUGIN_ROOT}/patterns/core/<name>.md)
   > <Pattern's one-line description from header>

[Apply patterns? (Y)es / (S)kip / (V)iew first]
```

### 5. Fallback Behavior

- **No matches**: Continue with task execution silently
- **Pattern file missing**: Log warning, skip pattern, continue with others
- **Pattern missing activation section**: Skip pattern (not activatable)
- **User skips patterns**: Proceed without applying patterns

### Default Paths (Patterns)
- **Pattern Registry**: `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`
- **Core Patterns**: `${CLAUDE_PLUGIN_ROOT}/patterns/core/`
- **Stack Patterns**: `${CLAUDE_PLUGIN_ROOT}/patterns/stack/` (future)
- **Pattern Template**: `${CLAUDE_PLUGIN_ROOT}/patterns/TEMPLATE.md`

## Skill Loading Protocol

**PROTOCOL: How to activate relevant skills during implementation.**

When beginning a task, follow this protocol to identify and load relevant skills from the Skill Registry. Skills provide domain-specific guidance, patterns, and protocols that enhance implementation quality.

### 1. Load Skill Registry

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

### 2. Check Project Settings

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

### 3. Validate Skill Manifests

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

### 4. Identify Always-Active Skills

Load all skills with `activation.always_active: true` immediately. These skills provide foundational guidance that applies to all tasks.

**Always-Active Loading:**
1. Read the skill's `SKILL.md` file from its path
2. Add skill guidance to implementation context
3. Mark skill as loaded (no score needed)
4. Always-active skills CANNOT be disabled via settings

### 5. Resolve Dependencies

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

### 6. Score Remaining Skills

For each non-always-active skill (not disabled, dependencies resolved), calculate activation score.

**6.1 Keyword Extraction from Task**

From the current task description:
1. **Tokenize**: Split into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter**: Remove stop words (a, an, the, in, on, for, with, is, are, etc.)
4. **Match**: Compare against skill's `activation.keywords`

**6.2 File Pattern Matching**

1. Get list of files to be modified in task (from plan or context)
2. Match against skill's `activation.file_patterns` globs
3. Any matching file contributes to score

**6.3 Tech Stack Matching**

1. Read project's detected stack from `conductor/tech-stack.md`
2. Match against skill's `activation.tech_stack` requirements:
   - `languages`: Array of language identifiers (e.g., `["typescript", "python"]`)
   - `frameworks`: Array of framework names (e.g., `["react", "nextjs"]`)
   - `tools`: Array of tool names (e.g., `["docker", "kubernetes"]`)

**6.4 Scoring Table**

| Match Type | Condition | Score |
|------------|-----------|-------|
| **Keyword match** | Task keyword matches activation keyword | +1.0 |
| **File pattern** | Modified file matches skill's file_pattern | +1.5 |
| **Language match** | Project language matches skill's tech_stack.languages | +2.0 |
| **Framework match** | Project framework matches skill's tech_stack.frameworks | +1.5 |
| **Tool match** | Project tool matches skill's tech_stack.tools | +1.0 |

### 7. Activation Decision

| Total Score | Action |
|-------------|--------|
| **>= 3.0** | Activate with high confidence |
| **1.5 - 2.9** | Activate with medium confidence |
| **< 1.5** | Do not activate |

**Constraints:**
- Maximum 5 skills per task (excluding always-active)
- Sort by score descending
- If no skills score >= 1.5, continue with only always-active skills

### 8. Skill Loading Priority

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

### 9. Load Skill Context

For each activated skill:
1. Read the skill's `SKILL.md` file from `<skill_path>/SKILL.md`
2. Parse YAML frontmatter for metadata
3. Add skill guidance to implementation context
4. Track which skills are active for the current task

### 10. Skill Announcement Format

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

### 11. Error Handling

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

### Default Paths (Skills)
- **Skill Registry**: `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json`
- **Skill Directory**: `${CLAUDE_PLUGIN_ROOT}/skills/`
- **Skill Definition**: `${CLAUDE_PLUGIN_ROOT}/skills/<skill_id>/SKILL.md`
- **Skill Manifest**: `${CLAUDE_PLUGIN_ROOT}/skills/<skill_id>/manifest.json`
- **Project Settings**: `conductor/settings.json` (project file, not plugin file)
