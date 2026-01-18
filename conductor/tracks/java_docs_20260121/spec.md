# Specification: Java-Specific Documentation

## Overview

Add comprehensive Java support to the Conductor plugin, matching the existing documentation depth for Python and TypeScript. This includes a Java best practices skill, code snippets, and a style guide.

## Target Versions

- **Java 17 LTS** - Records, sealed classes, pattern matching for instanceof
- **Java 21 LTS** - Virtual threads, pattern matching in switch, sequenced collections

## Target Frameworks

- **Spring Boot** - Dependency injection, configuration, web services
- **Jakarta EE** - CDI, JPA, JAX-RS standards

## Functional Requirements

### 1. Java Best Practices Skill (`skills/java-best-practices/`)

Create a new skill with the following structure:

- **SKILL.md** - Main skill content covering:
  - Type safety & null handling (Optional, @Nullable/@NonNull annotations, defensive coding)
  - Concurrency patterns (CompletableFuture, virtual threads, ExecutorService, thread safety)
  - Modern Java features (records, sealed classes, pattern matching, switch expressions)

- **manifest.json** - Activation rules:
  - Keywords: java, optional, completablefuture, record, sealed, virtual thread
  - File patterns: `**/*.java`, `**/pom.xml`, `**/build.gradle`
  - Tech stack: languages: ["Java"]

- **patterns/** - Subdirectory with detailed patterns:
  - `type-safety.md`
  - `concurrency.md`
  - `modern-features.md`

- **README.md** - Skill documentation

### 2. Java Snippets (`snippets/java/`)

Create production-ready snippets with AI-optimized headers:

| Snippet | Description | Pattern |
|---------|-------------|---------|
| `api-client.java` | Type-safe HTTP client using HttpClient (Java 11+) with retry logic and error handling | Error Handling, Configuration |
| `error-handler.java` | Custom exception hierarchy with error codes and context | Error Handling |
| `dependency-injection.java` | Spring/Jakarta DI patterns with configuration examples | Configuration |

### 3. Java Code Styleguide (`templates/code_styleguides/java.md`)

Create a Google Java Style Guide summary with:
- AI Quick Reference section (formatting, naming, patterns to avoid)
- Detailed sections matching Python/TypeScript styleguide format

### 4. Registry Updates

- **skills/skill-registry.json** - Add java-best-practices skill entry
- **snippets/index.md** - Add Java snippets section

## Non-Functional Requirements

- All code examples must compile with Java 17+
- Snippets must be production-ready with proper error handling
- Documentation must follow existing Conductor formatting conventions
- Skill must integrate with existing activation protocols

## Acceptance Criteria

- [ ] `skills/java-best-practices/SKILL.md` exists with type safety, concurrency, and modern features sections
- [ ] `skills/java-best-practices/manifest.json` has valid activation rules for Java projects
- [ ] `skills/java-best-practices/patterns/` contains at least 3 pattern files
- [ ] `snippets/java/` contains 3 snippets (api-client, error-handler, dependency-injection)
- [ ] `templates/code_styleguides/java.md` exists with AI Quick Reference section
- [ ] `skills/skill-registry.json` includes java-best-practices entry
- [ ] `snippets/index.md` includes Java section with all snippets listed
- [ ] All Java code compiles without errors on Java 17+

## Out of Scope

- Android-specific patterns (separate skill if needed)
- Kotlin interoperability
- Legacy Java (pre-Java 8) support
- Build tool configurations (Maven/Gradle setup guides)
- IDE-specific settings
