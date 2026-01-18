# Implementation Plan: Java-Specific Documentation

## Phase 1: Java Best Practices Skill Structure [checkpoint: 7f566b5]

- [x] Task: Create skill directory and manifest [2fc558e]
    - [x] Create `skills/java-best-practices/` directory
    - [x] Create `manifest.json` with activation rules (keywords, file_patterns, tech_stack)
    - [x] Create `README.md` with skill overview

- [x] Task: Create SKILL.md core content [2cd5a27]
    - [x] Add YAML frontmatter (name, description, version)
    - [x] Write Core Principles section
    - [x] Write Type Safety section (Optional usage, @Nullable/@NonNull, defensive coding)
    - [x] Write Null Handling section (Optional patterns, orElse/orElseThrow, map/flatMap)

- [x] Task: Create SKILL.md concurrency content [1900bd1]
    - [x] Write CompletableFuture patterns section
    - [x] Write Virtual Threads section (Java 21)
    - [x] Write ExecutorService and thread safety section
    - [x] Write async error handling patterns

- [x] Task: Create SKILL.md modern features content [0da6c6c]
    - [x] Write Records section with examples
    - [x] Write Sealed Classes section with examples
    - [x] Write Pattern Matching section (instanceof, switch expressions)
    - [x] Add Quick Reference checklist

- [x] Task: Conductor - User Manual Verification 'Phase 1: Java Best Practices Skill Structure' (Protocol in workflow.md)

## Phase 2: Java Skill Patterns [checkpoint: 6bfb7c4]

- [x] Task: Create type-safety pattern [482b2c1]
    - [x] Create `skills/java-best-practices/patterns/` directory
    - [x] Create `type-safety.md` with Optional best practices
    - [x] Add annotation-based null safety examples
    - [x] Add defensive coding patterns

- [x] Task: Create concurrency pattern [53319f3]
    - [x] Create `concurrency.md` with CompletableFuture examples
    - [x] Add virtual threads migration patterns
    - [x] Add thread-safe collection patterns

- [x] Task: Create modern-features pattern [e065001]
    - [x] Create `modern-features.md` with record patterns
    - [x] Add sealed class hierarchy examples
    - [x] Add pattern matching examples

- [x] Task: Conductor - User Manual Verification 'Phase 2: Java Skill Patterns' (Protocol in workflow.md)

## Phase 3: Java Snippets [checkpoint: 506b619]

- [x] Task: Create API Client snippet [dcb98eb]
    - [x] Create `snippets/java/` directory
    - [x] Create `api-client.java` with HttpClient implementation
    - [x] Add retry logic with exponential backoff
    - [x] Add structured error handling
    - [x] Add AI header comment block

- [x] Task: Create Error Handler snippet [bb20195]
    - [x] Create `error-handler.java` with custom exception hierarchy
    - [x] Add error codes enum
    - [x] Add context/details support
    - [x] Add AI header comment block

- [x] Task: Create Dependency Injection snippet [3f4e558]
    - [x] Create `dependency-injection.java` with Spring/Jakarta examples
    - [x] Add configuration class patterns
    - [x] Add constructor injection examples
    - [x] Add AI header comment block

- [x] Task: Conductor - User Manual Verification 'Phase 3: Java Snippets' (Protocol in workflow.md)

## Phase 4: Java Code Styleguide

- [~] Task: Create Java styleguide
    - [ ] Create `templates/code_styleguides/java.md`
    - [ ] Add AI Quick Reference section
    - [ ] Add Language Rules section (formatting, imports, exceptions)
    - [ ] Add Naming Conventions section
    - [ ] Add Type System section
    - [ ] Add Comments and Documentation section

- [ ] Task: Conductor - User Manual Verification 'Phase 4: Java Code Styleguide' (Protocol in workflow.md)

## Phase 5: Registry Updates and Final Integration

- [ ] Task: Update skill registry
    - [ ] Read current `skills/skill-registry.json`
    - [ ] Add java-best-practices skill entry
    - [ ] Validate JSON structure

- [ ] Task: Update snippets index
    - [ ] Read current `snippets/index.md`
    - [ ] Add Java section with all 3 snippets
    - [ ] Maintain consistent table format

- [ ] Task: Final validation
    - [ ] Verify all files exist in correct locations
    - [ ] Verify manifest.json schema compliance
    - [ ] Verify skill-registry.json is valid JSON

- [ ] Task: Conductor - User Manual Verification 'Phase 5: Registry Updates and Final Integration' (Protocol in workflow.md)
