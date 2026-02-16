# Specification: Plugin Marketplace Support

> **Type:** chore
> **Track ID:** `add-marketplace-json-native_20260212`

## Overview

Add a `marketplace.json` file to enable native installation and updates of Claude Conductor via the Claude Code plugin marketplace system (`/plugin marketplace add` and `/plugin install`).

## Background

GitHub issue #28 requests marketplace support so users can install and update the plugin natively from within Claude Code. The Claude Code plugin marketplace system uses a `.claude-plugin/marketplace.json` file to define available plugins and their sources.

## Requirements

### Functional Requirements

- [ ] Create `.claude-plugin/marketplace.json` with marketplace name `claude-conductor`, owner info, and a single plugin entry for `conductor` pointing to the repo root (`"."`)
- [ ] The marketplace file must conform to the Claude Code marketplace schema

### Non-Functional Requirements

- [ ] File must be valid JSON
- [ ] Must be compatible with `claude plugin validate .`

## Acceptance Criteria

- [ ] `.claude-plugin/marketplace.json` exists with correct structure
- [ ] Users can add the marketplace via `/plugin marketplace add rbarcante/claude-conductor`
- [ ] Users can install the plugin via `/plugin install conductor@claude-conductor`
- [ ] Plugin validates successfully with `claude plugin validate .`

## Out of Scope

- Multi-plugin marketplace (only one plugin: conductor)
- Automated CI/CD publishing
- Version pinning or SHA references

## Dependencies

- None identified

## References

- [GitHub Issue #28](https://github.com/rbarcante/claude-conductor/issues/28)
- [Claude Code Marketplace Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Official Marketplace Example](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)
