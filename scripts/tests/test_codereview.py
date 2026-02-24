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
Unit tests for scripts/commands/codereview.py
"""

import subprocess
from pathlib import Path
from unittest.mock import patch
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from commands.codereview import (
    filtered_diff,
    _compute_language_stats,
    _parse_file_stats,
    TRUNCATION_INDICATOR,
    DEFAULT_MAX_LINES,
)


# ---------------------------------------------------------------------------
# _compute_language_stats
# ---------------------------------------------------------------------------


def test_compute_language_stats_basic():
    file_stats = [
        {"file": "a.py", "language": "Python", "lines_added": 10, "lines_removed": 2, "is_binary": False},
        {"file": "b.py", "language": "Python", "lines_added": 5, "lines_removed": 0, "is_binary": False},
        {"file": "c.ts", "language": "TypeScript", "lines_added": 20, "lines_removed": 8, "is_binary": False},
    ]
    result = _compute_language_stats(file_stats)

    assert "Python" in result
    assert result["Python"]["files"] == 2
    assert result["Python"]["lines_added"] == 15
    assert result["Python"]["lines_removed"] == 2

    assert "TypeScript" in result
    assert result["TypeScript"]["files"] == 1
    assert result["TypeScript"]["lines_added"] == 20


def test_compute_language_stats_empty():
    assert _compute_language_stats([]) == {}


def test_compute_language_stats_binary_files():
    file_stats = [
        {"file": "image.png", "language": "Other", "lines_added": 0, "lines_removed": 0, "is_binary": True},
    ]
    result = _compute_language_stats(file_stats)
    assert "Other" in result
    assert result["Other"]["files"] == 1
    assert result["Other"]["lines_added"] == 0


def test_compute_language_stats_multiple_languages():
    file_stats = [
        {"file": "a.py", "language": "Python", "lines_added": 5, "lines_removed": 1, "is_binary": False},
        {"file": "b.go", "language": "Go", "lines_added": 3, "lines_removed": 0, "is_binary": False},
        {"file": "c.rs", "language": "Rust", "lines_added": 7, "lines_removed": 2, "is_binary": False},
    ]
    result = _compute_language_stats(file_stats)
    assert len(result) == 3


# ---------------------------------------------------------------------------
# filtered_diff — max-lines truncation
# ---------------------------------------------------------------------------


@pytest.fixture
def git_repo_with_changes(tmp_path):
    """Set up a git repo with committed changes on a branch."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=tmp_path, capture_output=True)

    (tmp_path / "main.py").write_text("x = 1\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, capture_output=True)
    return tmp_path


def test_filtered_diff_returns_success_on_no_commits(git_repo_with_changes):
    """filtered_diff should succeed even on a repo with no upstream."""
    result = filtered_diff(git_repo_with_changes, base_branch="master")
    # On a single-commit repo with no remote, diff may be empty but should not crash
    assert "success" in result


def test_filtered_diff_max_lines_truncation():
    """Verify that diff content is truncated when it exceeds max_lines."""
    large_diff = "\n".join([f"line {i}" for i in range(200)])

    with patch("commands.codereview._get_raw_diff", return_value=large_diff), \
         patch("commands.codereview._parse_file_stats", return_value=[]), \
         patch("commands.codereview._add_untracked_file_stats", side_effect=lambda r, e, s: s), \
         patch("commands.codereview._generate_untracked_diff", return_value=""):
        result = filtered_diff(Path("/fake"), max_lines=50, base_branch="master")

    assert result["success"] is True
    assert result["data"]["stats"]["truncated"] is True
    assert TRUNCATION_INDICATOR in result["data"]["diff_content"]
    assert len(result["data"]["diff_content"].split("\n")) <= 55


def test_filtered_diff_no_truncation_when_within_limit():
    """Diff within max_lines should not be truncated."""
    small_diff = "\n".join([f"line {i}" for i in range(10)])

    with patch("commands.codereview._get_raw_diff", return_value=small_diff), \
         patch("commands.codereview._parse_file_stats", return_value=[]), \
         patch("commands.codereview._add_untracked_file_stats", side_effect=lambda r, e, s: s), \
         patch("commands.codereview._generate_untracked_diff", return_value=""):
        result = filtered_diff(Path("/fake"), max_lines=DEFAULT_MAX_LINES, base_branch="master")

    assert result["success"] is True
    assert result["data"]["stats"]["truncated"] is False
    assert TRUNCATION_INDICATOR not in result["data"]["diff_content"]


def test_filtered_diff_empty_diff():
    """Empty diff should return success with zero stats."""
    with patch("commands.codereview._get_raw_diff", return_value=""), \
         patch("commands.codereview._parse_file_stats", return_value=[]), \
         patch("commands.codereview._add_untracked_file_stats", side_effect=lambda r, e, s: s), \
         patch("commands.codereview._generate_untracked_diff", return_value=""):
        result = filtered_diff(Path("/fake"), base_branch="master")

    assert result["success"] is True
    assert result["data"]["stats"]["files_changed"] == 0
    assert result["data"]["stats"]["lines_added"] == 0


def test_filtered_diff_exclude_paths():
    """Paths in --exclude should not appear in diff_content."""
    diff = (
        "diff --git a/src/main.py b/src/main.py\n"
        "+added\n"
        "diff --git a/conductor/tracks/plan.md b/conductor/tracks/plan.md\n"
        "+track change\n"
    )

    with patch("commands.codereview._get_raw_diff", return_value=diff), \
         patch("commands.codereview._parse_file_stats", return_value=[
             {"file": "src/main.py", "language": "Python", "lines_added": 1, "lines_removed": 0, "is_binary": False},
         ]), \
         patch("commands.codereview._add_untracked_file_stats", side_effect=lambda r, e, s: s), \
         patch("commands.codereview._generate_untracked_diff", return_value=""):
        result = filtered_diff(Path("/fake"), exclude=["conductor/tracks"], base_branch="master")

    assert result["success"] is True
    assert "conductor/tracks/plan.md" not in result["data"]["diff_content"]
    assert "src/main.py" in result["data"]["diff_content"]


def test_filtered_diff_language_breakdown():
    """Language breakdown should aggregate file stats correctly."""
    with patch("commands.codereview._get_raw_diff", return_value="diff output"), \
         patch("commands.codereview._parse_file_stats", return_value=[
             {"file": "a.py", "language": "Python", "lines_added": 10, "lines_removed": 2, "is_binary": False},
             {"file": "b.py", "language": "Python", "lines_added": 5, "lines_removed": 1, "is_binary": False},
             {"file": "c.go", "language": "Go", "lines_added": 8, "lines_removed": 0, "is_binary": False},
         ]), \
         patch("commands.codereview._add_untracked_file_stats", side_effect=lambda r, e, s: s), \
         patch("commands.codereview._generate_untracked_diff", return_value=""):
        result = filtered_diff(Path("/fake"), base_branch="master")

    assert result["success"] is True
    lang = result["data"]["language_breakdown"]
    assert lang["Python"]["files"] == 2
    assert lang["Python"]["lines_added"] == 15
    assert lang["Go"]["files"] == 1


def test_filtered_diff_fail_on_no_diff():
    """Should return failure when diff cannot be generated."""
    with patch("commands.codereview._get_raw_diff", return_value=None):
        result = filtered_diff(Path("/fake"), base_branch="master")

    assert result["success"] is False
    assert "error" in result
