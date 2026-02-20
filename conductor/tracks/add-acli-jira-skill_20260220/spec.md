# Specification: Add ACLI Jira Skill

## Overview

Create a new Conductor skill (`acli-jira`) that provides Claude with embedded knowledge of Atlassian CLI (ACLI) Jira commands, eliminating the need to repeatedly consult documentation or run `--help`. The skill covers work item CRUD, search/filters, and project management operations.

## Functional Requirements

### 1. SKILL.md - Core Skill File

- YAML frontmatter with trigger phrases for ACLI/Jira CLI usage
- Quick-reference command patterns for the most common Jira workflows
- Command syntax for `jira workitem`, `jira project`, `jira board`, `jira sprint`, `jira filter` subcommands
- Common flag patterns and option combinations
- Authentication workflow (`jira auth login/logout/status/switch`)

### 2. Skill Structure

- `skills/acli-jira/SKILL.md` - Contains all essential command reference inline
- No separate `references/` directory (lean, minimal approach)
- Imperative writing style per skill development guidelines

### 3. Command Coverage - Jira Operations

- **Work Items**: create, view, edit, delete, assign, transition, comment, clone, search, link, attachments
- **Projects**: create, list, view, update, archive/restore, delete
- **Boards & Sprints**: search boards, list sprints, list sprint workitems
- **Filters**: search, list, add-favourite, change-owner
- **Auth**: login, logout, status, switch

## Non-Functional Requirements

- SKILL.md body should be ~1,500-2,000 words (progressive disclosure principle)
- Written in imperative/infinitive form
- Third-person trigger description in frontmatter
- Organized by workflow (not alphabetically) for natural discovery

## Acceptance Criteria

- [ ] Skill triggers when user mentions "acli", "atlassian cli", "jira cli", "jira command"
- [ ] Provides correct command syntax without needing `--help`
- [ ] Covers all three user-specified areas: work items, search/filters, project management
- [ ] Follows skill-development best practices (lean SKILL.md, imperative style, third-person description)
- [ ] Integrates into Conductor's `skills/` directory with auto-discovery

## Out of Scope

- Admin commands (`admin auth`, `admin user`)
- Rovo Dev commands
- Feedback commands
- Separate reference files or scripts
- Automated testing of ACLI commands
