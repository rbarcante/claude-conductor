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
Tests for the lib utilities.
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager
from lib.tracks_parser import TracksParser, TaskStatus
from lib.markdown_parser import MarkdownParser
from lib.git_ops import GitOps
from lib.formatters import Formatters


class TestFileResolver:
    """Tests for FileResolver class."""

    def test_project_defaults(self, tmp_path):
        """Test default path resolution."""
        resolver = FileResolver(tmp_path)

        # Create a file that is in PROJECT_DEFAULTS
        (tmp_path / "conductor").mkdir()
        (tmp_path / "conductor" / "workflow.md").write_text("# Workflow")

        path = resolver.resolve_project_file("workflow")
        assert path is not None
        assert path.name == "workflow.md"

    def test_missing_file(self, tmp_path):
        """Test resolution of missing file."""
        resolver = FileResolver(tmp_path)
        path = resolver.resolve_project_file("workflow")
        assert path is None

    def test_track_directory(self, tmp_path):
        """Test track directory resolution."""
        resolver = FileResolver(tmp_path)

        # Create track directory
        track_dir = tmp_path / "conductor" / "tracks" / "test_track"
        track_dir.mkdir(parents=True)

        result = resolver.get_track_directory("test_track")
        assert result is not None
        assert result.name == "test_track"

    def test_list_tracks(self, tmp_path):
        """Test listing tracks."""
        resolver = FileResolver(tmp_path)

        # Create some tracks
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)
        (tracks_dir / "track1").mkdir()
        (tracks_dir / "track2").mkdir()
        (tracks_dir / "not_a_track.txt").write_text("file")

        tracks = resolver.list_tracks()
        assert "track1" in tracks
        assert "track2" in tracks
        assert "not_a_track.txt" not in tracks


class TestTrackIdValidation:
    """Tests for track_id validation."""

    def test_valid_track_id(self, tmp_path):
        """Valid track IDs pass validation."""
        from lib.file_resolver import validate_track_id

        # Should not raise
        validate_track_id("my-track_20260101")
        validate_track_id("track.v2")
        validate_track_id("simple")

    def test_path_traversal_rejected(self, tmp_path):
        """Path traversal in track_id is rejected."""
        from lib.file_resolver import validate_track_id

        with pytest.raises(ValueError):
            validate_track_id("../../etc/passwd")

    def test_slash_rejected(self, tmp_path):
        """Slashes in track_id are rejected."""
        from lib.file_resolver import validate_track_id

        with pytest.raises(ValueError):
            validate_track_id("foo/bar")

    def test_empty_rejected(self, tmp_path):
        """Empty track_id is rejected."""
        from lib.file_resolver import validate_track_id

        with pytest.raises(ValueError):
            validate_track_id("")

    def test_get_track_directory_validates(self, tmp_path):
        """get_track_directory rejects unsafe track IDs."""
        resolver = FileResolver(tmp_path)

        with pytest.raises(ValueError):
            resolver.get_track_directory("../../../etc")


class TestJsonManager:
    """Tests for JsonManager class."""

    def test_read_write(self, tmp_path):
        """Test basic read/write operations."""
        mgr = JsonManager(tmp_path)
        data = {"key": "value", "number": 42}

        # Write
        result = mgr.write(Path("test.json"), data)
        assert result is True

        # Read
        loaded = mgr.read(Path("test.json"))
        assert loaded == data

    def test_read_missing(self, tmp_path):
        """Test reading missing file."""
        mgr = JsonManager(tmp_path)
        result = mgr.read(Path("nonexistent.json"))
        assert result is None

    def test_settings_default(self, tmp_path):
        """Test settings with defaults."""
        mgr = JsonManager(tmp_path)

        settings = mgr.read_settings()
        assert "disabledSkills" in settings
        assert settings["disabledSkills"] == []

    def test_disabled_skills(self, tmp_path):
        """Test enabling/disabling skills."""
        mgr = JsonManager(tmp_path)

        # Disable a skill
        mgr.update_disabled_skills("test-skill", disable=True)
        settings = mgr.read_settings()
        assert "test-skill" in settings["disabledSkills"]

        # Enable it back
        mgr.update_disabled_skills("test-skill", disable=False)
        settings = mgr.read_settings()
        assert "test-skill" not in settings["disabledSkills"]

    def test_track_metadata(self, tmp_path):
        """Test track metadata creation."""
        mgr = JsonManager(tmp_path)

        metadata = mgr.create_track_metadata(
            track_id="test_20260121", track_type="feature", description="Test track"
        )

        assert metadata["track_id"] == "test_20260121"
        assert metadata["type"] == "feature"
        assert metadata["status"] == "new"
        assert "created_at" in metadata


class TestTracksParser:
    """Tests for TracksParser class."""

    def test_scan_basic(self, tmp_path):
        """scan_tracks_directory returns tracks from dirs with metadata.json."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        for tid, desc, status in [
            ("track-a_20260101", "Track A", "pending"),
            ("track-b_20260102", "Track B", "completed"),
        ]:
            d = tracks_dir / tid
            d.mkdir()
            (d / "metadata.json").write_text(
                json.dumps({"track_id": tid, "description": desc, "status": status})
            )

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 2
        descriptions = {t.description for t in tracks}
        assert "Track A" in descriptions
        assert "Track B" in descriptions

    def test_scan_excludes_archive_by_default(self, tmp_path):
        """archive/ dir is excluded when include_archived=False."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        # Active track
        active = tracks_dir / "active_20260101"
        active.mkdir()
        (active / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "active_20260101",
                    "description": "Active",
                    "status": "pending",
                }
            )
        )

        # Archived track
        archive = tracks_dir / "archive" / "old_20260101"
        archive.mkdir(parents=True)
        (archive / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "old_20260101",
                    "description": "Old",
                    "status": "completed",
                }
            )
        )

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 1
        assert tracks[0].description == "Active"

    def test_scan_includes_archive(self, tmp_path):
        """include_archived=True returns archived tracks too."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        active = tracks_dir / "active_20260101"
        active.mkdir()
        (active / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "active_20260101",
                    "description": "Active",
                    "status": "pending",
                }
            )
        )

        archive = tracks_dir / "archive" / "old_20260101"
        archive.mkdir(parents=True)
        (archive / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "old_20260101",
                    "description": "Old",
                    "status": "completed",
                }
            )
        )

        tracks = parser.scan_tracks_directory(include_archived=True)
        assert len(tracks) == 2
        descriptions = {t.description for t in tracks}
        assert "Active" in descriptions
        assert "Old" in descriptions

    def test_scan_skips_missing_metadata(self, tmp_path):
        """Dirs without metadata.json are silently skipped."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        # Dir with metadata
        good = tracks_dir / "good_20260101"
        good.mkdir()
        (good / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "good_20260101",
                    "description": "Good",
                    "status": "pending",
                }
            )
        )

        # Dir without metadata
        (tracks_dir / "no-meta_20260101").mkdir()

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 1
        assert tracks[0].description == "Good"

    def test_scan_status_mapping(self, tmp_path):
        """All status variants map correctly."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        for tid, status_val, expected in [
            ("t1_20260101", "new", TaskStatus.PENDING),
            ("t2_20260101", "pending", TaskStatus.PENDING),
            ("t3_20260101", "in-progress", TaskStatus.IN_PROGRESS),
            ("t4_20260101", "in_progress", TaskStatus.IN_PROGRESS),
            ("t5_20260101", "completed", TaskStatus.COMPLETED),
        ]:
            d = tracks_dir / tid
            d.mkdir()
            (d / "metadata.json").write_text(
                json.dumps({"track_id": tid, "description": tid, "status": status_val})
            )

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 5
        status_by_desc = {t.description: t.status for t in tracks}
        assert status_by_desc["t1_20260101"] == TaskStatus.PENDING
        assert status_by_desc["t2_20260101"] == TaskStatus.PENDING
        assert status_by_desc["t3_20260101"] == TaskStatus.IN_PROGRESS
        assert status_by_desc["t4_20260101"] == TaskStatus.IN_PROGRESS
        assert status_by_desc["t5_20260101"] == TaskStatus.COMPLETED

    def test_scan_empty_dir(self, tmp_path):
        """Empty tracks dir returns empty list."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert tracks == []

    def test_scan_nonexistent_tracks_dir(self, tmp_path):
        """Returns empty list when tracks directory doesn't exist."""
        parser = TracksParser(tmp_path)
        tracks = parser.scan_tracks_directory(include_archived=False)
        assert tracks == []

    def test_scan_corrupt_metadata_skipped(self, tmp_path):
        """Corrupt metadata.json is gracefully skipped."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        # Valid track
        good = tracks_dir / "good_20260101"
        good.mkdir()
        (good / "metadata.json").write_text(
            json.dumps(
                {
                    "track_id": "good_20260101",
                    "description": "Good",
                    "status": "pending",
                }
            )
        )

        # Corrupt track (invalid JSON)
        bad = tracks_dir / "bad_20260101"
        bad.mkdir()
        (bad / "metadata.json").write_text("{invalid json content")

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 1
        assert tracks[0].description == "Good"

    def test_scan_done_and_active_status_variants(self, tmp_path):
        """Status variants 'done' and 'active' map correctly."""
        parser = TracksParser(tmp_path)
        tracks_dir = tmp_path / "conductor" / "tracks"
        tracks_dir.mkdir(parents=True)

        for tid, status_val, expected in [
            ("t1_20260101", "done", TaskStatus.COMPLETED),
            ("t2_20260101", "active", TaskStatus.IN_PROGRESS),
        ]:
            d = tracks_dir / tid
            d.mkdir()
            (d / "metadata.json").write_text(
                json.dumps({"track_id": tid, "description": tid, "status": status_val})
            )

        tracks = parser.scan_tracks_directory(include_archived=False)
        assert len(tracks) == 2
        status_by_desc = {t.description: t.status for t in tracks}
        assert status_by_desc["t1_20260101"] == TaskStatus.COMPLETED
        assert status_by_desc["t2_20260101"] == TaskStatus.IN_PROGRESS

    def test_count_status_markers(self, tmp_path):
        """Test counting status markers."""
        parser = TracksParser(tmp_path)

        content = """
- [x] Done task 1
- [x] Done task 2
- [~] In progress
- [ ] Pending 1
- [ ] Pending 2
- [ ] Pending 3
"""

        counts = parser.count_status_markers(content)
        assert counts["completed"] == 2
        assert counts["in_progress"] == 1
        assert counts["pending"] == 3
        assert counts["total"] == 6

    def test_extract_track_id(self, tmp_path):
        """Test extracting track ID from path."""
        parser = TracksParser(tmp_path)

        track_id = parser.extract_track_id_from_path(
            "./conductor/tracks/test_20260121/"
        )
        assert track_id == "test_20260121"


class TestMarkdownParser:
    """Tests for MarkdownParser class."""

    def test_parse_frontmatter(self, tmp_path):
        """Test YAML frontmatter parsing."""
        parser = MarkdownParser(tmp_path)

        content = """---
name: Test
version: 1.0
tags: [one, two, three]
enabled: true
---
# Content here
"""

        frontmatter, remaining = parser.parse_frontmatter(content)
        assert frontmatter["name"] == "Test"
        assert frontmatter["version"] == 1.0
        assert frontmatter["tags"] == ["one", "two", "three"]
        assert frontmatter["enabled"] is True
        assert "# Content here" in remaining

    def test_extract_section(self, tmp_path):
        """Test section extraction."""
        parser = MarkdownParser(tmp_path)

        content = """# Main

## Section One
Content of section one.
More content.

## Section Two
Content of section two.

### Subsection
More content.
"""

        section = parser.extract_section(content, "Section One")
        assert "Content of section one" in section
        assert "Section Two" not in section

    def test_format_table(self, tmp_path):
        """Test table formatting."""
        parser = MarkdownParser(tmp_path)

        data = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]

        table = parser.format_table(data, ["name", "age"])
        assert "| Alice" in table
        assert "| Bob" in table
        assert "| name" in table

    def test_parse_snippet_header_python(self, tmp_path):
        """Test Python snippet header parsing."""
        parser = MarkdownParser(tmp_path)

        content = '''"""
USE: When building an API client
REQUIRES: httpx>=0.24
PATTERN: Error Handling
"""

import httpx
'''

        header = parser.parse_snippet_header(content, "python")
        assert header["use"] == "When building an API client"
        assert header["requires"] == "httpx>=0.24"
        assert header["pattern"] == "Error Handling"


class TestGitOps:
    """Tests for GitOps class."""

    def test_is_repo(self, tmp_path):
        """Test repo detection."""
        git = GitOps(tmp_path)

        # Not a repo initially
        assert git.is_repo() is False

        # Initialize
        git.init()
        assert git.is_repo() is True

    def test_status(self, tmp_path):
        """Test git status."""
        git = GitOps(tmp_path)
        git.init()

        status = git.status()
        assert "staged" in status
        assert "modified" in status


class TestFormatters:
    """Tests for Formatters class."""

    def test_status_symbol(self):
        """Test status symbols."""
        assert "✓" in Formatters.status_symbol("completed", use_color=False)
        assert "~" in Formatters.status_symbol("in_progress", use_color=False)
        assert "○" in Formatters.status_symbol("pending", use_color=False)

    def test_progress_bar(self):
        """Test progress bar."""
        bar = Formatters.progress_bar(50, 100)
        assert "50%" in bar
        assert "█" in bar
        assert "░" in bar

    def test_table(self):
        """Test table formatting."""
        data = [
            {"col1": "a", "col2": "b"},
            {"col1": "c", "col2": "d"},
        ]
        table = Formatters.table(data)
        assert "col1" in table.lower() or "Col1" in table
        assert "a" in table

    def test_truncate(self):
        """Test text truncation."""
        text = "This is a very long text that should be truncated"
        truncated = Formatters.truncate(text, 20)
        assert len(truncated) == 20
        assert truncated.endswith("...")

    def test_json_output(self):
        """Test JSON output structure."""
        output = Formatters.json_output({"key": "value"})
        assert output["success"] is True
        assert output["data"] == {"key": "value"}

        error_output = Formatters.json_output(None, success=False, error="Test error")
        assert error_output["success"] is False
        assert error_output["error"] == "Test error"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
