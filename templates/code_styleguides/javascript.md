# Google JavaScript Style Guide Summary

## AI Quick Reference

### Language Rules
- Use `const` by default, `let` when reassignment needed, never `var`
- Named exports only: `export { MyClass }` (no default exports)
- Single quotes for strings, template literals for multiline/interpolation
- Always use `===` and `!==` for equality
- End all statements with semicolons explicitly
- Braces required for all control structures (even single-line)
- +2 spaces indentation, max 80 characters per line

### Type Patterns
- `UpperCamelCase` for classes
- `lowerCamelCase` for methods, functions, variables
- `CONSTANT_CASE` for constants
- Use JSDoc for type annotations: `/** @param {string} name */`
- Prefer arrow functions for nested functions (preserves `this`)

### Avoid
- `var` declarations
- Default exports
- `eval()` and `Function(...string)`
- Modifying builtin prototypes (`Array.prototype.foo = ...`)
- Relying on Automatic Semicolon Insertion
- `with` keyword

---

This document summarizes key rules and best practices from the Google JavaScript Style Guide.

## 1. Source File Basics
- **File Naming:** All lowercase, with underscores (`_`) or dashes (`-`). Extension must be `.js`.
- **File Encoding:** UTF-8.
- **Whitespace:** Use only ASCII horizontal spaces (0x20). Tabs are forbidden for indentation.

## 2. Source File Structure
- New files should be ES modules (`import`/`export`).
- **Exports:** Use named exports (`export {MyClass};`). **Do not use default exports.**
- **Imports:** Do not use line-wrapped imports. The `.js` extension in import paths is mandatory.

## 3. Formatting
- **Braces:** Required for all control structures (`if`, `for`, `while`, etc.), even single-line blocks. Use K&R style ("Egyptian brackets").
- **Indentation:** +2 spaces for each new block.
- **Semicolons:** Every statement must be terminated with a semicolon.
- **Column Limit:** 80 characters.
- **Line-wrapping:** Indent continuation lines at least +4 spaces.
- **Whitespace:** Use single blank lines between methods. No trailing whitespace.

## 4. Language Features
- **Variable Declarations:** Use `const` by default, `let` if reassignment is needed. **`var` is forbidden.**
- **Array Literals:** Use trailing commas. Do not use the `Array` constructor.
- **Object Literals:** Use trailing commas and shorthand properties. Do not use the `Object` constructor.
- **Classes:** Do not use JavaScript getter/setter properties (`get name()`). Provide ordinary methods instead.
- **Functions:** Prefer arrow functions for nested functions to preserve `this` context.
- **String Literals:** Use single quotes (`'`). Use template literals (`` ` ``) for multi-line strings or complex interpolation.
- **Control Structures:** Prefer `for-of` loops. `for-in` loops should only be used on dict-style objects.
- **`this`:** Only use `this` in class constructors, methods, or in arrow functions defined within them.
- **Equality Checks:** Always use identity operators (`===` / `!==`).

## 5. Disallowed Features
- `with` keyword.
- `eval()` or `Function(...string)`.
- Automatic Semicolon Insertion.
- Modifying builtin objects (`Array.prototype.foo = ...`).

## 6. Naming
- **Classes:** `UpperCamelCase`.
- **Methods & Functions:** `lowerCamelCase`.
- **Constants:** `CONSTANT_CASE` (all uppercase with underscores).
- **Non-constant Fields & Variables:** `lowerCamelCase`.

## 7. JSDoc
- JSDoc is used on all classes, fields, and methods.
- Use `@param`, `@return`, `@override`, `@deprecated`.
- Type annotations are enclosed in braces (e.g., `/** @param {string} userName */`).

*Source: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)*