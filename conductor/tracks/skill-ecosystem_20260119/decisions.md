# Decisions: Skill Ecosystem

This document records Architecture Decision Records (ADRs) for the Skill Ecosystem track.

## Decisions

### ADR-001: Skill Architecture Pattern

**Date:** 2026-01-21
**Status:** Accepted

#### Context
Designing the skill ecosystem requires choosing an architecture pattern that balances extensibility, simplicity, and consistency with Conductor's markdown-first philosophy. Several approaches were considered: VS Code-style extension manifests, Babel-style configuration plugins, and simpler file-based approaches.

#### Decision
Adopt a **dual-file architecture** where each skill consists of:
1. **SKILL.md** - Human-readable content with AI-optimized guidance in YAML frontmatter + markdown body
2. **manifest.json** - Machine-readable metadata for discovery and activation rules
3. **Optional patterns/** - Skill-specific pattern files
4. **Optional README.md** - External documentation for skill users

Skills are registered in a central **skill-registry.json** that enables programmatic discovery without filesystem scanning.

#### Consequences
**Positive:**
- Consistent with Conductor's markdown-first approach
- Clear separation between content (SKILL.md) and metadata (manifest.json)
- No runtime dependencies or compilation required
- Easy for community contributors to create new skills

**Negative:**
- Requires maintaining two files per skill (SKILL.md + manifest.json)
- Registry must be manually updated when adding skills

#### Alternatives Considered
- **Single-file approach (everything in SKILL.md):** Rejected because YAML frontmatter becomes unwieldy for complex activation rules
- **Pure JSON configuration:** Rejected because it reduces readability and conflicts with markdown-first philosophy
- **Dynamic filesystem scanning:** Rejected for performance reasons and explicit registry provides better control
