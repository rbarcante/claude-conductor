---
name: conductor-methodology
description: Essential Conductor concepts for always-active skill loading
version: 1.0.0
is_summary: true
---

# Conductor Methodology (Summary)

**Full Reference:** `skills/conductor-methodology/SKILL.md`

## Core Philosophy

**Measure twice, code once.** Conductor structures development: **Context → Spec & Plan → Implement**.

## Project Structure

| Path | Purpose |
|------|---------|
| `conductor/product.md` | Product vision, users, goals |
| `conductor/tech-stack.md` | Technology choices |
| `conductor/workflow.md` | Development workflow (TDD) |
| `conductor/tracks.md` | Track registry with status |
| `conductor/tracks/<id>/spec.md` | Track requirements |
| `conductor/tracks/<id>/plan.md` | Hierarchical task plan |

## Plan Status Markers

- `[ ]` - Pending
- `[~]` - In progress
- `[x]` - Completed

## Track Lifecycle

1. **Create** (`/conductor:newTrack`) → Generate spec and plan
2. **Implement** (`/conductor:implement`) → Execute tasks with TDD
3. **Complete** → Mark `[x]`, sync docs, archive/delete

## Key Principles

1. Plan before you build - specs guide implementation
2. Maintain context - follow style guides and tech choices
3. Test-Driven Development - write tests before code
4. Phase checkpoints - verify and commit at phase boundaries
