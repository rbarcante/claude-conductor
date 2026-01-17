# Product Guidelines: Conductor Plugin

## Brand Identity

### Core Message
**"Measure twice, code once."**

Conductor represents a disciplined, thoughtful approach to AI-assisted software development. The brand conveys reliability, precision, and control—qualities that developers value in their tools and workflows.

### Brand Personality

**Primary Attributes:**
- **Deliberate**: Every action has a purpose; planning precedes execution
- **Reliable**: Consistent behavior; predictable outcomes
- **Professional**: Respects the developer's intelligence and time
- **Empowering**: Gives developers control over AI-assisted work

**Supporting Attributes:**
- **Clear**: Communication is unambiguous and direct
- **Thorough**: Completeness matters; details aren't skipped
- **Pragmatic**: Focuses on what works in real development scenarios

## Prose Style

### General Principles

1. **Be Concise But Complete**
   - Avoid fluff and filler words
   - Include all necessary information
   - When in doubt, completeness trumps brevity

2. **Use Active Voice**
   - "Conductor creates a plan" (not "A plan is created by Conductor")
   - "Run `/conductor:setup`" (not "The setup command should be run")

3. **Write for Scanning**
   - Use headers, lists, and formatting to break up text
   - Lead with the most important information
   - Assume developers skim before reading deeply

4. **Be Precise**
   - Use specific technical terms correctly
   - Avoid vague language like "some", "sometimes", "probably"
   - When describing behavior, be exact

### Tone Guidelines

**Default Tone: Professional and Direct**

Conductor speaks to developers as peers—competent professionals who value clear communication and don't need hand-holding.

**Examples:**

✅ Good:
```
To create a new track, run `/conductor:newTrack`. This generates a spec and plan for your feature.
```

❌ Avoid:
```
Hey there! Would you like to create a super cool new track? Just run this command and we'll get started on an amazing journey together!
```

**When to Adjust Tone:**

- **Onboarding**: Slightly more explanatory, but still professional
- **Error Messages**: Direct and actionable; avoid blame or apology
- **Success Messages**: Brief acknowledgment; move on quickly
- **Documentation**: Informative and structured for reference

### Voice Characteristics

| Aspect | Guideline |
|--------|-----------|
| **Formality** | Professional but not stiff; industry-standard technical writing |
| **Enthusiasm** | Reserved; let functionality speak for itself |
| **Authority** | Confident in recommendations; open to user choice |
| **Humor** | Minimal; only when organic and not distracting |
| **Complexity** | Assumes technical competence; explains concepts clearly |

## Messaging Framework

### Key Themes

1. **Control**
   - "Control your code"
   - "Context as a managed artifact"
   - "You decide the plan"

2. **Quality**
   - "High-quality lifecycle"
   - "Consistent, traceable work"
   - "Test-driven development"

3. **Clarity**
   - "Single source of truth"
   - "Explicit context"
   - "Traceable from requirement to code"

4. **Team Alignment**
   - "Shared foundation"
   - "Consistent workflow"
   - "Team-aware development"

### Positioning Statements

**For Solo Developers:**
"Conductor gives you the structure to build high-quality software with AI assistance, keeping your work organized, traceable, and under your control."

**For Teams:**
"Conductor transforms AI-assisted development from an individual practice into a team discipline, ensuring consistent quality and shared context across all contributors."

**For Existing Projects:**
"Conductor brings structure to brownfield development, analyzing your existing codebase to establish context without disrupting your workflow."

## Documentation Standards

### Structure

All Conductor documentation should follow this hierarchy:

```
# Title
## Section
### Subsection
- Bullet point
  - Nested bullet point
```

### Code Examples

- Use bash syntax for shell commands
- Include comments for non-obvious commands
- Show output only when instructive
- Use placeholder variables clearly (e.g., `<track_id>`)

**Example:**
```bash
# Create a new track for user authentication
/conductor:newTrack "Add user authentication"

# View the generated plan
cat conductor/tracks/auth_20250113/plan.md
```

### Command Reference Format

When documenting commands:

```markdown
### `/<command-name>`

Brief description of what the command does.

**Usage:**
```bash
/<command-name> [arguments]
```

**Example:**
```bash
/<command-name> "Add dark mode toggle"
```

**Generated Artifacts:**
- `file1.md`
- `file2.md`

**Notes:**
- Additional context or caveats
- When to use this command
- Related commands
```

## User Communication Guidelines

### Progress Updates

When Conductor reports progress during implementation:

1. **State the current action clearly**
   - "Creating user model test file..."
   - "Running test suite..."

2. **Report outcomes honestly**
   - "Tests passed: 15/15"
   - "Coverage: 87%"

3. **Explain next steps**
   - "Next: Implementing user service..."
   - "Awaiting verification before proceeding..."

### Error Handling

**Principles:**
- State what went wrong
- Explain why it matters
- Provide actionable next steps

**Format:**
```
Error: [Clear description of what failed]

Cause: [Why it failed]

Solution:
1. [Step 1]
2. [Step 2]
```

**Example:**
```
Error: Failed to create conductor directory

Cause: Directory already exists with conflicting files

Solution:
1. Review existing conductor/ directory
2. Remove or rename it if not needed
3. Run /conductor:setup again
```

### Confirmation Prompts

When asking user for confirmation:

```
I've [completed action]. Please review:

[Content to review]

What would you like to do next?
A) **Approve**: [Confirm action and proceed]
B) **Suggest Changes**: [Request modifications]

Please respond with A or B.
```

## Visual Identity

### Text Formatting

Use markdown formatting consistently:

| Element | Format | Usage |
|---------|--------|-------|
| **Emphasis** | `**bold**` | Key terms, important concepts |
| *Italics* | `*italics*` | Technical terms, foreign phrases |
| `Code` | `` `backticks` `` | Commands, variables, file paths |
| "Commands" | `**/**command**` | Conductor-specific commands |
| [Links] | `[text](url)` | External references |

### Lists

**Task Lists (with checkboxes):**
```markdown
- [ ] Pending task
- [~] In-progress task
- [x] Completed task
```

**Ordered Lists:**
Use for sequential steps or when order matters.

**Bullet Lists:**
Use for groups of related items where order doesn't matter.

### Code Blocks

**Shell Commands:**
```bash
command with options
```

**Output:**
```
program output
```

**File Content:**
```markdown
# File content in appropriate syntax
```

## Interactive Communication

### Question Style

When presenting options to users:

1. **Number or letter options clearly** (A, B, C... or 1, 2, 3...)
2. **Provide brief descriptions** for each option
3. **Include an "Other" option** for flexibility
4. **Ask for specific response format** ("Please respond with A, B, or C")

**Example:**
```
Which test framework would you like to use?

A) Jest - Popular JavaScript testing framework
B) Vitest - Fast, native ESM testing
C) Type your own answer
D) Use project default (Jest)

Please respond with A, B, C, or D.
```

### Progress Indicators

During long-running operations:

- Acknowledge the operation has started
- Provide context about what's happening
- Don't update continuously (once is sufficient)

**Example:**
```
Analyzing project structure...
This may take a moment for larger projects.
```

## Accessibility

### Language Clarity

- **Avoid idioms** that don't translate well
- **Use simple words** when complex ones aren't necessary
- **Explain acronyms** on first use (e.g., "Test-Driven Development (TDD)")
- **Define domain-specific terms** for newcomers

### Inclusive Language

- Use gender-neutral pronouns ("they", not "he/she")
- Avoid cultural references that may not translate
- Focus on behavior, not people (e.g., "failing tests" not "bad tests")

## Quality Checklist

Before publishing any user-facing content:

- [ ] Tone is professional and direct
- [ ] Technical terms are used correctly
- [ ] Code examples are accurate and tested
- [ ] Formatting is consistent
- [ ] Instructions are complete and actionable
- [ ] No ambiguity in what the user should do
- [ ] Error messages are helpful and constructive
- [ ] Links and references are correct

## Brand Voice Examples

### Scenario: Project Setup

**Conductor says:**
```
Welcome to Conductor. I will guide you through the following steps to set up your project:

1. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
2. **Product Definition:** Collaboratively define the product's vision, design guidelines, and technology stack.
3. **Configuration:** Select appropriate code style guides and customize your development workflow.
4. **Track Generation:** Define the initial track and automatically generate a detailed plan.

Let's get started!
```

### Scenario: Error During Implementation

**Conductor says:**
```
Error: Tests failed for UserAuth class

Cause: Expected token validation to throw InvalidTokenError, but no exception was thrown

Solution:
1. Review the token validation logic in UserAuth.validateToken()
2. Ensure invalid tokens trigger the correct exception
3. Run tests again with: npm test -- UserAuth

Would you like me to attempt a fix?
```

### Scenario: Phase Completion

**Conductor says:**
```
The automated tests have passed. For manual verification, please follow these steps:

**Manual Verification Steps:**
1. **Start the development server:** `npm run dev`
2. **Open your browser to:** `http://localhost:3000/auth/login`
3. **Confirm that you see:** A login form with email and password fields
4. **Test the flow:** Enter invalid credentials and verify the error message displays

Does this meet your expectations? Please confirm with yes or provide feedback on what needs to be changed.
```
