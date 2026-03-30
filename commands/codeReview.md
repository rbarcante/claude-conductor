---
name: conductor:codeReview
description: Performs comprehensive code review of changes in the current branch
argument-hint: "<base_branch> (e.g., master, develop, main)"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - Task
---

## Usage

```bash
/conductor:codeReview master    # Review against master
/conductor:codeReview develop   # Review against develop
/conductor:codeReview           # Will prompt for base branch
```

### What This Command Does

1. Generates filtered diff between current branch and base branch
2. Analyzes changes across: **Code Quality**, **Security**, **Test Coverage**
3. Generates report with findings organized by severity

---

## 1.0 SYSTEM DIRECTIVE

You are an AI agent specialized in code review. Analyze code across three dimensions: **Code Quality**, **Security**, and **Test Coverage**.

CRITICAL: Validate every tool call. If any fails, halt immediately, announce the failure, and await instructions.

---

## 1.1 SETUP CHECK

Verify existence of context files for standards-aware review:
- `conductor/product-guidelines.md` — product style and messaging
- `conductor/tech-stack.md` — technology choices
- `conductor/workflow.md` — TDD requirements, coverage thresholds
- `conductor/code_styleguides/` — code style guides

If missing, announce warning and continue with generic standards.

---

## 2.0 BRANCH SELECTION AND DIFF GENERATION

### 2.1 Select Base Branch

1. **Check argument:** Parse `{{args}}` for base branch name.
2. **If no argument:** Prompt via AskUserQuestion with options: master / develop / main.
3. Store selection as `BASE_BRANCH`.

### 2.2 Generate Filtered Diff via CLI

Execute a single call that handles fetch, diff, stats, and language detection:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json codereview filtered-diff --base <BASE_BRANCH>
```

The response includes:
- `data.base_branch` — validated base branch
- `data.stats` — `files_changed`, `lines_added`, `lines_removed`, `truncated`, `max_lines`
- `data.language_breakdown` — per-language file counts and line changes
- `data.file_stats` — per-file breakdown with language detection
- `data.diff_content` — full filtered diff (size-capped)

**Handle errors:**
- If base branch not found: "Branch `origin/<BASE_BRANCH>` not found." — re-prompt.
- If diff is empty: "No changes found. Your branch appears up-to-date." — halt.
- If CLI fails: Fall back to manual `git fetch origin && git diff origin/<BASE_BRANCH>...HEAD`.

Store `data.stats` for the report summary.

---

## 3.0 PARALLEL EXECUTION

### 3.1 Run Analysis

**Prepare agent input** from CLI response:

```json
{
  "diff_content": "<data.diff_content>",
  "file_list": ["<from data.file_stats[].file>"],
  "project_context": {
    "tech_stack": "<from conductor/tech-stack.md>",
    "language_breakdown": "<data.language_breakdown>",
    "styleguide_path": "conductor/code_styleguides/<primary_language>.md",
    "product_guidelines_path": "conductor/product-guidelines.md"
  }
}
```

Use `data.language_breakdown` to determine the primary language (highest `lines_added`) for styleguide selection — no manual file-extension detection needed.

If `conductor/product-guidelines.md` exists, read and include documentation/naming standards in the agent context.

**Launch all three agents simultaneously** in a single message:
- `subagent_type: "code-quality-analyzer"`
- `subagent_type: "security-scanner"`
- `subagent_type: "test-coverage-analyzer"`

Each returns structured JSON: `{ "findings": [...], "summary": { "high": N, "medium": N, "low": N } }`

### 3.2 Inline Fallback (Agent Failure Only)

When one or more agents fail, fall back to inline analysis for the failed dimension using the checklists below.

**Code Quality Checklist:**
- Code smells: functions >50 lines, nesting >3 levels, duplicate code, magic numbers, dead code
- Style: naming conventions, organization, imports, formatting
- Documentation: public API docstrings, complex logic comments
- Maintainability: SRP, abstraction levels, error handling

**Security Checklist:**
- **High:** Hardcoded secrets (API keys, passwords, tokens), injection (SQL, command, XSS, eval/exec), broken auth/access control
- **Medium:** Disabled security features (CSRF, CORS wildcards), weak crypto (MD5/SHA1 for passwords), missing input validation, verbose error messages, sensitive data in logs

**Test Coverage Checklist:**
- Map source files to expected test files, verify existence
- Check if tests were modified alongside source changes
- Evaluate assertion quality and edge case coverage

Record each finding with: severity, file, line, issue, recommendation.

---

## 4.0 ERROR HANDLING

### Agent Failures
- **1 agent fails:** Note failure in report, fall back to inline analysis (Section 3.2) for that dimension
- **2+ agents fail:** Fall back to inline analysis for all dimensions, announce: "Multiple agents failed. Running inline fallback analysis."
- **Invalid output:** Treat as failure, fall back to inline

| Failed Agent | Inline Fallback |
|---|---|
| code-quality-analyzer | Code Quality Checklist |
| security-scanner | Security Checklist |
| test-coverage-analyzer | Test Coverage Checklist |

### Other Errors
- Git errors: provide clear message, suggest common fixes
- File read errors: continue with generic standards, log unavailable files
- Large diffs (>5000 lines): warn user, consider summary-level analysis

---

## 5.0 REPORT GENERATION

### 5.1 Aggregate Findings

Parse JSON from each agent, merge `findings` arrays, sum severity counts. For any dimension that used inline fallback, include those findings in the same structure.

### 5.2 Generate Report

```markdown
# Code Review Report

**Branch:** `<current_branch>` vs `origin/<BASE_BRANCH>`
**Generated:** <timestamp>

---

## Summary

| Metric | Value |
|--------|-------|
| Files Changed | X |
| Lines Added | +Y |
| Lines Removed | -Z |
| **Findings** | 🔴 High: N \| 🟡 Medium: N \| 🟢 Low: N |

---

## Code Quality

### High Severity
[List findings or "No high severity issues found"]

### Medium Severity
[List findings]

### Low Severity
[List findings]

---

## Security Analysis

### Critical/High Severity
[List findings or "No security vulnerabilities detected"]

### Medium Severity
[List findings]

---

## Test Coverage

### Missing Tests
[List files without tests or "All changed files have corresponding tests"]

### Insufficient Coverage
[List coverage gaps]

---

## Recommendations

**Priority Actions (address before merging):**
1. [High severity items]

**Suggested Improvements:**
1. [Medium/Low severity items]

---

*Review generated by `/conductor:codeReview`*
```

### 5.3 Present Report

1. Display complete report to user
2. If high severity issues: "Please address high severity items before merging."
3. If no issues: "Code review passed. No blocking issues found."

---

## 6.0 SAVE REVIEW

### 6.1 Detect Track Context

1. Get current branch: `git branch --show-current`
2. Scan `conductor/tracks/*/metadata.json` files for a track whose branch matches the current git branch (match track shortname against branch name)
3. If a match is found, store `track_id` and `track_path`. Set `TRACK_DETECTED = true`.
4. If no match found, set `TRACK_DETECTED = false`.

### 6.2 Prompt User

Ask via AskUserQuestion:

**If `TRACK_DETECTED = true`:**
- Header: "Save review"
- Question: "Would you like to save this review?"
- Options: "Save to track (Recommended)" / "Save to file" / "Skip"

**If `TRACK_DETECTED = false`:**
- Header: "Save review"
- Question: "Would you like to save this review?"
- Options: "Save to file" / "Skip"

### 6.3 Execute Save

**"Save to track":**
1. Write the generated report to `conductor/tracks/<track_id>/review.md`
2. Read the track's `index.md` and add a link to the review file: `- [Review](./review.md) — Code review report`
3. Write the updated `index.md`
4. Announce: "Review saved to `conductor/tracks/<track_id>/review.md`."

**"Save to file":**
1. Ensure `conductor/reviews/` directory exists (`mkdir -p conductor/reviews/`)
2. Derive filename: `<branch_name>_<YYYY-MM-DD>.md` (replace `/` in branch name with `-`)
3. Write the generated report to `conductor/reviews/<filename>`
4. Announce: "Review saved to `conductor/reviews/<filename>`."

**"Skip":**
1. Announce: "Review not saved."
