# Specification: Improve newTrack.md with XML Tags

## Overview

Refactor `commands/newTrack.md` to use XML tags following Anthropic's prompt engineering best practices. XML tags will clearly delineate the prompt's logical sections — system directive, reference data, protocols, and workflow phases — so Claude can parse each component accurately without mixing up instructions with examples or context.

## Functional Requirements

1. **Wrap all major sections in descriptive XML tags:**
   - `<system_directive>` — Role definition and critical behavioral rules
   - `<cli_reference>` — CLI commands, track types, and fallback instructions
   - `<protocol name="...">` — Each protocol block (AskUserQuestion, verify-setup, git-isolation)
   - `<phase name="...">` — Each workflow phase (setup_check, git_isolation, initialization subsections)
   - `<instructions>` — Step-by-step procedural lists within phases
   - `<constraints>` — Rules tables and limit definitions
   - `<note>` — Critical callouts and important behaviors (e.g., CRITICAL markers)

2. **Nest tags hierarchically:**
   - `<phase>` contains `<instructions>`, `<constraints>`, and `<note>` as children
   - `<protocol>` contains `<constraints>` for rule tables

3. **Reference tags by name in instructions:**
   - e.g., "Using the commands defined in `<cli_reference>`..." to create explicit cross-references

4. **Preserve all existing markdown content inside tags:**
   - Tables, code blocks, lists, and bold formatting remain unchanged
   - XML tags add structural boundaries only — no content changes

5. **Maintain consistent tag naming throughout the file**

## Non-Functional Requirements

- Frontmatter (YAML) and `# Context` header remain unchanged (required by plugin system)
- File remains valid markdown (XML tags are treated as HTML by markdown parsers)
- No behavioral changes to the command's execution logic
- Tag names use snake_case and are semantically meaningful

## Acceptance Criteria

- [ ] All major sections are wrapped in appropriately named XML tags
- [ ] Tags are properly nested (phases contain instructions/constraints/notes)
- [ ] Tags are referenced by name where cross-referencing occurs
- [ ] Existing markdown formatting is preserved inside tags
- [ ] Tag naming is consistent throughout the file
- [ ] The command still executes correctly when invoked via `/conductor:newTrack`

## Out of Scope

- Applying XML tags to other command files (implement.md, setup.md, etc.)
- Applying XML tags to protocol files in `protocols/`
- Changing the command's behavioral logic or workflow steps
- Adding new sections or content beyond XML structural markup
