# Dual-Format Standard

This document defines the standard for creating AI-optimized content alongside human documentation in Conductor artifacts.

## Overview

The dual-format standard ensures all patterns, styleguides, and templates contain:
1. **AI Quick Reference** - Condensed, structured content optimized for AI context windows
2. **Human Documentation** - Detailed explanations with examples and context

This approach maximizes AI effectiveness by providing structured lookup formats while maintaining comprehensive documentation for human developers.

## Design Rationale

### Why Dual Format?

AI assistants operate under context window constraints and benefit from:
- **Condensed information** - More context fits in fewer tokens
- **Structured format** - Consistent parsing and reliable extraction
- **Clear sections** - Explicit boundaries reduce ambiguity
- **Actionable content** - Direct guidance over explanatory prose

Human developers need:
- **Detailed explanations** - Understanding the "why" behind rules
- **Multiple examples** - Different scenarios and edge cases
- **Trade-off analysis** - When to apply or deviate from patterns
- **Related concepts** - Links to other relevant resources

### Token Efficiency

The AI Quick Reference section targets approximately 10-20% of the full document size while capturing 80% of the actionable guidance. This allows AI assistants to:
- Load multiple patterns/styleguides simultaneously
- Quickly reference key decisions without full context
- Apply patterns consistently across implementations

## Format Specifications

### Patterns (AI Quick Reference)

**Location:** Top of pattern file, after YAML frontmatter
**Maximum:** 50 lines
**Required Sections:**

| Section | Purpose | Format |
|---------|---------|--------|
| **When to Apply** | Trigger conditions | Bullet list (3-5 items) |
| **Core Principles** | Key guiding rules | Numbered list (3-5 items) |
| **Quick Implementation Checklist** | Action items | Checkbox list |
| **Code Pattern** | Structure template | Pseudocode block |
| **Key Decisions** | Decision matrix | Table |

**Example Structure:**
```markdown
## AI Quick Reference

### When to Apply
- Condition 1
- Condition 2

### Core Principles
1. **Principle**: Explanation
2. **Principle**: Explanation

### Quick Implementation Checklist
- [ ] Step 1
- [ ] Step 2

### Code Pattern (Pseudocode)
```pseudocode
// Condensed pattern structure
```

### Key Decisions
| Decision | Recommended | Rationale |
|----------|-------------|-----------|
| Choice 1 | Option A    | Why       |
```

### Styleguides (AI Quick Reference)

**Location:** Top of styleguide file
**Maximum:** 30 lines
**Required Sections:**

| Section | Purpose | Format |
|---------|---------|--------|
| **Language Rules** | Critical syntax/style rules | Bullet list (5-8 items) |
| **Type Patterns** | Type system guidance | Bullet list (3-5 items) |
| **Avoid** | Anti-patterns to prevent | Bullet list (3-5 items) |

**Example Structure:**
```markdown
## AI Quick Reference

### Language Rules
- Rule 1: `example`
- Rule 2: `example`

### Type Patterns
- Pattern: explanation

### Avoid
- Anti-pattern 1
- Anti-pattern 2
```

### Skills (AI Quick Reference)

Skills follow a similar pattern within SKILL.md files:

**Maximum:** N/A (optimized throughout)
**Required Sections:**
- Core Principles (3-5 items)
- Topic-specific sections
- Quick Reference checklist at end

See [Skill Development Guide](./skill-development.md) for details.

## Writing Guidelines

### AI Quick Reference Sections

**Do:**
- Use imperative voice ("Use X" not "You should use X")
- Include inline code examples where helpful
- Keep bullet points to one line when possible
- Use tables for decision matrices
- Prefer pseudocode over language-specific code

**Don't:**
- Include lengthy explanations
- Duplicate content between AI and Human sections
- Use vague guidance ("consider" → "use when")
- Exceed line limits
- Add redundant context

### Counting Lines

Line limits apply to the rendered content:
- Empty lines count
- Code block markers count
- Table header separators count

Use this mental model: "Can an AI read and apply this in one pass?"

## Implementation Checklist

### For Patterns

- [ ] YAML frontmatter with activation keywords
- [ ] AI Quick Reference section (≤50 lines)
  - [ ] When to Apply
  - [ ] Core Principles
  - [ ] Quick Implementation Checklist
  - [ ] Code Pattern (Pseudocode)
  - [ ] Key Decisions
- [ ] `---` separator
- [ ] Human Documentation section
  - [ ] Overview
  - [ ] Detailed Explanation
  - [ ] Implementation Examples
  - [ ] Best Practices
  - [ ] Trade-offs and Considerations
- [ ] Anti-Patterns section
- [ ] Related Patterns links
- [ ] References

### For Styleguides

- [ ] AI Quick Reference section (≤30 lines)
  - [ ] Language Rules
  - [ ] Type Patterns
  - [ ] Avoid
- [ ] `---` separator
- [ ] Original styleguide content preserved
- [ ] Source attribution

## Validation

### Manual Validation

1. Count lines in AI Quick Reference (use `wc -l` or editor)
2. Verify all required sections present
3. Check for actionable, structured content
4. Ensure no duplication between sections

### Automated Validation (Future)

A validation script could check:
- Line count limits
- Required section headers
- Format consistency

## Examples

### Well-Formatted Pattern AI Section

```markdown
## AI Quick Reference

### When to Apply
- Implementing retry logic for network operations
- Handling transient failures in distributed systems
- Building resilient API clients

### Core Principles
1. **Exponential Backoff**: Increase delay between retries
2. **Jitter**: Add randomness to prevent thundering herd
3. **Max Attempts**: Always set a retry limit
4. **Circuit Breaker**: Stop retrying after threshold

### Quick Implementation Checklist
- [ ] Define retry-able error types
- [ ] Configure max retries (typically 3-5)
- [ ] Implement exponential backoff with jitter
- [ ] Log each retry attempt
- [ ] Set overall timeout

### Code Pattern (Pseudocode)
```
function withRetry(operation, maxAttempts = 3):
    for attempt in 1..maxAttempts:
        try:
            return operation()
        catch RetryableError as e:
            if attempt == maxAttempts:
                throw e
            delay = baseDelay * (2 ^ attempt) + random()
            sleep(delay)
```

### Key Decisions
| Decision | Recommended | Rationale |
|----------|-------------|-----------|
| Backoff type | Exponential + jitter | Prevents thundering herd |
| Max retries | 3-5 | Balances reliability vs latency |
| Timeout | Operation-specific | Prevents infinite waits |
```

### Well-Formatted Styleguide AI Section

```markdown
## AI Quick Reference

### Language Rules
- Use `const` by default, `let` when reassignment needed, never `var`
- Named exports only: `export { MyClass }` (no default exports)
- Single quotes for strings, template literals for interpolation
- Always use `===` and `!==` for equality
- End all statements with semicolons explicitly

### Type Patterns
- Prefer interfaces for object shapes over type aliases
- Use `T[]` for simple arrays, `Array<T>` for complex unions
- Optional params (`?`) over `| undefined`
- Use `unknown` over `any` when type is uncertain

### Avoid
- `any` type without explicit justification comment
- Type assertions (`as`) and non-null assertions (`!`)
- `namespace` declarations
- `#private` fields (use `private` modifier)
- Wrapper objects (`new String()`, `new Boolean()`)
```

## Related Documents

- [Pattern Template](../patterns/TEMPLATE.md) - Pattern file structure
- [Skill Development Guide](./skill-development.md) - Skill content guidelines
- [Skill Manifest Schema](./skill-manifest-schema.md) - Skill configuration
