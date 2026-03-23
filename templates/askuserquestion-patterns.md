# AskUserQuestion Patterns Reference

**Purpose:** Comprehensive examples of AskUserQuestion tool usage for Conductor commands

---

## Tool Structure

```json
{
  "questions": [
    {
      "question": "The complete question text ending with ?",
      "header": "Short label",  // Max 12 characters
      "options": [
        {"label": "Option label", "description": "What this option means"},
        {"label": "Another option", "description": "Explanation of this choice"}
      ],
      "multiSelect": false  // true if user can select multiple options
    }
  ]
}
```

---

## Mandatory Usage

<note type="critical">
All interactive questions in any Conductor command MUST use the AskUserQuestion tool. Do NOT ask plain text questions — every user-facing prompt must go through AskUserQuestion, without exception. This applies to all commands (newTrack, implement, setup, codeReview, etc.) and all question types (clarifications, approvals, confirmations, option selections).
</note>

---

## Key Rules

1. **Header Constraint:** Maximum 12 characters (e.g., "Interaction", "Data", "Scope")
2. **Options Constraint:** Minimum 2, maximum 4 options per question
3. **multiSelect:** Set to `true` for "Additive" questions; `false` for "Exclusive Choice" questions
4. **Sequential Questions:** Ask one question at a time. Wait for user response before next question
5. **"Other" Option:** Users can always select "Other" to provide custom text - do NOT add as explicit option
6. **Recommendations:** When recommending, add "(Recommended)" to label and make it first option

---

## Question Type Mapping

| Question Type | multiSelect | Example Use Case |
|--------------|-------------|------------------|
| **Additive** (multiple valid answers) | `true` | "Which capabilities should this feature include?" |
| **Exclusive Choice** (single answer) | `false` | "How should users interact with this feature?" |
| **Approval** (approve/change) | `false` | "Does this specification capture the requirements?" |

---

## Standard Patterns

### Approval Questions (Spec/Plan Review)

```json
{
  "questions": [{
    "question": "Does this specification accurately capture the requirements?",
    "header": "Review",
    "options": [
      {"label": "Approve", "description": "The document is correct, proceed to next step"},
      {"label": "Suggest changes", "description": "I want to modify some parts"}
    ],
    "multiSelect": false
  }]
}
```

### Feature Interaction Type (Exclusive)

```json
{
  "questions": [{
    "question": "How will users primarily interact with this feature?",
    "header": "Interaction",
    "options": [
      {"label": "UI component", "description": "Visual interface element (button, form, page)"},
      {"label": "API endpoint", "description": "Backend service or REST/GraphQL endpoint"},
      {"label": "CLI command", "description": "Command-line interface operation"},
      {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
    ],
    "multiSelect": false
  }]
}
```

### Feature Capabilities (Additive)

```json
{
  "questions": [{
    "question": "Which capabilities should this feature include?",
    "header": "Capabilities",
    "options": [
      {"label": "Create/Add", "description": "Ability to create new items"},
      {"label": "Read/View", "description": "Ability to view existing items"},
      {"label": "Update/Edit", "description": "Ability to modify existing items"},
      {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
    ],
    "multiSelect": true
  }]
}
```

### Data/Input Question (Additive)

```json
{
  "questions": [{
    "question": "What data or inputs does this feature need to handle?",
    "header": "Data",
    "options": [
      {"label": "User input", "description": "Form fields, text entry, selections"},
      {"label": "External API", "description": "Data from third-party services"},
      {"label": "Database", "description": "Stored records and relationships"},
      {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
    ],
    "multiSelect": true
  }]
}
```

### Bug Information (Additive)

```json
{
  "questions": [{
    "question": "Which details are available for this bug?",
    "header": "Bug Info",
    "options": [
      {"label": "Steps to reproduce", "description": "I can provide exact reproduction steps"},
      {"label": "Error message", "description": "I have the error message or stack trace"},
      {"label": "Expected behavior", "description": "I know what should happen instead"},
      {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
    ],
    "multiSelect": true
  }]
}
```

### Success Criteria (Additive)

```json
{
  "questions": [{
    "question": "What defines success for this task?",
    "header": "Success",
    "options": [
      {"label": "Specific files changed", "description": "I know exactly which files need modification"},
      {"label": "Test passes", "description": "Existing or new tests should pass"},
      {"label": "Behavior change", "description": "Observable change in application behavior"},
      {"label": "Auto-generate", "description": "Infer from context and generate the spec"}
    ],
    "multiSelect": true
  }]
}
```

### Commit Confirmation (Exclusive)

```json
{
  "questions": [{
    "question": "The track files have been created. Would you like to commit them now?",
    "header": "Commit",
    "options": [
      {"label": "Commit now", "description": "Stage and commit all track files"},
      {"label": "Skip commit", "description": "Leave files uncommitted for now"}
    ],
    "multiSelect": false
  }]
}
```

---

## Auto-Generate Option

Always include as the last option for interactive specification/plan generation:

```json
{"label": "Auto-generate", "description": "Infer from context and generate the document"}
```

**Behavior when selected:**
1. Stop asking questions immediately
2. Use gathered answers and project context to infer remaining details
3. Generate the complete document (spec or plan)
4. Present for review using an Approval question
