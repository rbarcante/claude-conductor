# Code Review Report

**Branch:** `feature/token-optimization-cli-batch` vs `origin/master`
**Generated:** 2026-02-25
**Track:** Rewrite command protocols for token optimization

---

## Summary

| Metric | Value |
|--------|-------|
| Files Changed | 24 |
| Lines Added | +2905 |
| Lines Removed | -1177 |
| **Findings** | 🔴 High: 4 \| 🟡 Medium: 14 \| 🟢 Low: 16 |

---

## Code Quality

### High Severity

1. **Nested `run()` duplicates `_run_git` helper** — `git_snapshot.py:105`
   - Nested function inside `detect_base_branch` duplicates subprocess logic that already exists as module-level `_run_git`
   - *Recommendation:* Remove nested helper, refactor to use `_run_git` or add a `_run_git_with_code` variant

2. **`detect_base_branch` exceeds 50-line threshold** — `git_snapshot.py:92`
   - 71 lines combining subprocess execution, reflog parsing, remote validation, and fallback logic
   - *Recommendation:* Extract into `_detect_from_reflog`, `_detect_from_remote_tracking`, `_detect_from_common_defaults` helpers

3. **Unhandled `OSError` on plan file write** — `tracks.py:269`
   - `write_text()` in `update_task` has no error handling; disk/permission failures would propagate unhandled
   - *Recommendation:* Wrap in `try/except OSError` and return structured error response

### Medium Severity

1. **Type annotation mismatch** — `codereview.py:101`, `git_snapshot.py:48`
   - `exclude: List[str] = None` should be `Optional[List[str]] = None`

2. **`STOP_WORDS` allocated per-call with duplicate entry** — `implement.py:122`
   - Move to module-level constant, remove duplicate `"into"`

3. **`read_text()` calls lack error handling** — `tracks.py:84`
   - `OSError`/`UnicodeDecodeError` not caught in `parse_plan`, `update_task`, `read_context`

4. **`sys.path.insert` repeated 6 times** — `codereview.py:33`, `git_snapshot.py`, `tracks.py`, all test files
   - Consolidate into shared conftest.py or proper package setup

5. **`batch_match_patterns` is 69 lines** — `implement.py:867`
   - Extract per-task processing into `_match_patterns_for_task` helper

6. **Regex constants compiled per-call** — `tracks.py:162`
   - Move `PHASE_RE`, `TASK_RE`, `STATUS_MAP` to module level

### Low Severity

1. Unnecessary f-string without interpolation — `git_snapshot.py:132`
2. Emoji in warning string may cause encoding issues — `codereview.py:298`
3. Long lines in test data — `test_codereview.py:49-51`
4. Inconsistent CLI Reference comment style — `implement.md:57`
5. Missing docstring on nested `run()` — `git_snapshot.py:105`
6. Dual status form (`in_progress`/`in-progress`) adds surface area — `tracks.py:208`

---

## Security Analysis

### Critical/High Severity

No critical or high security vulnerabilities detected.

### Medium Severity

1. **Path traversal via unvalidated file paths** — `git_snapshot.py:275`, `codereview.py:253`
   - `project_root / filepath` constructed from `git ls-files` output without containment check
   - Symlinks or `../` paths could escape repository boundary
   - *Fix:* Add `full_path.resolve().is_relative_to(project_root.resolve())` guard

2. **Unvalidated `track_id` in path construction** — `tracks.py:167, 263`
   - `track_id` from CLI flows into `tracks_dir / track_id` without sanitization
   - Value like `../../etc/passwd` could enable read/write outside tracks directory
   - *Fix:* Validate `re.fullmatch(r"[a-zA-Z0-9._-]+", track_id)` before use

### Low Severity

1. No subprocess `timeout` parameter set — `git_snapshot.py:101, 176`
2. Unsanitized `track_id` reflected in error messages — `tracks.py:75`

---

## Test Coverage

### Missing Tests

1. **`scripts/conductor_cli.py`** — No test file exists. Argument parser wiring, subcommand routing untested.

### Insufficient Coverage

1. `handle()` dispatch functions not tested in any module (codereview, git_snapshot, tracks)
2. `detect_base_branch()` — only offline fallback tested; reflog/remote detection paths untested
3. `_add_untracked_file_stats()` always patched away in tests, never exercised
4. `_parse_file_stats()` always patched away; binary files, exclude filter, ref fallback untested
5. `_get_uncommitted_summary()` — staged/modified counts not verified
6. `batch_match_patterns()` — never tested with actual matching patterns
7. `parse_plan_content()` — indented subtask handling not tested
8. Duplicate `'master'` in fallback assertion — `test_git_snapshot.py`

---

## Recommendations

**Priority Actions (address before merging):**
1. Add `track_id` validation (regex allowlist) in `tracks.py` to prevent path traversal
2. Add path containment checks in `git_snapshot.py` and `codereview.py` for `git ls-files` paths
3. Add error handling for `write_text`/`read_text` in `tracks.py`

**Suggested Improvements:**
1. Refactor `detect_base_branch` into smaller helpers
2. Move constants (STOP_WORDS, PHASE_RE, TASK_RE) to module level
3. Add `timeout` parameter to subprocess calls
4. Create `test_conductor_cli.py` for argument parser coverage
5. Test `handle()` dispatch functions in each module

---

*Auto-review generated by `/conductor:implement` on track completion*
