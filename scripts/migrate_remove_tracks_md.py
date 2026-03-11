#!/usr/bin/env python3
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
Migration script: Remove tracks.md registry.

Reads conductor/tracks.md, verifies all tracks have corresponding metadata.json,
and backfills any missing fields. Safe to run multiple times (idempotent).

Usage:
    python scripts/migrate_remove_tracks_md.py [--project-root PATH]
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Migrate from tracks.md to metadata.json"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing",
    )
    return parser.parse_args()


def parse_tracks_md(tracks_md_path: Path):
    """
    Parse conductor/tracks.md and extract track entries.

    Returns list of dicts with keys: track_id, description, status, path
    """
    if not tracks_md_path.exists():
        return []

    content = tracks_md_path.read_text()
    entries = []

    # Pattern 1: checkbox format
    # - [ ] **Track: Description**
    #   *Link: [track_id](./conductor/tracks/track_id/)*
    TRACK_PATTERN = re.compile(r"^\s*-\s*\[([ x~])\]\s*\*\*Track:\s*(.+?)\*\*")
    LINK_PATTERN = re.compile(r"\*Link:\s*\[([^\]]+)\]\(([^)]+)\)\*")

    # Pattern 2: table format
    TABLE_ROW_PATTERN = re.compile(r"^\s*\|(.+)\|\s*$")
    TABLE_SEP_PATTERN = re.compile(r"^\s*\|[\s\-|]+\|\s*$")

    STATUS_MAP = {
        " ": "pending",
        "x": "completed",
        "~": "in_progress",
    }

    lines = content.split("\n")
    table_headers = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Checkbox format
        track_match = TRACK_PATTERN.match(line)
        if track_match:
            status_char = track_match.group(1)
            description = track_match.group(2).strip()
            status = STATUS_MAP.get(status_char, "pending")

            track_id = None
            path = None
            if i + 1 < len(lines):
                link_match = LINK_PATTERN.search(lines[i + 1])
                if link_match:
                    path = link_match.group(2)
                    # Extract track_id from path
                    m = re.search(r"conductor/tracks/(?:archive/)?([^/]+)", path)
                    if m:
                        track_id = m.group(1)
                    i += 1

            if track_id:
                entries.append(
                    {
                        "track_id": track_id,
                        "description": description,
                        "status": status,
                        "path": path,
                    }
                )
            i += 1
            continue

        # Table format
        if TABLE_ROW_PATTERN.match(line):
            if TABLE_SEP_PATTERN.match(line):
                i += 1
                continue

            cols = [c.strip() for c in line.strip().strip("|").split("|")]

            # Header row
            if cols and cols[0].lower() == "id":
                table_headers = [c.lower() for c in cols]
                i += 1
                continue

            # Data row
            if table_headers and len(cols) >= len(table_headers):
                row = dict(zip(table_headers, cols))
                track_id = row.get("id", "").strip()
                description = row.get("title", "").strip()
                status_raw = row.get("status", "pending").strip().lower()

                if track_id and description:
                    # Normalize status
                    if status_raw in ("completed", "done"):
                        status = "completed"
                    elif status_raw in ("in-progress", "in_progress", "active"):
                        status = "in_progress"
                    else:
                        status = "pending"

                    entries.append(
                        {
                            "track_id": track_id,
                            "description": description,
                            "status": status,
                            "path": f"./conductor/tracks/{track_id}/",
                        }
                    )

            i += 1
            continue

        if line.strip() and not TABLE_ROW_PATTERN.match(line):
            table_headers = None

        i += 1

    return entries


def get_track_dir(project_root: Path, track_id: str) -> Path:
    """Find track directory in active or archive location."""
    active = project_root / "conductor" / "tracks" / track_id
    if active.exists():
        return active
    archived = project_root / "conductor" / "tracks" / "archive" / track_id
    if archived.exists():
        return archived
    return None


def migrate(project_root: Path, dry_run: bool = False):
    """
    Run migration: verify and backfill metadata.json from tracks.md.

    Returns:
        dict with migration report
    """
    tracks_md_path = project_root / "conductor" / "tracks.md"

    if not tracks_md_path.exists():
        print("conductor/tracks.md not found. Nothing to migrate.")
        return {"verified": [], "backfilled": [], "warnings": [], "missing_dirs": []}

    entries = parse_tracks_md(tracks_md_path)
    print(f"Found {len(entries)} entries in tracks.md")

    verified = []
    backfilled = []
    warnings = []
    missing_dirs = []

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    for entry in entries:
        track_id = entry["track_id"]
        track_dir = get_track_dir(project_root, track_id)

        if not track_dir:
            missing_dirs.append(track_id)
            warnings.append(f"WARNING: No directory found for track '{track_id}'")
            print(f"  WARNING MISSING DIR: {track_id}")
            continue

        metadata_path = track_dir / "metadata.json"

        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text())
            except Exception as e:
                warnings.append(
                    f"WARNING: Could not parse metadata.json for '{track_id}': {e}"
                )
                continue

            # Check if any required fields are missing
            required_fields = [
                "track_id",
                "type",
                "status",
                "created_at",
                "updated_at",
                "description",
            ]
            missing_fields = [f for f in required_fields if f not in metadata]

            if missing_fields:
                # Backfill missing fields
                metadata.setdefault("track_id", track_id)
                metadata.setdefault("type", "feature")
                metadata.setdefault("status", entry["status"])
                metadata.setdefault("created_at", now)
                metadata.setdefault("updated_at", now)
                metadata.setdefault("description", entry["description"])

                if not dry_run:
                    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")

                backfilled.append(
                    {
                        "track_id": track_id,
                        "backfilled_fields": missing_fields,
                    }
                )
                print(f"  BACKFILLED: {track_id} (fields: {', '.join(missing_fields)})")
            else:
                verified.append(track_id)
                print(f"  OK: {track_id}")
        else:
            # Create metadata.json from tracks.md data
            metadata = {
                "track_id": track_id,
                "type": "feature",
                "status": entry["status"],
                "created_at": now,
                "updated_at": now,
                "description": entry["description"],
            }

            if not dry_run:
                metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")

            backfilled.append(
                {
                    "track_id": track_id,
                    "backfilled_fields": list(metadata.keys()),
                }
            )
            print(f"  CREATED: {track_id} (new metadata.json)")

    report = {
        "verified": verified,
        "backfilled": backfilled,
        "warnings": warnings,
        "missing_dirs": missing_dirs,
    }

    print()
    print(f"Migration complete:")
    print(f"  Verified:    {len(verified)}")
    print(f"  Backfilled:  {len(backfilled)}")
    print(f"  Warnings:    {len(warnings)}")
    print(f"  Missing dirs: {len(missing_dirs)}")

    if warnings:
        print()
        for w in warnings:
            print(f"  {w}")

    if dry_run:
        print()
        print("(DRY RUN - no files were written)")

    return report


def main():
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    print(f"Project root: {project_root}")
    print(f"Dry run: {args.dry_run}")
    print()

    report = migrate(project_root, dry_run=args.dry_run)

    # Exit with error if there are missing directories
    if report["missing_dirs"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
