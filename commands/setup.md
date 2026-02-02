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
  - Task
---

# Context

!`python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --get 2>/dev/null; python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup detect`

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to set up and manage a software project using the Conductor methodology. Adhere to these instructions precisely and sequentially.

CRITICAL: Validate the success of every tool call. If any fails, halt immediately and await user instructions.

---

## Action CLI Commands

```bash
# Create conductor directory structure
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold

# Record setup progress
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "STEP_NAME"

# Copy code styleguides
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages LANG1 LANG2
```

### Fallback Instructions

If context injection fails:
1. **State check:** Read `conductor/setup_state.json` if it exists
2. **Project detection:** Check for `.git`, `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `src/`, `app/`, `lib/`

---

## AskUserQuestion Tool Protocol

**Full Pattern Reference:** `templates/askuserquestion-patterns.md`

### Quick Reference

| Rule | Constraint |
|------|------------|
| Header | Max 12 characters |
| Options | 2-4 per question |
| Sequential | One question at a time |
| multiSelect | `true` for additive, `false` for exclusive |

### Question Types

| Type | multiSelect | Use Case |
|------|-------------|----------|
| Additive | `true` | Multiple valid answers (users, features) |
| Exclusive | `false` | Single answer (language, framework) |
| Approval | `false` | Document review (Approve/Suggest changes) |
| Confirmation | `false` | Yes/No decisions |

### Auto-Generate Behavior

When user selects "Auto-generate": stop asking questions, use context to infer remaining details, generate document, present for approval.

---

## 1.1 RESUME CHECK

**PROTOCOL: Check setup state and resume from last successful step.**

1. **Parse Injected Context:** Check for `last_successful_step` in first JSON object from `# Context` section.

2. **Resume Mapping:**

| State Value | Resume Action |
|-------------|---------------|
| `2.0.2_analysis` | Skip to Section 2.1 |
| `2.1_product_guide` | Skip to Section 2.2 |
| `2.2_product_guidelines` | Skip to Section 2.3 |
| `2.3_tech_stack` | Skip to Section 2.4 |
| `2.4_code_styleguides` | Skip to Section 2.5 |
| `2.5_workflow` | Skip to Section 2.5.1 (brownfield) or 2.6 (greenfield) |
| `2.5.1_docs_generated` | Skip to Section 2.6 |
| `3.3_initial_track_generated` | Announce complete, halt. Use `/conductor:newTrack` or `/conductor:implement` |

3. **New Project:** If no state JSON returned, proceed to Section 1.2.

---

## 1.2 PRE-INITIALIZATION OVERVIEW

Present to user:
> "Welcome to Conductor. I will guide you through:
> 1. **Project Discovery:** Analyze directory to determine new or existing project
> 2. **Product Definition:** Define vision, guidelines, and technology stack
> 3. **Configuration:** Select code style guides and workflow
> 4. **Track Generation:** Create initial track with detailed plan
>
> Let's get started!"

---

## 2.0 PROJECT INCEPTION

### 2.0.1 Detect Project Maturity

1. **Use Injected Context:** Parse detection JSON from `# Context` section containing:
   - `project_type`: "brownfield" or "greenfield"
   - `languages`, `frameworks`, `ecosystems`, `indicators`

2. **Execute Based on Maturity:**

   **Brownfield:**
   - Announce existing project detected
   - If `indicators.has_uncommitted_changes`: warn user to commit/stash
   - Request read-only scan permission using AskUserQuestion (Confirmation type)
   - If denied: halt and await instructions
   - If approved: proceed to Section 2.0.2

   **Greenfield:**
   - Announce new project initialization
   - If no `.git`: run `git init`
   - Ask: "What do you want to build?"
   - Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold`
   - Initialize state: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set ""`
   - Write response to `conductor/product.md` under `# Initial Concept`
   - Proceed to Section 2.1

### 2.0.2 Automatic Stack Detection (Brownfield Only)

**Full Protocol Reference:** `protocols/stack-detection.md`

1. **Use Injected Context:** The detection results contain `languages`, `frameworks`, `ecosystems` from `# Context`.

2. **Present Detection Results:**

   Format by confidence level (HIGH/MEDIUM/LOW/UNCERTAIN):
   ```
   **Stack Detection Results** (Confidence: [LEVEL])

   **Primary Language:** [detected]
   **Frameworks:** [list]
   **Build Tools:** [list]
   ```

3. **User Confirmation:** Use AskUserQuestion with options: Accept / Edit / Skip
   - **Accept:** Store profile, set `stack_auto_detected = true`
   - **Edit:** Present each category for verification
   - **Skip:** Set `stack_auto_detected = false`

4. **Continue:** Proceed to Section 2.0.3.

### 2.0.3 Codebase Analysis (Brownfield Only)

**Full Protocol Reference:** `protocols/codebase-analysis.md`

#### Agent-Based Pattern Detection (Preferred)

Launch 4 `codebase-pattern-detector` agents in parallel using the Task tool:

| Agent | Operation | Scope |
|-------|-----------|-------|
| 1 | `naming-conventions` | src/, lib/, app/ |
| 2 | `architecture` | src/, lib/, app/ |
| 3 | `testing-patterns` | src/, lib/, app/, tests/ |
| 4 | `api-conventions` | src/, lib/, app/ |

Each agent prompt includes:
```json
{
  "operation": "<operation>",
  "scope": {
    "directories": ["src/", "lib/", "app/", "pkg/"],
    "exclude": ["node_modules/", "dist/", "vendor/", "build/", ".git/"]
  },
  "context": {"tech_stack": "<detected stack>"}
}
```

Merge `patterns` objects from all agents. If any agent fails, fall back to Inline Mode per protocol.

#### Consolidated Pattern Review

1. **Present Summary:** Display all detected patterns grouped by category with confidence levels

2. **User Category Selection:** Use AskUserQuestion with multiSelect to select which categories to document:
   - All categories (Recommended)
   - Individual categories (Code Conventions, Architecture, Testing, API Patterns, Configuration)

3. **Handle Selection:**
   - Store `approved_categories` array
   - If none selected: skip documentation generation

4. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.0.2_analysis"
   ```

5. **Continue:** Proceed to Section 2.1.

---

## 2.1 Generate Product Guide (Interactive)

**Pattern Examples:** See `templates/askuserquestion-patterns.md`

1. **Announce:** "I will now help create `product.md`."

2. **Questioning Phase:**
   - Ask up to 5 questions sequentially
   - Generate 2-3 suggested options per question
   - Topics: Target users, goals, features
   - Always include "Auto-generate" option
   - **Brownfield:** Ask context-aware questions based on code analysis

3. **Draft Document:** Generate comprehensive `product.md` content

4. **User Confirmation:** Use Approval pattern (Approve/Suggest changes loop)

5. **Write File:** Append to `conductor/product.md`, preserving `# Initial Concept`

6. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.1_product_guide"
   ```

---

## 2.2 Generate Product Guidelines (Interactive)

1. **Announce:** "I will now help create `product-guidelines.md`."

2. **Questioning Phase:**
   - Ask up to 5 questions (prose style, brand messaging, visual identity)
   - Include "Auto-generate" option

3. **Draft, Confirm, Write:** Same pattern as Section 2.1

4. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.2_product_guidelines"
   ```

---

## 2.3 Generate Tech Stack (Interactive)

1. **Check Auto-Detection:** If `stack_auto_detected = true`, skip questions and use stored profile.

2. **Questioning Phase (if not auto-detected):**
   - Ask up to 5 questions (languages, frameworks, databases)
   - **Brownfield:** Confirm inferred stack rather than propose changes

3. **Draft Document:** Map to tech-stack.md sections:
   - Primary Language, Languages, Frameworks, Build & Development, Testing, Infrastructure

4. **User Confirmation:** Use Approval pattern

5. **Write File:** Write to `conductor/tech-stack.md`
   - If auto-detected, include confidence comment at top

6. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.3_tech_stack"
   ```

---

## 2.4 Select Style Guides (Interactive)

**Template Reference:** `protocols/ai-template-generation.md`

1. **List Available Guides:** Check `${CLAUDE_PLUGIN_ROOT}/templates/code_styleguides/`

2. **Selection Flow:**
   - **Greenfield:** Recommend based on tech stack, offer customize option
   - **Brownfield:** Announce inferred guides, confirm or add more

3. **Copy Templates:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages <lang1> <lang2>
   ```

4. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.4_code_styleguides"
   ```

---

## 2.5 Select Workflow (Interactive)

1. **Copy Initial Workflow:** Copy `${CLAUDE_PLUGIN_ROOT}/templates/workflow.md` to `conductor/workflow.md`

2. **Customize:** Use AskUserQuestion (Use default / Customize)
   - If Customize: ask about coverage (80%/70%/90%), commit frequency, task summary storage

3. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5_workflow"
   ```

---

## 2.5.1 Documentation Generation (Brownfield Only)

**Skip Condition:** Only execute if `codebase_analyzed = true` AND `approved_categories` is not empty.

### Execution Steps

1. **Generate Product Guidelines Update:**
   - Add Quick Reference section with 5-10 key rules from approved categories
   - Add Project Structure section
   - Add links to detailed docs

2. **Generate conductor/docs/ Files:**
   - Create files for each approved category
   - Include code examples from analysis
   - Add confidence indicators

3. **User Confirmation:** Present file list and Quick Reference preview

4. **Write Files:** Write all approved documentation

5. **Commit State:**
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5.1_docs_generated"
   ```

---

## 2.6 Finalization

1. **Generate Index:** Create `conductor/index.md` with links to all context files

2. **Summarize:** List all created files and actions taken

3. **Transition:** Announce proceeding to initial track generation

---

## 3.0 INITIAL TRACK GENERATION

### 3.1 Generate Product Requirements (Greenfield Only)

1. **Analyze Context:** Read `conductor/product.md` and `conductor/tech-stack.md`

2. **Questioning Phase:** Ask up to 5 questions about user stories and requirements

3. **Continue:** Proceed to Section 3.2

### 3.2 Propose Initial Track

1. **Generate Track Title:** Analyze context and propose single initial track
   - **Greenfield:** Usually MVP-focused
   - **Brownfield:** Maintenance or targeted enhancement

2. **User Confirmation:** Use Approval pattern (Approve/Different track)

### 3.3 Create Track Artifacts

**PROTOCOL: Use CLI commands for operations. Fall back to manual if CLI fails.**

| Step | CLI Command | Fallback |
|------|-------------|----------|
| 1. Generate ID | - | Manual: `shortname_YYYYMMDD` |
| 2. Create Directory | - | `mkdir -p conductor/tracks/<track_id>/` |
| 3. Create Files | Write tool | index.md, metadata.json, spec.md, plan.md |
| 4. Initialize Tracks | Write tool | Create `conductor/tracks.md` |

**Plan Generation Rules:**
- Follow `conductor/workflow.md` methodology (TDD if specified)
- Include status markers `[ ]` for all tasks
- Append verification task to each phase: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

**Commit State:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "3.3_initial_track_generated"
```

### 3.4 Final Announcement

1. **Stage and Commit:**
   ```bash
   git add conductor/
   git commit -m "conductor(setup): Add conductor setup files"
   ```

2. **Next Steps:** Inform user to run `/conductor:implement`
