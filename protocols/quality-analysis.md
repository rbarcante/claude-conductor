# Quality Analysis Protocol

**Version:** 1.0.0
**Purpose:** Detect anti-patterns and code quality issues in modified files during task completion
**Scope:** Conductor implement command, quality gate verification

---

## Overview

This protocol defines the process for scanning modified files for anti-patterns, reporting findings with actionable guidance, and enforcing quality gates before task completion. The goal is to catch common code quality issues early while allowing documented exceptions.

---

## Algorithm Design

### Design Principles

1. **Incremental Analysis**: Only scan files modified in the current task
2. **Severity-Based Enforcement**: Critical issues block, high/medium warn
3. **Actionable Feedback**: Every finding includes file:line reference and fix suggestion
4. **Documented Exceptions**: Allow skipping with reason that persists in commit history

### File Selection Strategy

**Rationale**: Scanning all files on every task would be slow and noisy. Focus on changes.

```
File Selection Algorithm:
1. Get list of modified files: `git diff --name-only HEAD~1`
2. Filter to code files only (by extension)
3. Exclude generated/vendored directories
4. Return list for scanning
```

**Exclusion Patterns**:
- `node_modules/`, `vendor/`, `venv/`, `.venv/`
- `__pycache__/`, `target/`, `build/`, `dist/`
- `*.min.js`, `*.bundle.js`, `*.generated.*`
- Files matching patterns in `.gitignore`

### Pattern Matching Approach

**Rationale**: Use anti-pattern definitions from `/patterns/anti-patterns/` as source of truth.

```
Pattern Matching Algorithm:
1. For each modified file:
   a. Determine file extension
   b. Load applicable anti-patterns (by file_extensions in YAML)
   c. For each anti-pattern:
      i.  Apply regex patterns from detection.patterns
      ii. Check thresholds from detection.thresholds
      iii. Record matches with line numbers
2. Return consolidated findings
```

### Threshold-Based Detection

Some anti-patterns use metrics rather than regex:

| Anti-Pattern | Metric | How to Measure |
|--------------|--------|----------------|
| God Object | Line count | `wc -l` or file read |
| God Object | Method count | Regex: `(def|function|func|fn)\s+\w+` |
| Spaghetti Code | Cyclomatic complexity | Count decision points |
| Deep Nesting | Nesting depth | Track indentation levels |

### Result Aggregation

**Rationale**: Group findings by severity for clear action priority.

```
Aggregation Algorithm:
1. Collect all findings from all files
2. Group by severity: critical, high, medium
3. Sort within each group by:
   a. File path (alphabetical)
   b. Line number (ascending)
4. Calculate summary statistics:
   - Total findings per severity
   - Files with critical issues
   - Estimated fix time (based on finding count)
```

---

## Detection Process

### Step 1: Identify Modified Files

Execute at the start of quality gate verification:

```bash
# Get files modified in current task (since last commit)
git diff --name-only HEAD~1

# Or for uncommitted changes
git diff --name-only --cached
git diff --name-only
```

Filter results to include only scannable code files:

| Extension | Language | Scannable |
|-----------|----------|-----------|
| `.py` | Python | Yes |
| `.js`, `.jsx` | JavaScript | Yes |
| `.ts`, `.tsx` | TypeScript | Yes |
| `.java` | Java | Yes |
| `.go` | Go | Yes |
| `.cs` | C# | Yes |
| `.rb` | Ruby | Yes |
| `.php` | PHP | Yes |
| `.c`, `.cpp`, `.h` | C/C++ | Yes |
| `.md`, `.json`, `.yaml` | Config/Docs | No |
| `.css`, `.scss` | Styles | No |

### Step 2: Load Applicable Anti-Patterns

For each file, load anti-patterns whose `file_extensions` include the file's extension:

```
Load Anti-Patterns:
1. Read /patterns/anti-patterns/index.md to get list
2. For each anti-pattern:
   a. Read the anti-pattern file
   b. Parse YAML frontmatter
   c. Check if current file extension in file_extensions
   d. If yes, add to applicable patterns
```

### Step 3: Execute Pattern Matching

For each applicable anti-pattern against each file:

**Regex-Based Detection**:
```
For each pattern in anti-pattern.detection.patterns:
  matches = regex.findall(pattern, file_content)
  For each match:
    record(file, line_number, anti-pattern.name, anti-pattern.severity)
```

**Threshold-Based Detection**:
```
For each threshold in anti-pattern.detection.thresholds:
  measured_value = measure(threshold.metric, file_content)
  If measured_value > threshold.value:
    record(file, "file-level", anti-pattern.name, anti-pattern.severity)
```

### Step 4: Generate Report

Format findings for user presentation:

```
## Quality Gate Findings

### Critical Issues (1) - BLOCKING
❌ No critical issues can be skipped. Must fix before proceeding.

| File | Line | Anti-Pattern | Issue |
|------|------|--------------|-------|
| src/app.py | - | God Object | File has 623 lines (max: 500) |

### High Severity (2) - Can skip with documented reason

| File | Line | Anti-Pattern | Issue |
|------|------|--------------|-------|
| src/utils.py | 45 | Mutable Defaults | `def process(items=[])` uses mutable default |
| src/handler.py | 112 | Spaghetti Code | Cyclomatic complexity: 18 (max: 15) |

### Medium Severity (3) - Informational

| File | Line | Anti-Pattern | Issue |
|------|------|--------------|-------|
| src/config.py | 23 | Magic Numbers | Literal `86400` should be named constant |
| src/parser.py | 67 | Deep Nesting | 5 levels of nesting (max: 4) |
| src/parser.py | 89 | Deep Nesting | 5 levels of nesting (max: 4) |
```

---

## Severity Levels

### Critical Severity

**Definition**: Issues that indicate severe bugs or security vulnerabilities.

**Behavior**:
- Blocks task completion
- Cannot be skipped
- Must be fixed before proceeding

**Current Critical Anti-Patterns**: None defined (reserved for future security-related patterns)

### High Severity

**Definition**: Issues that significantly impact maintainability or may cause subtle bugs.

**Behavior**:
- Warns user with prominent display
- Can be skipped with documented reason
- Skip reason recorded in task completion record

**Current High Anti-Patterns**:
- God Object
- Spaghetti Code
- Mutable Defaults

### Medium Severity

**Definition**: Issues that affect code quality but are lower priority.

**Behavior**:
- Displayed as informational
- Automatically skippable (no reason required)
- Can be configured to require reason via workflow settings

**Current Medium Anti-Patterns**:
- Magic Numbers
- Deep Nesting

---

## User Interaction Flow

### Flow: No Issues Found

```
✅ Quality Gate Passed

No anti-patterns detected in modified files.
Proceeding with task completion.
```

### Flow: High/Medium Issues Only

```
⚠️ Quality Gate: Issues Detected

### High Severity (2)
[table of findings]

### Medium Severity (3)
[table of findings]

Options:
1. Fix issues and re-run quality gate
2. Skip with documented reasons
3. View anti-pattern details

Enter choice (1/2/3):
```

If user chooses "2 - Skip":
```
Please provide reasons for skipping:

1. src/utils.py:45 - Mutable Defaults
   Reason: _________________________________

2. src/handler.py:112 - Spaghetti Code
   Reason: _________________________________

[Submit] [Cancel]
```

### Flow: Critical Issues Present

```
🛑 Quality Gate: BLOCKED

Critical issues must be resolved before proceeding.

### Critical Issues (1)
[table of findings]

### High Severity (2)
[table of findings]

Action Required: Fix the critical issue(s) listed above.

View fix guidance for:
- God Object: /patterns/anti-patterns/core/god-object.md

After fixing, the quality gate will re-run automatically.
```

---

## Skip Documentation Format

When issues are skipped, record in the task completion documentation:

```markdown
## Quality Gate Decisions

### Skipped Anti-Patterns

#### High Severity
- **Mutable Defaults** at `src/utils.py:45`
  - Pattern: `def process(items=[])`
  - Reason: Intentional caching mechanism, documented in function docstring
  - Reviewed: 2026-01-20

- **Spaghetti Code** at `src/handler.py:112`
  - Metric: Cyclomatic complexity 18 (threshold: 15)
  - Reason: Protocol state machine, complexity is inherent to specification
  - Reviewed: 2026-01-20

#### Medium Severity (auto-skipped)
- Magic Numbers at `src/config.py:23` (3 occurrences)
- Deep Nesting at `src/parser.py:67,89` (2 occurrences)
```

---

## Configuration Options

Quality analysis behavior can be customized in `workflow.md`:

```yaml
quality_gate:
  enabled: true

  # Severity enforcement
  block_on_critical: true      # Always true, cannot be disabled
  block_on_high: false         # Default: warn only
  require_reason_for_medium: false  # Default: auto-skip

  # Scanning scope
  scan_modified_only: true     # Default: true
  scan_all_files: false        # Override for full scan

  # Exclusions
  exclude_patterns:
    - "**/*.test.js"
    - "**/*.spec.ts"
    - "**/fixtures/**"

  # Threshold overrides (per-project customization)
  thresholds:
    god_object_max_lines: 500
    god_object_max_methods: 20
    spaghetti_max_complexity: 15
    deep_nesting_max_depth: 4
```

---

## Integration Points

### Trigger: Task Completion

Quality analysis runs automatically when:
1. A task is marked as complete in the implementation workflow
2. Before the task completion commit is created
3. After tests pass but before final commit

### Output: Task Documentation

Findings and skip decisions are included in:
1. Console output during implementation
2. Task completion summary (if applicable)

### Feedback Loop

If issues are found and fixed:
1. User fixes the code
2. Quality gate re-runs automatically
3. Reduced findings shown
4. Process repeats until gate passes or remaining issues are skipped

---

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Only parse anti-pattern files when needed for current file types
2. **Caching**: Cache parsed anti-pattern definitions during a session
3. **Parallel Scanning**: Scan multiple files concurrently (if supported)
4. **Early Exit**: Stop on first critical issue (optional aggressive mode)

### Expected Performance

| Project Size | Modified Files | Expected Time |
|--------------|----------------|---------------|
| Small (<100 files) | 1-5 | <1 second |
| Medium (100-1000 files) | 5-20 | 1-3 seconds |
| Large (>1000 files) | 10-50 | 3-10 seconds |

---

## Error Handling

### Anti-Pattern File Errors

```
If anti-pattern file fails to parse:
  1. Log warning: "Failed to load anti-pattern: [name]"
  2. Skip this anti-pattern
  3. Continue with remaining anti-patterns
  4. Include note in report: "Some anti-patterns could not be loaded"
```

### File Access Errors

```
If modified file cannot be read:
  1. Log warning: "Cannot read file: [path]"
  2. Skip this file
  3. Continue with remaining files
  4. Include note in report: "Some files could not be scanned"
```

### Threshold Measurement Errors

```
If metric cannot be measured:
  1. Use conservative default (assume threshold not exceeded)
  2. Log info: "Could not measure [metric] for [file]"
  3. Continue processing
```

---

## Future Enhancements

1. **Language-Specific Patterns**: Load stack-specific anti-patterns based on detected tech stack
2. **Custom Anti-Patterns**: Support project-specific anti-patterns in `conductor/anti-patterns/`
3. **Trend Analysis**: Track anti-pattern counts over time
4. **IDE Integration**: Export findings in standard format (SARIF) for IDE display
5. **Auto-Fix Suggestions**: Generate code patches for simple fixes
