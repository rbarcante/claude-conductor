# Implementation Plan: Update Skills to Lower-Case Name Format

## Overview
Standardize all skill naming across the Conductor plugin to use the `lowercase-with-hyphens` format consistently.

---

## Phase 1: Discovery and Analysis

- [ ] Task: Identify all files containing skill name references
    - [ ] Search for "Conductor Methodology" references across codebase
    - [ ] Search for "TypeScript Best Practices" references across codebase
    - [ ] Search for "API Design" references across codebase
    - [ ] Search for "Testing Strategies" references across codebase
    - [ ] Document all file locations that need updates

- [ ] Task: Conductor - User Manual Verification 'Discovery and Analysis' (Protocol in workflow.md)

---

## Phase 2: Update Core Skill Files

- [ ] Task: Update skill-registry.json
    - [ ] Change all skill names to lowercase-with-hyphens format
    - [ ] Verify JSON structure remains valid
    - [ ] Ensure paths and names are aligned

- [ ] Task: Update manifest-schema.json
    - [ ] Update example skill names in the schema
    - [ ] Update description text if it references specific skill names
    - [ ] Verify schema remains valid

- [ ] Task: Update individual skill manifest.json files
    - [ ] Update conductor-methodology/manifest.json
    - [ ] Update typescript-best-practices/manifest.json
    - [ ] Update api-design/manifest.json
    - [ ] Update testing-strategies/manifest.json

- [ ] Task: Update SKILL.md files
    - [ ] Update conductor-methodology/SKILL.md headers
    - [ ] Update typescript-best-practices/SKILL.md headers
    - [ ] Update api-design/SKILL.md headers
    - [ ] Update testing-strategies/SKILL.md headers

- [ ] Task: Conductor - User Manual Verification 'Update Core Skill Files' (Protocol in workflow.md)

---

## Phase 3: Update Command Files

- [ ] Task: Update commands/skills.md
    - [ ] Search for skill name references
    - [ ] Update any examples or documentation
    - [ ] Update display logic if needed

- [ ] Task: Update other command files
    - [ ] Search commands/ directory for skill name references
    - [ ] Update any references found

- [ ] Task: Conductor - User Manual Verification 'Update Command Files' (Protocol in workflow.md)

---

## Phase 4: Update Documentation

- [ ] Task: Update README.md
    - [ ] Search for skill name references
    - [ ] Update to lowercase-with-hyphens format
    - [ ] Verify all examples are correct

- [ ] Task: Update CLAUDE.md
    - [ ] Search for skill name references
    - [ ] Update to lowercase-with-hyphens format

- [ ] Task: Update other documentation files
    - [ ] Search docs/ directory for skill name references
    - [ ] Update any references found

- [ ] Task: Conductor - User Manual Verification 'Update Documentation' (Protocol in workflow.md)

---

## Phase 5: Verification and Testing

- [ ] Task: Manual verification of all changes
    - [ ] Verify skill-registry.json is valid JSON
    - [ ] Verify manifest-schema.json is valid JSON Schema
    - [ ] Verify all manifest.json files are valid
    - [ ] Check for any remaining Title Case skill names

- [ ] Task: Test /conductor:skills list command
    - [ ] Run the command
    - [ ] Verify skills display with correct lowercase names
    - [ ] Verify status indicators work correctly

- [ ] Task: Test /conductor:skills info command
    - [ ] Test with each skill name
    - [ ] Verify information displays correctly
    - [ ] Ensure no broken references

- [ ] Task: Conductor - User Manual Verification 'Verification and Testing' (Protocol in workflow.md)

---

## Implementation Notes

- This is a refactoring task with no functional changes
- All JSON files must remain valid after updates
- Use grep/search extensively to find all references
- Be thorough to avoid leaving inconsistencies
