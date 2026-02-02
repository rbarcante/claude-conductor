# Conductor Context

If a user mentions a "plan" or asks about the plan, and they have used the claude conductor in the current session, they are likely referring to the `conductor/tracks.md` file or one of the track plans (`conductor/tracks/<track_id>/plan.md`).

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

**Full Protocol Reference:** `protocols/pattern-resolution.md`

### Quick Reference

1. **Extract keywords** from task description (tokenize, normalize, filter stop words)
2. **Match patterns** from `${CLAUDE_PLUGIN_ROOT}/patterns/index.md` using activation keywords and file patterns
3. **Score patterns:** Exact keyword (+1.0), Stem match (+0.8), Partial (+0.5), File pattern (+1.5)
4. **Surface** patterns scoring >= 1.0 (max 3, sorted by score)
5. **Announce** with format: `📚 Relevant Patterns Detected:` and options (Y/S/V)

### Default Paths (Patterns)
- **Pattern Registry**: `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`
- **Core Patterns**: `${CLAUDE_PLUGIN_ROOT}/patterns/core/`

## Skill Loading Protocol

**PROTOCOL: How to activate relevant skills during implementation.**

**Full Protocol Reference:** `protocols/skill-loading.md`

### Quick Reference

1. **Load registry** from `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json`
2. **Check settings** in `conductor/settings.json` for disabled skills
3. **Load always-active** skills immediately (cannot be disabled)
4. **Score remaining** skills using: keywords (+1.0), file patterns (+1.5), language (+2.0), framework (+1.5), tools (+1.0)
5. **Activate** skills scoring >= 1.5 (max 5, sorted by score)
6. **Announce** activated skills at task start

### Activation Thresholds

| Score | Action |
|-------|--------|
| >= 3.0 | Activate (high confidence) |
| 1.5 - 2.9 | Activate (medium confidence) |
| < 1.5 | Do not activate |

### Default Paths (Skills)
- **Skill Registry**: `${CLAUDE_PLUGIN_ROOT}/skills/skill-registry.json`
- **Skill Definition**: `${CLAUDE_PLUGIN_ROOT}/skills/<skill_id>/SKILL.md`
- **Project Settings**: `conductor/settings.json`
