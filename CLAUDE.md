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
