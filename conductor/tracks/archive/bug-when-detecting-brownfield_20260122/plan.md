# Implementation Plan: Bug when detecting Brownfield vs Greenfield project

> **Track ID:** `bug-when-detecting-brownfield_20260122`

## Overview

Fix the `setup detect` command to correctly identify brownfield projects when source code files exist, even without manifest files.

---

## Phase 1: Source Code Detection

- [x] Task: Write failing tests for source code detection
    - [x] Test: detect returns brownfield for project with `main.py` only
    - [x] Test: detect returns brownfield for project with `src/index.js` only
    - [x] Test: detect returns greenfield for project with only `.md` files
    - [x] Test: detect infers language from source files when no manifest exists
    - [x] Run tests and confirm they fail

- [x] Task: Implement source code file detection
    - [x] Add `SOURCE_CODE_EXTENSIONS` mapping (extension → language)
    - [x] Create `_detect_source_files()` helper function
    - [x] Integrate into `detect()` function to set brownfield status
    - [x] Run tests and confirm they pass

- [x] Task: Conductor - User Manual Verification 'Phase 1: Source Code Detection' (Protocol in workflow.md)

---

## Phase 2: Integration and Polish

- [x] Task: Verify full test suite passes
    - [x] Run all existing tests to ensure no regressions
    - [x] Verify coverage meets >80% threshold

- [x] Task: Test CLI integration manually
    - [x] Test `python scripts/conductor_cli.py setup detect` on a project with source code only
    - [x] Verify correct brownfield detection

- [x] Task: Conductor - User Manual Verification 'Phase 2: Integration and Polish' (Protocol in workflow.md)

---

## Notes

**Implementation Location:** `scripts/commands/setup.py`

**Source Extensions to Detect:**
- Python: `.py`
- JavaScript: `.js`, `.jsx`, `.mjs`
- TypeScript: `.ts`, `.tsx`
- Java: `.java`
- Go: `.go`
- Rust: `.rs`
- Ruby: `.rb`
- PHP: `.php`
- C#: `.cs`
- Dart: `.dart`
- C/C++: `.c`, `.cpp`, `.h`, `.hpp`

**Scan Depth:** Top-level + `src/` directory only (for performance)
