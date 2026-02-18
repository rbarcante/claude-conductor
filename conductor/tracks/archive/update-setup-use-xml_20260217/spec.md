# Specification: Update setup.md to use XML tags following newTrack.md pattern

## Overview

Refactor `commands/setup.md` to adopt the same XML tag structure used in `commands/newTrack.md` (introduced in PR #38). This improves prompt clarity and structured parsing by Claude, following Anthropic prompt engineering guidelines.

## Functional Requirements

### 1. Match XML Tag Structure from newTrack.md

Apply the following tag mapping to setup.md:

| newTrack.md tag | Purpose | setup.md equivalent section |
|---|---|---|
| `<system_directive>` | Top-level agent directive with critical note | Section 1.0 SYSTEM DIRECTIVE |
| `<cli_reference>` | CLI commands block | Action CLI Commands |
| `<protocol name="askuserquestion">` + `<constraints>` | AskUserQuestion protocol | AskUserQuestion Tool Protocol |
| `<phase name="...">` | Major workflow phase | Sections 1.1, 1.2, 2.0–2.6, 3.0–3.4 |
| `<instructions name="...">` | Instructions within a phase | Sub-sections within phases |
| `<note>` | Side notes or conditionals | Fallback instructions, Brownfield-only steps |
| `<note type="critical">` | Critical inline callouts | CRITICAL warnings |

### 2. Preserve All Existing Content

No functional content, protocol steps, or behavioral instructions may be removed or altered. Only the structural markup changes.

### 3. Apply to All Major Sections

- Section 1.0 SYSTEM DIRECTIVE → `<system_directive>`
- Action CLI Commands + Fallback → `<cli_reference>`
- AskUserQuestion Tool Protocol → `<protocol name="askuserquestion">` with `<constraints>`
- Section 1.1 RESUME CHECK → `<phase name="resume_check">`
- Section 1.2 PRE-INITIALIZATION OVERVIEW → `<phase name="pre_init">`
- Section 2.0 PROJECT INCEPTION (2.0.1–2.0.3) → `<phase name="inception">` with `<instructions>`
- Sections 2.1–2.5.1 → individual `<phase>` elements with `<instructions>`
- Section 2.6 Finalization → `<phase name="finalization">`
- Section 3.0–3.4 INITIAL TRACK GENERATION → `<phase name="track_generation">` with `<instructions>`

## Non-Functional Requirements

- The resulting file must load and execute identically to the current version
- File size increase should be minimal (XML tags are lightweight)

## Acceptance Criteria

- [ ] `commands/setup.md` uses the same XML tag schema as `commands/newTrack.md`
- [ ] All 9 section types have appropriate XML wrapper tags
- [ ] Critical notes use `<note type="critical">` inline
- [ ] Brownfield-only sections use `<note>` or `<instructions>` with appropriate condition labels
- [ ] No functional content is added, removed, or altered
- [ ] The file is valid markdown with correctly nested XML tags

## Out of Scope

- Changing the behavioral logic of any protocol step
- Adding new setup steps or modifying existing workflow
- Updating other command files (newTrack.md, implement.md, etc.)
