# Specification: Quality Intelligence

## Overview

Transform quality gates from simple thresholds into intelligent guidance systems. Add anti-pattern detection, smart coverage analysis with specific test suggestions, and automated quality verification before task completion. This elevates code quality from "meets minimum coverage" to "follows best practices and tests what matters."

## Background

Currently, Conductor enforces basic quality gates (>80% coverage, tests pass) but provides no guidance on what to test or how to avoid common mistakes. Developers get a pass/fail signal without actionable feedback. This feature adds intelligence to quality enforcement by detecting anti-patterns and suggesting specific tests based on coverage gaps.

## Functional Requirements

### FR1: Anti-Pattern Library
- Create `/patterns/anti-patterns/` directory structure
- Create anti-pattern index at `/patterns/anti-patterns/index.md`
- Create 5 core anti-patterns (god-object, magic-numbers, spaghetti-code, deep-nesting, mutable-defaults)
- Each anti-pattern includes: detection rules, severity, problem explanation, solution

### FR2: Anti-Pattern Detection Format
Each anti-pattern file must include:
- YAML frontmatter with name, severity, detection patterns (regex), file extensions
- Problem description
- Detection criteria
- Solution with code examples (Bad vs Good)
- When exceptions are acceptable

### FR3: Quality Analysis Protocol
- Create `/protocols/quality-analysis.md`
- Define anti-pattern scanning process for modified files
- Define severity levels: critical (blocks), high (warns), medium (info)
- Define reporting format with file path, line number, and suggestion

### FR4: Coverage Intelligence Protocol
- Create `/protocols/coverage-intelligence.md`
- Define coverage report parsing (lcov, coverage.py, etc.)
- Prioritize test suggestions (business logic > error paths > utilities)
- Calculate estimated coverage gain per suggested test

### FR5: Quality Gate Integration
- Modify `commands/implement.md` to run quality gate before task completion
- Execute anti-pattern scan and present findings
- Execute coverage intelligence and present suggestions
- Allow skip for high/medium severity with documented reason
- Block on critical severity issues

### FR6: Workflow Enhancement
- Modify `templates/workflow.md` to include coverage intelligence protocol
- Update quality gates section with anti-pattern checks
- Define git note format for quality decisions (skipped warnings, rationale)

## Non-Functional Requirements

### NFR1: Performance
- Quality analysis should complete in <10 seconds for typical changes
- Pattern matching should be efficient (compiled regex)

### NFR2: Extensibility
- Anti-pattern format supports community contributions
- Detection patterns use standard regex syntax
- New language-specific anti-patterns can be added easily

### NFR3: User Experience
- Warnings are actionable with specific suggestions
- Critical issues clearly explained
- Skip option available with documentation requirement

## Acceptance Criteria

- [ ] Anti-pattern library created with 5 core patterns
- [ ] Quality Analysis Protocol documented
- [ ] Coverage Intelligence Protocol documented
- [ ] Quality gate runs before task completion
- [ ] Anti-patterns detected and reported with file:line references
- [ ] Coverage suggestions prioritized and include estimated impact
- [ ] Critical issues block task completion
- [ ] Skipped warnings documented in git notes

## Out of Scope

- Language-specific anti-patterns beyond core 5 (future enhancement)
- Automated fixing of anti-patterns (suggest only, don't auto-fix)
- Integration with external linting tools (use existing project tools)
- Real-time anti-pattern detection during coding

## Dependencies

- Pattern Reference Layer (Track 1) - extends pattern directory structure
