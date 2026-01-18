# Specification: Update Skills to Lower-Case Name Format

## Overview

Standardize all skill naming across the Conductor plugin to use the `lowercase-with-hyphens` format consistently. Currently, skill names use "Title Case With Spaces" while directory paths use lowercase-with-hyphens, creating inconsistency. This refactor will align all skill references to use a single, consistent format.

## Motivation

- **Consistency**: Single naming convention across all skill references
- **Machine-Friendly**: Lowercase-with-hyphens is easier to parse and reference programmatically
- **Clarity**: Reduces ambiguity when referencing skills in commands and documentation
- **Maintainability**: Simplifies future skill additions and updates

## Functional Requirements

### 1. Update Skill Registry
- Modify `skills/skill-registry.json` to use lowercase-with-hyphens format for all skill names
- Current names to update:
  - "Conductor Methodology" → "conductor-methodology"
  - "TypeScript Best Practices" → "typescript-best-practices"
  - "API Design" → "api-design"
  - "Testing Strategies" → "testing-strategies"

### 2. Update Skill Manifest Schema
- Review and update `skills/manifest-schema.json` if it contains:
  - Example skill names in documentation/descriptions
  - Enum values or constraints on skill naming
  - Any references to the old naming format

### 3. Update Skill Directory Paths
- Verify all skill directory paths follow the lowercase-with-hyphens format
- Rename any directories that don't match (if applicable)
- Current paths appear to already be in correct format (./conductor-methodology, ./typescript-best-practices, etc.)

### 4. Update Command Files
- Review and update skill name references in:
  - `commands/skills.md` - Display logic for skill listing
  - Any other command files that reference skill names

### 5. Update Documentation
- Search and update skill name references in:
  - `README.md`
  - Any skill-specific documentation
  - `CLAUDE.md` if it contains skill references

### 6. Update SKILL.md Files
- Update headers and metadata within each skill's `SKILL.md` file:
  - `skills/conductor-methodology/SKILL.md`
  - `skills/typescript-best-practices/SKILL.md`
  - `skills/api-design/SKILL.md`
  - `skills/testing-strategies/SKILL.md`

## Acceptance Criteria

- [ ] All skill names in `skill-registry.json` use lowercase-with-hyphens format
- [ ] `skills/manifest-schema.json` updated to reflect new naming format
- [ ] All skill directory paths match the lowercase-with-hyphens convention
- [ ] Command files correctly reference skills using the new format
- [ ] Documentation files use the consistent lowercase-with-hyphens naming
- [ ] All SKILL.md files have updated headers/metadata
- [ ] No broken references or inconsistencies remain
- [ ] `/conductor:skills list` command displays skills correctly with new naming

## Out of Scope

- Changing the fundamental structure of the skill system
- Adding new skills or removing existing skills
- Modifying skill functionality or activation rules
- Updating user projects that may reference skills (only plugin files)

## Implementation Notes

- This is a refactoring task with no functional changes to skill behavior
- All changes are confined to the conductor-plugin repository
- Grep/search operations should be used to find all skill name references
- Care should be taken to maintain JSON schema compliance
