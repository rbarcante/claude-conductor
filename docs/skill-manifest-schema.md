# Skill Manifest Schema

This document defines the schema for skill manifests in the Conductor plugin ecosystem. Each skill must include a `manifest.json` file conforming to this schema.

## Overview

The skill manifest system enables:
- **Discovery**: Skills can be found and loaded by the registry
- **Context-aware activation**: Skills activate based on project context
- **Capability declaration**: Skills declare what they provide to the system

## Schema Reference

### Root Structure

```json
{
  "name": "<string>",
  "version": "<semver>",
  "path": "<relative-path>",
  "description": "<string>",
  "activation": { ... },
  "provides": { ... }
}
```

---

## Required Fields

### `name`
- **Type**: `string`
- **Required**: Yes
- **Description**: Human-readable skill name
- **Example**: `"Conductor Methodology"`

### `version`
- **Type**: `string` (Semantic Version)
- **Required**: Yes
- **Format**: `MAJOR.MINOR.PATCH` (e.g., `"1.0.0"`, `"2.3.1"`)
- **Description**: Skill version following [Semantic Versioning 2.0.0](https://semver.org/)
- **Example**: `"1.0.0"`

### `path`
- **Type**: `string`
- **Required**: Yes (in registry only)
- **Description**: Relative path from the skills directory to the skill folder
- **Example**: `"./conductor-methodology"`
- **Note**: In individual `manifest.json` files, this field is optional as the path is implicit

### `description`
- **Type**: `string`
- **Required**: Yes
- **Description**: Brief description of what the skill provides
- **Best Practice**: Keep under 200 characters
- **Example**: `"Core Conductor development methodology and context-driven principles"`

---

## Activation Rules Schema

The `activation` object defines when a skill should be activated.

```json
{
  "activation": {
    "keywords": ["list", "of", "trigger", "keywords"],
    "file_patterns": ["**/*.ts", "**/*.tsx"],
    "tech_stack": {
      "languages": ["TypeScript"],
      "frameworks": ["React"]
    },
    "always_active": false
  }
}
```

### Activation Fields

#### `keywords`
- **Type**: `array<string>`
- **Required**: No
- **Description**: Keywords that trigger skill activation when found in task descriptions
- **Matching**: Case-insensitive, supports partial matches
- **Example**: `["authentication", "auth", "login", "session"]`

#### `file_patterns`
- **Type**: `array<string>`
- **Required**: No
- **Description**: Glob patterns for files that trigger activation when modified
- **Format**: Standard glob syntax
- **Examples**:
  - `"**/*.ts"` - All TypeScript files
  - `"src/components/**/*.tsx"` - React components in src
  - `"**/test/**"` - All test directories

#### `tech_stack`
- **Type**: `object`
- **Required**: No
- **Description**: Technology requirements for activation

##### `tech_stack.languages`
- **Type**: `array<string>`
- **Description**: Programming languages that trigger activation
- **Matching**: Matched against project's `tech-stack.md` or detected languages
- **Examples**: `["TypeScript", "Python", "Go"]`

##### `tech_stack.frameworks`
- **Type**: `array<string>`
- **Description**: Frameworks that trigger activation
- **Examples**: `["React", "Next.js", "FastAPI"]`

#### `always_active`
- **Type**: `boolean`
- **Required**: No
- **Default**: `false`
- **Description**: When `true`, skill is always loaded regardless of other conditions
- **Use Case**: Core methodology skills, essential utilities

### Activation Logic

Skills are activated when ANY of the following conditions are met:

1. **Keyword Match**: Task description contains any keyword (score >= 1.0)
2. **File Pattern Match**: Modified files match any file pattern (score >= 1.5)
3. **Tech Stack Match**: Project tech stack matches declared requirements
4. **Always Active**: `always_active` is `true`

**Priority Order** (highest to lowest):
1. `always_active: true`
2. File pattern matches
3. Tech stack matches
4. Keyword matches

---

## Provides Schema

The `provides` object declares what capabilities the skill offers.

```json
{
  "provides": {
    "patterns": ["error-handling", "logging"],
    "templates": ["./templates/component.tsx.template"],
    "protocols": ["tdd-workflow", "code-review"],
    "guidance": ["conductor-concepts", "track-lifecycle"]
  }
}
```

### Provides Fields

#### `patterns`
- **Type**: `array<string>`
- **Required**: No
- **Description**: List of pattern IDs the skill provides
- **Reference**: Patterns defined in `patterns/core/` or `patterns/stack/`
- **Example**: `["error-handling", "logging", "validation"]`

#### `templates`
- **Type**: `array<string>`
- **Required**: No
- **Description**: Relative paths to template files
- **Example**: `["./templates/component.tsx", "./templates/test.spec.ts"]`

#### `protocols`
- **Type**: `array<string>`
- **Required**: No
- **Description**: Protocol IDs that the skill implements or extends
- **Example**: `["tdd-workflow", "git-commit-strategy"]`

#### `guidance`
- **Type**: `array<string>`
- **Required**: No
- **Description**: Topics for which the skill provides guidance
- **Example**: `["conductor-concepts", "context-driven-development", "track-lifecycle"]`

---

## Complete Example

### Individual Skill Manifest (`manifest.json`)

```json
{
  "name": "React Development",
  "version": "1.0.0",
  "description": "Best practices and patterns for React development",
  "activation": {
    "keywords": ["component", "hook", "state", "props", "react"],
    "file_patterns": ["**/*.tsx", "**/*.jsx"],
    "tech_stack": {
      "languages": ["TypeScript", "JavaScript"],
      "frameworks": ["React", "Next.js"]
    }
  },
  "provides": {
    "patterns": ["component-structure", "hook-patterns", "state-management"],
    "templates": ["./templates/component.tsx", "./templates/hook.ts"],
    "guidance": ["react-best-practices", "testing-components"]
  }
}
```

### Registry Entry (`skill-registry.json`)

```json
{
  "name": "React Development",
  "version": "1.0.0",
  "path": "./react-development",
  "description": "Best practices and patterns for React development",
  "activation": {
    "keywords": ["component", "hook", "state", "props", "react"],
    "file_patterns": ["**/*.tsx", "**/*.jsx"],
    "tech_stack": {
      "languages": ["TypeScript", "JavaScript"],
      "frameworks": ["React", "Next.js"]
    }
  },
  "provides": {
    "patterns": ["component-structure", "hook-patterns", "state-management"],
    "templates": ["./templates/component.tsx", "./templates/hook.ts"],
    "guidance": ["react-best-practices", "testing-components"]
  }
}
```

---

## Validation Rules

1. **Name**: Must be non-empty string
2. **Version**: Must be valid semver (X.Y.Z format)
3. **Path**: Must be valid relative path (registry only)
4. **Description**: Must be non-empty string
5. **Keywords**: Each keyword must be lowercase, alphanumeric with hyphens
6. **File Patterns**: Must be valid glob patterns
7. **Provides arrays**: Each item must be a valid identifier string

---

## Migration Notes

### From SKILL.md to manifest.json

Existing skills with `SKILL.md` files should add a companion `manifest.json`:

1. Extract metadata from YAML frontmatter
2. Determine activation rules based on skill description
3. Identify what the skill provides
4. Create `manifest.json` alongside `SKILL.md`

The `SKILL.md` file remains the human-readable skill documentation, while `manifest.json` enables programmatic discovery and activation.
