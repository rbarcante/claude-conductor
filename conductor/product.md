# Product: Conductor Plugin for Claude Code

## Initial Concept

Conductor is a Claude Code plugin that enables **Context-Driven Development**. It transforms Claude Code from a simple code-writing assistant into a proactive project manager that follows a strict, disciplined protocol: **Context -> Spec & Plan -> Implement**.

## Vision

**"Measure twice, code once."**

Conductor addresses a fundamental challenge in AI-assisted development: maintaining consistent, high-quality context across all interactions with AI agents. By treating context as a managed artifact alongside code, Conductor turns the repository into a single source of truth that drives every agent interaction with deep, persistent project awareness.

## Core Philosophy

Conductor's philosophy is simple: **control your code**. Rather than having AI agents make ad-hoc decisions or lose track of project conventions, Conductor ensures that:

1. **Context is explicit** - Product goals, technical choices, and workflow preferences are documented and versioned
2. **Planning precedes implementation** - Specs and detailed plans are created before any code is written
3. **Work is traceable** - Every task, phase, and feature is tracked and linked to git commits
4. **Teams stay aligned** - Shared context files ensure all team members (human and AI) follow the same standards

## Target Users

Conductor is designed for developers and teams who:

- Build software with AI assistance and want consistent, high-quality output
- Work on projects that benefit from careful planning before implementation
- Need to maintain context across multiple AI-assisted sessions
- Collaborate in teams and need shared standards and conventions
- Maintain existing codebases and want structured, traceable enhancements
- Practice or want to adopt Test-Driven Development (TDD)

## Key Product Goals

### 1. Context Management
Maintain persistent, versioned project context that includes:
- Product vision and requirements
- Design guidelines and brand standards
- Technology stack decisions and rationale
- Team workflow preferences and quality standards
- Code style guides for consistency

### 2. Structured Planning
Enforce a planning-first approach:
- **Specs**: Clear requirements documents for each feature or bug fix
- **Plans**: Actionable, phased task lists with sub-tasks
- **Review**: User approval before implementation begins

### 3. Traceable Implementation
Track every piece of work:
- Tasks are marked in-progress, completed, and linked to git commits
- Phases have verification checkpoints with attached reports
- Git notes provide detailed summaries attached to commits
- Full audit trail from requirement to code

### 4. Team Collaboration
Enable shared understanding:
- Context files live in the repository (single source of truth)
- Any team member can use `/conductor:status` to understand progress
- New team members (and AI agents) can quickly get up to speed
- Consistent workflow across all work

### 5. Smart Revert
Safe rollback capabilities:
- Revert by logical unit (track, phase, or task) not just commit hash
- Understand what work belongs to which feature
- Clean rollback without losing unrelated work

## High-Level Features

### Project Setup (`/conductor:setup`)
One-time initialization that creates the project's context foundation:
- Product definition (users, goals, features)
- Product guidelines (style, messaging, visual identity)
- Technology stack documentation
- Workflow configuration (TDD, coverage standards, commit strategy)
- Code styleguide selection

### Track Creation (`/conductor:newTrack`)
Start any new unit of work:
- Define the track (feature or bug fix)
- Generate detailed specification
- Create phased implementation plan
- Get user approval before coding begins

### Implementation (`/conductor:implement`)
Execute the plan systematically:
- Follow Test-Driven Development (Red-Green-Refactor)
- Maintain >80% code coverage
- Update task status in real-time
- Commit with proper messages and git notes
- Phase completion verification and checkpointing

### Progress Tracking (`/conductor:status`)
Always know where you stand:
- See all tracks and their status
- View active track progress
- Understand what's completed, in-progress, or pending

### Smart Revert (`/conductor:revert`)
Rollback with precision:
- Revert entire tracks (features/bugs)
- Revert specific phases
- Revert individual tasks
- Analyzes git history to identify relevant commits

## Differentiation

Conductor differs from other AI coding tools in several key ways:

1. **Context as Artifact**: Context isn't implicit in prompts—it's explicit, versioned files in your repo
2. **Planning First**: Specs and plans are created and reviewed before any code is written
3. **Human in the Loop**: Users review and approve plans, and verify phases before proceeding
4. **Git-Native**: Deep integration with git (commits, notes, history) for full traceability
5. **Workflow Enforcement**: TDD, coverage thresholds, and quality gates are built into the protocol
6. **Brownfield-Aware**: Intelligently analyzes existing projects to infer context without disruption

## Success Metrics

Conductor enables successful AI-assisted development when:

- **Consistency**: Code follows project conventions without constant reminders
- **Quality**: High test coverage and adherence to style guides
- **Traceability**: Every change can be traced back to a requirement and plan
- **Team Alignment**: All team members produce consistent, high-quality code
- **Onboarding**: New team members quickly understand project context and standards
- **Confidence**: Rollbacks are safe and well-understood

## Future Considerations

Potential enhancements that may be explored:

- Integration with external project management tools (Jira, GitHub Projects)
- Multi-repo context management for monorepos
- Context sharing across related projects
- Automated context inference from code patterns
- Team analytics and insights
- Enhanced mobile and web testing workflows
