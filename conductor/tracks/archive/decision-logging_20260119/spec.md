# Specification: Decision Logging

## Overview

Capture the "why" alongside the "what" by implementing Architecture Decision Record (ADR) logging within tracks. Create a decisions.md file for each track that documents key implementation choices, alternatives considered, and rationale. This transforms git history from a timeline of changes into a self-documenting codebase that explains reasoning.

## Background

Current git notes capture task summaries but not decision rationale. When developers encounter code months later, they see what was done but not why that approach was chosen. This feature adds structured decision logging following the ADR format, creating an audit trail that explains architectural and implementation decisions.

## Functional Requirements

### FR1: Decision Log Template
- Create `/templates/decisions.md` template file
- Use Architecture Decision Record (ADR) format
- Include sections: Decision title, Date, Status, Context, Decision, Consequences
- Support multiple decisions per track

### FR2: Track Structure Enhancement
- Modify `commands/newTrack.md` to create decisions.md for every new track
- Initialize with empty state and format explanation
- Include decisions.md in track's index.md

### FR3: Decision Capture Protocol
- Create protocol for identifying decision points during implementation
- Trigger on: technology selection, pattern choice, tradeoffs, API design
- Present options with recommendation to user
- Record user's choice with rationale

### FR4: Decision Recording Flow
- Prompt user when non-trivial choice detected
- Present context and alternatives (A/B/C format)
- Capture user selection and reasoning
- Append to track's decisions.md in ADR format
- Reference decision in git note for related commit

### FR5: Enhanced Git Notes
- Modify git note format to include "Decisions Made" section
- Reference specific decisions.md entries
- Link commit to decision context

### FR6: Workflow Template Update
- Modify `templates/workflow.md` to include enhanced git note format
- Document decision capture points in task workflow
- Add "Why" section to git notes

## Non-Functional Requirements

### NFR1: Decision Quality
- Decisions must capture context, not just outcome
- Alternatives must be documented, not just chosen option
- Consequences must include tradeoffs

### NFR2: Non-Intrusive
- Decision capture should not disrupt flow for trivial choices
- Only trigger on significant architectural/technical decisions
- User can defer decision documentation

### NFR3: Searchability
- decisions.md format is grep-friendly
- Decisions are chronologically ordered
- Each decision has clear title

## Acceptance Criteria

- [ ] decisions.md template created with ADR format
- [ ] newTrack.md creates decisions.md for every track
- [ ] Decision Capture Protocol documented
- [ ] implement.md prompts for decisions at appropriate points
- [ ] decisions.md includes context, alternatives, and consequences
- [ ] Git notes reference decisions made
- [ ] workflow.md updated with enhanced git note format

## Out of Scope

- Automatic decision extraction from code (manual capture only)
- Decision search/query tool (future enhancement)
- Decision visualization (future enhancement)
- Cross-track decision dependencies

## Dependencies

None - standalone feature that enhances existing tracking
