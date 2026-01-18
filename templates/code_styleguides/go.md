# Effective Go Style Guide Summary

## AI Quick Reference

### Language Rules
- Always format with `gofmt` (non-negotiable)
- Return `(value, error)` tuple for fallible operations
- Use `defer` for cleanup (file close, mutex unlock)
- Check errors explicitly, never discard with `_`
- Use `for...range` for iteration over slices, maps, channels
- Use `make()` for slices, maps, channels; `new()` for pointers

### Type Patterns
- `MixedCaps` for exported names (public), `mixedCaps` for unexported (private)
- No `Get` prefix for getters: `Owner()` not `GetOwner()`
- Interface names: method + `-er` suffix (`Reader`, `Writer`)
- Package names: short, single-word, lowercase
- Small interfaces preferred (single-method is ideal)

### Avoid
- Discarding errors with blank identifier `_`
- Using `panic` in libraries (reserved for truly unrecoverable)
- Underscores in names (use MixedCaps instead)
- Communicating by sharing memory (share by communicating via channels)
- Complex nested control flow (prefer early returns)

---

This document summarizes key rules and best practices from the official "Effective Go" guide for writing idiomatic Go code.

## 1. Formatting
- **`gofmt`:** All Go code **must** be formatted with `gofmt` (or `go fmt`). This is a non-negotiable, automated standard.
- **Indentation:** Use tabs for indentation (`gofmt` handles this).
- **Line Length:** Go has no strict line length limit. Let `gofmt` handle line wrapping.

## 2. Naming
- **`MixedCaps`:** Use `MixedCaps` or `mixedCaps` for multi-word names. Do not use underscores.
- **Exported vs. Unexported:** Names starting with an uppercase letter are exported (public). Names starting with a lowercase letter are not exported (private).
- **Package Names:** Short, concise, single-word, lowercase names.
- **Getters:** Do not name getters with a `Get` prefix. A getter for a field named `owner` should be named `Owner()`.
- **Interface Names:** One-method interfaces are named by the method name plus an `-er` suffix (e.g., `Reader`, `Writer`).

## 3. Control Structures
- **`if`:** No parentheses around the condition. Braces are mandatory. Can include an initialization statement (e.g., `if err := file.Chmod(0664); err != nil`).
- **`for`:** Go's only looping construct. Unifies `for` and `while`. Use `for...range` to iterate over slices, maps, strings, and channels.
- **`switch`:** More general than in C. Cases do not fall through by default (use `fallthrough` explicitly). Can be used without an expression to function as a cleaner `if-else-if` chain.

## 4. Functions
- **Multiple Returns:** Functions can return multiple values. This is the standard way to return a result and an error (e.g., `value, err`).
- **Named Result Parameters:** Return parameters can be named. This can make code clearer and more concise.
- **`defer`:** Schedules a function call to be run immediately before the function executing `defer` returns. Use it for cleanup tasks like closing files.

## 5. Data
- **`new` vs. `make`:**
  - `new(T)`: Allocates memory for a new item of type `T`, zeroes it, and returns a pointer (`*T`).
  - `make(T, ...)`: Creates and initializes slices, maps, and channels only. Returns an initialized value of type `T` (not a pointer).
- **Slices:** The preferred way to work with sequences. They are more flexible than arrays.
- **Maps:** Use the "comma ok" idiom to check for the existence of a key: `value, ok := myMap[key]`.

## 6. Interfaces
- **Implicit Implementation:** A type implements an interface by implementing its methods. No `implements` keyword is needed.
- **Small Interfaces:** Prefer many small interfaces over one large one. The standard library is full of single-method interfaces (e.g., `io.Reader`).

## 7. Concurrency
- **Share Memory By Communicating:** This is the core philosophy. Do not communicate by sharing memory; instead, share memory by communicating.
- **Goroutines:** Lightweight, concurrently executing functions. Start one with the `go` keyword.
- **Channels:** Typed conduits for communication between goroutines. Use `make` to create them.

## 8. Errors
- **`error` type:** The built-in `error` interface is the standard way to handle errors.
- **Explicit Error Handling:** Do not discard errors with the blank identifier (`_`). Check for errors explicitly.
- **`panic`:** Reserved for truly exceptional, unrecoverable situations. Generally, libraries should not panic.

*Source: [Effective Go](https://go.dev/doc/effective_go)*