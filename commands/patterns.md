---
name: conductor:patterns
description: Browse and search the Pattern Reference Layer
argument-hint: "[list|search <query>|show <pattern-name>]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to help users explore and retrieve patterns from the Pattern Reference Layer. This involves listing available patterns, searching for patterns by keyword, and displaying pattern content.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## CLI Operations
**PROTOCOL: Use the Python CLI for token-efficient pattern operations.**

The Python CLI (`${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns`) provides optimized commands for pattern operations:

| Subcommand | CLI Command | Description |
|------------|-------------|-------------|
| `list` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns list` | List all patterns with name, category, description, tags |
| `search` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns search "<query>"` | Full-text search with scored results |
| `show` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns show "<name>"` | Show detailed pattern information |
| `show --ai-only` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns show "<name>" --ai-only` | Show only AI Quick Reference section |

**CLI Output Format:**
- `patterns list`: Returns JSON array with `name`, `category`, `description`, `tags`, `activation_keywords`
- `patterns search`: Returns scored results sorted by relevance
- `patterns show`: Returns full pattern content with all sections
- `patterns show --ai-only`: Returns only the AI Quick Reference section

**When to Use CLI vs Manual:**
- **Use CLI (preferred):** For standard list, search, and show operations
- **Use Manual Fallback:** When CLI is unavailable or returns errors

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Pattern Reference Layer exists.**

1.  **Verify Pattern Registry:** Check for the existence of `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`.

2.  **Handle Failure:**
    -   If the file is missing, announce: "Pattern Reference Layer is not set up. The patterns/index.md file is missing."
    -   Do NOT proceed to command execution.

---

## 2.0 COMMAND ROUTING
**PROTOCOL: Parse user input and route to appropriate subcommand.**

1.  **Parse Arguments:** Examine `{{args}}` to determine the subcommand:
    -   If `{{args}}` is empty or equals "list" -> Execute **LIST PROTOCOL**
    -   If `{{args}}` starts with "search " -> Extract query and execute **SEARCH PROTOCOL**
    -   If `{{args}}` starts with "show " -> Extract pattern name and execute **SHOW PROTOCOL**
    -   Otherwise -> Show usage help

2.  **Usage Help:** If arguments don't match any subcommand:
    ```
    **Usage:** /conductor:patterns [subcommand]

    **Subcommands:**
    - `list` - List all available patterns (default)
    - `search <query>` - Search patterns by keyword
    - `show <pattern-name>` - Display a specific pattern

    **Examples:**
    - /conductor:patterns list
    - /conductor:patterns search error handling
    - /conductor:patterns show error-handling
    ```

---

## 3.0 LIST PROTOCOL
**PROTOCOL: Display all available patterns.**

### 3.1 Primary Method: CLI Command

1.  **Execute CLI:** Run the patterns list command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns list
    ```

2.  **Parse Output:** The CLI returns a formatted list of patterns with:
    - Pattern name
    - Category
    - Description
    - Tags
    - Activation keywords

3.  **Format Output:** Present patterns to user:
    ```
    **Available Patterns**

    | Pattern | Category | Description |
    |---------|----------|-------------|
    | error-handling | Resilience | Exception handling, error propagation |
    | logging | Observability | Log levels, structured logging |
    | ... | ... | ... |

    **Total:** X patterns available

    Use `/conductor:patterns show <pattern-name>` to view details.
    ```

### 3.2 Fallback Method: Manual Read

If the CLI command fails (exit code non-zero or command not found):

1.  **Read Registry:** Read the content of `${CLAUDE_PLUGIN_ROOT}/patterns/index.md`.

2.  **Parse Patterns:** Extract the pattern table from the "Core Patterns" section.

3.  **Format Output:** Present patterns in the same format as above.

---

## 4.0 SEARCH PROTOCOL
**PROTOCOL: Search patterns by keyword.**

### 4.1 Primary Method: CLI Command

1.  **Extract Query:** Get the search query from `{{args}}` (everything after "search ").

2.  **Execute CLI:** Run the patterns search command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns search "<query>"
    ```

3.  **Parse Output:** The CLI returns scored search results sorted by relevance, including:
    - Pattern name and path
    - Match score
    - Matched context (where the query was found)

4.  **Format Output:**
    ```
    **Search Results for "<query>"**

    **High Relevance:**
    1. **error-handling** (${CLAUDE_PLUGIN_ROOT}/patterns/core/error-handling.md)
       > Score: 2.5 - Matched: activation keyword, description

    **Medium Relevance:**
    2. **logging** (${CLAUDE_PLUGIN_ROOT}/patterns/core/logging.md)
       > Score: 1.2 - Matched: content

    **Total:** X patterns found

    Use `/conductor:patterns show <pattern-name>` to view details.
    ```

### 4.2 Fallback Method: Manual Search

If the CLI command fails (exit code non-zero or command not found):

1.  **Search Strategy:**
    a. **Search Pattern Registry:** Grep `${CLAUDE_PLUGIN_ROOT}/patterns/index.md` for the query.
    b. **Search Pattern Files:** Grep all files in `${CLAUDE_PLUGIN_ROOT}/patterns/core/` and `${CLAUDE_PLUGIN_ROOT}/patterns/stack/` for the query.
    c. **Search Activation Keywords:** For each pattern file, check if the query matches any `activation.keywords` in the YAML frontmatter.

2.  **Rank Results:**
    -   Patterns with query in name: High relevance
    -   Patterns with query in activation keywords: High relevance
    -   Patterns with query in description: Medium relevance
    -   Patterns with query in content: Low relevance

3.  **Format Output:** Same format as CLI method.

### 4.3 No Results

If no patterns match (either method):
```
**Search Results for "<query>"**

No patterns found matching "<query>".

Try a different keyword or use `/conductor:patterns list` to see all patterns.
```

---

## 5.0 SHOW PROTOCOL
**PROTOCOL: Display a specific pattern.**

### 5.1 Primary Method: CLI Command

1.  **Extract Pattern Name:** Get the pattern name from `{{args}}` (everything after "show ").

2.  **Execute CLI:** Run the patterns show command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns show "<pattern-name>"
    ```

3.  **Parse Output:** The CLI returns detailed pattern information including:
    - Pattern metadata (name, category, tags)
    - All sections with headers
    - AI Quick Reference content
    - When to Apply guidelines
    - Implementation checklist

4.  **Format Output:** Display the pattern with clear sections:
    ```
    **Pattern: <Pattern Name>**
    *Category: <Category> | Tags: <tag1>, <tag2>*

    ---

    ## AI Quick Reference
    <Content from AI Quick Reference section>

    ---

    ## When to Apply
    <Bullet points from When to Apply>

    ---

    ## Quick Implementation Checklist
    <Checklist items>

    ---

    For full documentation including examples and anti-patterns, read the file directly:
    `${CLAUDE_PLUGIN_ROOT}/patterns/core/<name>.md`
    ```

### 5.2 Fallback Method: Manual Read

If the CLI command fails (exit code non-zero or command not found):

1.  **Resolve Pattern Path:**
    a. Normalize the name (lowercase, replace spaces with hyphens).
    b. Check `${CLAUDE_PLUGIN_ROOT}/patterns/core/<name>.md` first.
    c. If not found, check `${CLAUDE_PLUGIN_ROOT}/patterns/stack/**/<name>.md`.
    d. If still not found, search `${CLAUDE_PLUGIN_ROOT}/patterns/index.md` for a matching link.

2.  **Read Pattern File:** Read the resolved pattern file.

3.  **Format Output:** Same format as CLI method.

### 5.3 Pattern Not Found

If pattern cannot be resolved (either method):
```
**Pattern Not Found:** "<pattern-name>"

Did you mean one of these?
- error-handling
- logging
- validation

Use `/conductor:patterns list` to see all available patterns.
```

---

## 6.0 AI-ONLY MODE
**PROTOCOL: Display only the AI Quick Reference section (for internal use).**

When called with `show <pattern-name> --ai-only`:

### 6.1 Primary Method: CLI Command

1.  **Extract Pattern Name:** Get the pattern name from `{{args}}` (between "show " and " --ai-only").

2.  **Execute CLI:** Run the patterns show command with the --ai-only flag:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py patterns show "<pattern-name>" --ai-only
    ```

3.  **Output:** Display only the AI Quick Reference content without additional formatting.

### 6.2 Fallback Method: Manual Read

If the CLI command fails (exit code non-zero or command not found):

1.  **Read Pattern File:** Same as SHOW PROTOCOL fallback.

2.  **Extract AI Section:** Parse only the "## AI Quick Reference" section (from header to next `---` or `## Human Documentation`).

3.  **Format Output:** Display only the AI Quick Reference content without additional formatting.

This mode is used internally during `/conductor:implement` pattern surfacing.

---

## 7.0 CLI AVAILABILITY CHECK
**PROTOCOL: Verify CLI is available before use.**

Before executing any CLI command:

1.  **Check Script Exists:** Verify `${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py` exists.

2.  **Check Python Available:** Verify Python 3 is available in PATH.

3.  **Handle Unavailability:**
    -   If CLI is unavailable, automatically use the fallback method.
    -   Do NOT announce CLI unavailability to the user unless they specifically ask.
    -   Log internally: "CLI unavailable, using fallback method."

**Error Handling:**
- CLI exit code 0: Success, use CLI output
- CLI exit code non-zero: Use fallback method
- CLI timeout (>5s): Use fallback method
- CLI output empty: Use fallback method
