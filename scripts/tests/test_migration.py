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
Tests for the migrate_remove_tracks_md.py migration script.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from migrate_remove_tracks_md import migrate, parse_tracks_md


TRACKS_MD_CONTENT = """# Project Tracks

- [x] **Track: Completed feature**
  *Link: [completed_20260101](./conductor/tracks/completed_20260101/)*

- [ ] **Track: Pending feature**
  *Link: [pending_20260102](./conductor/tracks/pending_20260102/)*
"""


class TestParseTracksMd:
    """Tests for parse_tracks_md()."""

    def test_parses_checkbox_format(self, tmp_path):
        """Parses checkbox-style tracks.md entries."""
        tracks_md = tmp_path / "conductor" / "tracks.md"
        tracks_md.parent.mkdir(parents=True)
        tracks_md.write_text(TRACKS_MD_CONTENT)

        entries = parse_tracks_md(tracks_md)
        assert len(entries) == 2

        ids = {e["track_id"] for e in entries}
        assert "completed_20260101" in ids
        assert "pending_20260102" in ids

    def test_parses_status_correctly(self, tmp_path):
        """Status chars map correctly."""
        content = """
- [x] **Track: Done**
  *Link: [done_20260101](./conductor/tracks/done_20260101/)*
- [~] **Track: WIP**
  *Link: [wip_20260101](./conductor/tracks/wip_20260101/)*
- [ ] **Track: Todo**
  *Link: [todo_20260101](./conductor/tracks/todo_20260101/)*
"""
        tracks_md = tmp_path / "conductor" / "tracks.md"
        tracks_md.parent.mkdir(parents=True)
        tracks_md.write_text(content)

        entries = parse_tracks_md(tracks_md)
        by_id = {e["track_id"]: e for e in entries}

        assert by_id["done_20260101"]["status"] == "completed"
        assert by_id["wip_20260101"]["status"] == "in_progress"
        assert by_id["todo_20260101"]["status"] == "pending"

    def test_missing_tracks_md(self, tmp_path):
        """Returns empty list when tracks.md does not exist."""
        tracks_md = tmp_path / "conductor" / "tracks.md"
        entries = parse_tracks_md(tracks_md)
        assert entries == []

    def test_parses_table_format(self, tmp_path):
        """Parses table-style tracks.md entries."""
        content = """# Tracks

| ID | Title | Status |
|----|-------|--------|
| table-track_20260101 | Table track | completed |
| table-pending_20260102 | Pending table | pending |
"""
        tracks_md = tmp_path / "conductor" / "tracks.md"
        tracks_md.parent.mkdir(parents=True)
        tracks_md.write_text(content)

        entries = parse_tracks_md(tracks_md)
        assert len(entries) == 2

        by_id = {e["track_id"]: e for e in entries}
        assert by_id["table-track_20260101"]["status"] == "completed"
        assert by_id["table-pending_20260102"]["status"] == "pending"
        assert by_id["table-track_20260101"]["description"] == "Table track"


class TestMigrate:
    """Tests for migrate()."""

    def _setup_project(self, tmp_path, tracks_md_content: str, track_dirs=None):
        """Set up a minimal conductor project."""
        conductor = tmp_path / "conductor"
        conductor.mkdir()
        tracks_dir = conductor / "tracks"
        tracks_dir.mkdir()

        (conductor / "tracks.md").write_text(tracks_md_content)

        for tid, metadata in (track_dirs or {}).items():
            d = tracks_dir / tid
            d.mkdir(parents=True)
            if metadata is not None:
                (d / "metadata.json").write_text(json.dumps(metadata))

        return tmp_path

    def test_backfills_missing_metadata(self, tmp_path):
        """Creates metadata.json when it doesn't exist for a track."""
        content = """
- [ ] **Track: My feature**
  *Link: [my-feature_20260101](./conductor/tracks/my-feature_20260101/)*
"""
        project = self._setup_project(
            tmp_path, content, {"my-feature_20260101": None}
        )

        report = migrate(project, dry_run=False)

        # metadata.json should now exist
        meta_path = (
            project / "conductor" / "tracks" / "my-feature_20260101" / "metadata.json"
        )
        assert meta_path.exists()
        metadata = json.loads(meta_path.read_text())
        assert metadata["track_id"] == "my-feature_20260101"
        assert metadata["description"] == "My feature"
        assert metadata["status"] == "pending"
        assert len(report["backfilled"]) == 1

    def test_idempotent_run_twice(self, tmp_path):
        """Running migrate twice does not overwrite existing valid metadata."""
        content = """
- [x] **Track: Done feature**
  *Link: [done_20260101](./conductor/tracks/done_20260101/)*
"""
        existing_metadata = {
            "track_id": "done_20260101",
            "type": "feature",
            "status": "completed",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T12:00:00Z",
            "description": "Done feature",
        }
        project = self._setup_project(
            tmp_path, content, {"done_20260101": existing_metadata}
        )

        report1 = migrate(project, dry_run=False)
        report2 = migrate(project, dry_run=False)

        # Both runs should succeed without errors
        assert len(report1["warnings"]) == 0
        assert len(report2["warnings"]) == 0

        # The metadata should still match original (not overwritten)
        meta_path = (
            project / "conductor" / "tracks" / "done_20260101" / "metadata.json"
        )
        metadata = json.loads(meta_path.read_text())
        assert metadata["created_at"] == "2026-01-01T00:00:00Z"

    def test_missing_tracks_md_is_noop(self, tmp_path):
        """When tracks.md doesn't exist, migrate does nothing gracefully."""
        conductor = tmp_path / "conductor"
        conductor.mkdir()
        (conductor / "tracks").mkdir()

        report = migrate(tmp_path, dry_run=False)

        assert report["verified"] == []
        assert report["backfilled"] == []
        assert report["warnings"] == []

    def test_dry_run_does_not_write(self, tmp_path):
        """dry_run=True reports what would change without writing files."""
        content = """
- [ ] **Track: Dry run feature**
  *Link: [dry-run_20260101](./conductor/tracks/dry-run_20260101/)*
"""
        project = self._setup_project(
            tmp_path, content, {"dry-run_20260101": None}
        )

        report = migrate(project, dry_run=True)

        # Should report backfill
        assert len(report["backfilled"]) == 1

        # But file should NOT have been created
        meta_path = (
            project / "conductor" / "tracks" / "dry-run_20260101" / "metadata.json"
        )
        assert not meta_path.exists()

    def test_corrupt_metadata_generates_warning(self, tmp_path):
        """Corrupt metadata.json generates a warning."""
        content = """
- [ ] **Track: Corrupt meta**
  *Link: [corrupt_20260101](./conductor/tracks/corrupt_20260101/)*
"""
        project = self._setup_project(
            tmp_path, content, {"corrupt_20260101": None}
        )
        # Write corrupt JSON
        meta_path = project / "conductor" / "tracks" / "corrupt_20260101" / "metadata.json"
        meta_path.write_text("{invalid json")

        report = migrate(project, dry_run=False)

        assert len(report["warnings"]) > 0
        assert any("corrupt_20260101" in w for w in report["warnings"])

    def test_warns_on_missing_track_directory(self, tmp_path):
        """Tracks in tracks.md without a directory generate warnings."""
        content = """
- [ ] **Track: Ghost track**
  *Link: [ghost_20260101](./conductor/tracks/ghost_20260101/)*
"""
        # Don't create the ghost track directory
        conductor = tmp_path / "conductor"
        conductor.mkdir()
        (conductor / "tracks").mkdir()
        (conductor / "tracks.md").write_text(content)

        report = migrate(tmp_path, dry_run=False)

        assert "ghost_20260101" in report["missing_dirs"]
        assert len(report["warnings"]) > 0
