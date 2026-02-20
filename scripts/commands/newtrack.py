# Copyright 2026 Ricardo Barcante
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Newtrack command - 60% scriptable.

Creates track directory structure, scaffolds files, and registers tracks.
LLM still needed for spec.md and plan.md content generation.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager
from lib.formatters import Formatters

# Valid track types
TRACK_TYPES = ["feature", "bugfix", "refactor", "docs", "chore"]


def handle(args) -> Dict[str, Any]:
    """Handle newtrack subcommands."""
    project_root = args.project_root

    if args.subcommand == "generate-id":
        return generate_id(args.description)
    elif args.subcommand == "scaffold":
        return scaffold(
            project_root,
            args.track_id,
            track_type=args.type,
            description=args.description,
        )
    elif args.subcommand == "register":
        return register(project_root, args.track_id, args.description)
    else:
        return {
            "success": False,
            "error": "No subcommand specified. Use: generate-id, scaffold, or register",
        }


def generate_id(description: str) -> Dict[str, Any]:
    """
    Generate a track ID from description.

    Format: shortname_YYYYMMDD
    - shortname: lowercase, hyphenated version of key words
    - YYYYMMDD: today's date

    Args:
        description: Track description

    Returns:
        Dict with generated track_id
    """
    # Extract key words from description
    # Remove common stop words and special characters
    stop_words = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "were",
        "been",
        "be",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "need",
        "this",
        "that",
        "these",
        "those",
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
    }

    # Clean and tokenize
    words = re.findall(r"[a-zA-Z]+", description.lower())
    words = [w for w in words if w not in stop_words and len(w) > 2]

    # Take first 3-4 significant words
    shortname_words = words[:4]

    if not shortname_words:
        # Fallback to first word even if it's a stop word
        shortname_words = re.findall(r"[a-zA-Z]+", description.lower())[:2]

    shortname = "-".join(shortname_words)

    # Limit length
    if len(shortname) > 40:
        shortname = shortname[:40].rsplit("-", 1)[0]

    # Add date
    date_str = datetime.now().strftime("%Y%m%d")
    track_id = f"{shortname}_{date_str}"

    return {
        "success": True,
        "data": {
            "track_id": track_id,
            "shortname": shortname,
            "date": date_str,
            "description": description,
        },
        "message": f"Generated track ID: {track_id}",
    }


def scaffold(
    project_root: Path,
    track_id: str,
    track_type: str = "feature",
    description: str = "",
) -> Dict[str, Any]:
    """
    Create track directory structure with boilerplate files.

    Creates:
    - conductor/tracks/{track_id}/
    - index.md (with links to other files)
    - metadata.json
    - spec.md (empty template)
    - plan.md (empty template)
    - decisions.md (from template)

    Args:
        project_root: Project root directory
        track_id: Track identifier
        track_type: Track type (feature, bugfix, refactor, docs, chore)
        description: Track description

    Returns:
        Dict with created files list
    """
    resolver = FileResolver(project_root)
    json_mgr = JsonManager(project_root)

    # Validate track type
    if track_type not in TRACK_TYPES:
        return {
            "success": False,
            "error": f"Invalid track type '{track_type}'. Must be one of: {', '.join(TRACK_TYPES)}",
        }

    # Check if track already exists
    if resolver.track_exists(track_id):
        return {"success": False, "error": f"Track '{track_id}' already exists"}

    # Create track directory
    tracks_dir = project_root / "conductor" / "tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)

    track_dir = tracks_dir / track_id
    track_dir.mkdir(parents=True, exist_ok=True)

    created_files = []

    # Create index.md
    index_content = _create_index_content(track_id, description)
    index_path = track_dir / "index.md"
    index_path.write_text(index_content)
    created_files.append(str(index_path.relative_to(project_root)))

    # Create metadata.json
    metadata = json_mgr.create_track_metadata(
        track_id=track_id, track_type=track_type, description=description
    )
    json_mgr.write_track_metadata(track_id, metadata)
    created_files.append(f"conductor/tracks/{track_id}/metadata.json")

    # Create spec.md (empty template)
    spec_content = _create_spec_template(track_id, description, track_type)
    spec_path = track_dir / "spec.md"
    spec_path.write_text(spec_content)
    created_files.append(str(spec_path.relative_to(project_root)))

    # Create plan.md (empty template)
    plan_content = _create_plan_template(track_id, description)
    plan_path = track_dir / "plan.md"
    plan_path.write_text(plan_content)
    created_files.append(str(plan_path.relative_to(project_root)))

    # Create decisions.md (from template if exists, otherwise create minimal)
    decisions_content = _get_decisions_template(project_root)
    decisions_path = track_dir / "decisions.md"
    decisions_path.write_text(decisions_content)
    created_files.append(str(decisions_path.relative_to(project_root)))

    return {
        "success": True,
        "data": {
            "track_id": track_id,
            "track_type": track_type,
            "description": description,
            "track_dir": str(track_dir.relative_to(project_root)),
            "created_files": created_files,
            "metadata": metadata,
        },
        "message": Formatters.success(
            f"Created track '{track_id}' with {len(created_files)} files"
        ),
    }


def register(project_root: Path, track_id: str, description: str) -> Dict[str, Any]:
    """
    Validate and enforce metadata.json for a track (replaces tracks.md registration).

    - Verifies track directory exists (error if not)
    - Reads metadata.json; creates with defaults if missing
    - Validates required fields: track_id, type, status, created_at, updated_at, description
    - Normalizes status strings to canonical underscore form
    - Backfills any missing fields with sensible defaults
    - Writes validated metadata.json back

    Args:
        project_root: Project root directory
        track_id: Track identifier
        description: Track description (used as fallback if missing from metadata)

    Returns:
        Dict with validation result
    """
    from datetime import datetime

    resolver = FileResolver(project_root)
    json_mgr = JsonManager(project_root)

    # Verify track directory exists
    track_dir = resolver.get_track_directory(track_id)
    if not track_dir:
        return {
            "success": False,
            "error": f"Track directory for '{track_id}' not found. Run scaffold first.",
        }

    # Read existing metadata or start fresh
    metadata = json_mgr.read_track_metadata(track_id) or {}

    now = datetime.utcnow().isoformat() + "Z"

    # Backfill missing required fields
    metadata.setdefault("track_id", track_id)
    metadata.setdefault("type", "feature")
    metadata.setdefault("status", "pending")
    metadata.setdefault("created_at", now)
    metadata.setdefault("updated_at", now)
    metadata.setdefault("description", description or track_id)

    # Ensure track_id is correct
    metadata["track_id"] = track_id

    # Normalize status to canonical underscore form
    status_raw = str(metadata.get("status", "pending"))
    status_map = {
        "new": "pending",
        "in-progress": "in_progress",
        "active": "in_progress",
        "done": "completed",
    }
    metadata["status"] = status_map.get(status_raw, status_raw)

    # Validate type
    valid_types = {"feature", "bugfix", "refactor", "docs", "chore"}
    if metadata.get("type") not in valid_types:
        metadata["type"] = "feature"

    # Write validated metadata back
    json_mgr.write_track_metadata(track_id, metadata)

    return {
        "success": True,
        "data": {
            "track_id": track_id,
            "description": metadata["description"],
            "metadata_path": f"conductor/tracks/{track_id}/metadata.json",
            "metadata": metadata,
        },
        "message": Formatters.success(
            f"Validated and registered track '{track_id}' via metadata.json"
        ),
    }


def _create_index_content(track_id: str, description: str) -> str:
    """Create index.md content for track."""
    return f"""# Track: {description}

> Track ID: `{track_id}`

## Contents

- [Specification](./spec.md) - Requirements and acceptance criteria
- [Implementation Plan](./plan.md) - Task breakdown and progress
- [Decisions](./decisions.md) - Architecture Decision Records (ADRs)
- [Metadata](./metadata.json) - Track metadata and status

## Quick Links

| Document | Description |
|----------|-------------|
| Specification | What we're building and why |
| Plan | How we're building it (tasks, phases) |
| Decisions | Technical decisions and rationale |

"""


def _create_spec_template(track_id: str, description: str, track_type: str) -> str:
    """Create spec.md template."""
    type_guidance = {
        "feature": "Define the new feature, its user value, and acceptance criteria.",
        "bugfix": "Describe the bug, reproduction steps, root cause, and fix criteria.",
        "refactor": "Explain what is being refactored, why, and the expected improvements.",
        "docs": "Outline what documentation needs to be created or updated.",
        "chore": "Describe the maintenance task and its importance.",
    }

    guidance = type_guidance.get(
        track_type, "Define the scope and acceptance criteria."
    )

    return f"""# Specification: {description}

> **Type:** {track_type}
> **Track ID:** `{track_id}`

## Overview

{guidance}

<!-- TODO: Fill in the specification -->

## Background

<!-- Why is this work needed? What problem does it solve? -->

## Requirements

### Functional Requirements

<!-- List what the system must do -->

- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements

<!-- Performance, security, accessibility, etc. -->

- [ ] Non-functional requirement 1

## Acceptance Criteria

<!-- How will we know this is complete? -->

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

## Out of Scope

<!-- What is explicitly NOT part of this track -->

- Item 1

## Dependencies

<!-- External dependencies, other tracks, etc. -->

- None identified

## References

<!-- Links to related documents, issues, designs, etc. -->

- None

"""


def _create_plan_template(track_id: str, description: str) -> str:
    """Create plan.md template."""
    return f"""# Implementation Plan: {description}

> **Track ID:** `{track_id}`

## Overview

This plan outlines the implementation tasks for this track. Each task follows TDD methodology.

---

## Phase 1: Setup and Foundation

<!-- Tasks for initial setup -->

- [ ] Task: Set up initial structure
- [ ] Task: Configure dependencies

## Phase 2: Core Implementation

<!-- Main implementation tasks -->

- [ ] Task: Implement core functionality
- [ ] Task: Add tests

## Phase 3: Integration and Polish

<!-- Final integration and cleanup -->

- [ ] Task: Integration testing
- [ ] Task: Documentation
- [ ] Task: Final validation

---

## Notes

<!-- Implementation notes, decisions made during development -->

"""


def _get_decisions_template(project_root: Path) -> str:
    """Get decisions.md content from template or create default."""
    template_path = project_root / "templates" / "decisions.md"

    if template_path.exists():
        return template_path.read_text()

    # Default template if no template file exists
    return """# Decisions Log

> Architecture Decision Records (ADRs) for this track.

## About This File

This file captures significant technical and architectural decisions made during implementation.

## Decision Format

```markdown
### ADR-###: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded

#### Context
[Facts and circumstances that led to this decision point]

#### Decision
[The choice that was made]

#### Consequences
[Both positive and negative outcomes of this decision]
```

---

## Decisions

_No decisions recorded yet._

"""
