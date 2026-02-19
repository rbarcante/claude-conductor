# Technology Stack: Claude Conductor

## Overview

Conductor is a **documentation and protocol-driven plugin** for Claude Code. The project uses markdown-based command definitions to extend Claude Code's functionality, implementing a context-driven development methodology.

## Architecture

### Plugin System

**Type:** Claude Code Plugin
**Architecture Pattern:** Modular Command/Skill System

Conductor extends Claude Code through:
- **Commands** - Top-level invocable commands (e.g., `/conductor:setup`, `/conductor:newTrack`)
- **Skills** - Reusable capabilities that can be invoked by commands or workflows
- **Templates** - Boilerplate files for project initialization (workflows, styleguides)

### Directory Structure

```
claude-conductor/
├── commands/           # CLI command protocol definitions
│   ├── setup.md        # Project initialization command
│   ├── newTrack.md     # Track creation command
│   ├── implement.md    # Implementation execution command
│   ├── revert.md       # Revert/rollback command
│   ├── status.md       # Progress tracking command
│   └── patterns.md     # Pattern browsing command
├── protocols/          # Detection and analysis protocols
│   ├── stack-detection.md  # Technology stack detection algorithm
│   └── decision-capture.md # Decision identification and capture protocol
├── skills/             # Reusable skill definitions
│   ├── skill-registry.json    # Central skill index
│   └── conductor-methodology/ # Core methodology skill
│       ├── SKILL.md           # Skill content
│       └── manifest.json      # Activation rules
├── patterns/           # Pattern Reference Layer
│   ├── index.md        # Pattern registry
│   └── core/           # Language-agnostic patterns
├── docs/               # Schema and development documentation
│   └── skill-manifest-schema.md  # Skill manifest specification
├── templates/          # Template files for project setup
│   ├── workflow.md     # Default workflow template
│   └── code_styleguides/  # Code style guide templates
│       ├── general.md
│       ├── python.md
│       ├── javascript.md
│       ├── typescript.md
│       ├── go.md
│       ├── csharp.md
│       ├── dart.md
│       └── html-css.md
└── README.md           # Project documentation
```

## Core Technologies

### Language and Formats

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Protocol Definitions** | Markdown | Command and skill definitions |
| **Documentation** | Markdown (GitHub Flavored) | All user-facing docs |
| **Data Storage** | JSON | Metadata files (metadata.json, setup_state.json) |
| **Configuration** | YAML/JSON | Project context files (product.md, tech-stack.md, etc.) |

### Version Control

| Tool | Purpose |
|------|---------|
| **Git** | Version control for all project artifacts |
| **Git Notes** | Attach detailed summaries to commits (task reports, verification reports) |
| **Git History** | Track changes, enable smart revert functionality |

## Conductor Artifacts

Conductor generates and manages the following artifacts in user projects:

### Context Files

Located in `conductor/` directory:

| File | Purpose |
|------|---------|
| `product.md` | Product vision, goals, target users, features |
| `product-guidelines.md` | Brand messaging, prose style, visual identity |
| `tech-stack.md` | Technical choices and rationale |
| `workflow.md` | Development workflow (TDD, coverage, commit strategy) |
| `tracks.md` | High-level tracking of all project tracks |

### Track Artifacts

Located in `conductor/tracks/<track_id>/`:

| File | Purpose |
|------|---------|
| `spec.md` | Detailed requirements specification |
| `plan.md` | Phased implementation plan with tasks and sub-tasks |
| `decisions.md` | Architecture Decision Records (ADR) for track decisions |
| `review.md` | Auto-generated code review report on track completion |
| `metadata.json` | Track metadata (type, status, timestamps) |

### Style Guides

Located in `conductor/code_styleguides/`:

- Copied from templates based on project's selected technologies
- Provide coding standards for implementation

## Data Formats

### Metadata JSON Structure

```json
{
  "track_id": "unique_identifier_YYYYMMDD",
  "type": "feature|bug",
  "status": "new|in_progress|completed|cancelled",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "Initial user description"
}
```

### Setup State JSON Structure

```json
{
  "last_successful_step": "step_identifier"
}
```

## Tooling

### Development Environment

Conductor itself requires minimal tooling:

- **Text Editor** - Any markdown-capable editor (VS Code, vim, etc.)
- **Git** - For version control and git notes
- **Claude Code CLI** - The environment where the plugin runs

### User Project Requirements

Projects using Conductor typically require:

- Language-specific tooling (based on their tech stack)
- Testing framework
- Git repository
- (Optional) CI/CD pipeline integration

## Integration Points

### Claude Code CLI

Conductor integrates with Claude Code through:
- Plugin directory structure
- Command protocol definitions in markdown
- Skill definitions for reusable functionality

### User Projects

Conductor integrates into user projects by:
- Creating `conductor/` directory for context
- Generating track-specific artifacts
- Modifying `plan.md` to track progress
- Creating git commits with notes

## Design Principles

### Technology Choices

1. **Markdown-First**
   - Human-readable protocol definitions
   - Easy to version and diff
   - No compilation required
   - Accessible to non-technical stakeholders

2. **No Runtime Dependencies**
   - Conductor itself has no package.json, requirements.txt, or similar
   - Reduces maintenance burden
   - Increases portability
   - Simplifies installation

3. **Git-Native**
   - Leverages git for all state tracking
   - Git notes for rich metadata
   - Commit history for audit trail
   - Standard git operations for collaboration

4. **Template-Driven**
   - Workflow is customizable via template
   - Styleguides are selectable based on project needs
   - Consistent structure across projects

## Limitations and Considerations

### Current Limitations

1. **Markdown-Based Protocols**
   - Protocol logic is embedded in markdown files
   - Requires Claude Code to parse and execute
   - Not executable outside of Claude Code environment

2. **No Automated Testing**
   - Conductor plugin itself lacks test coverage
   - Manual testing required for changes

3. **File-Based State**
   - State stored in JSON files (setup_state.json)
   - Potential for sync issues in collaborative environments

### Future Enhancements

Potential areas for technology evolution:

- **Schema Validation**: JSON schemas for all JSON artifacts
- **Testing Framework**: Automated testing for protocol logic
- **Language Support**: Protocol definitions in structured formats (YAML, TOML)
- **External Integrations**: API hooks for external project management tools

## Security Considerations

### File System Access

Conductor requires:
- Read access to project files for analysis
- Write access to `conductor/` directory
- Git operations (commit, notes, log)

### Data Privacy

- All context files are stored locally in the repository
- No external API calls
- No telemetry or data collection

### Git Notes

Git notes are used to store:
- Task summaries
- Verification reports
- These are part of the git repository and subject to normal git access controls

## Version Control Strategy

### Branching Model

Conductor supports:
- Feature branches via tracks
- Phase checkpoints via git commits
- Task-level commits for granular tracking

### Commit Conventions

Conductor follows conventional commits:

```
<type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- conductor: Conductor-specific changes (setup, plan, checkpoint)
```

### Git Notes Usage

Git notes attach detailed information:
- Task completion summaries
- Phase verification reports
- Rich context beyond commit messages

## Technology Rationale

### Why Markdown?

- **Ubiquity**: Supported by all editors and platforms
- **Readability**: Human-readable without special tools
- **Version Control**: Diff-friendly
- **Documentation**: Serves as both code and documentation

### Why Git Notes?

- **Non-Destructive**: Doesn't alter commit messages
- **Queryable**: Can be searched and retrieved
- **Structured**: Allows for detailed, formatted information
- **Auditable**: Part of git history

### Why Template-Based?

- **Customization**: Users can adapt workflow to their needs
- **Consistency**: Standard starting point across projects
- **Evolution**: Templates can be updated without affecting existing projects

## Compatibility

### Claude Code Versions

Conductor is designed for:
- Claude Code CLI with plugin support
- Compatible with the skill and command system

### Operating Systems

- Cross-platform (works wherever Claude Code runs)
- No OS-specific dependencies

### Git Versions

- Requires Git with notes support (Git 1.7.9+)
- Tested with standard Git distributions

## Migration Path

### Upgrading Conductor

When upgrading the Conductor plugin:
1. Copy new plugin files to plugin directory
2. Existing `conductor/` directories remain compatible
3. Workflow templates can be updated per-project

### Migrating from Other Systems

Conductor can be adopted into existing projects:
- Brownfield setup analyzes existing codebase
- Context files created without disrupting existing work
- Gradual adoption possible (start with new tracks)

## Dependencies

### Claude Conductor

**Runtime Dependencies:** None

**Development Dependencies:** None

### User Projects

User projects must have:
- Git repository
- Language-specific tooling (per their tech stack)
- Testing framework (per workflow requirements)

## Performance Considerations

### File Operations

- Conductor reads multiple files during analysis
- Uses ignore patterns (.claudeignore, .gitignore) to exclude irrelevant files
- Large files are sampled (head/tail) rather than read entirely

### Git Operations

- Leverages git log for history analysis
- Uses efficient git commands (log, diff, notes)
- Avoids expensive operations when possible

## Technology Stack Summary

| Category | Technology |
|----------|------------|
| **Language** | Markdown |
| **Data Format** | JSON, YAML |
| **Version Control** | Git (with notes) |
| **Architecture** | Plugin-based, modular |
| **Runtime** | Claude Code CLI |
| **Dependencies** | None |
| **Platform** | Cross-platform |

This technology stack prioritizes simplicity, portability, and integration with existing developer workflows while enabling sophisticated context-driven development practices.
