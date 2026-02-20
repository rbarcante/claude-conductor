---
name: acli-jira
description: Use this skill when working with Atlassian CLI (ACLI) Jira commands, managing Jira work items, searching issues, or performing project management via the command line.
version: 1.0.0
---

# ACLI Jira Command Reference

Quick-reference for Atlassian CLI (`acli`) Jira commands. Covers authentication, work item CRUD, search, project management, boards, sprints, and filters.

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

# Open editor to compose
acli jira workitem create -p "PROJ" -t "Task" --editor
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

# Edit with editor
acli jira workitem edit --key "PROJ-123" --editor
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
acli jira workitem comment update --key "PROJ-123" --comment-id "10001" --body "Updated comment"

# Delete a comment
acli jira workitem comment delete --key "PROJ-123" --comment-id "10001"
```

### Clone

```bash
# Clone a work item
acli jira workitem clone --key "PROJ-123"
```

### Link

```bash
# Link two work items
acli jira workitem link --key "PROJ-123" --target "PROJ-456" --type "blocks"
```

### Attachments

```bash
# List attachments
acli jira workitem attachment list --key "PROJ-123"

# Delete an attachment
acli jira workitem attachment delete --key "PROJ-123" --attachment-id "10001"
```

### Watchers

```bash
# Remove a watcher
acli jira workitem watcher remove --key "PROJ-123" --account-id "user-account-id"
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
# Create a new project
acli jira project create --name "My Project" --key "MYPROJ" --type "software" --lead "lead@company.com"
```

### List Projects

```bash
# List all projects
acli jira project list
```

### View Project

```bash
# View project details
acli jira project view PROJ

# View as JSON
acli jira project view PROJ --json
```

### Update Project

```bash
# Update project settings
acli jira project update --key "PROJ" --name "New Name" --lead "newlead@company.com"
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
acli jira board list-sprints --board-id 42
```

### Sprints

```bash
# List work items in a sprint
acli jira sprint list-workitems --sprint-id 100

# List with field selection
acli jira sprint list-workitems --sprint-id 100 --fields "key,summary,status,assignee"
```

### Filters

```bash
# Search filters
acli jira filter search

# List all filters
acli jira filter list

# Add a filter to favourites
acli jira filter add-favourite --filter-id "12345"

# Change filter owner
acli jira filter change-owner --filter-id "12345" --owner "newowner@company.com"
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
| `--limit` | `-l` | Max results to return |
| `--paginate` | | Fetch all results via pagination |
| `--assignee` | `-a` | User email or `@me` |
| `--project` | `-p` | Project key |
| `--type` | `-t` | Work item type (Epic, Story, Task, Bug) |
| `--summary` | `-s` | Work item summary text |
| `--description` | `-d` | Work item description text |

## Common Workflows

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

# Unassigned items in backlog
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

```bash
# JSON output for scripting and piping
acli jira workitem search --jql "project = PROJ" --json

# CSV for spreadsheet export
acli jira workitem search --jql "project = PROJ" --csv

# Select specific fields to reduce noise
acli jira workitem search --jql "project = PROJ" -f "key,summary,status,priority"

# Get just the count
acli jira workitem search --jql "project = PROJ AND type = Bug" --count

# Paginate through large result sets
acli jira workitem search --jql "project = PROJ" --paginate --limit 100
```
