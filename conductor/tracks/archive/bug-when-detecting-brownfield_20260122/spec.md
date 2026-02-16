# Specification: Bug when detecting Brownfield vs Greenfield project

> **Type:** bugfix
> **Track ID:** `bug-when-detecting-brownfield_20260122`

## Overview

The `setup detect` command incorrectly classifies projects as "greenfield" when they contain source code files but no manifest files (package.json, requirements.txt, etc.).

## Problem Analysis

**Root Cause:** `scripts/commands/setup.py` line 162-183 only checks for manifest files in `PROJECT_INDICATORS` dictionary to determine brownfield status. Source code files are not considered.

**Current Behavior:**
- Project with `package.json` → Brownfield ✓
- Project with `main.py` but no `requirements.txt` → Greenfield ✗ (incorrect)
- Project with `src/App.js` but no `package.json` → Greenfield ✗ (incorrect)

**Expected Behavior:**
- Project with manifest files → Brownfield
- Project with source code files (*.py, *.js, *.ts, *.java, *.go, etc.) → Brownfield
- Empty project or only config/docs → Greenfield

## Functional Requirements

1. **FR-1**: Add source code file detection to `detect()` function
   - Check for common source code extensions: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.rb`, `.php`, `.cs`, `.dart`
   - Use shallow directory scan (top-level + one level deep) for performance

2. **FR-2**: Set `project_type = 'brownfield'` if source code files exist, even without manifest files

3. **FR-3**: Infer language from source code files when no manifest file provides this information

## Acceptance Criteria

- [ ] `detect` returns `brownfield` for project with `main.py` but no `requirements.txt`
- [ ] `detect` returns `brownfield` for project with `src/index.js` but no `package.json`
- [ ] `detect` returns `greenfield` for empty project
- [ ] `detect` returns `greenfield` for project with only `.md` files
- [ ] Language is inferred from source files when no manifest exists
- [ ] Existing tests continue to pass

## Out of Scope

- Deep recursive scanning of entire directory tree (performance concern)
- Binary file detection
- Changing existing manifest-based detection logic

## References

- Bug location: `scripts/commands/setup.py` lines 136-216
- Existing test: `scripts/tests/test_commands.py::TestSetupCommand::test_detect`
