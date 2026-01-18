---
name: conductor-methodology
description: Use this skill when the user asks about Conductor concepts, workflow patterns, track lifecycle, plan structures, or context-driven development principles. Also activate when working with conductor/ directory files or when implementing tasks following TDD and verification protocols.
version: 1.0.0
---

# Conductor Methodology Skill

Conductor is a context-driven development framework that structures software development through a rigorous lifecycle: **Context → Spec & Plan → Implement**. This skill provides guidance on Conductor's principles, file structures, and workflows.

## Core Philosophy

**Measure twice, code once.** Conductor treats context as a managed artifact alongside code, transforming repositories into a single source of truth that drives every agent interaction with deep, persistent project awareness.

### Key Principles

1. **Plan before you build**: Create specs and plans that guide implementation
2. **Maintain context**: Ensure AI follows style guides, tech stack choices, and product goals
3. **Iterate safely**: Review plans before code is written
4. **Work as a team**: Set project-level context shared across the team

## Project Structure

### Core Context Files (conductor/)

Located in the `conductor/` directory at project root:

- **`product.md`**: Product vision, users, goals, and features
- **`product-guidelines.md`**: Prose style, brand messaging, visual identity
- **`tech-stack.md`**: Technology choices, languages, frameworks, databases
- **`workflow.md`**: Development workflow (TDD, commit strategy, coverage requirements)
- **`code_styleguides/`**: Language-specific coding standards
- **`tracks.md`**: Master list of all tracks with status and links

### Track Structure (conductor/tracks/)

Each track lives in `conductor/tracks/<track_id>/`:

- **`spec.md`**: Detailed requirements for the track
- **`plan.md`**: Hierarchical plan with phases, tasks, and sub-tasks
- **`metadata.json`**: Track metadata (ID, type, status, timestamps)

### Track Lifecycle

Tracks represent high-level units of work (features, bugs, chores):

1. **Creation** (`/conductor:newTrack`): Generate spec and plan
2. **In Progress**: Mark as `[~]` when work begins
3. **Completed**: Mark as `[x]` when all tasks finish
4. **Cleanup**: Archive or delete completed tracks

## Plan File Structure

Plans use hierarchical markdown with status markers:

```markdown
# Phase 1: Foundation

- [ ] Task: Set up database schema
    - [ ] Create users table
    - [ ] Create posts table
    - [ ] Add indexes

- [~] Task: Implement user model
    - [x] Write failing tests
    - [~] Implement User class

# Phase 2: Features

- [ ] Task: Build authentication
```

### Status Markers

- `[ ]` - Pending
- `[~]` - In progress
- `[x]` - Completed

### Plan Format Rules

1. **Phases**: Top-level markdown headers (`# Phase Name`)
2. **Parent Tasks**: Bullet points with `- [ ] Task: Description`
3. **Sub-tasks**: Indented bullet points with `- [ ] Description`
4. **Commit SHAs**: Appended after completion (e.g., `- [x] Task: Description [abc1234]`)
5. **Phase Checkpoints**: Appended to phase headers (e.g., `# Phase 1 [checkpoint: def5678]`)

## Workflow Patterns

### Test-Driven Development (TDD)

Standard workflow from `workflow.md`:

1. **Select Task**: Choose next pending task from plan
2. **Mark In Progress**: Change `[ ]` to `[~]` in plan
3. **Write Failing Tests (Red)**: Create tests that define expected behavior
4. **Implement to Pass (Green)**: Write minimal code to pass tests
5. **Refactor**: Improve code while keeping tests passing
6. **Verify Coverage**: Ensure >80% coverage (or configured percentage)
7. **Document Deviations**: Update tech-stack.md if needed
8. **Commit Code**: Stage and commit with descriptive message
9. **Attach Task Summary**: Use git notes for detailed summary
10. **Record SHA**: Update plan with commit hash
11. **Commit Plan**: Commit plan.md changes

### Phase Completion Protocol

When a phase completes:

1. **Ensure Test Coverage**: Verify all changed files have tests
2. **Execute Automated Tests**: Run full test suite with `CI=true`
3. **Propose Manual Verification Plan**: Provide step-by-step verification steps
4. **Await User Feedback**: Get explicit confirmation
5. **Create Checkpoint Commit**: Commit with message `conductor(checkpoint): Checkpoint end of Phase X`
6. **Attach Verification Report**: Use git notes with test results and user confirmation
7. **Record Checkpoint SHA**: Append to phase header in plan
8. **Commit Plan Update**: Commit plan changes

### Commit Message Patterns

- **Implementation**: `feat(module): Add feature description`
- **Bug Fix**: `fix(module): Fix issue description`
- **Tests**: `test(module): Add tests for feature`
- **Plan Updates**: `conductor(plan): Mark task 'description' as complete`
- **Checkpoints**: `conductor(checkpoint): Checkpoint end of Phase X`
- **Track Management**: `conductor(track): Create track 'description'`
- **Setup**: `conductor(setup): Add conductor setup files`
- **Documentation**: `docs(conductor): Synchronize docs for track 'description'`

## Git Notes Usage

Conductor uses git notes for auditable tracking:

### Task Notes

Attached to implementation commits with format:
```
Task: <Task Name>
Summary: <Brief description of changes>
Files Changed:
  - path/to/file1.ts
  - path/to/file2.ts
Why: <Rationale for changes>
```

### Checkpoint Notes

Attached to checkpoint commits with format:
```
Phase: <Phase Name>
Automated Tests: <Command run and result>
Manual Verification:
  - Step 1: <Action and expected result>
  - Step 2: <Action and expected result>
User Confirmation: <User's confirmation statement>
```

## Question Types for Interactive Workflows

When gathering requirements or context:

### Additive Questions

For brainstorming and scope (users, goals, features):
- Allow multiple answers
- Add "(Select all that apply)"
- Present as options A, B, C, D, E

### Exclusive Choice Questions

For singular commitments (technology selection, workflow rules):
- Require single answer
- Do NOT add "(Select all that apply)"
- Present as options A, B, C, D, E

### Option Format

Always include:
- A, B, C: Suggested answers
- D: "Type your own answer"
- E: "Autogenerate and review <filename>"

## Track ID Format

Track IDs follow the pattern: `shortname_YYYYMMDD`

Examples:
- `darkmode_20260113` - Add dark mode feature
- `bugfix_20260113` - Fix login issue
- `refactor_20260113` - Refactor database layer

## State Management

### Setup State (conductor/setup_state.json)

Tracks setup progress for resumability:

```json
{
  "last_successful_step": "2.3_tech_stack"
}
```

Possible values:
- `""` - Initial state
- `"2.1_product_guide"` - Product guide complete
- `"2.2_product_guidelines"` - Guidelines complete
- `"2.3_tech_stack"` - Tech stack complete
- `"2.4_code_styleguides"` - Style guides copied
- `"2.5_workflow"` - Workflow configured
- `"3.3_initial_track_generated"` - Setup fully complete

### Track Metadata (metadata.json)

```json
{
  "track_id": "feature_20260113",
  "type": "feature",
  "status": "in_progress",
  "created_at": "2026-01-13T10:30:00Z",
  "updated_at": "2026-01-13T15:45:00Z",
  "description": "Add user authentication"
}
```

## Best Practices

### When Creating Specs

1. Ask context-aware questions based on product.md and tech-stack.md
2. Provide 2-3 plausible options for each question
3. Ask questions sequentially (one at a time)
4. Include acceptance criteria and out-of-scope items
5. Get user confirmation before proceeding

### When Creating Plans

1. Read and follow the workflow.md methodology
2. Break features into testable tasks
3. Include phase completion verification tasks
4. Use hierarchical structure (phases > tasks > sub-tasks)
5. Add status markers to EVERY item
6. Get user confirmation before starting work

### When Implementing

1. Follow the workflow.md task lifecycle precisely
2. Never skip test-writing step in TDD
3. Verify tool call success before proceeding
4. Update plan.md status in real-time
5. Use git notes for audit trails
6. Get user confirmation for phase completions

### When Syncing Documentation

1. Only update docs when track completes (`[x]`)
2. Analyze spec.md for significant changes
3. Propose changes with diff format
4. Get explicit user approval before editing
5. Be very conservative with product-guidelines.md
6. Commit all doc changes together

## Reverting Work

Conductor provides git-aware revert for logical units:

1. **Identify Target**: Track, phase, or task
2. **Find Commits**: Implementation + plan updates + track creation (if applicable)
3. **Handle Rewritten History**: Search for similar commit messages if SHA missing
4. **Present Plan**: Show all commits to be reverted
5. **Get Confirmation**: Explicit user approval required
6. **Execute**: Revert in reverse chronological order

## Integration with Claude Code

All commands are invoked with `/conductor:<command>`:

- `/conductor:setup` - Initialize project
- `/conductor:newTrack [description]` - Create new track
- `/conductor:implement [track]` - Execute track plan
- `/conductor:status` - Show progress overview
- `/conductor:revert [target]` - Revert work

Commands use Claude Code tools (Read, Write, Edit, Bash, Glob, Grep) and follow plugin best practices.
