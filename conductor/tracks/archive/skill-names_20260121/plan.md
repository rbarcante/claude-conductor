# Implementation Plan: Update Skills to Lower-Case Name Format

## Overview
Standardize all skill naming across the Conductor plugin to use the `lowercase-with-hyphens` format consistently.

---

## Phase 1: Discovery and Analysis

- [x] Task: Identify all files containing skill name references [40a78ca]
    - [x] Search for "Conductor Methodology" references across codebase
    - [x] Search for "TypeScript Best Practices" references across codebase
    - [x] Search for "API Design" references across codebase
    - [x] Search for "Testing Strategies" references across codebase
    - [x] Document all file locations that need updates

- [x] Task: Conductor - User Manual Verification 'Discovery and Analysis' (Protocol in workflow.md)

---

## Phase 2: Update Core Skill Files

- [x] Task: Update skill-registry.json [40a78ca]
    - [x] Change all skill names to lowercase-with-hyphens format
    - [x] Verify JSON structure remains valid
    - [x] Ensure paths and names are aligned

- [x] Task: Update manifest-schema.json [40a78ca]
    - [x] Update example skill names in the schema
    - [x] Update description text if it references specific skill names
    - [x] Verify schema remains valid

- [x] Task: Update individual skill manifest.json files [40a78ca]
    - [x] Update conductor-methodology/manifest.json
    - [x] Update typescript-best-practices/manifest.json
    - [x] Update api-design/manifest.json
    - [x] Update testing-strategies/manifest.json

- [x] Task: Update SKILL.md files [40a78ca]
    - [x] Update conductor-methodology/SKILL.md headers
    - [x] Update typescript-best-practices/SKILL.md headers
    - [x] Update api-design/SKILL.md headers
    - [x] Update testing-strategies/SKILL.md headers

- [x] Task: Conductor - User Manual Verification 'Update Core Skill Files' (Protocol in workflow.md)

---

## Phase 3: Update Command Files

- [x] Task: Update commands/skills.md [40a78ca]
    - [x] Search for skill name references
    - [x] Update any examples or documentation
    - [x] Update display logic if needed

- [x] Task: Update other command files [40a78ca]
    - [x] Search commands/ directory for skill name references
    - [x] Update any references found

- [x] Task: Conductor - User Manual Verification 'Update Command Files' (Protocol in workflow.md)

---

## Phase 4: Update Documentation

- [x] Task: Update README.md [40a78ca]
    - [x] Search for skill name references
    - [x] Update to lowercase-with-hyphens format
    - [x] Verify all examples are correct

- [x] Task: Update CLAUDE.md [40a78ca]
    - [x] Search for skill name references
    - [x] Update to lowercase-with-hyphens format

- [x] Task: Update other documentation files [40a78ca]
    - [x] Search docs/ directory for skill name references
    - [x] Update any references found

- [x] Task: Conductor - User Manual Verification 'Update Documentation' (Protocol in workflow.md)

---

## Phase 5: Verification and Testing

- [x] Task: Manual verification of all changes [40a78ca]
    - [x] Verify skill-registry.json is valid JSON
    - [x] Verify manifest-schema.json is valid JSON Schema
    - [x] Verify all manifest.json files are valid
    - [x] Check for any remaining Title Case skill names

- [x] Task: Test /conductor:skills list command [40a78ca]
    - [x] Run the command
    - [x] Verify skills display with correct lowercase names
    - [x] Verify status indicators work correctly

- [x] Task: Test /conductor:skills info command [40a78ca]
    - [x] Test with each skill name
    - [x] Verify information displays correctly
    - [x] Ensure no broken references

- [x] Task: Conductor - User Manual Verification 'Verification and Testing' (Protocol in workflow.md)

---

## Implementation Notes

- This is a refactoring task with no functional changes
- All JSON files must remain valid after updates
- Use grep/search extensively to find all references
- Be thorough to avoid leaving inconsistencies
