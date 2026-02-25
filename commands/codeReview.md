---
name: conductor:codeReview
description: Performs comprehensive code review of changes in the current branch
argument-hint: "<base_branch> (e.g., master, develop, main)"
allowed-tools:
  - Read
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

## 3.0 EXECUTION STRATEGY

### 3.1 Prompt User

Ask via AskUserQuestion: "How would you like to run the analysis?"
- "Parallel (Recommended)" — specialist agents simultaneously
- "Sequential" — inline analysis

### 3.2 Parallel Execution (Preferred)

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

### 3.3 Sequential Execution (Fallback)

If user selects Sequential, or as fallback for failed agents, run analysis inline using the checklists below.

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
- **1 agent fails:** Note failure in report, fall back to inline analysis (Section 3.3) for that dimension
- **2+ agents fail:** Switch to full sequential mode, announce: "Switching to sequential analysis."
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

**Parallel:** Parse JSON from each agent, merge `findings` arrays, sum severity counts.
**Sequential:** Gather findings from inline analysis.

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
