# Specification: Add GLAB Skill for consistent GitLab CLI usage

## Overview
Add a new `glab-cli` skill to the Conductor skill ecosystem that provides a comprehensive command reference for the GitLab CLI (`glab`). This follows the same pattern as the existing `acli-jira` skill — a single `SKILL.md` file with YAML frontmatter, registered in `skill-registry.json` with keyword-based activation.

## Background
The `acli-jira` skill demonstrates the proven pattern: a self-contained SKILL.md with structured command reference (~480 lines), activated by keywords in the skill registry. The `glab-cli` skill mirrors this for GitLab CLI operations — authentication, issues, merge requests, CI/CD pipelines, releases, labels, variables, snippets, and repo management. Commands are verified against official glab documentation at docs.gitlab.com/cli.

## Functional Requirements
1. **SKILL.md** with YAML frontmatter (name, description, version) covering all major `glab` command groups: `auth`, `issue`, `mr`, `ci`, `release`, `repo`, `label`, `variable`, `snippet`, `milestone`
2. **Skill registry entry** in `skill-registry.json` with activation keywords: `glab`, `gitlab`, `gitlab-cli`, `merge request`, `mr`, `gitlab issue`, `gitlab pipeline`, `gitlab ci`, `gitlab release`
3. **Content structure** matching `acli-jira` pattern: Core Principles → Authentication → command sections with code blocks → Common Flag Patterns table → Common Workflows
4. **Official docs accuracy** — all commands verified against official `glab` documentation (docs.gitlab.com/cli)

## Non-Functional Requirements
- Content length comparable to `acli-jira` (~400-500 lines)
- Code blocks use `bash` syntax highlighting
- No manifest.json (activation via registry only, matching acli-jira pattern)
- Professional, direct tone addressing developers as peers

## Acceptance Criteria
- [ ] `skills/glab-cli/SKILL.md` exists with complete command reference
- [ ] `skill-registry.json` includes `glab-cli` entry with proper activation keywords
- [ ] Skill activates when user mentions "glab", "gitlab", "merge request", or related keywords
- [ ] Command syntax matches official glab documentation
- [ ] Structure and style consistent with `acli-jira` skill

## Out of Scope
- manifest.json file
- SKILL-SUMMARY.md
- patterns/ directory
- GitLab REST/GraphQL API reference — only CLI (`glab`) commands
- Self-managed GitLab instance configuration details
