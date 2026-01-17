---
name: conductor:patterns
description: Browse and search the Pattern Reference Layer
argument-hint: "[list|search <query>|show <pattern-name>]"
allowed-tools:
  - Read
  - Glob
  - Grep
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to help users explore and retrieve patterns from the Pattern Reference Layer. This involves listing available patterns, searching for patterns by keyword, and displaying pattern content.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Pattern Reference Layer exists.**

1.  **Verify Pattern Registry:** Check for the existence of `patterns/index.md`.

2.  **Handle Failure:**
    -   If the file is missing, announce: "Pattern Reference Layer is not set up. The patterns/index.md file is missing."
    -   Do NOT proceed to command execution.

---

## 2.0 COMMAND ROUTING
**PROTOCOL: Parse user input and route to appropriate subcommand.**

1.  **Parse Arguments:** Examine `{{args}}` to determine the subcommand:
    -   If `{{args}}` is empty or equals "list" → Execute **LIST PROTOCOL**
    -   If `{{args}}` starts with "search " → Extract query and execute **SEARCH PROTOCOL**
    -   If `{{args}}` starts with "show " → Extract pattern name and execute **SHOW PROTOCOL**
    -   Otherwise → Show usage help

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

1.  **Read Registry:** Read the content of `patterns/index.md`.

2.  **Parse Patterns:** Extract the pattern table from the "Core Patterns" section.

3.  **Format Output:** Present patterns in a formatted table:
    ```
    📚 **Available Patterns**

    | Pattern | Category | Description |
    |---------|----------|-------------|
    | [Error Handling](patterns/core/error-handling.md) | Resilience | Exception handling, error propagation |
    | [Logging](patterns/core/logging.md) | Observability | Log levels, structured logging |
    | ... | ... | ... |

    **Total:** X patterns available

    💡 Use `/conductor:patterns show <pattern-name>` to view details.
    ```

---

## 4.0 SEARCH PROTOCOL
**PROTOCOL: Search patterns by keyword.**

1.  **Extract Query:** Get the search query from `{{args}}` (everything after "search ").

2.  **Search Strategy:**
    a. **Search Pattern Registry:** Grep `patterns/index.md` for the query.
    b. **Search Pattern Files:** Grep all files in `patterns/core/` and `patterns/stack/` for the query.
    c. **Search Activation Keywords:** For each pattern file, check if the query matches any `activation.keywords` in the YAML frontmatter.

3.  **Rank Results:**
    -   Patterns with query in name: High relevance
    -   Patterns with query in activation keywords: High relevance
    -   Patterns with query in description: Medium relevance
    -   Patterns with query in content: Low relevance

4.  **Format Output:**
    ```
    🔍 **Search Results for "<query>"**

    **High Relevance:**
    1. **[Pattern Name]** (patterns/core/<name>.md)
       > Matched: activation keyword "error"

    **Medium Relevance:**
    2. **[Pattern Name]** (patterns/core/<name>.md)
       > Matched: description contains "error"

    **Total:** X patterns found

    💡 Use `/conductor:patterns show <pattern-name>` to view details.
    ```

5.  **No Results:** If no patterns match:
    ```
    🔍 **Search Results for "<query>"**

    No patterns found matching "<query>".

    💡 Try a different keyword or use `/conductor:patterns list` to see all patterns.
    ```

---

## 5.0 SHOW PROTOCOL
**PROTOCOL: Display a specific pattern.**

1.  **Extract Pattern Name:** Get the pattern name from `{{args}}` (everything after "show ").

2.  **Resolve Pattern Path:**
    a. Normalize the name (lowercase, replace spaces with hyphens).
    b. Check `patterns/core/<name>.md` first.
    c. If not found, check `patterns/stack/**/<name>.md`.
    d. If still not found, search `patterns/index.md` for a matching link.

3.  **Read Pattern File:** Read the resolved pattern file.

4.  **Format Output:** Display the pattern with clear sections:
    ```
    📖 **Pattern: <Pattern Name>**
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

    💡 For full documentation including examples and anti-patterns, read the file directly:
    `patterns/core/<name>.md`
    ```

5.  **Pattern Not Found:** If pattern cannot be resolved:
    ```
    ❌ **Pattern Not Found:** "<pattern-name>"

    Did you mean one of these?
    - error-handling
    - logging
    - validation

    💡 Use `/conductor:patterns list` to see all available patterns.
    ```

---

## 6.0 AI-ONLY MODE
**PROTOCOL: Display only the AI Quick Reference section (for internal use).**

When called with `show <pattern-name> --ai-only`:

1.  **Read Pattern File:** Same as SHOW PROTOCOL.

2.  **Extract AI Section:** Parse only the "## AI Quick Reference" section (from header to next `---` or `## Human Documentation`).

3.  **Format Output:** Display only the AI Quick Reference content without additional formatting.

This mode is used internally during `/conductor:implement` pattern surfacing.
