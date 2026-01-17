# Decision Capture Protocol

**Version:** 1.0.0
**Purpose:** Capture significant implementation decisions in Architecture Decision Record (ADR) format
**Scope:** Conductor implementation command, task execution workflow

---

## Overview

This protocol defines when and how to capture implementation decisions during task execution. The goal is to document the "why" alongside the "what" without disrupting development flow for trivial choices.

---

## Decision Identification Rules

### What Constitutes a "Significant Decision"

A decision is significant when it:

1. **Has Long-Term Implications** - The choice affects code architecture, maintainability, or future development
2. **Involves Tradeoffs** - Multiple valid approaches exist with different pros/cons
3. **Deviates from Convention** - The choice differs from standard patterns or project conventions
4. **Impacts External Contracts** - Changes to APIs, data formats, or integration points
5. **Introduces Dependencies** - Adding new libraries, tools, or external services

### Decision Trigger Checklist

The following scenarios SHOULD trigger a decision prompt:

| Trigger Category | Examples | Priority |
|-----------------|----------|----------|
| **Technology Selection** | Choosing a library, framework, or tool | High |
| **Pattern Choice** | Selecting design patterns (singleton vs factory, etc.) | High |
| **API Design** | Endpoint structure, response formats, versioning | High |
| **Data Modeling** | Schema design, relationships, normalization level | High |
| **Architecture** | Component boundaries, service decomposition | High |
| **Error Handling Strategy** | Exception types, retry policies, fallback behavior | Medium |
| **Performance Tradeoffs** | Caching strategy, lazy vs eager loading | Medium |
| **Security Approach** | Authentication method, authorization model | High |
| **Testing Strategy** | Unit vs integration, mocking approach | Medium |
| **Configuration** | Environment handling, feature flags | Low |

### When to Prompt vs. When to Skip

**PROMPT when:**
- The choice is not obvious from the specification
- Multiple reasonable alternatives exist
- The decision affects code outside the current task
- The choice contradicts or extends existing patterns
- Future maintainers would benefit from understanding the rationale

**SKIP when:**
- The approach is dictated by the spec or tech stack
- Only one reasonable option exists
- The choice is easily reversible with no downstream impact
- The decision follows an established project pattern
- The scope is purely cosmetic (naming, formatting)

---

## Decision Capture Flow

### Step 1: Detect Decision Point

During implementation, identify when a decision point is reached using the trigger checklist above.

### Step 2: Present Decision Context

Format the decision prompt as follows:

```
---
**Decision Point Detected**

**Context:** [Brief description of what triggered this decision]

**Options:**
A. [First option] - [Brief description]
   - Pros: [List pros]
   - Cons: [List cons]

B. [Second option] - [Brief description]
   - Pros: [List pros]
   - Cons: [List cons]

C. [Third option if applicable] - [Brief description]
   - Pros: [List pros]
   - Cons: [List cons]

**Recommendation:** [Option letter] - [Why this is recommended]

---
Select an option (A/B/C) or type 'skip' to proceed without recording:
```

### Step 3: Capture User Choice

After user selects an option:
1. Confirm the selection
2. Ask for any additional rationale the user wants to record (optional)
3. Proceed to record the decision

### Step 4: Record Decision to decisions.md

Generate an ADR entry and append to the track's `decisions.md`:

```markdown
### ADR-[NNN]: [Decision Title]

**Date:** [Current date YYYY-MM-DD]
**Status:** Accepted

#### Context
[The situation that led to this decision point, including any constraints or requirements]

#### Decision
[The choice that was made, stated as a declarative sentence]

#### Consequences
**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Tradeoff 1]
- [Tradeoff 2]

#### Alternatives Considered
- **[Option A]:** [Why not chosen]
- **[Option B]:** [Why not chosen]
```

### Step 5: Update ADR Counter

Track the ADR number by:
1. Reading the current decisions.md
2. Finding the highest ADR number
3. Incrementing for the new entry

If no ADRs exist, start with ADR-001.

---

## Decision Prompt Format

### Standard Decision Prompt Template

```
**Decision Required: [Category]**

[Context paragraph explaining the situation]

**Options:**

**A. [Option Name]** (Recommended)
   [Description of this approach]
   - Pros: [Key advantages]
   - Cons: [Key disadvantages]

**B. [Option Name]**
   [Description of this approach]
   - Pros: [Key advantages]
   - Cons: [Key disadvantages]

**C. [Option Name]**
   [Description of this approach]
   - Pros: [Key advantages]
   - Cons: [Key disadvantages]

Which approach should we take? (A/B/C/skip)
```

### Minimal Decision Prompt (for lower priority decisions)

```
**Quick Decision: [Topic]**

Context: [One sentence context]

A. [Option A] - [One line description]
B. [Option B] - [One line description]

Recommendation: [A/B] because [brief reason]

Proceed with recommendation? (yes/no/other)
```

---

## Integration Points

### With implement.md

The Decision Capture Protocol is invoked during task implementation:
1. After understanding the task requirements
2. Before making non-trivial implementation choices
3. During the "Green Phase" when implementation approach is being determined

### With Git Commits

Decisions are referenced in commit context:
- Task commits can reference related ADR entries
- ADR IDs provide traceability from code to rationale

### With decisions.md

All captured decisions are appended to the track's `decisions.md` file in chronological order.

---

## Examples

### Example 1: Technology Selection

```
**Decision Required: Library Selection**

We need to implement HTTP client functionality for API calls.

**Options:**

**A. axios** (Recommended)
   Popular HTTP client with interceptors and automatic transforms
   - Pros: Wide adoption, good TypeScript support, interceptors
   - Cons: Additional dependency, larger bundle size

**B. Native fetch**
   Built-in browser/Node.js API
   - Pros: No dependencies, native support
   - Cons: More boilerplate, no interceptors, manual error handling

**C. got**
   Node.js focused HTTP library
   - Pros: Powerful retry logic, streams support
   - Cons: Node-only, different API patterns

Which approach should we take? (A/B/C/skip)
```

### Example 2: Pattern Choice

```
**Decision Required: State Management Pattern**

The feature requires sharing state between multiple components.

**Options:**

**A. Context API** (Recommended)
   React's built-in context for state sharing
   - Pros: No additional deps, simple for moderate complexity
   - Cons: Re-render concerns, less powerful than Redux

**B. Redux Toolkit**
   Centralized state management
   - Pros: Predictable, powerful devtools, middleware
   - Cons: Boilerplate, learning curve, overkill for simple cases

Which approach should we take? (A/B/skip)
```

---

## Error Handling

### If User Skips Decision

- Log that the decision was skipped (do not record in decisions.md)
- Proceed with implementation using recommended option
- No ADR entry is created

### If User Provides Custom Option

- Capture the custom approach
- Record it as the selected option in the ADR
- Mark alternatives as the originally presented options

---

## Metrics and Quality

### Decision Documentation Quality Checklist

- [ ] Context explains the situation clearly
- [ ] Decision is stated declaratively
- [ ] Consequences include both positive and negative
- [ ] Alternatives are documented with reasons for rejection
- [ ] ADR number is sequential and unique
