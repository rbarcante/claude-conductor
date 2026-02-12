# Specification: Remove scaffold from newTrack command

## Overview

Remove the CLI `scaffold` command from the `newTrack` command workflow (`commands/newTrack.md`). The scaffold step invokes `conductor_cli.py newtrack scaffold`, which creates template files in the track directory. This adds latency to the workflow and produces verbose terminal output that makes it harder to read the spec/plan approval flow.

## Functional Requirements

1. **Remove scaffold CLI call** from Section 2.4 of `commands/newTrack.md`
2. **Replace with direct Write tool usage** — create each track file (index.md, metadata.json, spec.md, plan.md, decisions.md) using the Write tool inline during step 2.4
3. **Preserve the `generate-id` CLI call** — still use `conductor_cli.py newtrack generate-id` for track ID generation
4. **Preserve the `register` CLI call** — still use `conductor_cli.py newtrack register` for tracks.md registration
5. **Update fallback instructions** — remove scaffold fallback since the primary path no longer uses scaffold
6. **Update the CLI Commands reference section** to remove the scaffold command documentation

## Non-Functional Requirements

1. Terminal output during track creation should be cleaner and more readable
2. The spec/plan approval flow should be the focal point of the terminal interaction
3. No change to the files produced — same set of files created in `conductor/tracks/<track_id>/`

## Acceptance Criteria

- [ ] `commands/newTrack.md` no longer references the `scaffold` CLI command
- [ ] Section 2.4 uses Write tool to create track directory and files directly
- [ ] `generate-id` and `register` CLI commands remain unchanged
- [ ] Fallback instructions updated to reflect new approach
- [ ] CLI Commands reference section updated (scaffold removed)

## Out of Scope

- Changes to `conductor_cli.py` itself (the scaffold subcommand can remain in the CLI for backward compatibility)
- Changes to the spec/plan generation questioning flow (Sections 2.1–2.3)
- Changes to git isolation or setup check protocols
