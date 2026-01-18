# Specification: Git Branch/Worktree Integration for Implement Command

## Overview

Enhance the `/conductor:implement` command to enforce isolated development environments by requiring users to create or switch to a dedicated git branch or worktree before implementation begins. This ensures that track work is properly isolated from the main codebase and follows git branching best practices.

## Functional Requirements

### FR-1: Branch Creation Prompt

The implement command MUST prompt the user to create or switch to a git branch after track selection and before loading track context.

**Behavior:**
1. After a track is selected (Section 2.0 of implement.md), check the current git branch state
2. Use the `AskUserQuestion` tool to present branch options
3. The prompt MUST include suggested branch names based on track metadata

### FR-2: Branch Name Auto-Suggestion

The system MUST auto-suggest branch names using the track's type from `metadata.json`:

| Track Type | Branch Prefix | Example |
|------------|---------------|---------|
| `feature` | `feature/` | `feature/dark-mode-toggle` |
| `bugfix` | `fix/` | `fix/login-validation` |
| `refactor` | `refactor/` | `refactor/api-cleanup` |
| `docs` | `docs/` | `docs/api-reference` |
| `chore` | `chore/` | `chore/dependency-update` |

The suggested branch name format: `<prefix><track_shortname>`

### FR-3: Worktree Support

The system MUST offer worktree creation as an alternative to branches:

**Options presented to user:**
1. Create new branch (recommended for most cases)
2. Create new worktree (for parallel development)
3. Type custom branch name

### FR-4: Existing Branch Detection

Before prompting, the system MUST check if the user is already on a suitable branch:

1. Get current branch name via `git branch --show-current`
2. Compare against track's expected branch pattern (e.g., `feature/<track_shortname>`)
3. If match found, ask user: "You're already on branch `<branch_name>` which matches this track. Continue on this branch or create a new one?"

### FR-5: AskUserQuestion Integration

The branch prompt MUST use the `AskUserQuestion` tool with:
- Header: "Branch"
- Options including: suggested branch, worktree option, and "Type your own name"
- Clear descriptions for each option

**Example prompt structure:**
```
Question: "How would you like to isolate your work for this track?"
Options:
1. Create branch `feature/dark-mode-toggle` (Recommended)
2. Create worktree at `../project-dark-mode-toggle`
3. Type your own branch name
```

### FR-6: Git Operations

**For branch creation:**
```bash
git checkout -b <branch_name>
```

**For worktree creation:**
```bash
git worktree add ../<project>-<track_shortname> -b <branch_name>
```

The system MUST verify the operation succeeded before proceeding.

## Non-Functional Requirements

### NFR-1: Error Handling
- If git operations fail, display error and halt implementation
- Provide clear error messages for common issues (dirty working tree, branch exists, etc.)

### NFR-2: Protocol Placement
- Insert the branch creation step as a new Section 2.1 in `implement.md`
- The section should be titled "GIT ISOLATION SETUP"

## Acceptance Criteria

- [ ] AC-1: Running `/conductor:implement` prompts for branch/worktree creation after track selection
- [ ] AC-2: Branch prefix is auto-suggested based on track type from metadata.json
- [ ] AC-3: User can choose between creating a branch, worktree, or typing custom name
- [ ] AC-4: If already on a matching branch, user is asked whether to continue or create new
- [ ] AC-5: Git operations are executed and verified before proceeding to implementation
- [ ] AC-6: The feature uses the AskUserQuestion tool for structured user interaction

## Out of Scope

- Automatic merging of branches after track completion
- Branch protection rules or policies
- Integration with GitHub/GitLab branch naming conventions
- Automatic cleanup of stale branches/worktrees
