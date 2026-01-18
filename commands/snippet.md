---
name: conductor:snippet
description: Browse, search, and display code snippets from the Snippet Library
argument-hint: "[list|search <query>|show <snippet-name>]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to help users explore and retrieve code snippets from the Snippet Library. This involves listing available snippets, searching for snippets by keyword, and displaying snippet content for use in implementation.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## CLI Operations
**PROTOCOL: Use Python CLI for efficient snippet operations.**

The Python CLI (`${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets`) provides optimized, token-efficient operations for snippet management. **Always prefer CLI commands over manual file parsing.**

### Available CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `snippets list` | List all snippets organized by language | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets list` |
| `snippets show NAME` | Show snippet with AI header and content | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets show api-client.ts` |
| `snippets show NAME -l LANG` | Show snippet for specific language | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets show api-client -l python` |
| `snippets search QUERY` | Search snippets by keyword | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets search error handling` |
| `snippets detect_language FILE` | Detect language from file extension | `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets detect_language app.tsx` |

### CLI Output Format

The CLI returns structured output including:
- **List:** Snippets grouped by language with name, path, category, and USE/REQUIRES/PATTERN metadata
- **Show:** AI header block followed by full snippet content with syntax highlighting hints
- **Search:** Scored results with relevance ranking and matched metadata
- **Detect Language:** Language identifier and comment style for the file type

### Fallback Protocol

If the CLI command fails (non-zero exit code, Python not available, or script missing):
1. Log the error for diagnostics
2. Fall back to manual file-based operations as described in each protocol section
3. Continue with the operation using the fallback method
4. Do NOT halt unless both CLI and fallback methods fail

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Snippet Library exists.**

1.  **Verify Snippet Index:** Check for the existence of `${CLAUDE_PLUGIN_ROOT}/snippets/index.md`.

2.  **Handle Failure:**
    -   If the file is missing, announce: "Snippet Library is not set up. The ${CLAUDE_PLUGIN_ROOT}/snippets/index.md file is missing."
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

### Primary Method: CLI Command

1.  **Execute CLI:** Run the list command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets list
    ```

2.  **Parse Output:** The CLI returns snippets organized by language with metadata:
    - Snippet name and path
    - Category/pattern information
    - USE, REQUIRES, and PATTERN metadata from AI headers

3.  **Format Output:** Present the CLI output in a user-friendly format:
    ```
    📦 **Snippet Library**

    ### TypeScript Snippets
    | Snippet | Description | Pattern |
    |---------|-------------|---------|
    | [api-client.ts](${CLAUDE_PLUGIN_ROOT}/snippets/typescript/api-client.ts) | Type-safe HTTP client | Error Handling |
    | [error-handler.ts](${CLAUDE_PLUGIN_ROOT}/snippets/typescript/error-handler.ts) | Custom error types | Error Handling |
    | ... | ... | ... |

    ### Python Snippets
    | Snippet | Description | Pattern |
    |---------|-------------|---------|
    | [api-client.py](${CLAUDE_PLUGIN_ROOT}/snippets/python/api-client.py) | HTTP client with httpx | Error Handling |
    | ... | ... | ... |

    ### Pattern Snippets
    | Snippet | Description | Language |
    |---------|-------------|----------|
    | [repository-pattern.md](${CLAUDE_PLUGIN_ROOT}/snippets/patterns/repository-pattern.md) | Data access abstraction | Both |
    | ... | ... | ... |

    **Total:** X snippets available

    💡 Use `/conductor:snippet show <snippet-name>` to view and copy a snippet.
    ```

### Fallback Method: Manual File Parsing

If CLI fails, fall back to manual parsing:

1.  **Read Index:** Read the content of `${CLAUDE_PLUGIN_ROOT}/snippets/index.md`.

2.  **Parse Snippets:** Extract the snippet tables from each category section (TypeScript, Python, Patterns).

3.  **Format Output:** Present snippets in the same organized format as above.

---

## 4.0 SEARCH PROTOCOL
**PROTOCOL: Search snippets by keyword.**

### Primary Method: CLI Command

1.  **Extract Query:** Get the search query from `{{args}}` (everything after "search ").

2.  **Execute CLI:** Run the search command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets search "<query>"
    ```

3.  **Parse Output:** The CLI returns scored search results including:
    - Relevance score for each match
    - Snippet name and path
    - Matched content (USE, REQUIRES, PATTERN, or code)

4.  **Format Output:**
    ```
    🔍 **Search Results for "<query>"**

    **High Relevance:**
    1. **api-client.ts** (${CLAUDE_PLUGIN_ROOT}/snippets/typescript/api-client.ts)
       > USE: When building a type-safe HTTP client for API communication
       > PATTERN: Error Handling, Configuration

    2. **api-client.py** (${CLAUDE_PLUGIN_ROOT}/snippets/python/api-client.py)
       > USE: When building a type-safe HTTP client for API communication
       > PATTERN: Error Handling, Configuration

    **Medium Relevance:**
    3. **async-wrapper.ts** (${CLAUDE_PLUGIN_ROOT}/snippets/typescript/async-wrapper.ts)
       > Matched: description contains "api"

    **Total:** X snippets found

    💡 Use `/conductor:snippet show <snippet-name>` to view the full snippet.
    ```

### Fallback Method: Manual Search

If CLI fails, fall back to manual search:

1.  **Search Strategy:**
    a. **Search Snippet Index:** Grep `${CLAUDE_PLUGIN_ROOT}/snippets/index.md` for the query.
    b. **Search Snippet Files:** Grep all files in `${CLAUDE_PLUGIN_ROOT}/snippets/typescript/`, `${CLAUDE_PLUGIN_ROOT}/snippets/python/`, and `${CLAUDE_PLUGIN_ROOT}/snippets/patterns/` for the query.
    c. **Search AI Headers:** For each snippet file, check if the query matches:
       - `USE:` description
       - `REQUIRES:` dependencies
       - `PATTERN:` related patterns

2.  **Rank Results:**
    -   Snippets with query in filename: High relevance
    -   Snippets with query in USE/PATTERN header: High relevance
    -   Snippets with query in description (index): Medium relevance
    -   Snippets with query in code content: Low relevance

3.  **No Results:** If no snippets match:
    ```
    🔍 **Search Results for "<query>"**

    No snippets found matching "<query>".

    💡 Try a different keyword or use `/conductor:snippet list` to see all snippets.
    ```

---

## 5.0 SHOW PROTOCOL
**PROTOCOL: Display a specific snippet with usage instructions.**

### Primary Method: CLI Command

1.  **Extract Snippet Name:** Get the snippet name from `{{args}}` (everything after "show ").

2.  **Execute CLI:** Run the show command:
    ```bash
    # With extension (auto-detects language)
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets show "<snippet-name>"

    # Or specify language explicitly
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets show "<snippet-name>" -l <language>
    ```

3.  **Parse Output:** The CLI returns:
    - Parsed AI header (USE, REQUIRES, PATTERN)
    - Full snippet content
    - Language identifier for syntax highlighting

4.  **Format Output:**
    ```
    📄 **Snippet: <filename>**
    *Path: ${CLAUDE_PLUGIN_ROOT}/snippets/<category>/<filename>*

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

### Fallback Method: Manual File Reading

If CLI fails, fall back to manual file reading:

1.  **Resolve Snippet Path:**
    a. If name includes extension (.ts, .py, .md), search directly:
       - `${CLAUDE_PLUGIN_ROOT}/snippets/typescript/<name>` for .ts files
       - `${CLAUDE_PLUGIN_ROOT}/snippets/python/<name>` for .py files
       - `${CLAUDE_PLUGIN_ROOT}/snippets/patterns/<name>` for .md files
    b. If no extension, try all directories with common extensions.
    c. Normalize: lowercase, replace spaces with hyphens.

2.  **Read Snippet File:** Read the resolved snippet file.

3.  **Parse AI Header:** Extract the AI header comment block:
    - For TypeScript/JavaScript: `/** ... */` at start of file
    - For Python: `""" ... """` at start of file
    - For Markdown: YAML frontmatter `--- ... ---`

4.  **Snippet Not Found:** If snippet cannot be resolved:
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

### Primary Method: CLI Command

1.  **Execute CLI:** Run the detect_language command:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py snippets detect_language "<filename>"
    ```

2.  **Parse Output:** The CLI returns:
    - Language identifier (e.g., "typescript", "python")
    - Comment style for AI header parsing

### Fallback Method: Extension Mapping

If CLI fails, use the manual extension mapping:

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
