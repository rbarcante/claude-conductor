# Specification: Implement AskUserQuestion Tool Standardization

## Overview

Refactor `commands/implement.md` to use the `AskUserQuestion` tool for all user interactions instead of text-based prompts. This brings consistency with the pattern already established in `newTrack.md` and provides a better user experience with clickable options.

## Functional Requirements

### FR-1: Track Selection (Section 2.0)

Convert track selection confirmation prompts to use AskUserQuestion:
- Track match confirmation ("Is this correct?")
- Use exclusive choice (multiSelect: false)

### FR-2: Pattern Surfacing (Section 3.0, Step 4)

Convert pattern application prompt to AskUserQuestion:
- Options: Apply, Skip, View first
- Replace "Y/S/V" text prompt with structured options
- Use exclusive choice (multiSelect: false)

### FR-3: Quality Gate (Section 3.5)

Convert quality gate prompts to AskUserQuestion:
- **Options prompt (1/2/3):** Convert to structured options (Fix, Skip, View details)
- **Skip reason prompt:** Convert to AskUserQuestion with common reason options plus custom text
- Combine follow-up prompts where possible using multiSelect

### FR-4: Decision Capture (Section 3.6)

Convert decision point prompts to AskUserQuestion:
- Present options A/B/skip as structured choices
- Include option descriptions from existing prose
- Use exclusive choice (multiSelect: false)

### FR-5: Documentation Synchronization (Section 4.0)

Convert approval prompts to AskUserQuestion:
- Product Definition approval (yes/no → Approve/Reject)
- Tech Stack approval (yes/no → Approve/Reject)
- Product Guidelines approval (with warning) → Approve/Reject with critical styling
- Use exclusive choice (multiSelect: false)

### FR-6: Track Cleanup (Section 5.0)

Convert cleanup prompts to AskUserQuestion:
- Archive/Delete/Skip options → structured choices with descriptions
- Delete confirmation → separate AskUserQuestion with warning in question text
- Use exclusive choice (multiSelect: false)

## Non-Functional Requirements

### NFR-1: Consistency

All AskUserQuestion calls must follow the protocol defined in newTrack.md:
- Header max 12 characters
- 2-4 options per question
- Options include label and description
- No explicit "Other" option (provided automatically)

### NFR-2: Backward Compatibility

The logical flow and outcomes must remain unchanged. Only the interaction mechanism changes.

## Acceptance Criteria

1. All user-facing prompts in implement.md use AskUserQuestion tool
2. No text-based prompts remain (no "Enter choice", "yes/no", "A/B/C" patterns)
3. AskUserQuestion protocol section added to implement.md (matching newTrack.md)
4. All headers are ≤12 characters
5. All questions have 2-4 options with descriptions

## Out of Scope

- Changes to the logical flow of implement.md
- Changes to CLI commands or fallback behavior
- Adding new questions or removing existing ones
- Changes to other command files
