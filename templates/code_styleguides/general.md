# General Code Style Principles

## AI Quick Reference

### Core Principles
- Readability over cleverness (code is read more than written)
- Consistency with existing codebase patterns
- Single responsibility per function/class
- Fail fast with clear error messages
- Explicit over implicit behavior

### Code Patterns
- Extract repeated code into named functions (DRY)
- Prefer composition over inheritance
- Use meaningful names that reveal intent
- Keep functions small (<20 lines guideline)
- Return early to reduce nesting

### Avoid
- Magic numbers/strings (use named constants)
- Deep nesting (>3 levels)
- Side effects in functions that appear pure
- Commented-out code (use version control)
- Over-engineering for hypothetical future needs

---

This document outlines general coding principles that apply across all languages and frameworks used in this project.

## Readability
- Code should be easy to read and understand by humans.
- Avoid overly clever or obscure constructs.

## Consistency
- Follow existing patterns in the codebase.
- Maintain consistent formatting, naming, and structure.

## Simplicity
- Prefer simple solutions over complex ones.
- Break down complex problems into smaller, manageable parts.

## Maintainability
- Write code that is easy to modify and extend.
- Minimize dependencies and coupling.

## Documentation
- Document *why* something is done, not just *what*.
- Keep documentation up-to-date with code changes.
