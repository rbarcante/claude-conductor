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
- **AI-Optimized Templates**: Dual-format patterns and styleguides with AI Quick Reference sections, plus a searchable snippet library.
- **Skill Ecosystem**: Extensible skill plugin architecture with reference skills for typescript-best-practices, api-design, and testing-strategies that provide domain-specific guidance.
- **Quality Intelligence**: Automated anti-pattern detection and coverage analysis with actionable test suggestions during implementation.
- **Decision Logging**: Architecture Decision Record (ADR) logging that captures the "why" behind implementation choices for self-documenting codebases.

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
- `conductor/tracks/<track_id>/decisions.md` (ADR logging)
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
| `/conductor:newTrack` | Starts a new feature or bug track. Generates `spec.md`, `plan.md`, and `decisions.md`. | `conductor/tracks/<id>/spec.md`<br>`conductor/tracks/<id>/plan.md`<br>`conductor/tracks/<id>/decisions.md`<br>`conductor/tracks/<id>/index.md`<br>`conductor/tracks.md` |
| `/conductor:implement` | Executes the tasks defined in the current track's plan. | `conductor/tracks.md`<br>`conductor/tracks/<id>/plan.md` |
| `/conductor:status` | Displays the current progress of the tracks file and active tracks. | Reads `conductor/tracks.md` |
| `/conductor:revert` | Reverts a track, phase, or task by analyzing git history. | Reverts git history |
| `/conductor:patterns` | Browse and search the Pattern Reference Layer. | Reads `patterns/index.md` |
| `/conductor:skills` | Manage and explore Conductor skills (list, info, enable, disable). | Reads/writes `skills/skill-registry.json`, `conductor/settings.json` |
| `/conductor:snippet` | Browse, search, and display code snippets from the Snippet Library. | Reads `snippets/index.md` |

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

## AI-Optimized Templates

Conductor includes AI-optimized templates that follow a **Dual-Format Standard** - every template contains both a concise AI Quick Reference section and detailed human documentation.

### Dual-Format Standard

All patterns, styleguides, and documentation follow this structure:

```markdown
# Document Title

## AI Quick Reference
[Structured, scannable content - max 30-50 lines]
[Tables, bullet lists, minimal code examples]

---

## Human Documentation
[Detailed explanations, examples, rationale]
```

This design ensures:
- **Fast AI parsing**: Key rules immediately accessible at the top
- **Complete documentation**: Detailed explanations for human readers
- **Consistent structure**: Predictable format across all templates

### AI-Enhanced Styleguides

All code styleguides in `templates/code_styleguides/` include AI Quick Reference sections (max 30 lines) with:

| Section | Purpose |
|:--------|:--------|
| **Language Rules** | Core syntax and conventions (6-10 items) |
| **Type Patterns** | Type system best practices (5-8 items) |
| **Avoid** | Anti-patterns and common mistakes (4-6 items) |

Available styleguides: TypeScript, Python, JavaScript, Go, General

### Snippet Library

Conductor includes a reusable code snippet library with AI-optimized headers:

```bash
# List all snippets
/conductor:snippet list

# Search snippets by keyword
/conductor:snippet search api client

# View a specific snippet
/conductor:snippet show api-client.ts
```

#### Snippet Categories

| Category | Contents |
|:---------|:---------|
| **TypeScript** | api-client, error-handler, type-guard, async-wrapper, config-loader |
| **Python** | api-client, error-handler, dependency-injection, config-loader, async-patterns |
| **Patterns** | repository-pattern, factory-pattern |

#### Snippet AI Headers

Each snippet includes an AI header with:
- **USE**: When to use this snippet
- **REQUIRES**: Dependencies and prerequisites
- **PATTERN**: Related patterns

Example (TypeScript):
```typescript
/**
 * USE: When building a type-safe HTTP client for API communication
 * REQUIRES: TypeScript 4.5+
 * PATTERN: Error Handling, Configuration
 */
```

### AI Template Generation Protocol

The generation protocol ensures consistent AI-optimized content during setup. When running `/conductor:setup`:

1. Styleguides are copied with AI Quick Reference sections intact
2. Each copied file is verified for AI-enhanced content
3. Announcements confirm AI sections are present

See `protocols/ai-template-generation.md` for the complete protocol specification.

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

- **Always-Active Skills**: Core methodology loaded for every task (e.g., conductor-methodology)
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
- conductor-methodology: Core development workflow guidance

**Context-Activated:** (based on track/task matching)
- React Best Practices (score: 3.5): Component patterns, hooks usage, state management
```

### Creating Custom Skills

See [docs/skill-development.md](docs/skill-development.md) for a comprehensive guide on creating custom skills. Each skill includes:

- **manifest.json**: Metadata and activation rules
- **SKILL.md**: Guidance content for the AI agent
- **patterns/** (optional): Skill-specific pattern files
- **README.md** (optional): External documentation

## Skill Ecosystem

Conductor includes a rich skill ecosystem with reference skills and a management command for exploring and configuring skills.

### Managing Skills

Use the skills command to explore and configure skills:

```bash
# List all available skills
/conductor:skills list

# View detailed information about a skill
/conductor:skills info typescript-best-practices

# Disable a skill for the current project
/conductor:skills disable api-design

# Re-enable a skill
/conductor:skills enable api-design
```

### Reference Skills

Conductor includes the following reference skills out of the box:

| Skill | Description | Activation |
| :--- | :--- | :--- |
| **typescript-best-practices** | Type safety, async patterns, null handling | `.ts`, `.tsx` files; TypeScript tech stack |
| **api-design** | REST conventions, error responses, versioning | routes/controllers/api directories; backend frameworks |
| **testing-strategies** | Unit testing, integration testing, mocking | test files (`*.test.*`, `*.spec.*`); test frameworks |

### Skill Patterns

Each reference skill includes domain-specific patterns:

**typescript-best-practices:**
- `type-safety.md` - Type definitions, generics, discriminated unions
- `async-patterns.md` - Async/await, Promise handling, error management
- `null-handling.md` - Optional chaining, nullish coalescing, type guards

**api-design:**
- `rest-conventions.md` - URL naming, HTTP methods, resource design
- `error-responses.md` - Error format, status codes, error classes
- `versioning.md` - URL versioning, deprecation, migration

**testing-strategies:**
- `unit-test-patterns.md` - Structure, naming, assertions
- `integration-patterns.md` - Database, API, service tests
- `mocking-strategies.md` - When and how to mock

### Project-Level Skill Configuration

Skills can be enabled/disabled per-project via `conductor/settings.json`:

```json
{
  "version": "1.0.0",
  "disabledSkills": ["./api-design"]
}
```

Note: Always-active skills (like conductor-methodology) cannot be disabled.

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

## Decision Logging

Conductor captures the "why" alongside the "what" through Architecture Decision Record (ADR) logging. When significant decisions are made during implementation, they're automatically documented in a track-specific `decisions.md` file.

### How It Works

During `/conductor:implement`, when Conductor detects a significant decision point (technology selection, pattern choice, API design, etc.), it prompts you with options:

```
---
**Decision Point: Library Selection**

**Context:** We need to implement HTTP client functionality for API calls.

**Options:**
A. **axios** (Recommended)
   Popular HTTP client with interceptors and automatic transforms
   - Pros: Wide adoption, good TypeScript support
   - Cons: Additional dependency

B. **Native fetch**
   Built-in browser/Node.js API
   - Pros: No dependencies
   - Cons: More boilerplate, no interceptors

Select an option (A/B/skip):
---
```

### ADR Format

Decisions are recorded in the standard ADR format:

```markdown
### ADR-001: Use axios for HTTP client

**Date:** 2026-01-20
**Status:** Accepted

#### Context
The feature requires making API calls to external services. We need a
reliable HTTP client that supports interceptors for authentication headers.

#### Decision
We will use axios as the HTTP client library.

#### Consequences
**Positive:**
- Consistent error handling across the application
- Built-in request/response interceptors for auth

**Negative:**
- Additional 15KB dependency
- Learning curve for team members unfamiliar with axios

#### Alternatives Considered
- **Native fetch:** Rejected due to lack of built-in interceptors
```

### Generated Artifacts

Each track includes a decisions log:
- `conductor/tracks/<track_id>/decisions.md` - Track-specific decision log

### When Decisions Are Captured

Decisions are prompted for significant choices that:
- Involve tradeoffs between alternatives
- Have long-term architectural implications
- Deviate from established patterns
- Would benefit future maintainers

Trivial choices (dictated by spec, single option, easily reversible) are skipped automatically.

### Browsing Decisions

View a track's decisions by reading its `decisions.md` file or through the track index:

```bash
cat conductor/tracks/<track_id>/decisions.md
```

## Universal File Resolution Protocol (UFRP)

Conductor uses a flexible file resolution system that allows you to customize your project structure while maintaining compatibility. The system works through `index.md` files that act as navigation indexes:

- **Project Index**: `conductor/index.md` - Links to all project-level documents
- **Track Index**: `conductor/tracks/<track_id>/index.md` - Links to track-specific documents

Commands automatically resolve file paths using these index files with fallback to standard default paths. This means you can reorganize your conductor directory structure by updating the index files, and all commands will continue to work correctly.

For more details, see [CLAUDE.md](CLAUDE.md).

## License

Apache License 2.0
