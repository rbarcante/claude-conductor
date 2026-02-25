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

<system_directive>

## 1.0 SYSTEM DIRECTIVE

You are an AI agent. Set up and manage a software project using the Conductor methodology. Adhere to these instructions precisely and sequentially.

<note type="critical">
CRITICAL: Validate every tool call. If any fails, halt immediately and await user instructions.
</note>

</system_directive>

---

<cli_reference>

## CLI Reference

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "STEP_NAME"
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages LANG1 LANG2
```

**Fallback:** If context injection fails: read `conductor/setup_state.json` for state, check for `.git`, `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `src/`, `app/`, `lib/` for project detection.

</cli_reference>

---

<protocol name="askuserquestion">

## AskUserQuestion Protocol

**Full Reference:** `templates/askuserquestion-patterns.md`

| Rule | Constraint |
|------|------------|
| Header | Max 12 characters |
| Options | 2-4 per question |
| Sequential | One question at a time |
| multiSelect | `true` for additive, `false` for exclusive |

**Auto-Generate Behavior:** When user selects "Auto-generate", stop asking questions, use context to infer remaining details, generate document, present for approval.

</protocol>

---

<phase name="resume_check">

## 1.1 RESUME CHECK

1. **Parse Injected Context:** Check for `last_successful_step` in first JSON object from `# Context`.

2. **Resume Mapping:**

| State Value | Resume Action |
|-------------|---------------|
| `2.0.2_analysis` | Skip to Section 2.1 |
| `2.1_product_guide` | Skip to Section 2.2 |
| `2.2_product_guidelines` | Skip to Section 2.3 |
| `2.3_tech_stack` | Skip to Section 2.4 |
| `2.4_code_styleguides` | Skip to Section 2.5 |
| `2.5_workflow` | Skip to 2.5.1 (brownfield) or 2.6 (greenfield) |
| `2.5.1_docs_generated` | Skip to Section 2.6 |
| `3.3_initial_track_generated` | Announce complete, halt. Use `/conductor:newTrack` or `/conductor:implement` |

3. **New Project:** If no state JSON returned, proceed to Section 1.2.

</phase>

---

<phase name="pre_init">

## 1.2 PRE-INITIALIZATION

Present:
> "Welcome to Conductor. I will guide you through:
> 1. **Project Discovery:** Analyze directory to determine new or existing project
> 2. **Product Definition:** Define vision, guidelines, and technology stack
> 3. **Configuration:** Select code style guides and workflow
> 4. **Track Generation:** Create initial track with detailed plan
>
> Let's get started!"

</phase>

---

<phase name="inception">

## 2.0 PROJECT INCEPTION

### 2.0.1 Detect Project Maturity

Parse detection JSON from `# Context` containing `project_type`, `languages`, `frameworks`, `ecosystems`, `indicators`.

**Brownfield:**
- Announce existing project detected
- If `indicators.has_uncommitted_changes`: warn to commit/stash
- Request read-only scan permission (Confirmation pattern)
- If denied: halt. If approved: proceed to 2.0.2

**Greenfield:**
- Announce new project initialization
- If no `.git`: run `git init`
- Ask: "What do you want to build?"
- Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup scaffold`
- Initialize state: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set ""`
- Write response to `conductor/product.md` under `# Initial Concept`
- Proceed to Section 2.1

### 2.0.2 Automatic Stack Detection (Brownfield Only)

**Full Reference:** `protocols/stack-detection.md`

1. Use `languages`, `frameworks`, `ecosystems` from injected context
2. Present results formatted by confidence (HIGH/MEDIUM/LOW):
   ```
   **Stack Detection Results** (Confidence: [LEVEL])
   **Primary Language:** [detected]
   **Frameworks:** [list]
   **Build Tools:** [list]
   ```
3. AskUserQuestion: Accept / Edit / Skip
   - Accept → store profile, set `stack_auto_detected = true`
   - Edit → present each category for verification
   - Skip → set `stack_auto_detected = false`
4. Proceed to 2.0.3

### 2.0.3 Codebase Analysis (Brownfield Only)

**Full Reference:** `protocols/codebase-analysis.md`

Launch 4 `codebase-pattern-detector` agents in parallel:

| Agent | Operation | Scope |
|-------|-----------|-------|
| 1 | `naming-conventions` | src/, lib/, app/ |
| 2 | `architecture` | src/, lib/, app/ |
| 3 | `testing-patterns` | src/, lib/, app/, tests/ |
| 4 | `api-conventions` | src/, lib/, app/ |

Each receives: `{ "operation": "<op>", "scope": { "directories": [...], "exclude": ["node_modules/", "dist/", "vendor/", "build/", ".git/"] }, "context": {"tech_stack": "<detected>"} }`

Merge `patterns` from all agents. If any fails, fall back to inline per protocol.

**Pattern Review:**
1. Present all detected patterns grouped by category with confidence levels
2. AskUserQuestion (multiSelect): select categories to document (All recommended, or individual)
3. Store `approved_categories` array
4. Commit state: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.0.2_analysis"`
5. Proceed to Section 2.1

</phase>

---

<phase name="product_guide">

## 2.1 Generate Product Guide

1. Announce: "I will now help create `product.md`."
2. Ask up to 5 sequential questions (target users, goals, features). Include "Auto-generate" option. Brownfield: context-aware questions.
3. Draft comprehensive `product.md` content
4. User confirmation (Approval pattern: Approve / Suggest changes)
5. Write to `conductor/product.md`, preserving `# Initial Concept`
6. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.1_product_guide"`

</phase>

---

<phase name="product_guidelines">

## 2.2 Generate Product Guidelines

1. Announce: "I will now help create `product-guidelines.md`."
2. Ask up to 5 questions (prose style, brand messaging, visual identity). Include "Auto-generate" option.
3. Draft, confirm (Approval pattern), write to `conductor/product-guidelines.md`
4. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.2_product_guidelines"`

</phase>

---

<phase name="tech_stack">

## 2.3 Generate Tech Stack

1. If `stack_auto_detected = true`: skip questions, use stored profile
2. Otherwise: ask up to 5 questions (languages, frameworks, databases). Brownfield: confirm inferred stack.
3. Draft tech-stack.md (sections: Primary Language, Frameworks, Build & Development, Testing, Infrastructure)
4. User confirmation (Approval pattern)
5. Write to `conductor/tech-stack.md` (auto-detected: include confidence comment)
6. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.3_tech_stack"`

</phase>

---

<phase name="style_guides">

## 2.4 Select Style Guides

**Template Reference:** `protocols/ai-template-generation.md`

1. List available guides from `${CLAUDE_PLUGIN_ROOT}/templates/code_styleguides/`
2. **Greenfield:** recommend based on tech stack, offer customize. **Brownfield:** announce inferred, confirm or add.
3. Copy: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup copy-templates --languages <lang1> <lang2>`
4. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.4_code_styleguides"`

</phase>

---

<phase name="workflow">

## 2.5 Select Workflow

1. Copy `${CLAUDE_PLUGIN_ROOT}/templates/workflow.md` to `conductor/workflow.md`
2. AskUserQuestion: Use default / Customize
   - Customize: ask about coverage (80%/70%/90%), commit frequency, task summary storage
3. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5_workflow"`

</phase>

---

<phase name="docs_generation">

## 2.5.1 Documentation Generation (Brownfield Only)

**Skip if** `codebase_analyzed != true` OR `approved_categories` is empty.

1. Generate Product Guidelines update: Quick Reference (5-10 rules), Project Structure, links
2. Generate `conductor/docs/` files for each approved category with code examples and confidence indicators
3. User confirmation: present file list and Quick Reference preview
4. Write all approved documentation
5. State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "2.5.1_docs_generated"`

</phase>

---

<phase name="finalization">

## 2.6 Finalization

1. Generate `conductor/index.md` with links to all context files
2. Summarize all created files and actions
3. Announce proceeding to initial track generation

</phase>

---

<phase name="track_generation">

## 3.0 INITIAL TRACK GENERATION

### 3.1 Product Requirements (Greenfield Only)

1. Read `conductor/product.md` and `conductor/tech-stack.md`
2. Ask up to 5 questions about user stories and requirements
3. Proceed to 3.2

### 3.2 Propose Initial Track

1. Analyze context, propose single initial track
   - **Greenfield:** MVP-focused. **Brownfield:** maintenance or targeted enhancement.
2. User confirmation (Approval pattern: Approve / Different track)

### 3.3 Create Track Artifacts

| Step | Action | Fallback |
|------|--------|----------|
| 1. Generate ID | `shortname_YYYYMMDD` | Manual |
| 2. Create directory | `mkdir -p conductor/tracks/<track_id>/` | Manual |
| 3. Create files | Write tool: index.md, metadata.json, spec.md, plan.md | Manual |
| 4. Init tracks registry | Write tool: `conductor/tracks.md` | Manual |

**Plan rules:** Follow `conductor/workflow.md` methodology (TDD if specified). Include `[ ]` markers. Append verification task per phase: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

State: `python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json setup state --set "3.3_initial_track_generated"`

### 3.4 Final Announcement

1. Stage and commit:
   ```bash
   git add conductor/
   git commit -m "conductor(setup): Add conductor setup files"
   ```
2. Inform user to run `/conductor:implement`

</phase>
