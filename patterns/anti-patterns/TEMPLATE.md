---
# Anti-Pattern Metadata (YAML Frontmatter)
name: "Anti-Pattern Name"
severity: "critical|high|medium"  # critical blocks, high warns, medium informs
category: "Code Structure|Data Handling|Control Flow|Naming|Performance"
tags:
  - tag1
  - tag2
detection:
  patterns:
    - "regex-pattern-1"
    - "regex-pattern-2"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
  thresholds:
    max_lines: null
    max_methods: null
    max_nesting: null
version: "1.0"
last_updated: "YYYY-MM-DD"
---

# Anti-Pattern Name

> One-line description of what makes this an anti-pattern.

---

## AI Quick Reference

<!--
  INSTRUCTIONS: This section is optimized for AI detection.
  - Maximum 40 lines
  - Focus on detection rules and quick fixes
  - Include regex patterns for automated scanning
-->

### Detection Triggers
- Condition 1 that identifies this anti-pattern
- Condition 2 that identifies this anti-pattern
- Quantitative threshold (if applicable)

### Quick Detection Checklist
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

### Regex Detection Patterns

```regex
# Pattern 1: Description
pattern-here

# Pattern 2: Description
pattern-here
```

### Immediate Fix Actions
1. **Action**: Brief description of fix
2. **Action**: Brief description of fix
3. **Action**: Brief description of fix

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| Condition A | critical | Block - must fix |
| Condition B | high | Warn - should fix |
| Condition C | medium | Info - consider fixing |

---

## Problem

<!--
  INSTRUCTIONS: Explain why this is problematic.
  - Clear explanation of the issue
  - Impact on code quality, maintenance, performance
  - Real-world consequences
-->

### What It Is

Detailed explanation of this anti-pattern and how it manifests in code.

### Why It's Harmful

1. **Impact 1**: Explanation of negative consequence
2. **Impact 2**: Explanation of negative consequence
3. **Impact 3**: Explanation of negative consequence

### Common Causes

- Cause 1: Why developers introduce this anti-pattern
- Cause 2: Why developers introduce this anti-pattern

---

## Detection

<!--
  INSTRUCTIONS: Detailed detection criteria.
  - Specific patterns to look for
  - Code examples showing the anti-pattern
  - Quantitative thresholds
-->

### Signs to Look For

1. **Sign 1**: Description
2. **Sign 2**: Description
3. **Sign 3**: Description

### Code Examples (Bad)

#### Example 1: Basic Case

```language
// This is the anti-pattern
code_example_here
```

**Why this is problematic:** Explanation of what's wrong.

#### Example 2: Severe Case

```language
// More severe version of the anti-pattern
code_example_here
```

**Why this is problematic:** Explanation of what's wrong.

### Metrics Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Metric 1 | > X | > Y |
| Metric 2 | > X | > Y |

---

## Solution

<!--
  INSTRUCTIONS: How to fix this anti-pattern.
  - Step-by-step refactoring guidance
  - Before/after code examples
  - Techniques to apply
-->

### Refactoring Steps

1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

### Code Examples (Good)

#### Fixed Example 1

```language
// Correct approach
code_example_here
```

**Why this is better:** Explanation of improvements.

#### Fixed Example 2

```language
// Alternative correct approach
code_example_here
```

**Why this is better:** Explanation of improvements.

### Prevention Strategies

- Strategy 1: How to avoid introducing this in the future
- Strategy 2: How to avoid introducing this in the future

---

## Exceptions

<!--
  INSTRUCTIONS: When this anti-pattern is acceptable.
  - Legitimate use cases
  - Trade-off scenarios
  - How to document exceptions
-->

### When It's Acceptable

1. **Exception Case 1**: Description of when this is okay
2. **Exception Case 2**: Description of when this is okay

### How to Document Exceptions

When this anti-pattern is intentional, document it with:

```language
// EXCEPTION: [anti-pattern-name]
// Reason: Explanation of why this is acceptable here
// Reviewed: YYYY-MM-DD
code_here
```

---

## Related Anti-Patterns

- [Related Anti-Pattern 1](./related.md) - How they relate
- [Related Anti-Pattern 2](./related.md) - How they relate

---

## References

- [External Resource 1](https://example.com) - Description
- [External Resource 2](https://example.com) - Description
