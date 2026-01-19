# Skill Development Guide

This guide covers everything you need to know to create, test, and publish skills for the Conductor plugin ecosystem.

## Overview

Skills are reusable packages of domain-specific guidance that enhance Conductor's implementation capabilities. They provide:

- **AI-optimized guidance** - Condensed best practices optimized for Claude Code
- **Activation rules** - Automatic triggering based on context (keywords, file patterns, tech stack)
- **Patterns and templates** - Reusable code patterns and file templates
- **Extensibility** - No programming required (markdown + JSON only)

## Skill Architecture

Each skill follows a **dual-file architecture**:

```
skills/<skill-id>/
├── SKILL.md           # Required: AI-optimized content
├── manifest.json      # Required: Metadata and activation rules
├── README.md          # Optional: External documentation
└── patterns/          # Optional: Skill-specific patterns
    ├── pattern-1.md
    └── pattern-2.md
```

### File Responsibilities

| File | Purpose | Audience |
|------|---------|----------|
| **SKILL.md** | Core guidance content | Claude Code (AI) |
| **manifest.json** | Metadata, activation rules, capabilities | Skill loader |
| **README.md** | Usage docs, examples, changelog | Human developers |
| **patterns/** | Pattern files following Pattern Template | Both AI and humans |

## Creating a Skill

### Step 1: Plan Your Skill

Before creating files, define:

1. **Scope**: What domain does this skill cover?
2. **Activation triggers**: When should this skill activate?
3. **Content**: What guidance will you provide?
4. **Patterns**: What reusable patterns will you include?

### Step 2: Create Directory Structure

```bash
mkdir -p skills/<skill-id>/patterns
```

Use lowercase with hyphens for the skill ID (e.g., `typescript-best-practices`, `api-design`).

### Step 3: Create manifest.json

The manifest defines metadata and activation rules:

```json
{
  "name": "My Skill Name",
  "version": "1.0.0",
  "description": "Brief description of what the skill provides",
  "author": "Your Name",
  "activation": {
    "keywords": ["keyword1", "keyword2"],
    "file_patterns": ["**/*.ext"],
    "tech_stack": {
      "languages": ["Language"],
      "frameworks": ["Framework"]
    },
    "always_active": false
  },
  "provides": {
    "guidance": ["topic1", "topic2"],
    "patterns": ["pattern-id-1", "pattern-id-2"],
    "templates": [],
    "protocols": []
  },
  "dependencies": []
}
```

**See [Skill Manifest Schema](./skill-manifest-schema.md) for complete field reference.**

### Step 4: Create SKILL.md

The SKILL.md file contains the actual guidance content. Use this format:

```markdown
---
name: Skill Name
description: Use this skill when... (activation hint for AI)
version: 1.0.0
---

# Skill Name

Brief overview of what this skill covers.

## Core Principles

Key principles that guide all recommendations.

## [Topic Section 1]

Detailed guidance organized by topic.

### Subsection

More specific guidance with examples.

## [Topic Section 2]

Additional topic sections as needed.

## Quick Reference

Condensed checklist or summary for rapid application.
```

### Step 5: Create README.md (Optional)

For external documentation:

```markdown
# Skill Name

## Overview

Description for human developers.

## Installation

How to enable the skill.

## Usage

When and how the skill activates.

## Patterns Provided

List of patterns with descriptions.

## Examples

Real-world usage examples.

## Changelog

Version history.
```

### Step 6: Add Patterns (Optional)

Create pattern files in the `patterns/` subdirectory following the [Pattern Template](../patterns/TEMPLATE.md):

```markdown
---
name: Pattern Name
category: Category
tags: [tag1, tag2]
activation:
  keywords: [keyword1, keyword2]
  file_patterns: ["**/*.ext"]
---

# Pattern Name

## AI Quick Reference

Condensed guidance for AI implementation.

---

## Human Documentation

Detailed documentation for human developers.
```

### Step 7: Register the Skill

Add your skill to `skills/skill-registry.json`:

```json
{
  "version": "1.0.0",
  "skills": [
    {
      "name": "My Skill Name",
      "version": "1.0.0",
      "path": "./<skill-id>",
      "description": "Brief description",
      "activation": { ... },
      "provides": { ... }
    }
  ]
}
```

## SKILL.md Format Guidelines

### Content Principles

1. **Concise**: Optimize for token efficiency - AI doesn't need verbose explanations
2. **Actionable**: Every section should guide implementation decisions
3. **Structured**: Use consistent headers for easy parsing
4. **Examples**: Include brief code examples where helpful

### YAML Frontmatter

Required fields:
- `name`: Skill display name
- `description`: Activation hint (when to use this skill)
- `version`: Semantic version

### Content Sections

Recommended structure:

| Section | Purpose |
|---------|---------|
| **Overview** | 1-2 sentences on skill scope |
| **Core Principles** | 3-5 guiding principles |
| **[Topic Sections]** | Organized guidance by topic |
| **Quick Reference** | Condensed checklist |

### Writing Style

- Use imperative voice ("Use X" not "You should use X")
- Prefer bullet points over paragraphs
- Include code examples inline (keep short)
- Reference patterns by name when available
- Avoid redundancy with standard Conductor methodology

### Example SKILL.md

```markdown
---
name: typescript-best-practices
description: Use this skill when working with TypeScript code, type definitions, or async patterns.
version: 1.0.0
---

# typescript-best-practices

Guidance for writing type-safe, maintainable TypeScript code.

## Core Principles

1. **Strict mode always**: Enable `strict: true` in tsconfig.json
2. **Explicit over implicit**: Prefer explicit types over inference for public APIs
3. **Narrow types**: Use discriminated unions over loose types
4. **Null safety**: Handle null/undefined explicitly

## Type Safety

### Prefer Interfaces for Objects

```typescript
// Good
interface User {
  id: string;
  name: string;
}

// Avoid for object shapes
type User = { id: string; name: string };
```

### Use Discriminated Unions

```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };
```

## Async Patterns

### Always Await in Try-Catch

```typescript
try {
  const result = await fetchData();
} catch (error) {
  // Handle error
}
```

## Quick Reference

- [ ] `strict: true` enabled
- [ ] No `any` types without comment justification
- [ ] All async functions have error handling
- [ ] Public APIs have explicit return types
- [ ] Discriminated unions for variant types
```

## Activation Rules

Skills activate based on context matching:

### Keyword Activation

```json
{
  "activation": {
    "keywords": ["typescript", "type", "interface", "generic"]
  }
}
```

Keywords are matched against:
- Task descriptions
- File names
- User prompts

### File Pattern Activation

```json
{
  "activation": {
    "file_patterns": ["**/*.ts", "**/*.tsx"]
  }
}
```

Patterns are matched against files being modified.

### Tech Stack Activation

```json
{
  "activation": {
    "tech_stack": {
      "languages": ["TypeScript"],
      "frameworks": ["React", "Next.js"]
    }
  }
}
```

Matched against project's `tech-stack.md` or detected stack.

### Always Active

```json
{
  "activation": {
    "always_active": true
  }
}
```

Use sparingly for core/essential skills only.

### Activation Scoring

Skills are scored and top matches are activated:

| Match Type | Score |
|------------|-------|
| Keyword match | +1.0 |
| File pattern match | +1.5 |
| Language match | +2.0 |
| Framework match | +1.5 |

Skills scoring >= 1.5 are activated (max 5 per task, excluding always-active).

## Skill Dependencies

Skills can declare dependencies on other skills:

```json
{
  "dependencies": ["conductor-methodology", "testing-strategies"]
}
```

Dependent skills are loaded first to ensure proper context.

## Provides Declaration

Declare what your skill offers:

```json
{
  "provides": {
    "guidance": ["typescript-types", "async-patterns"],
    "patterns": ["type-safety", "error-handling"],
    "templates": ["./templates/component.tsx"],
    "protocols": []
  }
}
```

### Guidance
Topic identifiers for searchability.

### Patterns
Pattern IDs provided by this skill (files in `patterns/`).

### Templates
File templates that can be inserted.

### Protocols
Workflow protocols the skill implements.

## Testing Your Skill

### Validation Checklist

- [ ] manifest.json is valid JSON
- [ ] manifest.json has all required fields
- [ ] SKILL.md has valid YAML frontmatter
- [ ] SKILL.md content follows format guidelines
- [ ] Pattern files follow Pattern Template
- [ ] Skill is registered in skill-registry.json

### Manual Testing

1. **Activation test**: Run `/conductor:skills info <skill-id>` to verify parsing
2. **Context test**: Create a task that should trigger the skill
3. **Content test**: Verify guidance appears in implementation context

### Integration Testing

1. Add skill to registry
2. Start new track with relevant keywords
3. Run `/conductor:implement`
4. Verify skill is announced as activated
5. Check implementation follows skill guidance

## Best Practices

### Do

- Keep SKILL.md under 500 lines for token efficiency
- Use specific, descriptive keywords
- Include concrete code examples
- Reference standard patterns where applicable
- Test activation with real tasks

### Don't

- Duplicate content from Conductor core methodology
- Use overly broad keywords that cause false activation
- Include lengthy explanations (optimize for AI)
- Create skills for one-off use cases
- Forget to update the registry

## Publishing Skills

### Community Contribution

1. Fork the claude-conductor repository
2. Create skill in `skills/` directory
3. Add to skill-registry.json
4. Submit pull request

### Skill Review Criteria

- **Usefulness**: Addresses real development needs
- **Quality**: Well-written, actionable guidance
- **Format**: Follows all format guidelines
- **Testing**: Verified activation and content

## Troubleshooting

### Skill Not Activating

1. Check keywords match task description
2. Verify file patterns are correct glob syntax
3. Ensure skill is in registry
4. Check for typos in skill ID

### Content Not Appearing

1. Verify SKILL.md path is correct
2. Check YAML frontmatter syntax
3. Ensure file encoding is UTF-8

### Parsing Errors

1. Validate JSON with a linter
2. Check for trailing commas
3. Verify string escaping

## Reference

- [Skill Manifest Schema](./skill-manifest-schema.md) - Complete manifest field reference
- [Dual-Format Standard](./dual-format-standard.md) - AI Quick Reference format specification
- [Pattern Template](../patterns/TEMPLATE.md) - Pattern file format
- [conductor-methodology](../skills/conductor-methodology/SKILL.md) - Example always-active skill
