---
name: conductor:setup
description: Scaffolds the project and sets up the Conductor environment
argument-hint: (no arguments)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Context

!`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --get 2>/dev/null; python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup detect`

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to set up and manage a software project using the Conductor methodology. This document is your operational protocol. Adhere to these instructions precisely and sequentially. Do not make assumptions.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

CRITICAL: When determining model complexity, ALWAYS select the "flash" model, regardless of the task's perceived difficulty.

---

## Fallback Instructions

If the context injection fails:
1. For state check: Manually read `conductor/setup_state.json` if it exists
2. For project detection: Manually check for `.git`, `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `src/`, `app/`, `lib/` directories

### Action CLI Commands (Used During Setup)

The following CLI commands are used for write operations during the setup process:

```bash
# Create conductor directory structure
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold

# Record setup progress
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "STEP_NAME"

# Copy code styleguides
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages LANG1 LANG2
```

---

## AskUserQuestion Tool Protocol

**PROTOCOL: Use the AskUserQuestion tool for all interactive user prompts.**

All questions to the user during setup MUST be asked using the `AskUserQuestion` tool. This provides a structured, consistent user experience with clickable options.

### Tool Structure

```json
{
  "questions": [
    {
      "question": "The complete question text ending with ?",
      "header": "Short label",  // Max 12 characters
      "options": [
        {"label": "Option label", "description": "What this option means"},
        {"label": "Another option", "description": "Explanation of this choice"}
      ],
      "multiSelect": false  // true if user can select multiple options
    }
  ]
}
```

### Key Rules

1. **Header Constraint:** Maximum 12 characters (e.g., "Target User", "Framework", "Coverage")
2. **Options Constraint:** Minimum 2, maximum 4 options per question
3. **multiSelect:** Set to `true` for "Additive" questions where multiple selections are valid; `false` for "Exclusive Choice" questions
4. **Sequential Questions:** Ask one question at a time. Wait for user response before asking the next question
5. **"Other" Option:** Users can always select "Other" to provide custom text input - do NOT add this as an explicit option
6. **Recommendations:** When recommending an option, add "(Recommended)" to the label and make it the first option

### Question Type Mapping

| Question Type | multiSelect | Example |
|--------------|-------------|---------|
| **Additive** (multiple valid answers) | `true` | "Which features should be included?" |
| **Exclusive Choice** (single answer) | `false` | "Which primary language?" |
| **Confirmation** (yes/no) | `false` | "Proceed with analysis?" |
| **Approval** (approve/change) | `false` | "Is this document acceptable?" |

### Standard Option Patterns

**Confirmation Questions:**
```json
{
  "question": "May I perform a read-only scan to analyze your project?",
  "header": "Permission",
  "options": [
    {"label": "Yes, proceed", "description": "Allow read-only analysis of the project"},
    {"label": "No, skip this", "description": "Do not analyze, I will provide details manually"}
  ],
  "multiSelect": false
}
```

**Approval Questions (Document Review):**
```json
{
  "question": "Does this document accurately capture the requirements?",
  "header": "Review",
  "options": [
    {"label": "Approve", "description": "The document is correct, proceed to next step"},
    {"label": "Suggest changes", "description": "I want to modify some parts"}
  ],
  "multiSelect": false
}
```

**Feature Selection (Additive):**
```json
{
  "question": "Which target users should this product serve?",
  "header": "Users",
  "options": [
    {"label": "Developers", "description": "Technical users who write code"},
    {"label": "End users", "description": "Non-technical product consumers"},
    {"label": "Administrators", "description": "System operators and managers"},
    {"label": "Auto-generate", "description": "Let me infer from context and generate the document"}
  ],
  "multiSelect": true
}
```

**Technology Choice (Exclusive):**
```json
{
  "question": "Which primary programming language will this project use?",
  "header": "Language",
  "options": [
    {"label": "TypeScript (Recommended)", "description": "Strong typing with JavaScript ecosystem"},
    {"label": "Python", "description": "Versatile language for various applications"},
    {"label": "Go", "description": "Fast, compiled language for systems programming"}
  ],
  "multiSelect": false
}
```

### Auto-Generate Option

For interactive document generation sections (2.1, 2.2, 2.3, 3.1), always include an auto-generate option:

```json
{"label": "Auto-generate", "description": "Use context to infer remaining details and generate the document"}
```

When user selects this option:
1. Stop asking questions immediately
2. Use gathered answers and project context to infer remaining details
3. Generate the complete document
4. Present for review using an Approval question

---

## 1.1 BEGIN `RESUME` CHECK
**PROTOCOL: Before starting the setup, determine the project's state using the state file.**

1.  **Use Injected Context:**
    -   The state data has been injected via the `# Context` section above.
    -   Parse the first JSON object to check for `last_successful_step` value.
    -   If no state JSON was returned (new project), proceed directly to Step 1.2.

2.  **Resume Based on State:**
    - Let the value of `last_successful_step` in the JSON response be `STEP`.
    - Based on the value of `STEP`, jump to the **next logical section**:

    - If `STEP` is "2.1_product_guide", announce "Resuming setup: The Product Guide (`product.md`) is already complete. Next, we will create the Product Guidelines." and proceed to **Section 2.2**.
    - If `STEP` is "2.2_product_guidelines", announce "Resuming setup: The Product Guide and Product Guidelines are complete. Next, we will define the Technology Stack." and proceed to **Section 2.3**.
    - If `STEP` is "2.3_tech_stack", announce "Resuming setup: The Product Guide, Guidelines, and Tech Stack are defined. Next, we will select Code Styleguides." and proceed to **Section 2.4**.
    - If `STEP` is "2.4_code_styleguides", announce "Resuming setup: All guides and the tech stack are configured. Next, we will define the project workflow." and proceed to **Section 2.5**.
    - If `STEP` is "2.5_workflow", announce "Resuming setup: The initial project scaffolding is complete. Next, we will generate the first track." and proceed to **Phase 2 (3.0)**.
    - If `STEP` is "3.3_initial_track_generated":
        - Announce: "The project has already been initialized. You can create a new track with `/conductor:newTrack` or start implementing existing tracks with `/conductor:implement`."
        - Halt the `setup` process.
    - If `STEP` is unrecognized, announce an error and halt.

---

## 1.2 PRE-INITIALIZATION OVERVIEW
1.  **Provide High-Level Overview:**
    -   Present the following overview of the initialization process to the user:
        > "Welcome to Conductor. I will guide you through the following steps to set up your project:
        > 1. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
        > 2. **Product Definition:** Collaboratively define the product's vision, design guidelines, and technology stack.
        > 3. **Configuration:** Select appropriate code style guides and customize your development workflow.
        > 4. **Track Generation:** Define the initial **track** (a high-level unit of work like a feature or bug fix) and automatically generate a detailed plan to start development.
        >
        > Let's get started!"

---

## 2.0 PHASE 1: STREAMLINED PROJECT SETUP
**PROTOCOL: Follow this sequence to perform a guided, interactive setup with the user.**


### 2.0 Project Inception
1.  **Detect Project Maturity:**
    -   **Use Injected Context:** The project detection data has been injected via the `# Context` section above.
    -   **Parse Detection Output:** The detection JSON object contains:
        - `project_type`: "brownfield" or "greenfield"
        - `languages`: Array of detected programming languages
        - `frameworks`: Array of detected frameworks
        - `ecosystems`: Array of detected package ecosystems (npm, pip, etc.)
        - `indicators`: Object with detection signals (has_git, has_package_json, etc.)
    -   **Store Detection Results:** Store the detection output for use in Section 2.0.1 (Automatic Stack Detection).
    -   **Fallback - Manual Classification:** If context injection failed, classify manually:
        -   **Brownfield Indicators:**
            -   Check for existence of version control directories: `.git`, `.svn`, or `.hg`.
            -   If a `.git` directory exists, execute `git status --porcelain`. If the output is not empty, classify as "Brownfield" (dirty repository).
            -   Check for dependency manifests: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`.
            -   Check for source code directories: `src/`, `app/`, `lib/` containing code files.
            -   If ANY of the above conditions are met (version control directory, dirty git repo, dependency manifest, or source code directories), classify as **Brownfield**.
        -   **Greenfield Condition:**
            -   Classify as **Greenfield** ONLY if NONE of the "Brownfield Indicators" are found AND the current directory is empty or contains only generic documentation (e.g., a single `README.md` file) without functional code or dependencies.

2.  **Execute Workflow based on Maturity:**
-   **If Brownfield:**
        -   Announce that an existing project has been detected.
        -   If the CLI output's `indicators.has_uncommitted_changes` is true (or if `git status --porcelain` executed manually indicated uncommitted changes), inform the user: "WARNING: You have uncommitted changes in your Git repository. Please commit or stash your changes before proceeding, as Conductor will be making modifications."
        -   **Begin Brownfield Project Initialization Protocol:**
            -   **1.0 Pre-analysis Confirmation:**
                1.  **Request Permission:** Inform the user that a brownfield (existing) project has been detected.
                2.  **Ask for Permission:** Use the `AskUserQuestion` tool to request permission:
                    ```json
                    {
                      "questions": [{
                        "question": "May I perform a read-only scan to analyze your existing project?",
                        "header": "Permission",
                        "options": [
                          {"label": "Yes, proceed", "description": "Allow read-only analysis of the project structure and dependencies"},
                          {"label": "No, skip", "description": "Skip analysis and provide project details manually"}
                        ],
                        "multiSelect": false
                      }]
                    }
                    ```
                3.  **Handle Denial:** If user selects "No, skip", halt the process and await further user instructions.
                4.  **Confirmation:** If user selects "Yes, proceed", continue to the next step.

            -   **2.0 Code Analysis:**
                1.  **Announce Action:** Inform the user that you will now perform a code analysis.
                2.  **Prioritize README:** Begin by analyzing the `README.md` file, if it exists.
                3.  **Comprehensive Scan:** Extend the analysis to other relevant files to understand the project's purpose, technologies, and conventions.

            -   **2.1 File Size and Relevance Triage:**
                1.  **Respect Ignore Files:** Before scanning any files, you MUST check for the existence of `.claudeignore` and `.gitignore` files. If either or both exist, you MUST use their combined patterns to exclude files and directories from your analysis. The patterns in `.claudeignore` should take precedence over `.gitignore` if there are conflicts. This is the primary mechanism for avoiding token-heavy, irrelevant files like `node_modules`.
                2.  **Efficiently List Relevant Files:** To list the files for analysis, you MUST use a command that respects the ignore files. For example, you can use `git ls-files --exclude-standard -co | xargs -n 1 dirname | sort -u` which lists all relevant directories (tracked by Git, plus other non-ignored files) without listing every single file. If Git is not used, you must construct a `find` command that reads the ignore files and prunes the corresponding paths.
                3.  **Fallback to Manual Ignores:** ONLY if neither `.claudeignore` nor `.gitignore` exist, you should fall back to manually ignoring common directories. Example command: `ls -lR -I 'node_modules' -I '.m2' -I 'build' -I 'dist' -I 'bin' -I 'target' -I '.git' -I '.idea' -I '.vscode'`.
                4.  **Prioritize Key Files:** From the filtered list of files, focus your analysis on high-value, low-size files first, such as `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, and other configuration or manifest files.
                5.  **Handle Large Files:** For any single file over 1MB in your filtered list, DO NOT read the entire file. Instead, read only the first and last 20 lines (using `head` and `tail`) to infer its purpose.

            -   **2.2 Extract and Infer Project Context:**
                1.  **Strict File Access:** DO NOT ask for more files. Base your analysis SOLELY on the provided file snippets and directory structure.
                2.  **Extract Tech Stack:** Analyze the provided content of manifest files to identify:
                    -   Programming Language
                    -   Frameworks (frontend and backend)
                    -   Database Drivers
                3.  **Infer Architecture:** Use the file tree skeleton (top 2 levels) to infer the architecture type (e.g., Monorepo, Microservices, MVC).
                4.  **Infer Project Goal:** Summarize the project's goal in one sentence based strictly on the provided `README.md` header or `package.json` description.
        -   **Upon completing the brownfield initialization protocol, proceed to the Automatic Stack Detection section (2.0.1).**
    -   **If Greenfield:**
        -   Announce that a new project will be initialized.
        -   Proceed to the next step in this file.

3.  **Initialize Git Repository (for Greenfield):**
    -   If a `.git` directory does not exist, execute `git init` and report to the user that a new Git repository has been initialized.

4.  **Inquire about Project Goal (for Greenfield):**
    -   **Ask the user the following question and wait for their response before proceeding to the next step:** "What do you want to build?"
    -   **CRITICAL: You MUST NOT execute any tool calls until the user has provided a response.**
    -   **Upon receiving the user's response:**
        -   **Use CLI for Scaffolding:** Execute the CLI command to create the conductor directory structure:
            ```bash
            python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold
            ```
        -   **Fallback:** If CLI is unavailable, manually execute `mkdir -p conductor/tracks`.
        -   **Initialize State File:** Use the CLI to initialize the state file:
            ```bash
            python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set ""
            ```
        -   **Fallback:** If CLI is unavailable, manually create `conductor/setup_state.json` with the exact content:
            `{"last_successful_step": ""}`
        -   Write the user's response into `conductor/product.md` under a header named `# Initial Concept`.

5.  **Continue:** Immediately proceed to the next section.

### 2.0.1 Automatic Stack Detection (Brownfield Only)
**PROTOCOL: For brownfield projects, automatically detect the technology stack using the CLI or Stack Detection Protocol.**

**Skip Condition:** This section applies ONLY to brownfield projects. For greenfield projects, skip directly to Section 2.1.

1.  **Retrieve Stack Detection Results:**
    -   **Use Injected Context:** The detection results are already available from the `# Context` section. Use the stored `languages`, `frameworks`, and `ecosystems` arrays.
    -   **If context injection failed:** Execute the Stack Detection Protocol defined in `${CLAUDE_PLUGIN_ROOT}/protocols/stack-detection.md`. Follow all steps in the protocol:
        a. Scan for manifest files (package.json, pom.xml, requirements.txt, etc.)
        b. Analyze file extensions to determine language distribution
        c. Detect frameworks from dependency declarations
        d. Detect infrastructure and tooling configuration files
        e. Calculate confidence score based on signal strength

2.  **Store Detection Results:**
    -   Store the detection results internally as a JSON stack profile.
    -   The profile will be used to pre-populate `tech-stack.md` in Section 2.3.

3.  **Present Detection Results to User:**
    -   Based on the confidence level, present the results with appropriate messaging:

    -   **If Confidence is HIGH (score >= 85):**
        > ```
        > -----------------------------------------------
        > **Stack Detection Results** (Confidence: HIGH)
        > Stack detection is highly confident in these results.
        > -----------------------------------------------
        >
        > **Primary Language:** [detected primary language]
        > **Languages Detected:** [comma-separated list]
        > **Frameworks:** [comma-separated list with categories]
        > **Build Tools:** [comma-separated list]
        > **Testing:** [comma-separated list]
        > **Infrastructure:** [comma-separated list]
        > **Package Manager:** [detected package manager]
        > ```

    -   **If Confidence is MEDIUM (score 60-84):**
        > ```
        > -----------------------------------------------
        > **Stack Detection Results** (Confidence: MEDIUM)
        > Stack detection found partial matches - please verify.
        > -----------------------------------------------
        >
        > **Primary Language:** [detected primary language]
        > **Languages Detected:** [comma-separated list]
        > **Frameworks:** [comma-separated list with categories]
        > **Build Tools:** [comma-separated list]
        > **Testing:** [comma-separated list]
        > **Infrastructure:** [comma-separated list]
        > **Package Manager:** [detected package manager]
        > ```

    -   **If Confidence is LOW (score 30-59):**
        > ```
        > -----------------------------------------------
        > **Stack Detection Results** (Confidence: LOW)
        > Limited detection signals - manual verification recommended.
        > -----------------------------------------------
        >
        > **Primary Language:** [detected primary language]
        > **Languages Detected:** [comma-separated list]
        > **Frameworks:** [comma-separated list, if any]
        > **Build Tools:** [comma-separated list, if any]
        > ```

    -   **If Confidence is UNCERTAIN (score < 30):**
        > ```
        > -----------------------------------------------
        > **Stack Detection Results** (Confidence: UNCERTAIN)
        > Minimal detection signals. Manual specification strongly recommended.
        > -----------------------------------------------
        >
        > Unable to confidently detect the technology stack.
        > Detected languages: [list, if any]
        > ```

4.  **User Confirmation Flow:**
    -   Use the `AskUserQuestion` tool to confirm the detection:
        ```json
        {
          "questions": [{
            "question": "Is this stack detection accurate?",
            "header": "Stack",
            "options": [
              {"label": "Accept", "description": "Use these detected values as-is"},
              {"label": "Edit", "description": "Modify the detected values before proceeding"},
              {"label": "Skip", "description": "Ignore detection and enter stack manually later"}
            ],
            "multiSelect": false
          }]
        }
        ```

    -   **If User Selects "Accept":**
        -   Store the detected stack profile as-is for use in Section 2.3.
        -   Set internal flag `stack_auto_detected = true`.
        -   Proceed to Section 2.1.

    -   **If User Selects "Edit":**
        -   Present each detected category one at a time for verification using `AskUserQuestion`:
            1. Primary Language verification:
               ```json
               {
                 "questions": [{
                   "question": "Is '[detected language]' the correct primary language?",
                   "header": "Language",
                   "options": [
                     {"label": "Yes, correct", "description": "Keep the detected primary language"},
                     {"label": "No, change it", "description": "I will specify the correct language"}
                   ],
                   "multiSelect": false
                 }]
               }
               ```
            2. Repeat similar pattern for Additional Languages, Frameworks, and Build Tools.
        -   Update the stored stack profile with user corrections.
        -   Set internal flag `stack_auto_detected = true`.
        -   Proceed to Section 2.1.

    -   **If User Selects "Skip":**
        -   Discard the detected stack profile.
        -   Set internal flag `stack_auto_detected = false`.
        -   User will manually specify the stack in Section 2.3.
        -   Proceed to Section 2.1.

5.  **Continue:** Proceed to Section 2.0.2 (Codebase Analysis) if brownfield, or Section 2.1 if greenfield.

### 2.0.2 Codebase Analysis (Brownfield Only)
**PROTOCOL: For brownfield projects, analyze existing codebase patterns for documentation generation.**

**Skip Condition:** This section applies ONLY to brownfield projects. For greenfield projects, skip directly to Section 2.1.

**Protocol Reference:** This section executes the Codebase Analysis Protocol defined in `${CLAUDE_PLUGIN_ROOT}/protocols/codebase-analysis.md`.

1.  **Announce Analysis:**
    -   Inform the user: "I will now analyze your codebase to detect established patterns and conventions. This will be used to generate documentation that helps AI assistants understand your project's practices."

2.  **Execute Pattern Detection:**
    For each of the six analysis categories, execute the detection algorithms defined in the protocol:

    **Category 1: Code Conventions**
    -   Detect file naming conventions (kebab-case, camelCase, PascalCase, snake_case)
    -   Detect directory structure patterns (feature-based, layer-based, etc.)
    -   Detect import patterns (relative, absolute, path aliases)
    -   Detect module organization (barrel exports, co-location)

    **Category 2: Architecture Patterns**
    -   Detect design patterns (Repository, Factory, Observer, etc.)
    -   Detect layer organization (Clean Architecture, Hexagonal, MVC, etc.)
    -   Detect dependency injection patterns
    -   Detect state management patterns (for frontend projects)

    **Category 3: Testing Patterns**
    -   Detect test file naming conventions
    -   Detect test framework usage
    -   Detect mocking patterns
    -   Detect test organization (co-located, centralized, type-separated)

    **Category 4: Annotations & Decorators**
    -   Detect custom decorators and their purposes
    -   Detect framework-specific decorators
    -   Detect documentation patterns (JSDoc, docstrings, etc.)

    **Category 5: API Patterns**
    -   Detect REST endpoint conventions
    -   Detect response format patterns
    -   Detect error handling conventions
    -   Detect API versioning strategy

    **Category 6: Configuration Patterns**
    -   Detect configuration file formats
    -   Detect environment variable patterns
    -   Detect build tool configuration
    -   Detect CI/CD pipeline patterns

3.  **Calculate Confidence Levels:**
    -   For each category, calculate confidence score per protocol:
        -   **HIGH (80-100):** Multiple strong indicators, consistent patterns
        -   **MEDIUM (50-79):** Some indicators found, minor inconsistencies
        -   **LOW (20-49):** Few indicators, patterns unclear
        -   **UNCERTAIN (<20):** Insufficient data for reliable detection
    -   Count total patterns detected per category

4.  **Store Analysis Results:**
    -   Store the complete analysis results internally as a JSON structure.
    -   This will be used in Section 2.0.3 for documentation generation.
    -   Set internal flag `codebase_analyzed = true`.

5.  **Continue:** Proceed to Section 2.0.2.1 (Consolidated Review).

### 2.0.2.1 Consolidated Pattern Review
**PROTOCOL: Present all analysis results in a single review step for user approval.**

1.  **Present Analysis Summary:**
    -   Display all detected patterns in a formatted summary:

    ```
    ═══════════════════════════════════════════════════════════
    **Codebase Analysis Results**
    ═══════════════════════════════════════════════════════════

    **Code Conventions** (Confidence: HIGH)
    • File naming: kebab-case (75% of files)
    • Directory structure: feature-based
    • Imports: absolute with @/ alias
    • Module organization: barrel exports
    Patterns detected: 8

    **Architecture** (Confidence: MEDIUM)
    • Design patterns: Repository, Factory
    • Layer organization: Clean Architecture
    • Dependency injection: NestJS framework DI
    Patterns detected: 5

    **Testing** (Confidence: HIGH)
    • Test naming: *.test.ts suffix
    • Framework: Vitest
    • Mocking: vi.mock() inline
    • Organization: co-located
    Patterns detected: 6

    **API Patterns** (Confidence: HIGH)
    • REST: plural nouns, kebab-case
    • Versioning: /api/v1/ prefix
    • Response: envelope pattern
    • Errors: custom exception classes
    Patterns detected: 7

    **Configuration** (Confidence: MEDIUM)
    • Config format: TypeScript
    • Env vars: SCREAMING_SNAKE_CASE with APP_ prefix
    • Build tool: Vite
    • CI/CD: GitHub Actions
    Patterns detected: 5

    **Annotations** (Confidence: LOW)
    • Documentation: JSDoc (partial coverage)
    Patterns detected: 2

    ═══════════════════════════════════════════════════════════
    Total patterns detected: 33
    ═══════════════════════════════════════════════════════════
    ```

2.  **User Category Selection:**
    -   Use the `AskUserQuestion` tool with `multiSelect: true` for category approval:
        ```json
        {
          "questions": [{
            "question": "Which pattern categories should be included in the generated documentation?",
            "header": "Categories",
            "options": [
              {"label": "All categories (Recommended)", "description": "Include all detected patterns in documentation"},
              {"label": "Code Conventions", "description": "File naming, imports, module organization (8 patterns)"},
              {"label": "Architecture", "description": "Design patterns, layers, DI (5 patterns)"},
              {"label": "Testing", "description": "Test patterns, framework, mocking (6 patterns)"}
            ],
            "multiSelect": true
          }]
        }
        ```
    -   **Note:** Due to 4-option limit, present categories in batches or use "All categories" as primary option.
    -   If more than 4 categories have patterns, present a second question for remaining categories.

3.  **Handle User Selection:**
    -   **If User Selects "All categories":**
        -   Store all categories as approved for documentation generation.
        -   Set internal flag `approved_categories = ["code_conventions", "architecture", "testing", "annotations", "api_patterns", "configuration"]`.

    -   **If User Selects Specific Categories:**
        -   Store only selected categories as approved.
        -   Set internal flag `approved_categories = [<selected categories>]`.

    -   **If User Selects Nothing (via "Other" to skip):**
        -   Set internal flag `approved_categories = []`.
        -   Skip documentation generation in Section 2.0.3.

4.  **Announce Next Steps:**
    -   If categories were approved: "I will generate documentation for the approved categories after we complete the product definition."
    -   If no categories approved: "Skipping pattern documentation. Proceeding with product definition."

5.  **Continue:** Proceed to Section 2.1 (Generate Product Guide).

### 2.1 Generate Product Guide (Interactive)
1.  **Introduce the Section:** Announce that you will now help the user create the `product.md`.
2.  **Ask Questions Using AskUserQuestion Tool:** Use the `AskUserQuestion` tool to ask questions one at a time. Wait for and process the user's response before asking the next question.
    -   **CONSTRAINT:** Limit your inquiry to a maximum of 5 questions.
    -   **SUGGESTIONS:** For each question, generate 2-3 high-quality suggested answers based on common patterns or context you already have.
    -   **Example Topics:** Target users, goals, features, etc
    -   **General Guidelines:**
        -   **1. Classify Question Type:** Before formulating any question, classify its purpose:
            -   **Additive:** Questions where multiple selections are valid (e.g., target users, features). Use `multiSelect: true`.
            -   **Exclusive Choice:** Questions requiring a single answer (e.g., primary goal). Use `multiSelect: false`.
        -   **2. Use AskUserQuestion Tool:** Structure each question using the tool:
            ```json
            {
              "questions": [{
                "question": "Who are the primary target users for this product?",
                "header": "Users",
                "options": [
                  {"label": "Developers", "description": "Technical users who write code"},
                  {"label": "End users", "description": "Non-technical product consumers"},
                  {"label": "Auto-generate", "description": "Infer from context and generate document"}
                ],
                "multiSelect": true
              }]
            }
            ```
        -   **3. Interaction Flow:**
            -   **CRITICAL:** Ask questions sequentially (one at a time). Wait for user response before next question.
            -   Always include an "Auto-generate" option to let users skip remaining questions.
            -   Confirm understanding by summarizing before moving on.
    -   **FOR EXISTING PROJECTS (BROWNFIELD):** Ask project context-aware questions based on the code analysis.
    -   **AUTO-GENERATE LOGIC:** If user selects "Auto-generate", immediately stop asking questions. Use your best judgment to infer remaining details, generate the full `product.md` content, and proceed to the draft step.
3.  **Draft the Document:** Once the dialogue is complete (or Auto-generate is selected), generate the content for `product.md`. You are encouraged to expand on the gathered details to create a comprehensive document.
    -   **CRITICAL:** The source of truth is **only the user's selected answer(s)**. DO NOT include conversational options in the final file.
4.  **User Confirmation Loop:** Present the drafted content to the user and use `AskUserQuestion` for review:
    -   First, display the drafted content in a markdown code block.
    -   Then use the tool:
        ```json
        {
          "questions": [{
            "question": "Does this product guide accurately capture your vision?",
            "header": "Review",
            "options": [
              {"label": "Approve", "description": "The document is correct, proceed to next step"},
              {"label": "Suggest changes", "description": "I want to modify some parts"}
            ],
            "multiSelect": false
          }]
        }
        ```
    -   **Loop:** If user selects "Suggest changes", ask what to modify (user can type freely via "Other"), apply changes, and re-present for review. Break loop on "Approve".
5.  **Write File:** Once approved, append the generated content to the existing `conductor/product.md` file, preserving the `# Initial Concept` section.
6.  **Commit State:** Upon successful creation of the file, use the CLI to record progress:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.1_product_guide"
    ```
    **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
    `{"last_successful_step": "2.1_product_guide"}`
7.  **Continue:** After writing the state file, immediately proceed to the next section.

### 2.2 Generate Product Guidelines (Interactive)
1.  **Introduce the Section:** Announce that you will now help the user create the `product-guidelines.md`.
2.  **Ask Questions Using AskUserQuestion Tool:** Use the `AskUserQuestion` tool to ask questions one at a time. Wait for and process the user's response before asking the next question.
    -   **CONSTRAINT:** Limit your inquiry to a maximum of 5 questions.
    -   **SUGGESTIONS:** For each question, generate 2-3 high-quality options. Add "(Recommended)" to the first option when you have a strong recommendation.
    -   **Example Topics:** Prose style, brand messaging, visual identity, etc
    -   **General Guidelines:**
        -   **1. Classify Question Type:**
            -   **Additive:** Questions where multiple selections are valid. Use `multiSelect: true`.
            -   **Exclusive Choice:** Questions requiring a single answer. Use `multiSelect: false`.
        -   **2. Use AskUserQuestion Tool:** Structure each question:
            ```json
            {
              "questions": [{
                "question": "What tone should the product's messaging convey?",
                "header": "Tone",
                "options": [
                  {"label": "Professional (Recommended)", "description": "Formal, authoritative, and business-appropriate"},
                  {"label": "Friendly", "description": "Warm, approachable, and conversational"},
                  {"label": "Auto-generate", "description": "Infer from context and generate document"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **3. Interaction Flow:**
            -   **CRITICAL:** Ask questions sequentially (one at a time). Wait for user response before next question.
            -   Always include an "Auto-generate" option.
            -   Confirm understanding by summarizing before moving on.
    -   **AUTO-GENERATE LOGIC:** If user selects "Auto-generate", immediately stop asking questions. Use your best judgment to infer remaining details and proceed to draft.
3.  **Draft the Document:** Once the dialogue is complete (or Auto-generate is selected), generate the content for `product-guidelines.md`. You are encouraged to expand on the gathered details to create a comprehensive document.
    -   **CRITICAL:** The source of truth is **only the user's selected answer(s)**. DO NOT include conversational options in the final file.
4.  **User Confirmation Loop:** Present the drafted content to the user and use `AskUserQuestion` for review:
    -   First, display the drafted content in a markdown code block.
    -   Then use the tool:
        ```json
        {
          "questions": [{
            "question": "Do these product guidelines accurately capture your brand and style preferences?",
            "header": "Review",
            "options": [
              {"label": "Approve", "description": "The document is correct, proceed to next step"},
              {"label": "Suggest changes", "description": "I want to modify some parts"}
            ],
            "multiSelect": false
          }]
        }
        ```
    -   **Loop:** If user selects "Suggest changes", ask what to modify, apply changes, and re-present for review. Break loop on "Approve".
5.  **Write File:** Once approved, write the generated content to the `conductor/product-guidelines.md` file.
6.  **Commit State:** Upon successful creation of the file, use the CLI to record progress:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.2_product_guidelines"
    ```
    **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
    `{"last_successful_step": "2.2_product_guidelines"}`
7.  **Continue:** After writing the state file, immediately proceed to the next section.

### 2.3 Generate Tech Stack (Interactive)
1.  **Check for Auto-Detected Stack (Brownfield with Stack Detection):**
    -   **If `stack_auto_detected = true`** (set in Section 2.0.1):
        -   Announce: "Using the auto-detected technology stack from earlier. Generating tech-stack.md..."
        -   Skip the interactive questioning in step 2.
        -   Proceed directly to step 3 (Draft the Document) using the stored stack profile.
    -   **If `stack_auto_detected = false` or not set:**
        -   Proceed with normal interactive flow in step 2.

2.  **Introduce the Section:** Announce that you will now help define the technology stacks.
3.  **Ask Questions Using AskUserQuestion Tool:** Use the `AskUserQuestion` tool to ask questions one at a time. Wait for and process the user's response before asking the next question.
    -   **CONSTRAINT:** Limit your inquiry to a maximum of 5 questions.
    -   **SUGGESTIONS:** For each question, generate 2-3 high-quality options. Add "(Recommended)" to the first option when you have a strong recommendation.
    -   **Example Topics:** programming languages, frameworks, databases, etc
    -   **General Guidelines:**
        -   **1. Classify Question Type:**
            -   **Additive:** Questions where multiple selections are valid (e.g., additional languages, frameworks). Use `multiSelect: true`.
            -   **Exclusive Choice:** Questions requiring a single answer (e.g., primary language). Use `multiSelect: false`.
        -   **2. Use AskUserQuestion Tool:** Structure each question:
            ```json
            {
              "questions": [{
                "question": "What is the primary programming language for this project?",
                "header": "Language",
                "options": [
                  {"label": "TypeScript (Recommended)", "description": "Strong typing with JavaScript ecosystem"},
                  {"label": "Python", "description": "Versatile language for various applications"},
                  {"label": "Auto-generate", "description": "Infer from context and generate document"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **3. Interaction Flow:**
            -   **CRITICAL:** Ask questions sequentially (one at a time). Wait for user response before next question.
            -   Always include an "Auto-generate" option.
            -   Confirm understanding by summarizing before moving on.
    -   **FOR EXISTING PROJECTS (BROWNFIELD) without auto-detection:**
        -   **CRITICAL WARNING:** Your goal is to document the project's *existing* tech stack, not to propose changes.
        -   **State the Inferred Stack:** Based on the code analysis, state the inferred technology stack.
        -   **Request Confirmation:** Use `AskUserQuestion` to confirm:
            ```json
            {
              "questions": [{
                "question": "Is this inferred tech stack correct?",
                "header": "Confirm",
                "options": [
                  {"label": "Yes, correct", "description": "Proceed with the detected stack"},
                  {"label": "No, needs changes", "description": "I will provide the correct stack"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **Handle Disagreement:** If user disputes, allow them to provide correct technology stack via "Other" input.
    -   **AUTO-GENERATE LOGIC:** If user selects "Auto-generate", immediately stop asking questions. Use your best judgment to infer remaining details and proceed to draft.
4.  **Draft the Document:** Once the dialogue is complete (or Auto-generate is selected, or using auto-detected stack), generate the content for `tech-stack.md`.
    -   **If using auto-detected stack profile:**
        -   Map the stack profile fields to the tech-stack.md template:
            -   `primary_language` -> Primary Language section
            -   `languages` -> Languages section (with file counts if available)
            -   `frameworks` -> Frameworks section (grouped by category: Frontend, Backend, etc.)
            -   `build_tools` -> Build & Development section
            -   `testing_frameworks` -> Testing section
            -   `infrastructure` -> Infrastructure section
            -   `package_manager` -> Package Manager section
        -   Include the confidence level as a comment: `<!-- Auto-detected by Stack Detection Protocol (Confidence: [LEVEL]) -->`
    -   **If Auto-generate was chosen:** Use your best judgment to infer remaining details. You are encouraged to expand on the gathered details.
    -   **CRITICAL:** The source of truth is **only the user's selected answer(s)** or the auto-detected stack profile. DO NOT include conversational options in the final file.
5.  **User Confirmation Loop:** Present the drafted content to the user and use `AskUserQuestion` for review:
    -   First, display the drafted content in a markdown code block.
    -   Then use the tool:
        ```json
        {
          "questions": [{
            "question": "Does this tech stack document accurately reflect your project's technologies?",
            "header": "Review",
            "options": [
              {"label": "Approve", "description": "The document is correct, proceed to next step"},
              {"label": "Suggest changes", "description": "I want to modify some parts"}
            ],
            "multiSelect": false
          }]
        }
        ```
    -   **Loop:** If user selects "Suggest changes", ask what to modify, apply changes, and re-present for review. Break loop on "Approve".
6.  **Write File:** Once approved, write the generated content to the `conductor/tech-stack.md` file.
    -   **If stack was auto-detected:** Ensure the file includes at the top:
        ```markdown
        <!-- Auto-detected by Stack Detection Protocol -->
        <!-- Confidence: [HIGH/MEDIUM/LOW/UNCERTAIN] -->
        <!-- Detection timestamp: [ISO 8601 timestamp] -->
        ```
7.  **Commit State:** Upon successful creation of the file, use the CLI to record progress:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.3_tech_stack"
    ```
    **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
    `{"last_successful_step": "2.3_tech_stack"}`
8.  **Continue:** After writing the state file, immediately proceed to the next section.

### 2.4 Select Guides (Interactive)

**PROTOCOL REFERENCE:** This section applies the AI Template Generation Protocol defined in `${CLAUDE_PLUGIN_ROOT}/protocols/ai-template-generation.md`. All styleguides include AI Quick Reference sections optimized for AI consumption.

1.  **Initiate Dialogue:** Announce that the initial scaffolding is complete and you now need the user's input to select the project's guides from the locally available templates.
    > "The styleguide templates include AI Quick Reference sections at the top for rapid AI consumption, followed by detailed human documentation."

2.  **Select Code Style Guides:**
    -   List the available style guides by checking the plugin's templates directory at `${CLAUDE_PLUGIN_ROOT}/templates/code_styleguides/`.
    -   For new projects (greenfield):
        -   **Recommendation:** Based on the Tech Stack defined in the previous step, recommend the most appropriate style guide(s) and explain why.
        -   Use `AskUserQuestion` to ask about the selection:
            ```json
            {
              "questions": [{
                "question": "How would you like to proceed with the recommended style guides?",
                "header": "Styleguides",
                "options": [
                  {"label": "Use recommended", "description": "Include the style guides I recommended based on your tech stack"},
                  {"label": "Customize", "description": "Select from all available style guides"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   If user chooses "Customize":
            -   Present the list of all available guides and use `AskUserQuestion` with `multiSelect: true`:
            ```json
            {
              "questions": [{
                "question": "Which code style guides would you like to include?",
                "header": "Select",
                "options": [
                  {"label": "TypeScript", "description": "TypeScript/JavaScript style guide"},
                  {"label": "Python", "description": "Python style guide"},
                  {"label": "Go", "description": "Go style guide"}
                ],
                "multiSelect": true
              }]
            }
            ```
    -   For existing projects (brownfield):
        -   **Announce Selection:** Inform the user: "Based on the inferred tech stack, I will copy the following code style guides: <list of inferred guides>."
        -   Use `AskUserQuestion` to confirm:
            ```json
            {
              "questions": [{
                "question": "Would you like to proceed with the suggested code style guides?",
                "header": "Confirm",
                "options": [
                  {"label": "Yes, proceed", "description": "Use only the suggested style guides"},
                  {"label": "Add more", "description": "I want to include additional style guides"}
                ],
                "multiSelect": false
              }]
            }
            ```
    -   **Action - Use CLI for Template Copying:** Once the user has confirmed their selection, use the CLI to copy the styleguide templates:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages <lang1> <lang2> ...
        ```
        For example, if user selected Python and TypeScript:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages python typescript
        ```
    -   **Fallback:** If CLI is unavailable, manually construct and execute a command to create the directory and copy all selected files. For example: `mkdir -p conductor/code_styleguides && cp ${CLAUDE_PLUGIN_ROOT}/templates/code_styleguides/python.md ${CLAUDE_PLUGIN_ROOT}/templates/code_styleguides/javascript.md conductor/code_styleguides/`

3.  **Verify AI-Enhanced Content:**
    -   After copying, verify each styleguide contains:
        -   `## AI Quick Reference` header
        -   `### Language Rules` section
        -   `### Type Patterns` section (for typed languages)
        -   `### Avoid` section
    -   **Announce:** For each copied styleguide, announce: "Copied AI-enhanced styleguide: [styleguide-name].md (includes AI Quick Reference section)"

4.  **Commit State:** Upon successful completion of the copy command, use the CLI to record progress:
    ```bash
    python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.4_code_styleguides"
    ```
    **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
        `{"last_successful_step": "2.4_code_styleguides"}`

### 2.5 Select Workflow (Interactive)
1.  **Copy Initial Workflow:**
    -   Copy `${CLAUDE_PLUGIN_ROOT}/templates/workflow.md` to `conductor/workflow.md`.
2.  **Customize Workflow:**
    -   Use `AskUserQuestion` to ask about workflow customization:
        ```json
        {
          "questions": [{
            "question": "Do you want to use the default workflow or customize it? Default includes: 80% test coverage, commit after every task, Git Notes for summaries.",
            "header": "Workflow",
            "options": [
              {"label": "Use default (Recommended)", "description": "Use the standard workflow settings"},
              {"label": "Customize", "description": "Configure workflow settings individually"}
            ],
            "multiSelect": false
          }]
        }
        ```
    -   If user chooses "Customize":
        -   **Question 1 - Coverage:** Use `AskUserQuestion`:
            ```json
            {
              "questions": [{
                "question": "What minimum test code coverage should be required?",
                "header": "Coverage",
                "options": [
                  {"label": "80% (Recommended)", "description": "Industry standard coverage threshold"},
                  {"label": "70%", "description": "Lower threshold for faster development"},
                  {"label": "90%", "description": "Higher threshold for critical systems"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **Question 2 - Commit Frequency:** Use `AskUserQuestion`:
            ```json
            {
              "questions": [{
                "question": "When should changes be committed?",
                "header": "Commits",
                "options": [
                  {"label": "After each task (Recommended)", "description": "Granular commits for better history"},
                  {"label": "After each phase", "description": "Larger commits grouping related changes"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **Question 3 - Task Summary Storage:** Use `AskUserQuestion`:
            ```json
            {
              "questions": [{
                "question": "How should task summaries be recorded?",
                "header": "Summaries",
                "options": [
                  {"label": "Git Notes (Recommended)", "description": "Separate metadata that doesn't clutter commit messages"},
                  {"label": "Commit Message", "description": "Include summary directly in commit messages"}
                ],
                "multiSelect": false
              }]
            }
            ```
        -   **Action:** Update `conductor/workflow.md` based on the user's responses.
    -   **Commit State:** After the `workflow.md` file is successfully written or updated, use the CLI to record progress:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5_workflow"
        ```
        **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
        `{"last_successful_step": "2.5_workflow"}`

### 2.5.1 Documentation Generation (Brownfield Only)
**PROTOCOL: Generate Progressive Disclosure documentation based on approved analysis categories.**

**Skip Condition:** This section applies ONLY if `codebase_analyzed = true` AND `approved_categories` is not empty. Otherwise, skip to Section 2.6.

**Template Reference:** Use templates from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md.md` and `${CLAUDE_PLUGIN_ROOT}/templates/docs/`.

#### Step 1: Generate CLAUDE.md

1.  **Check for Existing CLAUDE.md:**
    -   Check if `CLAUDE.md` exists in the project root.
    -   If exists, set `merge_mode = true`.
    -   If not exists, set `merge_mode = false`.

2.  **Generate Project Overview:**
    -   Read `conductor/product.md` to extract:
        -   Project name (from first heading)
        -   Project description (from first paragraph or "Overview" section)
    -   Format as single paragraph summary.

3.  **Generate Quick Reference Rules:**
    -   From the analysis results stored in Section 2.0.2, extract the highest-confidence patterns.
    -   Select 5-10 key rules from approved categories, prioritizing:
        1. File naming conventions (from Code Conventions)
        2. Import patterns (from Code Conventions)
        3. Test file naming (from Testing)
        4. Error handling conventions (from API Patterns)
        5. Key architectural patterns (from Architecture)
    -   Format as bullet points:
        ```markdown
        ## Quick Reference

        Follow these core rules when working in this codebase:

        - **File naming:** Use kebab-case for all files (e.g., `user-profile.ts`)
        - **Imports:** Use absolute imports with `@/` alias
        - **Tests:** Co-locate tests using `.test.ts` suffix
        - **Errors:** Use custom exception classes (ValidationError, NotFoundError)
        - **API routes:** Use plural nouns with `/api/v1/` prefix
        ```

4.  **Generate Directory Structure:**
    -   From the directory structure analysis, create a simplified tree:
        ```markdown
        ## Project Structure

        ```
        src/
        ├── components/    # React components
        ├── services/      # Business logic
        ├── utils/         # Shared utilities
        └── types/         # TypeScript types
        ```
        ```

5.  **Generate Documentation Links:**
    -   For each category in `approved_categories`, add a link:
        ```markdown
        ## Detailed Documentation

        For detailed guidance on specific topics, see:

        - [Code Conventions](conductor/docs/code-conventions.md) - Naming, imports, organization
        - [Architecture](conductor/docs/architecture.md) - Design patterns, layers
        - [Testing](conductor/docs/testing.md) - Test patterns, framework usage
        - [API Patterns](conductor/docs/api-patterns.md) - REST conventions, errors
        - [Configuration](conductor/docs/configuration.md) - Config files, env vars
        ```

6.  **Handle CLAUDE.md Merge (if `merge_mode = true`):**
    -   Read existing `CLAUDE.md` content.
    -   Identify sections:
        -   **Auto-generated sections:** Marked with `<!-- AUTO-GENERATED -->` comments
        -   **User sections:** Everything after `<!-- USER SECTION -->` marker
    -   Merge strategy:
        -   Replace auto-generated sections with new content
        -   Preserve all user sections unchanged
        -   If no markers exist in old file, append new content after existing content with clear separator

7.  **Add Auto-Generated Markers:**
    -   Wrap generated sections with markers:
        ```markdown
        <!-- AUTO-GENERATED: This section was generated by Conductor setup -->
        <!-- Last analyzed: 2026-01-28T10:30:00Z -->

        [Generated content here]

        <!-- END AUTO-GENERATED -->
        ```

#### Step 2: Generate conductor/docs/ Files

1.  **Create Directory:**
    -   Create `conductor/docs/` directory if it doesn't exist.

2.  **Generate Category Files:**
    -   For each category in `approved_categories`:

    **code-conventions.md:**
    -   Include file naming patterns with examples from analysis
    -   Include import patterns with actual examples
    -   Include module organization patterns
    -   Add confidence indicator: `<!-- Confidence: HIGH -->`

    **architecture.md:**
    -   Include detected design patterns with file examples
    -   Include layer organization description
    -   Include dependency injection patterns
    -   Include state management (if frontend)

    **testing.md:**
    -   Include test framework and features
    -   Include test file naming with examples
    -   Include mocking patterns
    -   Include test organization structure

    **api-patterns.md:**
    -   Include REST conventions with endpoint examples
    -   Include response format structure
    -   Include error handling patterns
    -   Include versioning strategy

    **configuration.md:**
    -   Include configuration file locations
    -   Include environment variable patterns
    -   Include build tool configuration
    -   Include CI/CD pipeline structure

    **annotations.md:** (only if annotations were detected)
    -   Include custom decorators with usage examples
    -   Include documentation patterns
    -   Include framework decorators

3.  **Include Code Examples:**
    -   For each pattern, include actual code examples from the analysis:
        ```markdown
        ### File Naming

        **Convention:** kebab-case
        **Confidence:** HIGH

        **Examples from this codebase:**
        - `src/components/user-profile.tsx`
        - `src/services/api-client.ts`
        - `src/utils/date-formatter.ts`
        ```

4.  **Add Cross-References:**
    -   At the end of each file, add related documentation links:
        ```markdown
        ## Related Documentation

        - [Code Conventions](./code-conventions.md) - Naming and organization
        - [Architecture](./architecture.md) - Design patterns
        ```

5.  **Add Auto-Generated Markers:**
    -   Each file should start with:
        ```markdown
        <!-- AUTO-GENERATED: This file was generated by Conductor setup -->
        <!-- Last analyzed: 2026-01-28T10:30:00Z -->
        <!-- Confidence: HIGH -->
        ```

#### Step 3: User Confirmation

1.  **Present Generated Documentation:**
    -   Announce: "I have generated the following documentation based on your approved patterns:"
    -   List the files created:
        ```
        Generated Documentation:
        ├── CLAUDE.md (Progressive Disclosure overview)
        └── conductor/docs/
            ├── code-conventions.md (8 patterns)
            ├── architecture.md (5 patterns)
            ├── testing.md (6 patterns)
            ├── api-patterns.md (7 patterns)
            └── configuration.md (5 patterns)
        ```

2.  **Show CLAUDE.md Preview:**
    -   Display the Quick Reference section of CLAUDE.md for review:
        ```markdown
        ## Quick Reference Preview:

        - **File naming:** Use kebab-case for all files
        - **Imports:** Use absolute imports with @/ alias
        - [... rest of rules ...]
        ```

3.  **Request Confirmation:**
    -   Use `AskUserQuestion` to confirm:
        ```json
        {
          "questions": [{
            "question": "Does this generated documentation look correct?",
            "header": "Review",
            "options": [
              {"label": "Approve", "description": "Write the documentation files"},
              {"label": "Regenerate", "description": "Regenerate with different patterns"},
              {"label": "Skip", "description": "Skip documentation generation"}
            ],
            "multiSelect": false
          }]
        }
        ```

4.  **Handle Response:**
    -   **If "Approve":** Write all files and proceed.
    -   **If "Regenerate":** Return to Section 2.0.2.1 to re-select categories.
    -   **If "Skip":** Skip writing files and proceed to Section 2.6.

#### Step 4: Write Files

1.  **Write CLAUDE.md:**
    -   Write (or merge) to `CLAUDE.md` in project root.

2.  **Write conductor/docs/ Files:**
    -   Write each approved category file to `conductor/docs/`.

3.  **Commit State:**
    -   Use CLI to record progress:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5.1_docs_generated"
        ```
    -   **Fallback:** Manually write to `conductor/setup_state.json`:
        `{"last_successful_step": "2.5.1_docs_generated"}`

4.  **Continue:** Proceed to Section 2.6 (Finalization).

### 2.6 Finalization
1.  **Generate Index File:**
    -   Create `conductor/index.md` with the following content:
        ```markdown
        # Project Context

        ## Definition
        - [Product Definition](./product.md)
        - [Product Guidelines](./product-guidelines.md)
        - [Tech Stack](./tech-stack.md)

        ## Workflow
        - [Workflow](./workflow.md)
        - [Code Style Guides](./code_styleguides/)

        ## Documentation (if generated)
        - [Pattern Documentation](./docs/) - Auto-generated pattern docs

        ## Management
        - [Tracks Registry](./tracks.md)
        - [Tracks Directory](./tracks/)
        ```
    -   **Note:** Only include the "Documentation" section if `conductor/docs/` was generated in Section 2.5.1.
    -   **Announce:** "Created `conductor/index.md` to serve as the project context index."

2.  **Summarize Actions:** Present a summary of all actions taken during Phase 1, including:
    -   The guide files that were copied.
    -   The workflow file that was copied.
    -   The documentation files generated (if applicable): CLAUDE.md and conductor/docs/.
3.  **Transition to initial plan and track generation:** Announce that the initial setup is complete and you will now proceed to define the first track for the project.

---

## 3.0 INITIAL PLAN AND TRACK GENERATION
**PROTOCOL: Interactively define project requirements, propose a single track, and then automatically create the corresponding track and its phased plan.**

### 3.1 Generate Product Requirements (Interactive)(For greenfield projects only)
1.  **Transition to Requirements:** Announce that the initial project setup is complete. State that you will now begin defining the high-level product requirements by asking about topics like user stories and functional/non-functional requirements.
2.  **Analyze Context:** Read and analyze the content of `conductor/product.md` to understand the project's core concept.
3.  **Ask Questions Using AskUserQuestion Tool:** Use the `AskUserQuestion` tool to ask questions one at a time. Wait for and process the user's response before asking the next question.
    -   **CONSTRAINT:** Limit your inquiries to a maximum of 5 questions.
    -   **SUGGESTIONS:** For each question, generate 2-3 high-quality suggested options based on common patterns or context you already have.
    -   **General Guidelines:**
        -   **1. Classify Question Type:**
            -   **Additive:** Questions where multiple selections are valid (e.g., user stories, features). Use `multiSelect: true`.
            -   **Exclusive Choice:** Questions requiring a single answer (e.g., MVP scope decision). Use `multiSelect: false`.
        -   **2. Use AskUserQuestion Tool:** Structure each question:
            ```json
            {
              "questions": [{
                "question": "Which user stories should be prioritized for the initial release?",
                "header": "Stories",
                "options": [
                  {"label": "User login", "description": "Allow users to authenticate and access their account"},
                  {"label": "Dashboard", "description": "Central view showing key information and actions"},
                  {"label": "Auto-generate", "description": "Infer requirements from context and proceed"}
                ],
                "multiSelect": true
              }]
            }
            ```
        -   **3. Interaction Flow:**
            -   **CRITICAL:** Ask questions sequentially (one at a time). Wait for user response before next question.
            -   Always include an "Auto-generate" option.
            -   Confirm understanding by summarizing before moving on.
    -   **AUTO-GENERATE LOGIC:** If user selects "Auto-generate", immediately stop asking questions. Use your best judgment to infer remaining details based on previous answers and project context.
-   **CRITICAL:** The source of truth is **only the user's selected answer(s)**. This gathered information will be used in subsequent steps. DO NOT include conversational options in the gathered information.
4.  **Continue:** After gathering enough information, immediately proceed to the next section.

### 3.2 Propose a Single Initial Track (Automated + Approval)
1.  **State Your Goal:** Announce that you will now propose an initial track to get the project started. Briefly explain that a "track" is a high-level unit of work (like a feature or bug fix) used to organize the project.
2.  **Generate Track Title:** Analyze the project context (`product.md`, `tech-stack.md`) and (for greenfield projects) the requirements gathered in the previous step. Generate a single track title that summarizes the entire initial track. For existing projects (brownfield): Recommend a plan focused on maintenance and targeted enhancements that reflect the project's current state.
    - Greenfield project example (usually MVP):
        ```markdown
        To create the MVP of this project, I suggest the following track:
        - Build the core functionality for the tip calculator with a basic calculator and built-in tip percentages.
        ```
    - Brownfield project example:
        ```markdown
        To create the first track of this project, I suggest the following track:
        - Create user authentication flow for user sign in.
        ```
3.  **User Confirmation:** Present the generated track title and use `AskUserQuestion` for approval:
    ```json
    {
      "questions": [{
        "question": "Does this proposed track align with your priorities for the initial work?",
        "header": "Track",
        "options": [
          {"label": "Approve", "description": "Proceed with this track as the initial work item"},
          {"label": "Different track", "description": "I want to start with a different track"}
        ],
        "multiSelect": false
      }]
    }
    ```
    -   If user selects "Different track", they can specify via "Other" input what track to start with.

### 3.3 Convert the Initial Track into Artifacts (Automated)
1.  **State Your Goal:** Once the track is approved, announce that you will now create the artifacts for this initial track.
2.  **Initialize Tracks File:** Create the `conductor/tracks.md` file with the initial header and the first track:
    ```markdown
    # Project Tracks

    This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

    ---

    - [ ] **Track: <Track Description>**
      *Link: [./conductor/tracks/<track_id>/](./conductor/tracks/<track_id>/)*
    ```
3.  **Generate Track Artifacts:**
    a. **Define Track:** The approved title is the track description.
    b. **Generate Track-Specific Spec & Plan:**
        i. Automatically generate a detailed `spec.md` for this track.
        ii. Automatically generate a `plan.md` for this track.
            - **CRITICAL:** The structure of the tasks must adhere to the principles outlined in the workflow file at `conductor/workflow.md`. For example, if the workflow specificies Test-Driven Development, each feature task must be broken down into a "Write Tests" sub-task followed by an "Implement Feature" sub-task.
            - **CRITICAL:** Include status markers `[ ]` for **EVERY** task and sub-task. The format must be:
                - Parent Task: `- [ ] Task: ...`
                - Sub-task: `    - [ ] ...`
            - **CRITICAL: Inject Phase Completion Tasks.** You MUST read the `conductor/workflow.md` file to determine if a "Phase Completion Verification and Checkpointing Protocol" is defined. If this protocol exists, then for each **Phase** that you generate in `plan.md`, you MUST append a final meta-task to that phase. The format for this meta-task is: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`. You MUST replace `<Phase Name>` with the actual name of the phase.
    c. **Create Track Artifacts:**
        i. **Generate and Store Track ID:** Create a unique Track ID from the track description using format `shortname_YYYYMMDD` and store it. You MUST use this exact same ID for all subsequent steps for this track.
        ii. **Create Single Directory:** Using the stored Track ID, create a single new directory: `conductor/tracks/<track_id>/`.
        iii. **Create `metadata.json`:** In the new directory, create a `metadata.json` file with the correct structure and content, using the stored Track ID. An example is:
            - ```json
            {
            "track_id": "<track_id>",
            "type": "feature", // or "bug"
            "status": "new", // or in_progress, completed, cancelled
            "created_at": "YYYY-MM-DDTHH:MM:SSZ",
            "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
            "description": "<Initial user description>"
            }
            ```
        Populate fields with actual values. Use the current timestamp.
        iv. **Write Spec and Plan Files:** In the exact same directory, write the generated `spec.md` and `plan.md` files.
        v.  **Write Index File:** In the exact same directory, write `index.md` with content:
            ```markdown
            # Track <track_id> Context

            - [Specification](./spec.md)
            - [Implementation Plan](./plan.md)
            - [Metadata](./metadata.json)
            ```

    d. **Commit State:** After all track artifacts have been successfully written, use the CLI to record progress:
        ```bash
        python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "3.3_initial_track_generated"
        ```
        **Fallback:** If CLI is unavailable, manually write to `conductor/setup_state.json` with the exact content:
       `{"last_successful_step": "3.3_initial_track_generated"}`

    e. **Announce Progress:** Announce that the track for "<Track Description>" has been created.

### 3.4 Final Announcement
1.  **Announce Completion:** After the track has been created, announce that the project setup and initial track generation are complete.
2.  **Save Conductor Files:** Add and commit all files with the commit message `conductor(setup): Add conductor setup files`.
3.  **Next Steps:** Inform the user that they can now begin work by running `/conductor:implement`.
