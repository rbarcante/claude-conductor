---
name: glab-cli
description: This skill should be used when the user asks to "run glab commands", "create a GitLab issue", "create a merge request", "check pipeline status", "manage GitLab projects", "create a release", or mentions glab, GitLab CLI, gitlab-cli, merge request, MR, GitLab pipeline, GitLab CI, GitLab issue keys, or gitlab operations via the command line.
version: 1.0.0
---

# GLAB CLI Command Reference

Quick-reference for the GitLab CLI (`glab`). Covers authentication, issues, merge requests, CI/CD pipelines, releases, repo management, labels, variables, snippets, and milestones.

## Core Principles

1. **Authenticate first**: Verify auth status before running commands
2. **Use `-R` for cross-repo**: Target any repo with `-R OWNER/REPO` or `GROUP/NAMESPACE/REPO`
3. **Output format matters**: Use `--output json` for scripting, default for readability
4. **Prefer flags over interactive**: Use flags (`-t`, `-d`, `-l`) for reproducible, non-interactive commands
5. **Current branch context**: Many `mr` and `ci` commands auto-detect the current branch's MR or pipeline

## Authentication

Authenticate before running any glab command.

```bash
# Interactive login (browser-based OAuth flow)
glab auth login

# Login to a self-managed instance
glab auth login --hostname gitlab.example.com

# Login with token from stdin
echo "glpat-xxxxxxxxxxxx" | glab auth login --stdin --hostname gitlab.example.com

# Check current auth status
glab auth status

# Log out
glab auth logout
```

## Issues

### Create

```bash
# Interactive creation
glab issue create

# Create with inline fields
glab issue create -t "Implement feature X" -d "Detailed description here"

# Create with labels, milestone, and assignee
glab issue create -t "Fix login bug" -l "bug,critical" -m "v2.0" -a "username"

# Create with linked merge request
glab issue create -t "Fix CVE-YYYY-XXXX" -l security --linked-mr 123

# Create and open in browser
glab issue create -t "New feature" --web

# Recover a previously started issue creation
glab issue create --recover
```

### View

```bash
# View issue details
glab issue view 42

# View with comments and activity
glab issue view 42 --comments --system-logs

# Open issue in browser
glab issue view 42 --web

# View from a different repo
glab issue view 42 -R group/project
```

### List

```bash
# List open issues
glab issue list

# List closed issues
glab issue list --closed

# List all issues (open + closed)
glab issue list -A

# Filter by labels
glab issue list -l "bug,critical"

# Filter by assignee
glab issue list --assignee "username"

# Filter by milestone
glab issue list -m "v2.0"

# Search by keyword
glab issue list --search "login"

# Output as JSON
glab issue list --output json

# Paginate results
glab issue list --per-page 50 --page 2
```

### Close / Reopen

```bash
# Close an issue
glab issue close 42

# Reopen an issue
glab issue reopen 42
```

### Note (Comment)

```bash
# Add a comment
glab issue note 42 -m "This is fixed in MR !123"

# Open editor to compose a multi-line comment
glab issue note 42
```

### Board

```bash
# View project issue board
glab issue board view

# Filter board by assignee
glab issue board view --assignee "username"

# Filter board by labels
glab issue board view --labels "bug,frontend"

# Filter board by milestone
glab issue board view --milestone "v2.0"
```

## Merge Requests

### Create

```bash
# Interactive creation
glab mr create

# Create with title and description
glab mr create -t "Add user authentication" -d "Implements OAuth2 login flow"

# Create with auto-fill from commits
glab mr create --fill

# Create as draft
glab mr create -t "WIP: New feature" --draft

# Create with labels, assignee, and reviewer
glab mr create -t "Fix bug" -l "bugfix" -a "dev" --reviewer "reviewer1,reviewer2"

# Create with specific source and target branches
glab mr create --source-branch feature/auth --target-branch main

# Create with squash on merge
glab mr create -t "Feature" --squash-before-merge

# Create and remove source branch on merge
glab mr create -t "Feature" --remove-source-branch

# Create with milestone
glab mr create -t "Feature" -m "v2.0"

# Create and open in browser
glab mr create -t "Feature" --web
```

### List

```bash
# List open MRs
glab mr list

# List merged MRs
glab mr list --merged

# List MRs by assignee
glab mr list --assignee "username"

# List MRs by reviewer
glab mr list --reviewer "username"

# List MRs by label
glab mr list -l "needs-review"

# Search by keyword
glab mr list --search "auth"

# Output as JSON
glab mr list --output json
```

### View

```bash
# View MR details
glab mr view 123

# View MR from current branch
glab mr view

# Open MR in browser
glab mr view 123 --web
```

### Checkout

```bash
# Checkout MR by ID
glab mr checkout 123

# Checkout MR by branch name
glab mr checkout feature-branch

# Checkout MR by URL
glab mr checkout "https://gitlab.com/group/project/-/merge_requests/123"
```

### Diff

```bash
# View MR diff
glab mr diff 123

# View diff from current branch's MR
glab mr diff

# View raw diff (for piping)
glab mr diff 123 --raw

# View diff without color
glab mr diff 123 --color=never
```

### Merge

```bash
# Merge MR
glab mr merge 123

# Merge with squash
glab mr merge 123 --squash

# Merge and remove source branch
glab mr merge 123 --remove-source-branch

# Merge when pipeline succeeds
glab mr merge 123 --when-pipeline-succeeds

# Merge current branch's MR
glab mr merge
```

### Approve / Revoke

```bash
# Approve MR
glab mr approve 123

# Approve multiple MRs
glab mr approve 123 345

# Approve MR matching specific SHA
glab mr approve 123 --sha abc123def

# Approve current branch's MR
glab mr approve

# Revoke approval
glab mr revoke 123
```

### Rebase

```bash
# Rebase MR source branch
glab mr rebase 123

# Rebase current branch's MR
glab mr rebase

# Rebase and skip CI
glab mr rebase 123 --skip-ci
```

### Note (Comment)

```bash
# Add a comment to MR
glab mr note 123 -m "Looks good to me!"

# Open editor for multi-line comment
glab mr note 123
```

### Update

```bash
# Update MR title
glab mr update 123 --title "Updated title"

# Update MR description
glab mr update 123 --description "New description"

# Mark MR as draft
glab mr update 123 --draft

# Mark MR as ready
glab mr update 123 --ready

# Add labels
glab mr update 123 --label "reviewed,approved"

# Set assignee
glab mr update 123 --assignee "username"

# Lock discussion
glab mr update 123 --lock-discussion
```

### Close / Reopen / Delete

```bash
# Close MR
glab mr close 123

# Reopen MR
glab mr reopen 123

# Delete MR
glab mr delete 123
```

### Other MR Operations

```bash
# List approvers for MR
glab mr approvers 123

# List issues closed by MR
glab mr issues 123

# Subscribe to MR notifications
glab mr subscribe 123

# Unsubscribe from MR
glab mr unsubscribe 123

# Add MR to your todo list
glab mr todo 123
```

## CI/CD Pipelines & Jobs

### Pipeline Status

```bash
# View current branch pipeline status (interactive)
glab ci status

# View pipeline status with live updates
glab ci status --live

# View pipeline in browser
glab ci status --web
```

### List Pipelines

```bash
# List recent pipelines
glab ci list

# List pipelines for a specific branch
glab ci list --branch main

# Output as JSON
glab ci list --output json
```

### View Pipeline / Job

```bash
# View pipeline details (interactive job selection)
glab ci view

# View specific branch pipeline
glab ci view main
```

### Retry Jobs

```bash
# Interactively select a job to retry
glab ci retry

# Retry specific job by ID
glab ci retry 224356863

# Retry job by name
glab ci retry lint

# Retry job on specific branch
glab ci retry lint --branch main
```

### Run Pipeline

```bash
# Run pipeline on current branch
glab ci run

# Run pipeline on specific branch
glab ci run --branch main
```

### Trigger Pipeline

```bash
# Trigger pipeline with token
glab ci run-trig -t <CI_JOB_TOKEN>

# Trigger on specific branch with variables
glab ci run-trig -t <CI_JOB_TOKEN> -b main --variables key1:val1,key2:val2

# Trigger with typed inputs
glab ci run-trig -t <CI_JOB_TOKEN> -b main --input "replicas:int(3)" --input "debug:bool(false)"
```

### Lint CI Config

```bash
# Lint .gitlab-ci.yml
glab ci lint

# Lint a specific file
glab ci lint path/to/.gitlab-ci.yml
```

## Releases

### Create

```bash
# Create release with tag
glab release create v1.0.0

# Create with release notes
glab release create v1.0.0 -n "Release notes here"

# Create with notes from file
glab release create v1.0.0 -F changelog.md

# Create with asset files
glab release create v1.0.0 ./build/app.zip ./build/app.tar.gz

# Create with milestone association
glab release create v1.0.0 -m "v1.0.0"

# Create with custom name
glab release create v1.0.0 --name "Production Release 1.0"

# Create with tag message (annotated tag)
glab release create v1.0.0 --tag-message "Version 1.0.0"

# Create with custom release date
glab release create v1.0.0 --released-at "2026-03-30T12:00:00Z"
```

### List

```bash
# List releases
glab release list
```

### View

```bash
# View latest release
glab release view

# View specific release
glab release view v1.0.0

# View in browser
glab release view v1.0.0 --web
```

### Delete

```bash
# Delete a release
glab release delete v1.0.0
```

## Repository

### Clone

```bash
# Clone a repository
glab repo clone group/project

# Clone to specific directory
glab repo clone group/project my-local-dir
```

### Fork

```bash
# Fork current repo
glab repo fork

# Fork a specific repo
glab repo fork group/project

# Fork and clone
glab repo fork group/project --clone

# Fork with custom name and path
glab repo fork group/project --name "my-fork" --path "my-fork-path"
```

### View

```bash
# View repo details
glab repo view

# View specific repo
glab repo view group/project

# Open in browser
glab repo view --web
```

## Labels

```bash
# Create a label
glab label create "bug" --color "#ff0000" --description "Bug reports"

# List all labels
glab label list

# Get label details
glab label get 1234

# Edit a label
glab label edit "bug" --color "#cc0000" --description "Updated description"

# Delete a label
glab label delete "bug"
```

## Variables

```bash
# Set a variable
glab variable set MY_VAR "my_value"

# Set with description
glab variable set MY_VAR "my_value" --description "API key for service X"

# Set a masked variable
glab variable set SECRET_TOKEN "s3cret" --masked

# Set a protected variable
glab variable set PROD_KEY "value" --protected

# Set a hidden variable
glab variable set HIDDEN_VAR "value" --hidden

# Set variable with environment scope
glab variable set DB_HOST "prod-db.example.com" --scope "production"

# Set variable for a group
glab variable set GROUP_VAR "value" -g mygroup

# Set variable from file
glab variable set SERVER_CERT < cert.pem

# Set variable from stdin
cat token.txt | glab variable set API_TOKEN

# List project variables
glab variable list

# List group variables
glab variable list -g mygroup

# List as JSON
glab variable list --output json

# Get a specific variable
glab variable get MY_VAR

# Delete a variable
glab variable delete MY_VAR
```

## Snippets

```bash
# Create a snippet from file
glab snippet create --title "My snippet" --filename "main.go"

# Create a personal snippet
glab snippet create --title "Notes" --filename "notes.md" --personal

# Set visibility
glab snippet create --title "Public snippet" --filename "example.sh" --visibility public
```

## Milestones

```bash
# Create a milestone
glab milestone create --title "v2.0" --description "Version 2.0 release"

# Create with dates
glab milestone create --title "v2.0" --start-date "2026-04-01" --due-date "2026-06-30"

# List milestones
glab milestone list
```

## Common Flag Patterns

| Flag | Short | Purpose |
|------|-------|---------|
| `--output json` | | Output as JSON |
| `--web` | `-w` | Open in browser |
| `--help` | `-h` | Show command help |
| `--repo OWNER/REPO` | `-R` | Target a different repository |
| `--page` | `-p` | Page number for pagination |
| `--per-page` | `-P` | Items per page |
| `--title` | `-t` | Set title (issues, MRs) |
| `--description` | `-d` | Set description |
| `--label` | `-l` | Add labels (comma-separated) |
| `--milestone` | `-m` | Set milestone |
| `--assignee` | `-a` | Set assignee |
| `--branch` | `-b` | Target branch |
| `--draft` | | Mark MR as draft |
| `--squash` | | Squash commits on merge |
| `--remove-source-branch` | | Delete source branch after merge |

## Common Workflows

### Create MR from Current Branch

```bash
# Push branch and create MR in one flow
git push -u origin HEAD
glab mr create --fill --draft
```

### Review and Merge an MR

```bash
# Checkout the MR locally
glab mr checkout 123

# View the diff
glab mr diff 123

# Approve and merge
glab mr approve 123
glab mr merge 123 --squash --remove-source-branch
```

### Triage Issues

```bash
# List unassigned bugs
glab issue list -l "bug" --assignee ""

# Assign and label
glab issue update 42 --assignee "dev" --label "priority::high"
```

### Check Pipeline and Retry

```bash
# Check current pipeline status
glab ci status

# If a job failed, retry it
glab ci retry lint

# Or run a fresh pipeline
glab ci run
```

### Create a Release

```bash
# Tag, create release, attach assets
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
glab release create v1.2.0 -F CHANGELOG.md ./dist/app.zip
```

### Work with Issues and MRs Together

```bash
# Create issue, then create MR that closes it
glab issue create -t "Add dark mode" -l "feature"
# ... implement on branch ...
glab mr create -t "Add dark mode" -d "Closes #42" --fill
```

## Output Formatting Tips

Use `--output json` for scripting/piping. Default output is human-readable. Add `--per-page` and `--page` for pagination. The `--web` flag opens any resource in your browser.

### JSON + jq Piping

```bash
# Extract MR IDs
glab mr list --output json | jq '.[].iid'

# Get issue titles and states
glab issue list --output json | jq '.[] | {title, state}'

# Count open MRs by author
glab mr list --output json | jq 'group_by(.author.username) | map({author: .[0].author.username, count: length})'
```
