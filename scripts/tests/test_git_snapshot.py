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
Unit tests for scripts/commands/git_snapshot.py
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from commands.git_snapshot import (
    filter_paths,
    filter_diff_content,
    git_snapshot,
    detect_base_branch,
    _get_diff_stats,
    _get_changed_files,
    _valid_branch,
)


# ---------------------------------------------------------------------------
# filter_paths
# ---------------------------------------------------------------------------


def test_filter_paths_no_exclude():
    paths = ["src/main.py", "tests/test_main.py", "conductor/tracks/foo/plan.md"]
    assert filter_paths(paths, []) == paths


def test_filter_paths_excludes_matching():
    paths = ["src/main.py", "conductor/tracks/foo/plan.md", "README.md"]
    result = filter_paths(paths, ["conductor/tracks"])
    assert result == ["src/main.py", "README.md"]


def test_filter_paths_multiple_patterns():
    paths = ["src/main.py", "docs/api.md", "tests/test.py", "dist/bundle.js"]
    result = filter_paths(paths, ["docs/", "dist/"])
    assert result == ["src/main.py", "tests/test.py"]


def test_filter_paths_no_match():
    paths = ["src/main.py", "tests/test.py"]
    result = filter_paths(paths, ["conductor/"])
    assert result == paths


def test_filter_paths_empty_list():
    assert filter_paths([], ["conductor/"]) == []


# ---------------------------------------------------------------------------
# filter_diff_content
# ---------------------------------------------------------------------------

SAMPLE_DIFF = """\
diff --git a/src/main.py b/src/main.py
index abc..def 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,2 +1,3 @@
+added line
 unchanged
-removed line
diff --git a/conductor/tracks/foo/plan.md b/conductor/tracks/foo/plan.md
index 111..222 100644
--- a/conductor/tracks/foo/plan.md
+++ b/conductor/tracks/foo/plan.md
@@ -1 +1 @@
-old
+new
diff --git a/tests/test_main.py b/tests/test_main.py
index 333..444 100644
--- a/tests/test_main.py
+++ b/tests/test_main.py
@@ -1 +2 @@
+new test"""


def test_filter_diff_content_no_exclude():
    result = filter_diff_content(SAMPLE_DIFF, [])
    assert result == SAMPLE_DIFF


def test_filter_diff_content_excludes_file():
    result = filter_diff_content(SAMPLE_DIFF, ["conductor/tracks"])
    assert "conductor/tracks/foo/plan.md" not in result
    assert "src/main.py" in result
    assert "tests/test_main.py" in result


def test_filter_diff_content_excludes_multiple():
    result = filter_diff_content(SAMPLE_DIFF, ["conductor/tracks", "tests/"])
    assert "conductor/tracks/foo/plan.md" not in result
    assert "tests/test_main.py" not in result
    assert "src/main.py" in result


def test_filter_diff_content_empty_diff():
    assert filter_diff_content("", ["conductor/"]) == ""


# ---------------------------------------------------------------------------
# _valid_branch
# ---------------------------------------------------------------------------


def test_valid_branch_simple():
    assert _valid_branch("master") is True
    assert _valid_branch("main") is True
    assert _valid_branch("feature/my-branch") is True
    assert _valid_branch("release/1.2.3") is True


def test_valid_branch_invalid():
    assert _valid_branch("") is False
    assert _valid_branch("branch with spaces") is False
    assert _valid_branch("branch$name") is False


# ---------------------------------------------------------------------------
# git_snapshot — using a real git repo (tmp_path)
# ---------------------------------------------------------------------------


@pytest.fixture
def git_repo(tmp_path):
    """Create a minimal git repository for testing."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        capture_output=True,
    )
    (tmp_path / "README.md").write_text("# Repo\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=tmp_path,
        capture_output=True,
    )
    return tmp_path


def test_git_snapshot_returns_success(git_repo):
    result = git_snapshot(git_repo)
    assert result["success"] is True
    data = result["data"]
    assert "current_branch" in data
    assert "base_branch" in data
    assert "uncommitted_changes" in data
    assert "diff_stats" in data
    assert "changed_files" in data
    assert "diff_content" in data


def test_git_snapshot_diff_stat_only(git_repo):
    result = git_snapshot(git_repo, diff_stat_only=True)
    assert result["success"] is True
    assert "diff_content" not in result["data"]
    assert "diff_stats" in result["data"]


def test_git_snapshot_not_a_repo(tmp_path):
    result = git_snapshot(tmp_path)
    assert result["success"] is False
    assert "error" in result


def test_git_snapshot_uncommitted_changes(git_repo):
    (git_repo / "new_file.py").write_text("print('hello')\n")
    result = git_snapshot(git_repo)
    assert result["success"] is True
    assert result["data"]["uncommitted_changes"]["has_changes"] is True
    assert result["data"]["uncommitted_changes"]["untracked"] >= 1


def test_git_snapshot_diff_stats_structure(git_repo):
    result = git_snapshot(git_repo, diff_stat_only=True)
    stats = result["data"]["diff_stats"]
    assert "files_changed" in stats
    assert "lines_added" in stats
    assert "lines_removed" in stats
    assert isinstance(stats["files_changed"], int)
    assert isinstance(stats["lines_added"], int)
    assert isinstance(stats["lines_removed"], int)


def test_git_snapshot_exclude_filters_changed_files(git_repo):
    """Exclude patterns should filter the changed_files list."""
    (git_repo / "src").mkdir()
    (git_repo / "src" / "code.py").write_text("x = 1\n")
    (git_repo / "docs").mkdir()
    (git_repo / "docs" / "api.md").write_text("# API\n")
    subprocess.run(["git", "add", "."], cwd=git_repo, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "add files"], cwd=git_repo, capture_output=True
    )

    # Make changes to both files
    (git_repo / "src" / "code.py").write_text("x = 2\n")
    (git_repo / "docs" / "api.md").write_text("# API v2\n")

    result_all = git_snapshot(git_repo)
    result_excl = git_snapshot(git_repo, exclude=["docs/"])

    assert result_all["success"] is True
    assert result_excl["success"] is True
    # Excluded result should not contain docs files in diff_content
    if result_excl["data"].get("diff_content"):
        assert "docs/api.md" not in result_excl["data"]["diff_content"]


# ---------------------------------------------------------------------------
# detect_base_branch — offline fallback
# ---------------------------------------------------------------------------


def test_detect_base_branch_falls_back_gracefully(git_repo):
    """Without a remote, detect_base_branch should return a valid string."""
    branch = detect_base_branch(git_repo)
    assert isinstance(branch, str)
    assert len(branch) > 0
    # Should return master as last resort
    assert branch in ("master", "main", "develop", "master")
