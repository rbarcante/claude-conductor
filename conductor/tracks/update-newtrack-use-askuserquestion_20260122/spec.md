# Specification: Update newTrack.md to Use AskUserQuestion Tool

> **Type:** feature
> **Track ID:** `update-newtrack-use-askuserquestion_20260122`

## Overview

Update the `commands/newTrack.md` file to use the structured `AskUserQuestion` tool for all interactive user prompts, aligning with the patterns established in `setup.md` and `implement.md`. This enhancement improves user experience by providing clickable options instead of free-form text prompts.

## Background

The `newTrack.md` command currently uses text-based prompts for user interaction, while `setup.md` and `implement.md` use the structured `AskUserQuestion` tool. This inconsistency creates a fragmented user experience. By updating `newTrack.md` to use `AskUserQuestion`, we achieve:
- Consistent UX across all Conductor commands
- Clickable options instead of typing responses
- Structured response handling
- Auto-generate capability for faster track creation

## Requirements

### Functional Requirements

#### FR-1: Add AskUserQuestion Tool Protocol Section

Add a new section after "CLI Operations" (approximately line 121) that documents:
- [x] JSON structure for the AskUserQuestion tool
- [x] Key constraints (header max 12 characters, 2-4 options, multiSelect rules)
- [x] Standard option patterns specific to newTrack command
- [x] Question type mapping (Additive vs Exclusive Choice)

#### FR-2: Update Section 2.1 (Get Track Description)

When `{{args}}` is empty and user needs to provide a track description:
- [x] Keep the free-form text approach for track descriptions (descriptions are inherently unique)
- [x] Add guidance on how the description will be used
- [x] No AskUserQuestion needed here since descriptions are not selectable options

#### FR-3: Update Section 2.2 (Interactive Specification Generation)

- [x] Replace text-based question guidelines with AskUserQuestion tool-based instructions
- [x] Add JSON template examples for Additive questions (multiSelect: true)
- [x] Add JSON template examples for Exclusive Choice questions (multiSelect: false)
- [x] Include Auto-generate option pattern in all spec questions
- [x] Replace text-based confirmation with AskUserQuestion approval pattern

#### FR-4: Update Section 2.3 (Interactive Plan Generation)

- [x] Replace text-based confirmation with AskUserQuestion approval pattern
- [x] Document response handling (Approve → proceed, Suggest changes → revise)

### Non-Functional Requirements

- [x] NFR-1: All AskUserQuestion patterns must match the structure and conventions used in `setup.md` and `implement.md`
- [x] NFR-2: The AskUserQuestion Tool Protocol section should be comprehensive enough to serve as a reference
- [x] NFR-3: The updated command must still support the existing workflow where `{{args}}` contains a track description

## Acceptance Criteria

- [x] AC-1: A new "AskUserQuestion Tool Protocol" section exists after "CLI Operations" with JSON structure, constraints, and example patterns
- [x] AC-2: Section 2.2 uses AskUserQuestion tool for all interactive spec questions
- [x] AC-3: Section 2.2 includes Auto-generate option in all question patterns
- [x] AC-4: Section 2.2 User Confirmation uses AskUserQuestion approval pattern
- [x] AC-5: Section 2.3 User Confirmation uses AskUserQuestion approval pattern
- [x] AC-6: All JSON examples are valid and match the documented structure
- [x] AC-7: The updated command correctly handles all response options (Approve, Suggest changes, Auto-generate)

## Out of Scope

- Section 2.4 (Create and Register Track) - CLI-based operations, no user interaction changes needed
- Adding new questions or changing the question content - only the format changes
- Changes to other commands (setup.md, implement.md)
- Changes to the conductor_cli.py script

## Dependencies

- None identified

## References

- `commands/setup.md` - Reference implementation for AskUserQuestion Tool Protocol (lines 149-261)
- `commands/implement.md` - Reference implementation for AskUserQuestion in Git Isolation (lines 180-257)
