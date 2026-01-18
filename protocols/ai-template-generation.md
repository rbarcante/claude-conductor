# AI Template Generation Protocol

**Version:** 1.0.0
**Purpose:** Generate AI-optimized dual-format content during setup and pattern creation
**Scope:** Conductor setup command, pattern creation, styleguide selection

---

## Overview

This protocol defines the rules and process for generating AI-optimized content that follows the Dual-Format Standard. All generated patterns, styleguides, and documentation should include both an AI Quick Reference section (for rapid AI consumption) and detailed human documentation.

---

## Dual-Format Standard

### Core Principle

Every template and pattern file should contain two distinct sections:
1. **AI Quick Reference** - Optimized for AI parsing (max 30-50 lines)
2. **Human Documentation** - Detailed explanations, examples, and rationale

### Format Structure

```markdown
# [Document Title]

## AI Quick Reference

[Structured, scannable content optimized for AI consumption]
[Maximum 50 lines for patterns, 30 lines for styleguides]

---

## [Human Documentation Sections]

[Detailed explanations, examples, code samples, rationale]
```

---

## AI Quick Reference Requirements

### Styleguides (Max 30 Lines)

AI Quick Reference for code styleguides MUST include these sections:

| Section | Purpose | Format |
|---------|---------|--------|
| **Language Rules** | Core syntax and conventions | Bullet list, 6-10 items |
| **Type Patterns** | Type system best practices | Bullet list, 5-8 items |
| **Avoid** | Anti-patterns and common mistakes | Bullet list, 4-6 items |

**Example Structure:**

```markdown
## AI Quick Reference

### Language Rules
- Use `const` by default, `let` when reassignment needed
- Named exports only: `export { MyClass }`
- [additional rules...]

### Type Patterns
- Prefer interfaces for object shapes
- Use `T[]` for simple arrays, `Array<T>` for unions
- [additional patterns...]

### Avoid
- `any` type without justification
- Type assertions (`as`) without validation
- [additional anti-patterns...]
```

### Patterns (Max 50 Lines)

AI Quick Reference for patterns MUST include these sections:

| Section | Purpose | Format |
|---------|---------|--------|
| **When to Apply** | Activation conditions | Bullet list, 3-5 items |
| **Core Principles** | Key concepts | Bullet list, 3-5 items |
| **Quick Implementation Checklist** | Step-by-step guide | Numbered list, 4-8 items |
| **Code Pattern** | Minimal code example | Fenced code block, max 15 lines |
| **Key Decisions** | Important choices | Table or bullet list |

**Example Structure:**

```markdown
## AI Quick Reference

### When to Apply
- External API communication
- User input validation required
- [additional conditions...]

### Core Principles
- Fail fast with meaningful errors
- Centralize error handling
- [additional principles...]

### Quick Implementation Checklist
1. Define custom error types
2. Implement error hierarchy
3. [additional steps...]

### Code Pattern
```typescript
// Minimal example showing core pattern
```

### Key Decisions
| Decision | Recommendation |
|----------|---------------|
| Error format | Structured JSON |
| [additional decisions...]
```

---

## Snippet AI Headers

### Code Snippets (TypeScript/JavaScript)

Code snippets MUST include a JSDoc header at the top of the file:

```typescript
/**
 * USE: [When to use this snippet - one sentence]
 * REQUIRES: [Dependencies - comma separated]
 * PATTERN: [Related patterns - comma separated]
 */
```

**Example:**

```typescript
/**
 * USE: When building a type-safe HTTP client for API communication
 * REQUIRES: TypeScript 4.5+
 * PATTERN: Error Handling, Configuration
 */
```

### Code Snippets (Python)

Python snippets MUST include a docstring header:

```python
"""
USE: [When to use this snippet - one sentence]
REQUIRES: [Dependencies - comma separated]
PATTERN: [Related patterns - comma separated]
"""
```

### Pattern Snippets (Markdown)

Pattern snippets MUST include YAML frontmatter:

```yaml
---
use: [When to use - one sentence]
requires: [Prerequisites]
pattern: [Related patterns]
---
```

---

## Generation Rules

### Rule 1: AI Section First

The AI Quick Reference section MUST appear immediately after the document title, before any detailed content.

**Rationale:** AI agents typically read from the top of a file. Placing AI-optimized content first ensures immediate access to key information.

### Rule 2: Strict Line Limits

| Content Type | Max Lines |
|--------------|-----------|
| Styleguide AI Quick Reference | 30 lines |
| Pattern AI Quick Reference | 50 lines |
| Snippet AI Header | 5 lines |

**Enforcement:** Count lines from `## AI Quick Reference` to the `---` separator. Exclude blank lines from count.

### Rule 3: Use Structured Formats

AI Quick Reference sections MUST use:
- **Tables** for decision matrices and comparisons
- **Bullet lists** for principles and rules
- **Numbered lists** for sequential steps
- **Code blocks** for minimal examples (max 15 lines)

**Avoid in AI sections:**
- Prose paragraphs
- Long explanations
- Multiple code examples
- Historical context

### Rule 4: Actionable Content Only

Every item in the AI Quick Reference MUST be:
- **Concrete** - Specific, not abstract
- **Actionable** - Can be directly applied
- **Verifiable** - Can be checked against code

**Good:** "Use `const` by default, `let` when reassignment needed"
**Bad:** "Variables should be declared appropriately"

### Rule 5: Cross-Reference Patterns

When generating styleguides or patterns, include cross-references to related:
- Patterns in `patterns/core/`
- Snippets in `snippets/`
- Skills in `skills/`

Format: `See: [Pattern Name](../patterns/core/pattern-name.md)`

---

## Generation Process

### Step 1: Identify Content Type

Determine what type of content is being generated:

| Content Type | Template Location | AI Section Limit |
|--------------|------------------|------------------|
| Code Styleguide | `templates/code_styleguides/` | 30 lines |
| Pattern | `patterns/core/` | 50 lines |
| Snippet (code) | `snippets/<language>/` | 5-line header |
| Snippet (pattern) | `snippets/patterns/` | YAML frontmatter |

### Step 2: Generate AI Quick Reference

For styleguides and patterns:

1. **Extract key rules** - Identify 15-25 most important rules
2. **Categorize** - Group into required sections
3. **Prioritize** - Place most critical rules first
4. **Format** - Use structured formats (tables, lists)
5. **Validate** - Ensure line count is within limits

For snippets:

1. **Identify use case** - Single sentence description
2. **List dependencies** - Required packages/versions
3. **Link patterns** - Related pattern names

### Step 3: Generate Human Documentation

After the AI Quick Reference:

1. **Add separator** - Use `---` after AI section
2. **Expand sections** - Provide detailed explanations
3. **Add examples** - Include comprehensive code samples
4. **Explain rationale** - Document why rules exist
5. **Link resources** - Reference official documentation

### Step 4: Validate Structure

Before finalizing:

- [ ] AI Quick Reference appears first
- [ ] Line count within limits
- [ ] All required sections present
- [ ] Structured formats used
- [ ] Actionable content only
- [ ] Cross-references included

---

## Setup Command Integration

### Section 2.4: Code Styleguide Selection

When copying styleguides during setup, the protocol ensures:

1. **Use AI-Enhanced Templates:** All styleguide templates in `templates/code_styleguides/` include AI Quick Reference sections.

2. **Verify AI Section:** After copying, verify the styleguide contains:
   - `## AI Quick Reference` header
   - `### Language Rules` section
   - `### Type Patterns` section
   - `### Avoid` section

3. **Report Enhancement:** Announce to user:
   > "Copied AI-enhanced styleguide: [styleguide-name].md (includes AI Quick Reference section)"

### Pattern Creation

When creating new patterns:

1. **Read Template:** Use `patterns/TEMPLATE.md` as the base
2. **Generate AI Section:** Follow AI Quick Reference requirements
3. **Populate Human Docs:** Add detailed content below separator
4. **Add Activation:** Include YAML frontmatter with activation keywords

---

## Validation Checklist

### Styleguide Validation

| Check | Requirement |
|-------|-------------|
| Header | `## AI Quick Reference` present |
| Language Rules | 6-10 bullet items |
| Type Patterns | 5-8 bullet items |
| Avoid | 4-6 bullet items |
| Line Count | ≤ 30 lines |
| Separator | `---` after AI section |

### Pattern Validation

| Check | Requirement |
|-------|-------------|
| Header | `## AI Quick Reference` present |
| When to Apply | 3-5 bullet items |
| Core Principles | 3-5 bullet items |
| Checklist | 4-8 numbered items |
| Code Pattern | ≤ 15 lines |
| Key Decisions | Table or list |
| Line Count | ≤ 50 lines |

### Snippet Validation

| Check | TypeScript/JS | Python | Markdown |
|-------|---------------|--------|----------|
| Header Format | JSDoc `/** */` | Docstring `""" """` | YAML `---` |
| USE field | Required | Required | Required |
| REQUIRES field | Required | Required | Required |
| PATTERN field | Required | Required | Required |
| CUSTOMIZE markers | Recommended | Recommended | N/A |

---

## Fallback Behavior

### Missing AI Section

If a template lacks an AI Quick Reference section:

1. **Log Warning:** "Template [name] missing AI Quick Reference section"
2. **Generate Section:** Create minimal AI section from existing content
3. **Mark as Auto-Generated:** Add comment `<!-- AI Quick Reference auto-generated -->`
4. **Continue Process:** Don't block on missing section

### Exceeds Line Limit

If AI section exceeds line limit:

1. **Prioritize Content:** Keep most critical rules
2. **Truncate Gracefully:** Remove least essential items
3. **Add Note:** `<!-- See full documentation below -->`
4. **Move Excess:** Place removed content in human documentation

### Template Not Found

If template file is missing:

1. **Use Base Template:** Fall back to generic template
2. **Notify User:** "Template not found, using default structure"
3. **Create Minimal:** Generate minimal AI section
4. **Request Review:** Ask user to review generated content

---

## Example: Complete Styleguide

```markdown
# TypeScript Style Guide

## AI Quick Reference

### Language Rules
- Use `const` by default, `let` when reassignment needed, never `var`
- Named exports only: `export { MyClass }` (no default exports)
- Single quotes for strings, template literals for interpolation
- Always use `===` and `!==` for equality
- End all statements with semicolons explicitly
- ES6 modules only (`import`/`export`), no `namespace`

### Type Patterns
- Prefer interfaces for object shapes over type aliases
- Use `T[]` for simple arrays, `Array<T>` for complex unions
- Optional params (`?`) over `| undefined`
- Use `unknown` over `any` when type is uncertain
- Rely on inference for simple types, be explicit for complex

### Avoid
- `any` type without explicit justification comment
- Type assertions (`as`) and non-null assertions (`!`)
- `#private` fields (use `private` modifier instead)
- `const enum` (use plain `enum`)
- Wrapper objects (`new String()`, `new Boolean()`, `new Number()`)
- `_` prefix/suffix for identifiers

---

## Detailed Guidelines

[Human-readable documentation continues here...]
```

---

## Integration Points

### With Conductor Setup

- Section 2.4 references this protocol for styleguide selection
- All templates include AI-optimized content by default
- Protocol ensures consistent AI section structure

### With Pattern Creation

- `patterns/TEMPLATE.md` follows this protocol
- New patterns must include AI Quick Reference
- Skills can reference patterns with AI sections

### With Snippet Library

- All snippets include AI headers
- `/conductor:snippet show` displays AI header prominently
- Search indexes AI header content

### With Skills

- Skills can activate based on styleguide language
- AI sections provide skill-relevant context
- Cross-references enable skill discovery
