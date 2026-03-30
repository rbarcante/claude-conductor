# Implementation Plan: Add GLAB Skill for consistent GitLab CLI usage

## Phase 1: Create SKILL.md

- [x] Task 1.1: Create `skills/glab-cli/` directory
- [x] Task 1.2: Write `skills/glab-cli/SKILL.md` with full command reference:
  - YAML frontmatter (name: glab-cli, description, version: 1.0.0)
  - Core Principles (authenticate first, use `--output json` for scripting, prefer flags over interactive, use `-R` for cross-repo)
  - **Authentication**: `glab auth login`, `auth status`, `auth logout`
  - **Issues**: Create, View, List, Close, Reopen, Note, Board view
  - **Merge Requests**: Create, List, View, Checkout, Diff, Merge, Approve, Revoke, Rebase, Note, Update, Close, Reopen, Delete
  - **CI/CD**: Status, List, View, Retry, Run, Lint, Run-Trig
  - **Releases**: Create, List, View, Delete
  - **Repo**: Clone, Fork, View
  - **Labels**: Create, List, Get, Edit, Delete
  - **Variables**: Set, List, Get, Delete
  - **Snippets**: Create
  - **Milestones**: Create, List
  - **Common Flag Patterns** table (`--output`, `--repo`, `--web`, `--page`/`--per-page`)
  - **Common Workflows** (create MR from branch, review & merge, triage issues, check pipeline status, create release)
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Register Skill

- [ ] Task 2.1: Add `glab-cli` entry to `skills/skill-registry.json` with:
  - Keywords: `glab`, `gitlab`, `gitlab-cli`, `gitlab cli`, `merge request`, `mr`, `gitlab issue`, `gitlab pipeline`, `gitlab ci`, `glab mr`, `glab issue`, `glab ci`, `gitlab release`
  - tech_stack.tools: `["glab", "GitLab CLI"]`
  - provides.guidance: `["gitlab-issues", "gitlab-merge-requests", "gitlab-ci", "gitlab-releases", "gitlab-labels", "gitlab-variables", "gitlab-auth"]`
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
