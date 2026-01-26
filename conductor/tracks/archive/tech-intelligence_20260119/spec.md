# Specification: Technology-Aware Intelligence

## Overview

Add technology detection and awareness capabilities to Conductor, enabling automatic stack detection, intelligent skill activation, and context-aware guidance during implementation. This transforms setup from a manual process into an intelligent system that understands the project's technology landscape.

## Background

Currently, Conductor's setup command asks users about their technology stack but doesn't leverage this information for intelligent behavior. For brownfield projects, users must manually describe their stack even though it can be inferred from manifest files and code patterns. This feature adds automatic detection and uses stack information to activate relevant skills and patterns.

## Functional Requirements

### FR1: Stack Detection Protocol
- Create `/protocols/stack-detection.md` documenting the detection algorithm
- Scan manifest files (package.json, pom.xml, requirements.txt, go.mod, Cargo.toml, etc.)
- Analyze file extension distribution to identify primary languages
- Detect frameworks from imports and dependencies
- Generate structured stack profile with confidence scores

### FR2: Enhanced Setup with Auto-Detection
- Modify `commands/setup.md` to run stack detection for brownfield projects
- Present detected stack to user with confidence level
- Allow user corrections before proceeding
- Pre-populate tech-stack.md with detected information

### FR3: Skill Registry System
- Create `/skills/skill-registry.json` as central skill index
- Define skill metadata schema (name, path, activation rules)
- Support activation by stack match, framework match, and task keywords
- Enable skill enable/disable via project settings

### FR4: Skill Activation Protocol
- Add Skill Loading Protocol to `CLAUDE.md`
- Build activation index from skill registry
- Match skills to current task context
- Load matching SKILL.md files into implementation context

### FR5: Context-Aware Task Execution
- Modify `commands/implement.md` to activate relevant skills before each task
- Announce activated skills to user
- Provide skill-specific guidance during implementation

## Non-Functional Requirements

### NFR1: Detection Accuracy
- Stack detection should achieve >85% accuracy for common stacks
- Graceful fallback when detection confidence is low
- Never override explicit user input

### NFR2: Performance
- Stack detection should complete in <5 seconds for typical projects
- Skill activation should add minimal overhead to task execution

### NFR3: Extensibility
- New stack types can be added without code changes
- Skill registry format supports community contributions

## Acceptance Criteria

- [ ] Stack Detection Protocol documented and functional
- [ ] Setup auto-detects stack for brownfield projects
- [ ] Skill registry system created with schema documentation
- [ ] Skills activate automatically based on task context
- [ ] User can override detected stack
- [ ] Existing Conductor functionality unchanged

## Out of Scope

- Creating technology-specific skills (separate tracks)
- Pattern activation (handled by Pattern Reference Layer)
- Anti-pattern detection (Quality Intelligence track)

## Dependencies

- Pattern Reference Layer (Track 1) - patterns may be activated alongside skills
