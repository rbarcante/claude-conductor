# Specification: Apache-2.0 License Compliance for Claude Conductor

## Overview

This track ensures the Claude Conductor for Claude Code is fully compliant with the Apache License 2.0 requirements for derivative works. The plugin is adapted from the original "Conductor Extension for Gemini CLI" project.

## Background

The Claude Conductor is a derivative work based on the Apache 2.0 licensed "Conductor Extension for Gemini CLI" (https://github.com/gemini-cli-extensions/conductor). As per Apache 2.0 Section 4 (Redistribution), derivative works must:

- (a) Provide recipients a copy of the License ✓ (already present)
- (b) Include prominent notices stating files were changed
- (c) Retain all copyright, patent, trademark, and attribution notices
- (d) Include NOTICE file contents if present in original (N/A - no NOTICE in original)

## Functional Requirements

### FR-1: Create NOTICE File

Create a `NOTICE` file at the project root containing:
- Project name: "Claude Conductor for Claude Code"
- Statement that this is a derivative work
- Original project name: "Conductor Extension for Gemini CLI"
- Original project URL: https://github.com/gemini-cli-extensions/conductor
- Original copyright holder attribution
- Year of original work and year of derivative work
- Statement that significant modifications were made

### FR-2: Create CONTRIBUTING.md

Create a `CONTRIBUTING.md` file adapted for Claude Code plugin contributions containing:
- How to contribute to the project
- Code of conduct reference (if applicable)
- Contribution guidelines
- License terms for contributions (Apache 2.0)
- Note about the project's origin as a derivative work

### FR-3: Update README.md Attribution Section

Add an "Attribution" or "Acknowledgments" section to `README.md` containing:
- Clear statement that this project is derived from Conductor for Gemini CLI
- Link to the original project repository
- Note that significant modifications and additions were made
- Apache 2.0 license reference

## Non-Functional Requirements

### NFR-1: Compliance Accuracy
All attribution text must accurately reflect the Apache 2.0 license requirements and not misrepresent the relationship between the projects.

### NFR-2: Maintainability
Attribution should be consolidated in standard locations (NOTICE, README) to minimize maintenance burden.

## Acceptance Criteria

- [ ] NOTICE file exists at project root with complete attribution
- [ ] CONTRIBUTING.md exists with contribution guidelines and license terms
- [ ] README.md contains an Attribution section with original project credit
- [ ] All files follow Apache 2.0 standard formatting conventions
- [ ] No misleading or incomplete attribution statements

## Out of Scope

- Adding license headers to individual source files (not required for this scope)
- Detailed changelog of all modifications from the original
- Per-component attribution tracking
- Legal review (this is a best-effort compliance implementation)
