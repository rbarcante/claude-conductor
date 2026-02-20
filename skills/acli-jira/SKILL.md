---
name: acli-jira
description: This skill should be used when the user asks to "run acli jira commands", "create a Jira issue", "search Jira issues", "manage Jira projects", "transition Jira status", "check jira issue", "consistent with jira issue", or mentions ACLI, Atlassian CLI, Jira CLI, Jira issue keys (e.g. KAN-1, PROJ-123), or jira workitem/project/board/sprint operations via the command line.
version: 1.1.0
---

# ACLI Jira Command Reference

Quick-reference for Atlassian CLI (`acli`) Jira commands. Covers authentication, work item CRUD, search, project management, boards, sprints, and filters.

## Core Principles

1. **Authenticate first**: Verify auth status before running commands
2. **JQL for precision**: Use JQL queries for targeted searches over broad listing
3. **Bulk via JQL**: Prefer `--jql` over comma-separated `--key` for operations on many items
4. **Output format matters**: Use `--json` for scripting, `--csv` for exports, default for readability
5. **Use short flags**: Combine `-p`, `-t`, `-s`, `-a` for faster command composition

## Authentication

Authenticate before running any Jira command.

```bash
# Log in (interactive browser flow)
acli jira auth login

# Check current auth status
acli jira auth status

# Switch between authenticated accounts
acli jira auth switch

# Log out
acli jira auth logout
```

## Work Items — Core Operations

### Create

> **Tip:** Issue types are project-specific. Before creating, check allowed types with:
> `acli jira workitem create -p "PROJ" --help` or attempt creation — the error message lists valid types.

```bash
# Create with inline fields
acli jira workitem create --project "PROJ" --type "Task" --summary "Implement feature X"

# Create with description
acli jira workitem create -p "PROJ" -t "Story" -s "User login" -d "As a user, I want to log in"

# Create with assignee and labels
acli jira workitem create -p "PROJ" -t "Bug" -s "Fix crash" -a "@me" -l "critical,backend"

# Create as subtask (specify parent)
acli jira workitem create -p "PROJ" -t "Subtask" -s "Write tests" --parent "PROJ-42"

# Create from JSON template
acli jira workitem create --generate-json > template.json  # generate template
acli jira workitem create --from-json template.json         # create from template

# Create from file (summary + description)
acli jira workitem create -p "PROJ" -t "Task" --from-file spec.txt

# Open editor to compose (summary + description)
acli jira workitem create -p "PROJ" -t "Task" -e
```

### View

```bash
# View work item details
acli jira workitem view PROJ-123

# View as JSON
acli jira workitem view PROJ-123 --json

# View specific fields only
acli jira workitem view PROJ-123 --fields summary,status,assignee

# Open in browser
acli jira workitem view PROJ-123 --web
```

### Edit

```bash
# Edit summary
acli jira workitem edit --key "PROJ-123" --summary "Updated summary"

# Edit multiple items
acli jira workitem edit --key "PROJ-1,PROJ-2,PROJ-3" --assignee "dev@company.com"

# Bulk edit via JQL
acli jira workitem edit --jql "project = PROJ AND status = Open" --assignee "dev@company.com"

# Edit description from file
acli jira workitem edit --key "PROJ-123" --description-file updated.txt
```

### Assign

```bash
# Assign to self
acli jira workitem assign --key "PROJ-123" --assignee "@me"

# Assign to someone
acli jira workitem assign --key "PROJ-123" --assignee "dev@company.com"

# Bulk assign via JQL
acli jira workitem assign --jql "project = PROJ AND sprint in openSprints()" --assignee "dev@company.com"
```

### Transition (Change Status)

```bash
# Transition to a new status
acli jira workitem transition --key "PROJ-123" --status "In Progress"

# Common transitions
acli jira workitem transition --key "PROJ-123" --status "Done"
acli jira workitem transition --key "PROJ-123" --status "In Review"
```

### Delete

```bash
# Delete a work item
acli jira workitem delete --key "PROJ-123"

# Delete multiple
acli jira workitem delete --key "PROJ-1,PROJ-2"
```

### Search

```bash
# Search with JQL
acli jira workitem search --jql "project = PROJ AND assignee = currentUser()"

# Search with field selection
acli jira workitem search -j "project = PROJ AND status = 'In Progress'" -f "key,summary,assignee,status"

# Search with limit
acli jira workitem search --jql "project = PROJ" --limit 50

# Count results only
acli jira workitem search --jql "project = PROJ AND type = Bug" --count

# Export as CSV
acli jira workitem search --jql "project = PROJ" --csv

# Export as JSON
acli jira workitem search --jql "sprint in openSprints()" --json

# Paginate through all results
acli jira workitem search --jql "project = PROJ" --paginate

# Search using saved filter
acli jira workitem search --filter "12345"

# Open search in browser
acli jira workitem search --jql "project = PROJ" --web
```

## Work Items — Secondary Operations

### Comments

```bash
# Add a comment
acli jira workitem comment create --key "PROJ-123" --body "Ready for review"

# List comments
acli jira workitem comment list --key "PROJ-123"

# Update a comment
acli jira workitem comment update --key "PROJ-123" --id "10001" --body "Updated comment"

# Delete a comment
acli jira workitem comment delete --key "PROJ-123" --id "10001"
```

### Clone

```bash
# Clone a work item (--to-project is required, even for same project)
acli jira workitem clone --key "PROJ-123" --to-project "PROJ"

# Clone to a different project
acli jira workitem clone --key "PROJ-123" --to-project "OTHER"
```

### Link

```bash
# Link two work items (outward blocks inward)
acli jira workitem link create --out "PROJ-123" --in "PROJ-456" --type "Blocks"

# Get available link types
acli jira workitem link type
```

### Attachments

```bash
# List attachments
acli jira workitem attachment list --key "PROJ-123"

# Delete an attachment (by attachment ID, no --key needed)
acli jira workitem attachment delete --id "10001"
```

### Watchers

```bash
# Remove a watcher (--user takes Atlassian account ID)
acli jira workitem watcher remove --key "PROJ-123" --user "5b10ac8d82e05b22cc7d4ef5"
```

### Archive / Unarchive

```bash
# Archive work items
acli jira workitem archive --key "PROJ-123"

# Unarchive work items
acli jira workitem unarchive --key "PROJ-123"
```

## Project Management

### Create Project

```bash
# Create a project cloned from an existing one (company-managed projects only)
acli jira project create --from-project "EXISTING" --key "NEWPROJ" --name "New Project"

# Create with description and lead
acli jira project create --from-project "EXISTING" --key "NEWPROJ" --name "New Project" \
  --description "Project description" --lead-email "lead@company.com"

# Generate JSON template for full control
acli jira project create --generate-json > project.json
acli jira project create --from-json project.json
```

### List Projects

```bash
# List projects (requires --limit, --recent, or --paginate)
acli jira project list --limit 50

# List recently accessed projects
acli jira project list --recent

# List all projects (paginated)
acli jira project list --paginate

# List as JSON for scripting
acli jira project list --limit 50 --json

# Extract project keys with jq
acli jira project list --limit 50 --json | jq '.[].key'
```

### View Project

```bash
# View project details
acli jira project view --key PROJ

# View as JSON
acli jira project view --key PROJ --json
```

### Update Project

```bash
# Update project name and lead (--project-key targets existing, --key sets new key)
acli jira project update --project-key "PROJ" --name "New Name" --lead-email "newlead@company.com"
```

### Archive / Restore

```bash
# Archive a project
acli jira project archive --key "PROJ"

# Restore an archived project
acli jira project restore --key "PROJ"
```

### Delete Project

```bash
# Delete a project (irreversible)
acli jira project delete --key "PROJ"
```

## Boards, Sprints & Filters

### Boards

```bash
# Search for boards
acli jira board search

# Search by name
acli jira board search --name "Team Board"

# List sprints on a board
acli jira board list-sprints --id 42
```

### Sprints

```bash
# List work items in a sprint (both --sprint and --board are required)
acli jira sprint list-workitems --sprint 100 --board 6

# List with field selection
acli jira sprint list-workitems --sprint 100 --board 6 --fields "key,summary,status,assignee"
```

### Filters

```bash
# Search filters (supports --owner, --name, --limit, --paginate)
acli jira filter search

# List my filters (--my or --favourite required)
acli jira filter list --my
acli jira filter list --favourite

# Add a filter to favourites
acli jira filter add-favourite --filter-id "12345"

# Change filter owner (--id, not --filter-id)
acli jira filter change-owner --id "12345" --owner "newowner@company.com"
```

## Common Flag Patterns

| Flag | Short | Purpose |
|------|-------|---------|
| `--json` | | Output as JSON |
| `--csv` | | Output as CSV |
| `--web` | `-w` | Open in browser |
| `--help` | `-h` | Show command help |
| `--key` | | Target work item(s), comma-separated |
| `--jql` | `-j` | JQL query for bulk operations |
| `--fields` | `-f` | Comma-separated field list |
| `--label` | `-l` | Add labels (comma-separated) |
| `--limit` | | Max results to return |
| `--paginate` | | Fetch all results via pagination |
| `--assignee` | `-a` | User email or `@me` |
| `--project` | `-p` | Project key |
| `--type` | `-t` | Work item type (Epic, Story, Task, Bug) |
| `--summary` | `-s` | Work item summary text |
| `--description` | `-d` | Work item description text |

## Common Workflows

### Discover Project & Create Items

```bash
# 1. Find available projects
acli jira project list --limit 50 --json | jq '.[] | {key, name}'

# 2. Check project details (issue types are listed in error if wrong type used)
acli jira project view --key PROJ --json

# 3. Create item with validated type
acli jira workitem create -p "PROJ" -t "Task" -s "My new task" -d "Description here"
```

### Start Working on an Item

```bash
# Find and assign item to yourself, then transition to In Progress
acli jira workitem assign --key "PROJ-123" --assignee "@me"
acli jira workitem transition --key "PROJ-123" --status "In Progress"
```

### Create Bug with Full Context

```bash
# Create bug with description, labels, and assignment
acli jira workitem create \
  -p "PROJ" -t "Bug" \
  -s "Login fails with SSO redirect loop" \
  -d "Steps: 1. Click SSO login 2. Redirects infinitely. Expected: Successful login." \
  -a "@me" -l "sso,auth,critical"
```

### Sprint Review — List Items by Status

```bash
# All items in current sprint
acli jira workitem search --jql "sprint in openSprints() AND project = PROJ" -f "key,summary,status,assignee"

# Incomplete items in current sprint
acli jira workitem search --jql "sprint in openSprints() AND project = PROJ AND status != Done" -f "key,summary,status"

# Export sprint report as CSV
acli jira workitem search --jql "sprint in openSprints() AND project = PROJ" --csv
```

### Bulk Reassignment

```bash
# Reassign all items from one person to another
acli jira workitem assign --jql "assignee = 'old@company.com' AND status != Done" --assignee "new@company.com"
```

### Complete an Item

```bash
# Add final comment and transition to Done
acli jira workitem comment create --key "PROJ-123" --body "Completed in PR #456"
acli jira workitem transition --key "PROJ-123" --status "Done"
```

## Useful JQL Patterns

```bash
# My open items
"assignee = currentUser() AND status != Done"

# Current sprint items
"sprint in openSprints() AND project = PROJ"

# Recently updated bugs
"project = PROJ AND type = Bug AND updated >= -7d"

# Unassigned items in backlog (sprint field requires Scrum board)
"project = PROJ AND assignee is EMPTY AND sprint is EMPTY"

# Items blocked or blocking
"issueFunction in linkedIssuesOf('key = PROJ-123', 'blocks')"

# Epics without completed stories
"type = Epic AND project = PROJ AND status != Done"

# High priority items needing attention
"project = PROJ AND priority in (Highest, High) AND status != Done"

# Items created this week
"project = PROJ AND created >= startOfWeek()"

# Items without estimates
"project = PROJ AND originalEstimate is EMPTY AND type in (Story, Task)"

# Overdue items
"project = PROJ AND duedate < now() AND status != Done"
```

## Output Formatting Tips

Use `--json` for scripting/piping, `--csv` for spreadsheet export, `--count` for totals only, and `-f` to select specific fields. Add `--paginate` with `--limit` for large result sets. These flags work across most `search` and `list` commands.

### JSON + jq Piping

```bash
# Extract specific fields from search results
acli jira workitem search --jql "project = PROJ" --json | jq '.[].key'

# Get project keys and names
acli jira project list --limit 50 --json | jq '.[] | {key, name}'

# Count items by status
acli jira workitem search --jql "project = PROJ" --json | jq 'group_by(.fields.status.name) | map({status: .[0].fields.status.name, count: length})'
```

### Description Formatting

- **Short descriptions**: Use `-d` with plain text. Avoid markdown headings (`##`) inline — they don't render well in all Jira views.
- **Long/rich descriptions**: Use `--editor` to compose in your editor, or `--from-file` to read from a file.
- **Multi-line inline**: Use shell line continuation (`\`) with `-d` for multi-paragraph descriptions.
