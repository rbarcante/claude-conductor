# Pattern Resolution Protocol

**Version:** 1.0.0
**Purpose:** Surface relevant patterns during implementation based on task context
**Scope:** Conductor commands, task execution workflow

---

## Overview

This protocol defines how to identify and surface relevant patterns from the Pattern Reference Layer when beginning a task. Patterns provide proven implementation approaches that enhance code quality and consistency.

---

## 1. Keyword Extraction

From the current task description:
1. **Tokenize**: Split into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter**: Remove stop words (a, an, the, in, on, for, with, is, are, etc.)
4. **Stem** (optional): Reduce to root form (e.g., "handling" → "handle")

---

## 2. Pattern Matching

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

---

## 3. Surfacing Decision

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

---

## 4. Surfacing Format

When patterns match (score >= 1.0), announce:

```
📚 **Relevant Patterns Detected:**

1. **[Pattern Name]** (${CLAUDE_PLUGIN_ROOT}/patterns/core/<name>.md)
   > <Pattern's one-line description from header>

[Apply patterns? (Y)es / (S)kip / (V)iew first]
```

---

## 5. Fallback Behavior

- **No matches**: Continue with task execution silently
- **Pattern file missing**: Log warning, skip pattern, continue with others
- **Pattern missing activation section**: Skip pattern (not activatable)
- **User skips patterns**: Proceed without applying patterns

---

## Default Paths

- **Pattern Registry**: `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`
- **Core Patterns**: `${CLAUDE_PLUGIN_ROOT}/patterns/core/`
- **Stack Patterns**: `${CLAUDE_PLUGIN_ROOT}/patterns/stack/` (future)
- **Pattern Template**: `${CLAUDE_PLUGIN_ROOT}/patterns/TEMPLATE.md`
