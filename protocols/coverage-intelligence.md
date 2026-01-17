# Coverage Intelligence Protocol

**Version:** 1.0.0
**Purpose:** Analyze code coverage and generate prioritized test suggestions
**Scope:** Conductor implement command, quality gate verification

---

## Overview

This protocol defines the process for parsing coverage reports, identifying untested code paths, and generating prioritized test suggestions. The goal is to move beyond simple coverage percentages to actionable guidance on what to test next and why.

---

## Algorithm Design

### Design Principles

1. **Format Agnostic**: Support common coverage report formats (lcov, Cobertura, Istanbul)
2. **Smart Prioritization**: Rank suggestions by business impact, not just line count
3. **Actionable Output**: Provide specific function/method names and test scenarios
4. **Estimated Impact**: Show expected coverage gain for each suggestion

### Coverage Report Parsing Strategy

**Rationale**: Different ecosystems use different coverage formats. Support the most common.

| Format | File Extension | Ecosystem | Parser |
|--------|---------------|-----------|--------|
| LCOV | `lcov.info`, `coverage.lcov` | JavaScript, C/C++ | Line-based |
| Cobertura XML | `coverage.xml`, `cobertura.xml` | Java, Python | XML |
| Istanbul JSON | `coverage-final.json` | JavaScript/TypeScript | JSON |
| Coverage.py | `.coverage`, `coverage.json` | Python | SQLite/JSON |
| Go Cover | `coverage.out` | Go | Line-based |
| JaCoCo | `jacoco.xml` | Java | XML |

### Prioritization Algorithm

**Rationale**: Not all uncovered code is equally important. Prioritize by impact.

```
Priority Score = (Business Weight × 3) + (Complexity Weight × 2) + (Risk Weight × 1)

Where:
- Business Weight: 1-5 based on code location/type
- Complexity Weight: 1-5 based on cyclomatic complexity
- Risk Weight: 1-5 based on error handling, edge cases
```

**Business Weight Categories**:

| Category | Weight | Examples |
|----------|--------|----------|
| Core Business Logic | 5 | Payment processing, user auth, data validation |
| API Endpoints | 4 | Controllers, route handlers, GraphQL resolvers |
| Data Models | 3 | Entity classes, DTOs, database models |
| Utilities | 2 | Helper functions, formatters, parsers |
| Configuration | 1 | Config loaders, constants, type definitions |

### Coverage Gain Estimation

```
Estimated Gain = (Uncovered Lines in Function) / (Total Project Lines) × 100

Adjusted Gain = Estimated Gain × Testability Factor

Testability Factor:
- Pure function (no side effects): 1.0
- Has dependencies (mockable): 0.8
- Has external I/O: 0.6
- Complex setup required: 0.4
```

---

## Detection Process

### Step 1: Locate Coverage Reports

Search for coverage files in standard locations:

```
Search Order:
1. ./coverage/                  # Common coverage directory
2. ./                           # Project root
3. ./reports/                   # Alternative reports directory
4. ./target/                    # Maven/Gradle output
5. ./build/                     # Build output directory
```

**File Patterns**:
```bash
# LCOV
**/lcov.info
**/coverage.lcov

# Cobertura/JaCoCo XML
**/coverage.xml
**/cobertura.xml
**/jacoco.xml

# Istanbul JSON
**/coverage-final.json
**/coverage-summary.json

# Python
**/.coverage
**/coverage.json

# Go
**/coverage.out
**/cover.out
```

### Step 2: Parse Coverage Data

Extract structured data from coverage reports:

**LCOV Format Parsing**:
```
SF:<source-file>        → Start of file section
DA:<line>,<hits>        → Line data (line number, execution count)
FN:<line>,<name>        → Function start
FNDA:<hits>,<name>      → Function execution count
LF:<count>              → Lines found (total)
LH:<count>              → Lines hit (covered)
end_of_record           → End of file section
```

**Cobertura XML Parsing**:
```xml
<class name="ClassName" filename="path/to/file.py">
  <methods>
    <method name="methodName" hits="0">
      <lines>
        <line number="10" hits="0"/>
        <line number="11" hits="5"/>
      </lines>
    </method>
  </methods>
</class>
```

**Output Structure**:
```json
{
  "summary": {
    "lines": { "total": 1000, "covered": 800, "percentage": 80.0 },
    "functions": { "total": 100, "covered": 75, "percentage": 75.0 },
    "branches": { "total": 200, "covered": 150, "percentage": 75.0 }
  },
  "files": [
    {
      "path": "src/services/payment.py",
      "lines": { "total": 50, "covered": 30, "percentage": 60.0 },
      "uncovered_lines": [15, 16, 17, 25, 26, 40, 41, 42, 43, 44],
      "uncovered_functions": ["process_refund", "validate_card"]
    }
  ]
}
```

### Step 3: Analyze Uncovered Code

For each file with coverage gaps:

**Identify Uncovered Functions**:
```
For each function with hits=0:
  1. Record function name and location
  2. Count total lines in function
  3. Classify function type (business, utility, etc.)
  4. Calculate complexity (if AST available)
```

**Identify Partially Covered Functions**:
```
For each function with 0 < coverage < 100%:
  1. Identify uncovered line ranges
  2. Analyze what those lines do (error handling, edge cases, etc.)
  3. Suggest specific scenarios to test
```

### Step 4: Generate Prioritized Suggestions

**Scoring Each Gap**:

```python
def calculate_priority(gap):
    business_weight = classify_business_importance(gap.file_path, gap.function_name)
    complexity_weight = estimate_complexity(gap.uncovered_lines)
    risk_weight = assess_risk(gap.code_content)

    return (business_weight * 3) + (complexity_weight * 2) + (risk_weight * 1)
```

**Classification Rules**:

| Pattern | Business Weight |
|---------|-----------------|
| `**/services/**`, `**/core/**` | 5 |
| `**/api/**`, `**/controllers/**`, `**/handlers/**` | 4 |
| `**/models/**`, `**/entities/**` | 3 |
| `**/utils/**`, `**/helpers/**` | 2 |
| `**/config/**`, `**/constants/**` | 1 |

| Risk Indicator | Risk Weight |
|----------------|-------------|
| Contains `try/catch/except` | +2 |
| Contains `if/else` branches | +1 |
| Handles user input | +2 |
| Database operations | +2 |
| External API calls | +1 |

---

## Output Format

### Summary Report

```markdown
## Coverage Intelligence Report

### Current Coverage
- **Lines**: 800/1000 (80.0%)
- **Functions**: 75/100 (75.0%)
- **Branches**: 150/200 (75.0%)

### Top Priority Test Suggestions

| Priority | Function | File | Est. Gain | Reason |
|----------|----------|------|-----------|--------|
| 🔴 High | `process_refund()` | services/payment.py | +2.5% | Core business logic, untested |
| 🔴 High | `validate_card()` | services/payment.py | +1.8% | Security-critical validation |
| 🟡 Medium | `handle_timeout()` | api/client.py | +1.2% | Error handling path |
| 🟡 Medium | `parse_response()` | utils/parser.py | +0.8% | Edge case handling |
| 🟢 Low | `format_date()` | utils/formatters.py | +0.3% | Utility function |

### Suggested Test Scenarios

#### 1. `process_refund()` in services/payment.py

**Why**: Core payment logic with 0% coverage. High business impact.

**Suggested Tests**:
- [ ] Test successful refund processing
- [ ] Test refund with invalid payment ID
- [ ] Test refund exceeding original amount
- [ ] Test refund on already-refunded transaction

**Estimated Coverage Gain**: +2.5% (25 lines)

#### 2. `validate_card()` in services/payment.py

**Why**: Security-critical input validation. Currently untested.

**Suggested Tests**:
- [ ] Test valid card number (Luhn algorithm)
- [ ] Test invalid card number format
- [ ] Test expired card
- [ ] Test card from blocked BIN range

**Estimated Coverage Gain**: +1.8% (18 lines)
```

### Machine-Readable Output

```json
{
  "report_version": "1.0",
  "generated_at": "2026-01-20T15:30:00Z",
  "summary": {
    "lines_covered": 800,
    "lines_total": 1000,
    "coverage_percentage": 80.0,
    "target_percentage": 80.0,
    "meets_target": true
  },
  "suggestions": [
    {
      "priority": "high",
      "function": "process_refund",
      "file": "services/payment.py",
      "line_start": 45,
      "line_end": 70,
      "estimated_gain_percentage": 2.5,
      "estimated_gain_lines": 25,
      "reason": "Core business logic with 0% coverage",
      "suggested_tests": [
        "Test successful refund processing",
        "Test refund with invalid payment ID",
        "Test refund exceeding original amount"
      ]
    }
  ]
}
```

---

## Test Suggestion Generation

### Pattern-Based Suggestions

Based on code patterns, generate specific test scenarios:

**For Validation Functions**:
```
Pattern: function name contains "validate", "check", "verify"
Suggestions:
- Valid input returns true/success
- Invalid input returns false/error
- Edge cases (empty, null, boundary values)
- Special characters / injection attempts
```

**For CRUD Operations**:
```
Pattern: function name contains "create", "read", "update", "delete", "get", "set"
Suggestions:
- Happy path operation
- Not found / does not exist
- Duplicate / already exists
- Permission denied
- Invalid input data
```

**For Error Handlers**:
```
Pattern: inside try/catch block, or function name contains "handle", "error"
Suggestions:
- Trigger the specific error condition
- Verify error is logged/reported
- Verify graceful degradation
- Verify user-friendly error message
```

**For API Endpoints**:
```
Pattern: route handler, controller method
Suggestions:
- Success response (200/201)
- Not found (404)
- Bad request (400)
- Unauthorized (401)
- Server error handling (500)
```

### Context-Aware Suggestions

Analyze surrounding code to provide context:

```python
# If uncovered code is inside an if-else branch:
if condition:
    covered_code()
else:
    uncovered_code()  # ← Suggest: "Test case where condition is false"

# If uncovered code is error handling:
try:
    risky_operation()
except SpecificError:
    uncovered_handler()  # ← Suggest: "Test that triggers SpecificError"
```

---

## Integration with Quality Gate

### Trigger Points

Coverage Intelligence runs:
1. After test execution completes
2. When coverage report is detected
3. Before task completion verification

### Coverage Threshold Enforcement

```
If coverage < target:
  1. Display coverage gap
  2. Show top 3 suggestions
  3. Ask: "Add tests now or skip with reason?"

If coverage >= target:
  1. Display success message
  2. Optionally show suggestions for further improvement
```

### Skip Documentation

When coverage target is not met but user proceeds:

```markdown
## Coverage Decision

**Current**: 75.0%
**Target**: 80.0%
**Gap**: 5.0%

**Reason for Proceeding**:
- Time constraint: Will address in follow-up task
- Specific gaps documented for future work

**Deferred Test Suggestions**:
1. process_refund() - Create task TASK-123
2. validate_card() - Create task TASK-124
```

---

## Configuration Options

Customize behavior in `workflow.md`:

```yaml
coverage_intelligence:
  enabled: true

  # Target thresholds
  target_line_coverage: 80
  target_function_coverage: 75
  target_branch_coverage: 70

  # Report locations (search order)
  report_paths:
    - "./coverage"
    - "./reports"
    - "./"

  # Prioritization weights
  weights:
    business_logic: 3
    complexity: 2
    risk: 1

  # Suggestion limits
  max_suggestions: 10
  min_priority_to_show: "medium"  # high, medium, low

  # Business classification overrides
  business_patterns:
    high:
      - "**/payments/**"
      - "**/auth/**"
      - "**/security/**"
    low:
      - "**/test/**"
      - "**/mock/**"
```

---

## Error Handling

### No Coverage Report Found

```
⚠️ Coverage Intelligence: No coverage report found

Searched locations:
- ./coverage/lcov.info
- ./coverage/coverage.xml
- ./coverage-final.json

To generate a coverage report, run your test suite with coverage enabled:
- JavaScript: `npm test -- --coverage`
- Python: `pytest --cov=src --cov-report=xml`
- Go: `go test -coverprofile=coverage.out ./...`

Skipping coverage analysis. Proceeding with task completion.
```

### Invalid Coverage Report

```
⚠️ Coverage Intelligence: Failed to parse coverage report

File: ./coverage/coverage.xml
Error: Invalid XML format at line 45

Please verify your coverage report is valid. Skipping coverage analysis.
```

### Partial Coverage Data

```
ℹ️ Coverage Intelligence: Partial data available

Line coverage: Available
Function coverage: Not available (format limitation)
Branch coverage: Not available

Proceeding with available data.
```

---

## Performance Considerations

### Optimization Strategies

1. **Lazy Parsing**: Only parse files with coverage below threshold
2. **Caching**: Cache parsed coverage data during session
3. **Incremental Analysis**: Only analyze changed files when possible
4. **Sampling**: For large codebases, sample representative functions

### Expected Performance

| Project Size | Coverage Report Size | Parse Time |
|--------------|---------------------|------------|
| Small (<1MB) | <100KB | <100ms |
| Medium (1-10MB) | 100KB-1MB | 100-500ms |
| Large (>10MB) | >1MB | 500ms-2s |

---

## Future Enhancements

1. **AST Analysis**: Deep code analysis for better test suggestions
2. **Historical Trends**: Track coverage changes over time
3. **Test Generation**: Auto-generate test stubs for uncovered functions
4. **IDE Integration**: Show coverage suggestions inline in editor
5. **Mutation Testing**: Identify tests that don't actually verify behavior
