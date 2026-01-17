# Anti-Pattern Registry

This file serves as the central index for all anti-patterns in the Conductor Quality Intelligence system.

## Overview

Anti-patterns are common code smells and problematic practices that should be avoided. They are automatically detected during quality gate verification and categorized by severity:

1. **Critical** - Blocks task completion; must be fixed
2. **High** - Warns strongly; should be fixed before proceeding
3. **Medium** - Informational; consider fixing when time permits

## How Anti-Patterns are Used

Anti-patterns are automatically scanned during `/conductor:implement` task completion. The quality gate:

1. Scans modified files for anti-pattern matches
2. Reports findings with file:line references
3. Blocks on critical severity issues
4. Allows documented skips for high/medium severity

---

## Critical Severity

Anti-patterns that indicate severe code quality issues. **Must be resolved before task completion.**

| Anti-Pattern | Category | Detection | Blocking |
|--------------|----------|-----------|----------|
| *None defined yet* | - | - | Yes |

---

## High Severity

Anti-patterns that significantly impact maintainability. **Should be resolved; can be skipped with documented reason.**

| Anti-Pattern | Category | Detection | Blocking |
|--------------|----------|-----------|----------|
| [God Object](./core/god-object.md) | Code Structure | Class/file >500 lines or >20 methods | No |
| [Spaghetti Code](./core/spaghetti-code.md) | Control Flow | Cyclomatic complexity >15 | No |
| [Mutable Defaults](./core/mutable-defaults.md) | Data Handling | Mutable default arguments | No |

---

## Medium Severity

Anti-patterns that affect code quality but are lower priority. **Informational; skip is automatic unless configured otherwise.**

| Anti-Pattern | Category | Detection | Blocking |
|--------------|----------|-----------|----------|
| [Magic Numbers](./core/magic-numbers.md) | Naming | Numeric literals outside constants | No |
| [Deep Nesting](./core/deep-nesting.md) | Control Flow | Nesting depth >4 levels | No |

---

## Stack-Specific Anti-Patterns

Technology-specific anti-patterns organized by stack. *Coming in future tracks.*

| Stack | Status | Anti-Patterns |
|-------|--------|---------------|
| Python | Planned | Bare except, mutable defaults in class attributes |
| JavaScript | Planned | Callback hell, implicit globals |
| TypeScript | Planned | Any abuse, type assertion overuse |
| Go | Planned | Naked returns, ignored errors |

---

## Skipping Anti-Pattern Warnings

When a high or medium severity anti-pattern is detected but intentional, document the skip:

1. The quality gate will prompt for a reason
2. The reason is recorded in the git note for the task
3. Future reviewers can understand the decision

### Skip Documentation Format

```
## Quality Gate Decisions

### Skipped Anti-Patterns
- **[anti-pattern-name]** at file.ext:42
  - Reason: [Explanation of why this is acceptable]
  - Reviewed: YYYY-MM-DD
```

---

## Contributing Anti-Patterns

To add a new anti-pattern:

1. Create a new markdown file in the appropriate directory (`core/` or `stack/<technology>/`)
2. Use the [TEMPLATE.md](./TEMPLATE.md) as your starting point
3. Define clear detection patterns (regex) and thresholds
4. Assign appropriate severity level
5. Add the anti-pattern to this index
6. Test detection with sample code containing the anti-pattern
