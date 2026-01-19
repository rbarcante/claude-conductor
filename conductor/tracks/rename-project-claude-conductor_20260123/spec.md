# Specification: Rename Project to "Claude Conductor"

## Overview

Comprehensive refactoring to rename the project from "conductor-plugin" / "Conductor Plugin" to "claude-conductor" / "Claude Conductor". This involves updating all references across code, documentation, configuration files, and text content throughout the repository.

## Functional Requirements

### FR-1: Name Replacements

Replace all instances of project names with their new equivalents:

| Old Name | New Name |
|----------|----------|
| `conductor-plugin` | `claude-conductor` |
| `Conductor Plugin` | `Claude Conductor` |
| `conductor_plugin` | `claude_conductor` |
| `ConductorPlugin` | `ClaudeConductor` |

### FR-2: Scope of Changes

The renaming must cover:

1. **Code Files:**
   - Python scripts in `/scripts`
   - Command definitions in `/commands`
   - Skill definitions in `/skills`
   - Protocol definitions in `/protocols`
   - Pattern definitions in `/patterns`

2. **Documentation:**
   - README.md
   - All markdown files in root and subdirectories
   - CLAUDE.md project instructions
   - Template files in `/templates`
   - Docs in `/docs`

3. **Configuration:**
   - plugin.json (if exists)
   - Package manifests
   - Build configurations
   - CI/CD configurations

4. **Project Structure:**
   - Directory names (if `conductor-plugin` is used)
   - File paths referenced in documentation
   - Import statements or module references

### FR-3: Exclusions

The following should NOT be changed:

1. **Git History:**
   - Existing commit messages
   - Commit metadata
   - Branch names (except current branch)
   - Tags

2. **External URLs:**
   - Links to external repositories
   - References to third-party documentation
   - GitHub URLs pointing to external resources

## Non-Functional Requirements

### NFR-1: Verification

After all replacements are complete:

1. Run `grep -r "conductor-plugin" .` to verify no old references remain (excluding git history and external URLs)
2. Run `grep -r "Conductor Plugin" .` to verify no old references remain
3. Check that all tests pass (if tests exist)
4. Verify documentation renders correctly

### NFR-2: Consistency

- All naming variations must be updated consistently
- File naming conventions must match new project name
- Case sensitivity must be preserved (lowercase `claude-conductor`, title case `Claude Conductor`, etc.)

## Acceptance Criteria

The refactoring is complete when:

1. [ ] Zero occurrences of "conductor-plugin" found via grep (excluding git history and external URLs)
2. [ ] Zero occurrences of "Conductor Plugin" found via grep (excluding git history and external URLs)
3. [ ] All documentation reflects new project name "Claude Conductor"
4. [ ] All code references use "claude-conductor" naming
5. [ ] All tests pass (if applicable)
6. [ ] README.md correctly introduces "Claude Conductor"
7. [ ] plugin.json (if exists) reflects new project name

## Out of Scope

The following are explicitly out of scope:

1. Rewriting git commit history or messages
2. Changing functionality or behavior (this is purely a naming refactor)
3. Updating external repositories or forks
4. Modifying third-party documentation
5. Renaming the GitHub repository (user's responsibility)
6. Updating package registry names (npm, PyPI, etc.) - user's responsibility
