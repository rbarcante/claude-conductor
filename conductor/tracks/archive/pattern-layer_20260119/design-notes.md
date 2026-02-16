# Design Notes: Pattern Resolution Algorithm

## Overview

The Pattern Resolution Protocol defines how patterns are matched to tasks during implementation. This algorithm extracts keywords from task descriptions, matches them against pattern activation keywords and file patterns, and scores relevance to determine which patterns to surface.

---

## 1. Keyword Extraction Logic

### Input
- Task description text (e.g., "Implement error handling for the API endpoints")
- List of files being modified (optional)

### Process

1. **Tokenize**: Split task description into individual words
2. **Normalize**: Convert to lowercase, remove punctuation
3. **Filter Stop Words**: Remove common words that don't carry meaning
   - Articles: a, an, the
   - Prepositions: in, on, at, to, for, of, with, by
   - Conjunctions: and, or, but
   - Pronouns: it, this, that
   - Common verbs: is, are, be, have, has, do, does
4. **Extract Stems** (optional): Reduce words to root form
   - "handling" → "handle"
   - "logging" → "log"
   - "validates" → "validate"

### Output
- Set of normalized keywords from task description
- Set of file paths being modified

### Example
```
Input: "Add error handling and logging for user authentication"
Tokens: ["add", "error", "handling", "and", "logging", "for", "user", "authentication"]
After filtering: ["error", "handling", "logging", "user", "authentication"]
After stemming: ["error", "handle", "log", "user", "authentication"]
```

---

## 2. Pattern Matching Rules

### 2.1 Keyword Matching

Patterns define activation keywords in their YAML frontmatter:
```yaml
activation:
  keywords:
    - error
    - exception
    - catch
    - throw
```

**Matching Types:**

| Match Type | Description | Score Weight |
|------------|-------------|--------------|
| **Exact** | Extracted keyword equals activation keyword exactly | 1.0 |
| **Stem** | Extracted keyword's stem matches activation keyword | 0.8 |
| **Partial** | Extracted keyword contains or is contained by activation keyword | 0.5 |

### 2.2 File Pattern Matching

Patterns define file patterns in their YAML frontmatter:
```yaml
activation:
  file_patterns:
    - "**/error*.{js,ts,py,go,rs,java,kt}"
    - "**/*Exception.java"
```

**Matching:**
- If ANY file being modified matches ANY file pattern → add bonus score
- File pattern match score: 1.5 (high weight to encourage surfacing when relevant files are touched)

---

## 3. Relevance Scoring Algorithm

### Score Calculation

```
totalScore = keywordScore + filePatternBonus

keywordScore = sum(matchWeight for each keyword match)
filePatternBonus = 1.5 if any file matches pattern, else 0

where matchWeight:
  - Exact match: 1.0
  - Stem match: 0.8
  - Partial match: 0.5
```

### Surfacing Threshold

| Score Range | Action |
|-------------|--------|
| score >= 2.0 | **Strong match** - Surface pattern with high confidence |
| 1.0 <= score < 2.0 | **Moderate match** - Surface pattern with note about relevance |
| 0.5 <= score < 1.0 | **Weak match** - Mention pattern exists, don't auto-surface |
| score < 0.5 | **No match** - Don't mention pattern |

### Ranking

When multiple patterns match:
1. Sort by score (descending)
2. Surface top 3 patterns maximum (to avoid overwhelming)
3. If scores are equal, prefer patterns with more keyword matches over file pattern matches

---

## 4. Resolution Process (Step-by-Step)

```
FUNCTION resolvePatterns(taskDescription, filesBeingModified):
    1. Load pattern registry from patterns/index.md
    2. Extract keywords from taskDescription
    3. For each pattern in registry:
        a. Read pattern file to get activation.keywords and activation.file_patterns
        b. Calculate keywordScore by matching extracted keywords
        c. Calculate filePatternBonus by checking filesBeingModified
        d. totalScore = keywordScore + filePatternBonus
        e. Store (pattern, totalScore) if totalScore >= 0.5
    4. Sort results by totalScore descending
    5. Return top 3 patterns with score >= 1.0

    FALLBACK: If no patterns have score >= 1.0, return empty list
```

---

## 5. Fallback Behavior

When no patterns match (empty result):
- Do NOT announce "no patterns found" (creates noise)
- Continue with task execution silently
- User can manually search with `/conductor:patterns search <keyword>`

When weak matches exist (0.5 <= score < 1.0):
- Optionally mention: "Tip: Related patterns may exist. Use `/conductor:patterns search <keyword>` to explore."
- This is informational only, not blocking

---

## 6. Edge Cases

| Scenario | Behavior |
|----------|----------|
| Empty task description | Skip pattern resolution, continue with task |
| Task with only stop words | Skip pattern resolution, continue with task |
| Very long task description | Limit keyword extraction to first 200 words |
| Pattern file missing/corrupt | Log warning, skip that pattern, continue with others |
| Pattern missing activation section | Skip that pattern (not activatable) |

---

## 7. Performance Considerations

- Pattern frontmatter should be cached per session
- Keyword extraction is O(n) where n = words in task
- Pattern matching is O(p * k) where p = patterns, k = keywords
- With 5-20 patterns and <50 keywords, this is negligible

---

## Example Scenarios

### Scenario 1: Strong Match
```
Task: "Add validation for user registration form inputs"
Extracted keywords: ["validation", "user", "registration", "form", "input"]
Files: ["src/validators/userValidator.ts"]

Pattern: validation.md
  - Keyword matches: "validation" (exact, 1.0), "input" (exact, 1.0)
  - File pattern: "**/valid*.{js,ts,...}" matches "userValidator.ts" (+1.5)
  - Total: 3.5 → STRONG MATCH, surface pattern
```

### Scenario 2: Moderate Match
```
Task: "Fix the bug in the checkout process"
Extracted keywords: ["fix", "bug", "checkout", "process"]
Files: ["src/checkout/payment.ts"]

Pattern: error-handling.md
  - Keyword matches: "bug" → partial match to "debug" (0.5)
  - File pattern: no match
  - Total: 0.5 → WEAK MATCH, don't surface but available if searched
```

### Scenario 3: No Match
```
Task: "Update the README documentation"
Extracted keywords: ["update", "readme", "documentation"]
Files: ["README.md"]

All patterns:
  - No keyword matches
  - No file pattern matches
  - Total: 0 → NO MATCH, continue silently
```
