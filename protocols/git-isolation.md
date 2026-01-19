# Git Isolation Protocol

> **Purpose:** Create or switch to an isolated git branch/worktree for track work.
>
> This protocol ensures track work is properly isolated from the main codebase by requiring a dedicated git branch or worktree before implementation begins.

---

## Protected Branches

The following branches are considered **protected** and require branch isolation before committing track work:

- `main`
- `master`
- `develop`

When on a protected branch, users MUST create or switch to a feature branch before proceeding with track work.

---

## Protocol Steps

### Step 1: Detect Current Branch

1. **Get Current Branch:**
   ```bash
   git branch --show-current
   ```

2. **Get Repository Status:**
   ```bash
   git status --porcelain
   ```

3. **Determine Branch State:**
   - If on `main`, `master`, or `develop`: User is on a protected branch and should create a new feature branch.
   - If on a branch matching the pattern `<prefix>/<track_shortname>` where prefix is `feature/`, `fix/`, `refactor/`, `docs/`, or `chore/`: User may already be on a suitable branch for this track.
   - Otherwise: User is on an unrelated branch.

4. **Check for Matching Branch:**
   - Extract the track's shortname from `track_id` (e.g., `dark-mode-toggle` from `dark-mode-toggle_20260122`)
   - For new tracks (no `track_id` yet), extract shortname from the track description
   - Check if current branch name contains the track shortname
   - If match found, set `branch_matches_track = true`

### Step 2: Generate Branch Name Suggestion

**Via CLI (preferred):**

Execute the suggest-branch command:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/conductor_cli.py --json implement suggest-branch <track_id>
```

The CLI returns:
```json
{
  "success": true,
  "data": {
    "track_id": "dark-mode-toggle_20260122",
    "track_type": "feature",
    "branch_prefix": "feature/",
    "branch_name": "feature/dark-mode-toggle",
    "worktree_path": "../project-dark-mode-toggle",
    "current_branch": "main"
  }
}
```

**For new tracks (before track_id exists):**

Generate the branch name manually using the track description and type:

1. **Extract shortname from description:**
   - Extract 3-4 key words (skip stop words)
   - Join with hyphens, convert to lowercase
   - Example: "Add dark mode toggle" → `dark-mode-toggle`

2. **Map track type to branch prefix:**

   | Track Type | Branch Prefix |
   |------------|---------------|
   | `feature` | `feature/` |
   | `bugfix` | `fix/` |
   | `bug` | `fix/` |
   | `refactor` | `refactor/` |
   | `docs` | `docs/` |
   | `chore` | `chore/` |
   | (other) | `feature/` |

3. **Generate suggested branch name:** `<prefix><shortname>`
   - Example: `feature/dark-mode-toggle`

4. **Generate suggested worktree path:** `../<project_name>-<shortname>`
   - Get project name from current directory name
   - Example: `../myproject-dark-mode-toggle`

**Manual fallback (if CLI fails):**

Read the track's `metadata.json` to get the track type, then apply the mapping above.

### Step 3: Present Options to User

Use the `AskUserQuestion` tool to present branch options based on the detection results.

**Scenario A: Already on a matching branch** (when `branch_matches_track = true`)

```json
{
  "questions": [{
    "question": "You're already on branch '<current_branch>' which matches this track. How would you like to proceed?",
    "header": "Branch",
    "options": [
      {"label": "Continue on current branch (Recommended)", "description": "Keep working on the existing branch"},
      {"label": "Create new branch", "description": "Create a fresh branch for this track"}
    ],
    "multiSelect": false
  }]
}
```

**Scenario B: On main/master/develop or unrelated branch**

```json
{
  "questions": [{
    "question": "How would you like to isolate your work for this track?",
    "header": "Branch",
    "options": [
      {"label": "Create branch '<suggested_branch>' (Recommended)", "description": "Create a new feature branch from current HEAD"},
      {"label": "Create worktree at '<suggested_worktree_path>'", "description": "Create a separate working directory with its own branch"},
      {"label": "Type your own branch name", "description": "Specify a custom branch name"}
    ],
    "multiSelect": false
  }]
}
```

**Handle User Response:**
- If user selects "Continue on current branch": Proceed without git operations
- If user selects "Create branch": Execute git checkout -b with suggested name
- If user selects "Create worktree": Execute git worktree add
- If user selects "Type your own": Prompt for custom branch name, then execute git checkout -b

### Step 4: Execute Git Operations

Based on the user's selection, execute the appropriate git command.

**For branch creation:**
```bash
git checkout -b <branch_name>
```

**For worktree creation:**
```bash
git worktree add <worktree_path> -b <branch_name>
```
- The worktree command creates both a new directory and a new branch.
- After creating a worktree, inform the user: "Worktree created at `<path>`. To work in it, open a new terminal and navigate to that directory."

**Verification:**
- After executing the git command, verify success by running `git branch --show-current`.
- If the current branch matches the expected branch name, proceed to the next section.
- If the command fails, proceed to Step 5 (Error Handling).

### Step 5: Handle Errors

If git operations fail, provide clear error messages and recovery options.

**Common Error Scenarios:**

| Error | Cause | Recovery |
|-------|-------|----------|
| `error: Your local changes would be overwritten` | Uncommitted changes in working tree | Announce: "You have uncommitted changes. Please commit or stash them before creating a new branch." HALT. |
| `fatal: A branch named '<name>' already exists` | Branch name already in use | Announce: "Branch `<name>` already exists. Would you like to switch to it or choose a different name?" Re-prompt with options. |
| `fatal: '<path>' already exists` | Worktree path exists | Announce: "Directory `<path>` already exists. Choose a different location or remove the existing directory." Re-prompt with options. |
| `fatal: not a git repository` | Not in a git repository | Announce: "This directory is not a git repository. Please initialize git first: `git init`" HALT. |

**Fallback Option:**
If git operations consistently fail, offer to skip branch isolation:
- Announce: "Git branch creation failed. You may continue on the current branch, but this is not recommended for track isolation."
- Use AskUserQuestion to ask: "Continue on current branch despite the error? (Not recommended)"
- If user confirms, proceed with a warning note in the track's implementation log.

---

## Example Scenarios

**Example 1: Feature track branch creation**
```
Track: dark-mode-toggle_20260122 (type: feature)
Current branch: main

→ Agent suggests: "Create branch 'feature/dark-mode-toggle' (Recommended)"
→ User selects option 1
→ Agent executes: git checkout -b feature/dark-mode-toggle
→ Agent verifies: git branch --show-current returns "feature/dark-mode-toggle"
→ Proceeds to next section
```

**Example 2: Bugfix track branch creation**
```
Track: login-validation_20260122 (type: bugfix)
Current branch: develop

→ Agent suggests: "Create branch 'fix/login-validation' (Recommended)"
→ User selects option 1
→ Agent executes: git checkout -b fix/login-validation
→ Proceeds to next section
```

**Example 3: Worktree creation**
```
Track: api-refactor_20260122 (type: refactor)
Current branch: main
Project directory: /home/user/myproject

→ Agent presents options including worktree
→ User selects: "Create worktree at '../myproject-api-refactor'"
→ Agent executes: git worktree add ../myproject-api-refactor -b refactor/api-refactor
→ Agent announces: "Worktree created. Navigate to ../myproject-api-refactor to work in it."
→ Proceeds to next section
```

**Example 4: Continuing on existing branch**
```
Track: dark-mode-toggle_20260122 (type: feature)
Current branch: feature/dark-mode-toggle

→ Agent detects branch matches track shortname
→ Agent asks: "You're already on branch 'feature/dark-mode-toggle'. Continue?"
→ User selects: "Continue on current branch (Recommended)"
→ No git operations needed
→ Proceeds to next section
```

**Example 5: New track (before track_id exists)**
```
Track description: "Add user authentication"
Track type: feature (inferred)
Current branch: master

→ Agent generates shortname: "user-authentication"
→ Agent suggests: "Create branch 'feature/user-authentication' (Recommended)"
→ User selects option 1
→ Agent executes: git checkout -b feature/user-authentication
→ Proceeds to track creation
```
