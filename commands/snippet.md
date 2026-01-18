---
name: conductor:snippet
description: Browse, search, and display code snippets from the Snippet Library
argument-hint: "[list|search <query>|show <snippet-name>]"
allowed-tools:
  - Read
  - Glob
  - Grep
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to help users explore and retrieve code snippets from the Snippet Library. This involves listing available snippets, searching for snippets by keyword, and displaying snippet content for use in implementation.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Snippet Library exists.**

1.  **Verify Snippet Index:** Check for the existence of `snippets/index.md`.

2.  **Handle Failure:**
    -   If the file is missing, announce: "Snippet Library is not set up. The snippets/index.md file is missing."
    -   Do NOT proceed to command execution.

---

## 2.0 COMMAND ROUTING
**PROTOCOL: Parse user input and route to appropriate subcommand.**

1.  **Parse Arguments:** Examine `{{args}}` to determine the subcommand:
    -   If `{{args}}` is empty or equals "list" → Execute **LIST PROTOCOL**
    -   If `{{args}}` starts with "search " → Extract query and execute **SEARCH PROTOCOL**
    -   If `{{args}}` starts with "show " → Extract snippet name and execute **SHOW PROTOCOL**
    -   Otherwise → Show usage help

2.  **Usage Help:** If arguments don't match any subcommand:
    ```
    **Usage:** /conductor:snippet [subcommand]

    **Subcommands:**
    - `list` - List all available snippets by category (default)
    - `search <query>` - Search snippets by keyword
    - `show <snippet-name>` - Display a specific snippet

    **Examples:**
    - /conductor:snippet list
    - /conductor:snippet search api client
    - /conductor:snippet show api-client.ts
    ```

---

## 3.0 LIST PROTOCOL
**PROTOCOL: Display all available snippets organized by category.**

1.  **Read Index:** Read the content of `snippets/index.md`.

2.  **Parse Snippets:** Extract the snippet tables from each category section (TypeScript, Python, Patterns).

3.  **Format Output:** Present snippets in organized categories:
    ```
    📦 **Snippet Library**

    ### TypeScript Snippets
    | Snippet | Description | Pattern |
    |---------|-------------|---------|
    | [api-client.ts](snippets/typescript/api-client.ts) | Type-safe HTTP client | Error Handling |
    | [error-handler.ts](snippets/typescript/error-handler.ts) | Custom error types | Error Handling |
    | ... | ... | ... |

    ### Python Snippets
    | Snippet | Description | Pattern |
    |---------|-------------|---------|
    | [api-client.py](snippets/python/api-client.py) | HTTP client with httpx | Error Handling |
    | ... | ... | ... |

    ### Pattern Snippets
    | Snippet | Description | Language |
    |---------|-------------|----------|
    | [repository-pattern.md](snippets/patterns/repository-pattern.md) | Data access abstraction | Both |
    | ... | ... | ... |

    **Total:** X snippets available

    💡 Use `/conductor:snippet show <snippet-name>` to view and copy a snippet.
    ```

---

## 4.0 SEARCH PROTOCOL
**PROTOCOL: Search snippets by keyword.**

1.  **Extract Query:** Get the search query from `{{args}}` (everything after "search ").

2.  **Search Strategy:**
    a. **Search Snippet Index:** Grep `snippets/index.md` for the query.
    b. **Search Snippet Files:** Grep all files in `snippets/typescript/`, `snippets/python/`, and `snippets/patterns/` for the query.
    c. **Search AI Headers:** For each snippet file, check if the query matches:
       - `USE:` description
       - `REQUIRES:` dependencies
       - `PATTERN:` related patterns

3.  **Rank Results:**
    -   Snippets with query in filename: High relevance
    -   Snippets with query in USE/PATTERN header: High relevance
    -   Snippets with query in description (index): Medium relevance
    -   Snippets with query in code content: Low relevance

4.  **Format Output:**
    ```
    🔍 **Search Results for "<query>"**

    **High Relevance:**
    1. **api-client.ts** (snippets/typescript/api-client.ts)
       > USE: When building a type-safe HTTP client for API communication
       > PATTERN: Error Handling, Configuration

    2. **api-client.py** (snippets/python/api-client.py)
       > USE: When building a type-safe HTTP client for API communication
       > PATTERN: Error Handling, Configuration

    **Medium Relevance:**
    3. **async-wrapper.ts** (snippets/typescript/async-wrapper.ts)
       > Matched: description contains "api"

    **Total:** X snippets found

    💡 Use `/conductor:snippet show <snippet-name>` to view the full snippet.
    ```

5.  **No Results:** If no snippets match:
    ```
    🔍 **Search Results for "<query>"**

    No snippets found matching "<query>".

    💡 Try a different keyword or use `/conductor:snippet list` to see all snippets.
    ```

---

## 5.0 SHOW PROTOCOL
**PROTOCOL: Display a specific snippet with usage instructions.**

1.  **Extract Snippet Name:** Get the snippet name from `{{args}}` (everything after "show ").

2.  **Resolve Snippet Path:**
    a. If name includes extension (.ts, .py, .md), search directly:
       - `snippets/typescript/<name>` for .ts files
       - `snippets/python/<name>` for .py files
       - `snippets/patterns/<name>` for .md files
    b. If no extension, try all directories with common extensions.
    c. Normalize: lowercase, replace spaces with hyphens.

3.  **Read Snippet File:** Read the resolved snippet file.

4.  **Parse AI Header:** Extract the AI header comment block:
    - For TypeScript/JavaScript: `/** ... */` at start of file
    - For Python: `""" ... """` at start of file
    - For Markdown: YAML frontmatter `--- ... ---`

5.  **Format Output:**
    ```
    📄 **Snippet: <filename>**
    *Path: snippets/<category>/<filename>*

    ---

    **USE:** <extracted from header>
    **REQUIRES:** <extracted from header>
    **PATTERN:** <extracted from header>

    ---

    ## Code

    ```<language>
    <full snippet content>
    ```

    ---

    💡 **Customization Points:** Look for `// CUSTOMIZE:` comments in the code.

    📋 **To use this snippet:**
    1. Copy the code above
    2. Adapt sections marked with `// CUSTOMIZE:` comments
    3. Install required dependencies listed in REQUIRES
    ```

6.  **Snippet Not Found:** If snippet cannot be resolved:
    ```
    ❌ **Snippet Not Found:** "<snippet-name>"

    Did you mean one of these?
    - api-client.ts
    - api-client.py
    - error-handler.ts

    💡 Use `/conductor:snippet list` to see all available snippets.
    ```

---

## 6.0 INSERT MODE (Future Enhancement)
**PROTOCOL: Insert snippet into current file context.**

When called with `show <snippet-name> --insert`:

1.  **Show Snippet:** Execute standard SHOW PROTOCOL.

2.  **Offer Insertion:** Ask user where to insert:
    ```
    Would you like me to insert this snippet?

    Options:
    A. Insert at cursor position (if in editor context)
    B. Create new file with this snippet
    C. Copy to clipboard (manual paste)

    Enter choice (A/B/C):
    ```

3.  **Handle Response:** Execute appropriate action based on user choice.

**Note:** This mode requires editor integration and may not be available in all contexts.

---

## 7.0 LANGUAGE DETECTION
**PROTOCOL: Determine snippet language for syntax highlighting.**

| Extension | Language | Comment Style |
|-----------|----------|---------------|
| `.ts` | TypeScript | `/** ... */` |
| `.tsx` | TypeScript (React) | `/** ... */` |
| `.js` | JavaScript | `/** ... */` |
| `.py` | Python | `""" ... """` |
| `.go` | Go | `// ...` block |
| `.md` | Markdown | YAML frontmatter |

Use detected language for:
- Syntax highlighting in code blocks
- AI header parsing
- File path resolution
