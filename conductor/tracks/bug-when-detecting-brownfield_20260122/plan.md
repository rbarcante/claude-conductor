# Implementation Plan: Bug when detecting Brownfield vs Greenfield project

> **Track ID:** `bug-when-detecting-brownfield_20260122`

## Overview

Fix the `setup detect` command to correctly identify brownfield projects when source code files exist, even without manifest files.

---

## Phase 1: Source Code Detection

- [ ] Task: Write failing tests for source code detection
    - [ ] Test: detect returns brownfield for project with `main.py` only
    - [ ] Test: detect returns brownfield for project with `src/index.js` only
    - [ ] Test: detect returns greenfield for project with only `.md` files
    - [ ] Test: detect infers language from source files when no manifest exists
    - [ ] Run tests and confirm they fail

- [ ] Task: Implement source code file detection
    - [ ] Add `SOURCE_CODE_EXTENSIONS` mapping (extension → language)
    - [ ] Create `_detect_source_files()` helper function
    - [ ] Integrate into `detect()` function to set brownfield status
    - [ ] Run tests and confirm they pass

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Source Code Detection' (Protocol in workflow.md)

---

## Phase 2: Integration and Polish

- [ ] Task: Verify full test suite passes
    - [ ] Run all existing tests to ensure no regressions
    - [ ] Verify coverage meets >80% threshold

- [ ] Task: Test CLI integration manually
    - [ ] Test `python scripts/conductor_cli.py setup detect` on a project with source code only
    - [ ] Verify correct brownfield detection

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Integration and Polish' (Protocol in workflow.md)

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
