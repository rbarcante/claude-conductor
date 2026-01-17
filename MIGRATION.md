# Migration from Gemini CLI to Claude Code

This document describes the port of the Conductor extension from Gemini CLI to Claude Code.

## Overview

Conductor has been successfully ported from a Gemini CLI extension to a Claude Code plugin with **full feature parity and enhancements**. All original functionality has been preserved while adapting to Claude Code's architecture and conventions. Version 0.2.0 adds the Universal File Resolution Protocol (UFRP) to match the latest gemini-cli extension.

## What Changed

### File Format

- **Gemini CLI**: Commands in TOML format (`.toml` files)
- **Claude Code**: Commands in Markdown format with YAML frontmatter (`.md` files)

### Directory Structure

**Gemini CLI:**
```
conductor/
├── gemini-extension.json
├── commands/conductor/*.toml
├── templates/
└── GEMINI.md (context file)
```

**Claude Code:**
```
conductor-plugin/
├── .claude-plugin/plugin.json
├── commands/*.md
├── skills/conductor-methodology/
├── templates/
├── CLAUDE.md (context file)
├── README.md
├── MIGRATION.md
└── TESTING.md
```

### Path References

- **Before**: `~/.gemini/extensions/conductor/templates/`
- **After**: `$CLAUDE_PLUGIN_ROOT/templates/`

This ensures portability across different installation methods.

### Ignore Files

- **Before**: `.geminiignore` (referenced in commands)
- **After**: `.claudeignore` (updated references)

## What Stayed the Same

### Core Functionality

All original features preserved:
- ✅ Project setup (greenfield & brownfield)
- ✅ Interactive context gathering
- ✅ Track creation with spec and plan generation
- ✅ TDD workflow implementation
- ✅ Phase completion verification
- ✅ Git-aware revert
- ✅ Documentation synchronization
- ✅ Track cleanup (archive/delete)

### Workflow Files

Template files remain identical:
- `workflow.md` - TDD workflow and protocols
- `code_styleguides/*` - Language style guides

### Command Protocols

All command protocols preserved exactly:
- Sequential question flow
- Option format (A/B/C/D/E)
- Additive vs Exclusive Choice questions
- Resume capability via state files
- Commit message patterns
- Git notes usage
- User confirmation loops

### Project Structure

The conductor/ directory structure in user projects (version 0.2.0+):
```
conductor/
├── product.md
├── product-guidelines.md
├── tech-stack.md
├── workflow.md
├── code_styleguides/
├── tracks.md
├── index.md (NEW - project navigation index)
├── setup_state.json
└── tracks/<track_id>/
    ├── spec.md
    ├── plan.md
    ├── metadata.json
    └── index.md (NEW - track navigation index)
```

## New Additions

### Universal File Resolution Protocol (UFRP) - Version 0.2.0

Matches gemini-cli extension v0.2.0 features:
- **Dynamic path resolution** via `index.md` files
- **Flexible project structure** - customize conductor/ directory layout
- **Fallback to defaults** - works with or without index files
- **Full parity** with gemini-cli extension UFRP implementation

Commands now use semantic references (e.g., "**Product Definition**", "**Tech Stack**") instead of hardcoded paths. Files are resolved dynamically via:
1. Read `conductor/index.md` to find project-level files
2. Read `conductor/tracks/<track_id>/index.md` for track files
3. Fallback to default paths if index files missing

See `CLAUDE.md` for complete protocol documentation.

### Skill System

Added `conductor-methodology` skill:
- Provides context-driven development knowledge
- Activates automatically when discussing Conductor concepts
- Contains comprehensive reference material

### Enhanced Documentation

New documentation files:
- `CLAUDE.md` - Context document with UFRP specification (v0.2.0+)
- `TESTING.md` - Comprehensive testing guide
- `MIGRATION.md` - This file
- Updated `README.md` for Claude Code with UFRP section

### Tool Declarations

Commands now explicitly declare required Claude Code tools:
- `Read`, `Write`, `Edit` for file operations
- `Bash` for git and shell commands
- `Glob`, `Grep` for file searching
- `TodoWrite` for task tracking (in implement command)

## Breaking Changes

**None.** The plugin is a direct port with no breaking changes to:
- File formats in conductor/ directory
- Workflow protocols
- Commit message patterns
- Plan file structure
- Track lifecycle

Users can migrate projects between Gemini CLI and Claude Code without modification.

## Installation Differences

### Gemini CLI
```bash
gemini extensions install https://github.com/user/conductor --auto-update
```

### Claude Code
```bash
# Option 1: Copy to plugins directory
cp -r conductor-plugin ~/.claude/plugins/conductor

# Option 2: Use plugin-dir flag
cc --plugin-dir /path/to/conductor-plugin
```

## Command Invocation

**Identical** - All commands use the same names and arguments:

```bash
/conductor:setup
/conductor:newTrack "description"
/conductor:implement
/conductor:status
/conductor:revert
```

## Compatibility

### Forward Compatible
Projects created with Gemini CLI Conductor extension work seamlessly with Claude Code Conductor plugin.

### Backward Compatible
Projects created with Claude Code Conductor plugin work with Gemini CLI Conductor extension.

### Version Parity
- **v0.1.1**: Initial port with core functionality
- **v0.2.0**: Added UFRP, matching Gemini CLI extension v0.2.0 features

## Testing

See `TESTING.md` for comprehensive testing guide covering:
- Greenfield and brownfield setup
- Track creation and implementation
- Status reporting
- Revert functionality
- Edge cases and performance

## Future Enhancements

Potential additions that don't exist in original Gemini extension:

1. **Agents**: Could add autonomous agents for:
   - Track validation
   - Plan review
   - Code quality checking

2. **Hooks**: Could add event-driven automation:
   - Auto-update plan on file changes
   - Validate commits match task format

3. **MCP Integration**: Could integrate with:
   - Project management tools (Jira, Linear)
   - Time tracking
   - Analytics

These would be additive enhancements beyond the original feature set.

## Support

For issues or questions:
- Gemini CLI version: Original repository
- Claude Code version: Check plugin directory for updates

## License

Both versions licensed under Apache License 2.0.
