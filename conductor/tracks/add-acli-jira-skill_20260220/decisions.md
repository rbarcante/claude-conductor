# Decisions: Add ACLI Jira Skill

## ADR-001: Minimal Reference Structure

**Date:** 2026-02-20
**Status:** Accepted
**Context:** Needed to decide between a full reference structure (references/, examples/, scripts/) or a lean single-file approach.
**Decision:** Use a lean, single-file SKILL.md without separate reference files. All command reference content will be inline.
**Consequences:** Simpler structure, easier to maintain. If content grows beyond ~2,000 words, may need to revisit and extract to references/.

## ADR-002: Jira-Only Scope

**Date:** 2026-02-20
**Status:** Accepted
**Context:** ACLI covers multiple Atlassian products (Jira, Admin, Rovo Dev). Needed to decide scope.
**Decision:** Focus exclusively on Jira operations (work items, projects, boards/sprints, filters, auth).
**Consequences:** Keeps skill focused and lean. Admin and Rovo Dev commands can be added as separate skills if needed later.
