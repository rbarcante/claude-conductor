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

For each pattern in `patterns/index.md`:
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

1. **[Pattern Name]** (patterns/core/<name>.md)
   > <Pattern's one-line description from header>

[Apply patterns? (Y)es / (S)kip / (V)iew first]
```

### 5. Fallback Behavior

- **No matches**: Continue with task execution silently
- **Pattern file missing**: Log warning, skip pattern, continue with others
- **Pattern missing activation section**: Skip pattern (not activatable)
- **User skips patterns**: Proceed without applying patterns

### Default Paths (Patterns)
- **Pattern Registry**: `patterns/index.md`
- **Core Patterns**: `patterns/core/`
- **Stack Patterns**: `patterns/stack/` (future)
- **Pattern Template**: `patterns/TEMPLATE.md`

## Skill Loading Protocol

**PROTOCOL: How to activate relevant skills during implementation.**

When beginning a task, follow this protocol to identify and load relevant skills from the Skill Registry. Skills provide domain-specific guidance, patterns, and protocols that enhance implementation quality.

### 1. Load Skill Registry

Read `skills/skill-registry.json` to get the list of available skills with their manifests.

**Registry Structure:**
```json
{
  "version": "1.0.0",
  "skills": [
    {
      "id": "conductor-methodology",
      "name": "Conductor Methodology",
      "path": "skills/conductor-methodology",
      "activation": {
        "always_active": true,
        "keywords": ["conductor", "track", "plan"],
        "file_patterns": ["conductor/**/*"],
        "tech_stack": {}
      }
    }
  ]
}
```

### 2. Identify Always-Active Skills

Load all skills with `activation.always_active: true` immediately. These skills provide foundational guidance that applies to all tasks.

**Always-Active Loading:**
1. Read the skill's `SKILL.md` file from its path
2. Add skill guidance to implementation context
3. Mark skill as loaded (no score needed)

### 3. Score Remaining Skills

For each non-always-active skill, calculate activation score based on task context.

**3.1 Keyword Extraction from Task**

From the current task description:
1. **Tokenize**: Split into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter**: Remove stop words (a, an, the, in, on, for, with, is, are, etc.)
4. **Match**: Compare against skill's `activation.keywords`

**3.2 File Pattern Matching**

1. Get list of files to be modified in task (from plan or context)
2. Match against skill's `activation.file_patterns` globs
3. Any matching file contributes to score

**3.3 Tech Stack Matching**

1. Read project's detected stack from `conductor/tech-stack.md`
2. Match against skill's `activation.tech_stack` requirements:
   - `languages`: Array of language identifiers (e.g., `["typescript", "python"]`)
   - `frameworks`: Array of framework names (e.g., `["react", "nextjs"]`)
   - `tools`: Array of tool names (e.g., `["docker", "kubernetes"]`)

**3.4 Scoring Table**

| Match Type | Condition | Score |
|------------|-----------|-------|
| **Keyword match** | Task keyword matches activation keyword | +1.0 |
| **File pattern** | Modified file matches skill's file_pattern | +1.5 |
| **Language match** | Project language matches skill's tech_stack.languages | +2.0 |
| **Framework match** | Project framework matches skill's tech_stack.frameworks | +1.5 |
| **Tool match** | Project tool matches skill's tech_stack.tools | +1.0 |

### 4. Activation Decision

| Total Score | Action |
|-------------|--------|
| **>= 3.0** | Activate with high confidence |
| **1.5 - 2.9** | Activate with medium confidence |
| **< 1.5** | Do not activate |

**Constraints:**
- Maximum 5 skills per task (excluding always-active)
- Sort by score descending
- If no skills score >= 1.5, continue with only always-active skills

### 5. Conflict Resolution

When multiple skills could apply:

1. **Always-active first**: Skills with `always_active: true` are loaded before scored skills
2. **Higher score wins**: Among scored skills, higher scores take priority
3. **Explicit over implicit**: Skills matching file patterns take priority over keyword-only matches
4. **Tech stack specificity**: Skills matching both language AND framework score higher than single matches
5. **Limit enforcement**: If more than 5 scored skills qualify, take top 5 by score

### 6. Load Skill Context

For each activated skill:
1. Read the skill's `SKILL.md` file from `<skill_path>/SKILL.md`
2. Parse YAML frontmatter for metadata
3. Add skill guidance to implementation context
4. Track which skills are active for the current task

### 7. Skill Announcement Format

When skills are activated, announce at the start of task execution:

```
🔧 **Skills Activated:**

1. **Conductor Methodology** (always active)
   > Core methodology guidance for TDD and verification protocols

2. **React Best Practices** (score: 3.5)
   > Component patterns, hooks usage, and state management guidance

[Proceed with implementation using activated skills]
```

**Announcement Rules:**
- List always-active skills first
- Show score for scored skills
- Include brief description from skill manifest
- Do not announce if only always-active skills are loaded (keep output clean)

### 8. Fallback Behavior

- **Registry missing**: Log warning, continue without skill loading
- **Skill file missing**: Log warning, skip skill, continue with others
- **No matches**: Continue with only always-active skills (no announcement)
- **Invalid manifest**: Skip skill with warning, continue with others

### Default Paths (Skills)
- **Skill Registry**: `skills/skill-registry.json`
- **Skill Directory**: `skills/`
- **Skill Definition**: `skills/<skill_id>/SKILL.md`
- **Skill Manifest**: `skills/<skill_id>/manifest.json` (optional, embedded in registry)
