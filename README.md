# Conductor Plugin for Claude Code

**Measure twice, code once.**

Conductor is a Claude Code plugin that enables **Context-Driven Development**. It turns Claude Code into a proactive project manager that follows a strict protocol to specify, plan, and implement software features and bug fixes.

Instead of just writing code, Conductor ensures a consistent, high-quality lifecycle for every task: **Context -> Spec & Plan -> Implement**.

The philosophy behind Conductor is simple: control your code. By treating context as a managed artifact alongside your code, you transform your repository into a single source of truth that drives every agent interaction with deep, persistent project awareness.

## Features

- **Plan before you build**: Create specs and plans that guide the agent for new and existing codebases.
- **Maintain context**: Ensure AI follows style guides, tech stack choices, and product goals.
- **Iterate safely**: Review plans before code is written, keeping you firmly in the loop.
- **Work as a team**: Set project-level context for your product, tech stack, and workflow preferences that become a shared foundation for your team.
- **Build on existing projects**: Intelligent initialization for both new (Greenfield) and existing (Brownfield) projects.
- **Smart revert**: A git-aware revert command that understands logical units of work (tracks, phases, tasks) rather than just commit hashes.
- **Universal File Resolution Protocol (UFRP)**: Flexible file organization with dynamic path resolution via index files, allowing customization of your project structure.
- **Pattern Reference Layer**: Reusable best-practice patterns that are automatically surfaced during implementation based on task context.
- **Quality Intelligence**: Automated anti-pattern detection and coverage analysis with actionable test suggestions during implementation.

## Installation

Install the Conductor plugin by copying it to your Claude Code plugins directory:

```bash
# Option 1: Project-specific installation
cp -r conductor-plugin ~/.claude/plugins/conductor

# Option 2: Use with --plugin-dir flag
cc --plugin-dir /path/to/conductor-plugin
```

## Usage

Conductor is designed to manage the entire lifecycle of your development tasks.

**Note on Token Consumption:** Conductor's context-driven approach involves reading and analyzing your project's context, specifications, and plans. This can lead to increased token consumption, especially in larger projects or during extensive planning and implementation phases.

### 1. Set Up the Project (Run Once)

When you run `/conductor:setup`, Conductor helps you define the core components of your project context. This context is then used for building new components or features by you or anyone on your team.

- **Product**: Define project context (e.g. users, product goals, high-level features).
- **Product guidelines**: Define standards (e.g. prose style, brand messaging, visual identity).
- **Tech stack**: Configure technical preferences (e.g. language, database, frameworks).
- **Workflow**: Set team preferences (e.g. TDD, commit strategy). Uses [workflow.md](templates/workflow.md) as a customizable template.

**Generated Artifacts:**
- `conductor/product.md`
- `conductor/product-guidelines.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`
- `conductor/code_styleguides/`
- `conductor/tracks.md`
- `conductor/index.md` (navigation index)

```bash
/conductor:setup
```

### 2. Start a New Track (Feature or Bug)

When you're ready to take on a new feature or bug fix, run `/conductor:newTrack`. This initializes a **track** — a high-level unit of work. Conductor helps you generate two critical artifacts:

- **Specs**: The detailed requirements for the specific job. What are we building and why?
- **Plan**: An actionable to-do list containing phases, tasks, and sub-tasks.

**Generated Artifacts:**
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/metadata.json`
- `conductor/tracks/<track_id>/index.md` (track navigation index)

```bash
/conductor:newTrack
# OR with a description
/conductor:newTrack "Add a dark mode toggle to the settings page"
```

### 3. Implement the Track

Once you approve the plan, run `/conductor:implement`. Your coding agent then works through the `plan.md` file, checking off tasks as it completes them.

**Updated Artifacts:**
- `conductor/tracks.md` (Status updates)
- `conductor/tracks/<track_id>/plan.md` (Status updates)
- Project context files (Synchronized on completion)

```bash
/conductor:implement
```

Conductor will:
1.  Select the next pending task.
2.  Follow the defined workflow (e.g., TDD: Write Test -> Fail -> Implement -> Pass).
3.  Update the status in the plan as it progresses.
4.  **Verify Progress**: Guide you through a manual verification step at the end of each phase to ensure everything works as expected.

During implementation, you can also:

- **Check status**: Get a high-level overview of your project's progress.
  ```bash
  /conductor:status
  ```
- **Revert work**: Undo a feature or a specific task if needed.
  ```bash
  /conductor:revert
  ```

## Commands Reference

| Command | Description | Artifacts |
| :--- | :--- | :--- |
| `/conductor:setup` | Scaffolds the project and sets up the Conductor environment. Run this once per project. | `conductor/product.md`<br>`conductor/product-guidelines.md`<br>`conductor/tech-stack.md`<br>`conductor/workflow.md`<br>`conductor/tracks.md`<br>`conductor/index.md` |
| `/conductor:newTrack` | Starts a new feature or bug track. Generates `spec.md` and `plan.md`. | `conductor/tracks/<id>/spec.md`<br>`conductor/tracks/<id>/plan.md`<br>`conductor/tracks/<id>/index.md`<br>`conductor/tracks.md` |
| `/conductor:implement` | Executes the tasks defined in the current track's plan. | `conductor/tracks.md`<br>`conductor/tracks/<id>/plan.md` |
| `/conductor:status` | Displays the current progress of the tracks file and active tracks. | Reads `conductor/tracks.md` |
| `/conductor:revert` | Reverts a track, phase, or task by analyzing git history. | Reverts git history |
| `/conductor:patterns` | Browse and search the Pattern Reference Layer. | Reads `patterns/index.md` |

## Pattern Reference Layer

Conductor includes a Pattern Reference Layer - a library of reusable best-practice patterns that are automatically surfaced during implementation based on task context.

### How It Works

When you run `/conductor:implement`, Conductor analyzes each task description and matches it against pattern activation keywords. If relevant patterns are found, they're surfaced before you begin the task:

```
📚 **Relevant Patterns Detected:**

1. **Error Handling** (patterns/core/error-handling.md)
   > Exception handling, error propagation, user-friendly messages

[Apply patterns? (Y)es / (S)kip / (V)iew first]
```

### Core Patterns

The following patterns are included out of the box:

| Pattern | Description |
| :--- | :--- |
| Error Handling | Exception handling, error propagation, user-friendly messages |
| Logging | Log levels, structured logging, context inclusion |
| Configuration | Config management, environment variables, secrets handling |
| Validation | Input validation, schema validation, error messages |
| Testing | Test structure, mocking, assertions, coverage strategies |

### Browse Patterns

Use the patterns command to explore available patterns:

```bash
# List all patterns
/conductor:patterns list

# Search for patterns by keyword
/conductor:patterns search validation

# View a specific pattern
/conductor:patterns show error-handling
```

### Adding Custom Patterns

Create new patterns in `patterns/core/` or `patterns/stack/` using the template at `patterns/TEMPLATE.md`. Each pattern includes:

- **YAML Frontmatter**: Metadata and activation keywords
- **AI Quick Reference**: Concise guidance for the AI agent
- **Human Documentation**: Detailed explanations and examples
- **Anti-Patterns**: Common mistakes to avoid

## Technology Intelligence

Conductor includes intelligent technology detection and skill activation capabilities that enhance the development experience.

### Automatic Stack Detection

For brownfield (existing) projects, Conductor automatically detects your technology stack during setup:

- **Primary Language**: Based on manifest files and file extensions
- **Frameworks**: From dependency analysis (React, Express, Django, FastAPI, etc.)
- **Build Tools**: Package managers and build systems
- **Testing Frameworks**: Detected from dev dependencies

Detection confidence levels:
- **HIGH**: Manifest files with matching dependencies found (score >= 85)
- **MEDIUM**: Partial matches detected (score 60-84)
- **LOW**: Limited signals available (score 30-59)
- **UNCERTAIN**: Minimal signals, manual specification recommended (score < 30)

#### Example Detection Output

```
🔍 **Stack Detection Results** (Confidence: HIGH)
Stack detection is highly confident in these results.

**Primary Language:** TypeScript
**Languages Detected:** TypeScript, JavaScript
**Frameworks:** React (Frontend), Express.js (Backend)
**Build Tools:** npm, Vite
**Testing:** Vitest, Playwright
**Package Manager:** npm
```

After detection, you can:
- **Accept** the detected values
- **Edit** specific categories
- **Skip** and enter manually

### Skill Activation System

Skills provide context-aware guidance during implementation. They're automatically activated based on your task context:

- **Always-Active Skills**: Core methodology loaded for every task (e.g., Conductor Methodology)
- **Context-Activated Skills**: Matched based on task keywords, tech stack, and file patterns

#### Activation Scoring

Skills are scored based on multiple factors:

| Match Type | Score |
|:-----------|:------|
| Keyword match | +1.0 |
| File pattern match | +1.5 |
| Language match | +2.0 |
| Framework match | +1.5 |
| Tool match | +1.0 |

Skills with a score >= 1.5 are activated (maximum 5 per task, plus always-active).

#### Skill Announcement

When running `/conductor:implement`, activated skills are announced:

```
🔧 **Skills Activated for This Track:**

**Always Active:**
- Conductor Methodology: Core development workflow guidance

**Context-Activated:** (based on track/task matching)
- React Best Practices (score: 3.5): Component patterns, hooks usage, state management
```

### Creating Custom Skills

See `/docs/skill-manifest-schema.md` for creating custom skills. Each skill includes:

- **manifest.json**: Metadata and activation rules
- **SKILL.md**: Guidance content for the AI agent

## Quality Intelligence

Conductor includes intelligent quality gates that automatically analyze code for common anti-patterns and provide actionable coverage suggestions during implementation.

### Anti-Pattern Detection

When you run `/conductor:implement`, Conductor automatically scans modified files for code quality issues. Anti-patterns are categorized by severity:

| Severity | Behavior | Examples |
|:---------|:---------|:---------|
| **Critical** | Blocks task completion | Security vulnerabilities |
| **High** | Warns, requires documented skip | God Object, Mutable Defaults, Spaghetti Code |
| **Medium** | Informational | Magic Numbers, Deep Nesting |

#### Example Quality Gate Output

```
⚠️ **Quality Gate: Issues Detected**

| Severity | File | Line | Anti-Pattern | Issue |
|----------|------|------|--------------|-------|
| 🔴 High | src/service.py | 45 | Mutable Defaults | `def process(items=[])` |
| 🟡 Medium | src/utils.py | 23 | Magic Numbers | Literal `86400` |

Options: (1) Fix issues (2) Skip with reason (3) View guidance
```

#### Core Anti-Patterns

The following anti-patterns are detected out of the box:

| Anti-Pattern | Severity | Detection |
|:-------------|:---------|:----------|
| God Object | High | Classes >500 lines or >20 methods |
| Mutable Defaults | High | `def f(x=[])` or `def f(x={})` patterns |
| Spaghetti Code | High | Cyclomatic complexity >15 |
| Magic Numbers | Medium | Unexplained numeric literals |
| Deep Nesting | Medium | Nesting depth >4 levels |

### Coverage Intelligence

When a coverage report is available, Conductor analyzes it to suggest prioritized tests based on business impact:

```
### Coverage Intelligence

**Current Coverage:** 75% (Target: 80%)

**Top Suggestions:**
1. `process_payment()` in services/payment.py (+2.5% gain)
   - Core business logic, currently untested
2. `validate_input()` in api/handlers.py (+1.8% gain)
   - Input validation with multiple branches
```

#### Supported Coverage Formats

- **LCOV**: `lcov.info`, `coverage.lcov`
- **Cobertura XML**: `coverage.xml`, `cobertura.xml`
- **Istanbul JSON**: `coverage-final.json`
- **Coverage.py**: `.coverage`, `coverage.json`
- **Go Cover**: `coverage.out`

### Skip Documentation

When skipping quality gate warnings, document your reasoning:

```markdown
### Quality Gate Decisions

**Skipped Anti-Patterns:**
- **Mutable Defaults** at src/service.py:45
  - Reason: Intentional memoization cache, documented in function docstring
  - Reviewed: 2026-01-20
```

### Adding Custom Anti-Patterns

Create new anti-patterns in `patterns/anti-patterns/core/` using the template at `patterns/anti-patterns/TEMPLATE.md`. Each anti-pattern includes:

- **YAML Frontmatter**: Severity, detection patterns, file extensions
- **AI Quick Reference**: Concise detection and fix guidance
- **Human Documentation**: Detailed explanations with examples
- **Exceptions**: Valid use cases where the pattern is acceptable

## Universal File Resolution Protocol (UFRP)

Conductor uses a flexible file resolution system that allows you to customize your project structure while maintaining compatibility. The system works through `index.md` files that act as navigation indexes:

- **Project Index**: `conductor/index.md` - Links to all project-level documents
- **Track Index**: `conductor/tracks/<track_id>/index.md` - Links to track-specific documents

Commands automatically resolve file paths using these index files with fallback to standard default paths. This means you can reorganize your conductor directory structure by updating the index files, and all commands will continue to work correctly.

For more details, see [CLAUDE.md](CLAUDE.md).

## License

Apache License 2.0
