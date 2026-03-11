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
Unit tests for scripts/commands/tracks.py and implement.batch_match_patterns.
"""

import json
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from commands.tracks import (
    parse_plan_content,
    parse_plan,
    update_task,
    read_context,
)
from commands.implement import batch_match_patterns, _extract_keywords

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_PLAN = """\
# Implementation Plan: Test

## Phase 1: Setup

- [ ] Task: Create initial structure
- [~] Task: Write failing tests
- [x] Task: Implement basic feature [commit: abc1234]

## Phase 2: Integration

- [ ] Task: Add integration tests
- [x] Task: Deploy to staging [commit: def5678]
"""

PLAN_WITH_CHECKPOINT = """\
## Phase 1: Core [checkpoint: aabb112]

- [x] Task: Build core module
- [x] Task: Write unit tests

## Phase 2: Extensions

- [ ] Task: Add plugin support
"""


@pytest.fixture
def track_dir(tmp_path):
    """Create a minimal conductor track directory structure."""
    conductor = tmp_path / "conductor"
    conductor.mkdir()
    tracks = conductor / "tracks"
    tracks.mkdir()
    track = tracks / "my-track_20260101"
    track.mkdir()

    (track / "plan.md").write_text(SAMPLE_PLAN)
    (track / "spec.md").write_text("# Spec\nThis is the spec.")
    (track / "metadata.json").write_text(
        json.dumps(
            {
                "track_id": "my-track_20260101",
                "type": "feature",
                "status": "in-progress",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
                "description": "My test track",
            }
        )
    )

    return tmp_path


# ---------------------------------------------------------------------------
# parse_plan_content
# ---------------------------------------------------------------------------


def test_parse_plan_content_basic():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert len(phases) == 2


def test_parse_plan_content_phase_names():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert phases[0]["name"] == "Setup"
    assert phases[1]["name"] == "Integration"


def test_parse_plan_content_phase_indices():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert phases[0]["index"] == 0
    assert phases[1]["index"] == 1


def test_parse_plan_content_task_count():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert len(phases[0]["tasks"]) == 3
    assert len(phases[1]["tasks"]) == 2


def test_parse_plan_content_task_statuses():
    phases = parse_plan_content(SAMPLE_PLAN)
    tasks = phases[0]["tasks"]
    assert tasks[0]["status"] == "pending"
    assert tasks[1]["status"] == "in_progress"
    assert tasks[2]["status"] == "completed"


def test_parse_plan_content_task_indices():
    phases = parse_plan_content(SAMPLE_PLAN)
    for i, task in enumerate(phases[0]["tasks"]):
        assert task["index"] == i


def test_parse_plan_content_commit_sha():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert phases[0]["tasks"][2]["commit_sha"] == "abc1234"
    assert phases[0]["tasks"][0]["commit_sha"] is None


def test_parse_plan_content_line_numbers():
    phases = parse_plan_content(SAMPLE_PLAN)
    # Phase 1 header is on line 3
    assert phases[0]["line_number"] == 3
    # First task of Phase 1 is on line 5
    assert phases[0]["tasks"][0]["line_number"] == 5


def test_parse_plan_content_checkpoint():
    phases = parse_plan_content(PLAN_WITH_CHECKPOINT)
    assert phases[0]["checkpoint_sha"] == "aabb112"
    assert phases[1]["checkpoint_sha"] is None


def test_parse_plan_content_empty():
    phases = parse_plan_content("")
    assert phases == []


def test_parse_plan_content_no_phases():
    content = "- [ ] Task: Orphan task without phase header\n"
    phases = parse_plan_content(content)
    assert phases == []


def test_parse_plan_content_task_content():
    phases = parse_plan_content(SAMPLE_PLAN)
    assert phases[0]["tasks"][0]["content"] == "Create initial structure"
    assert phases[0]["tasks"][1]["content"] == "Write failing tests"


# ---------------------------------------------------------------------------
# parse_plan (file-based)
# ---------------------------------------------------------------------------


def test_parse_plan_success(track_dir):
    result = parse_plan(track_dir, "my-track_20260101")
    assert result["success"] is True
    assert result["data"]["track_id"] == "my-track_20260101"


def test_parse_plan_summary(track_dir):
    result = parse_plan(track_dir, "my-track_20260101")
    summary = result["data"]["summary"]
    assert summary["total"] == 5
    assert summary["completed"] == 2
    assert summary["in_progress"] == 1
    assert summary["pending"] == 2


def test_parse_plan_next_pending(track_dir):
    result = parse_plan(track_dir, "my-track_20260101")
    npt = result["data"]["next_pending_task"]
    assert npt is not None
    assert npt["content"] == "Create initial structure"
    assert npt["phase_index"] == 0
    assert npt["task_index"] == 0


def test_parse_plan_missing_track(track_dir):
    result = parse_plan(track_dir, "nonexistent-track_99990101")
    assert result["success"] is False
    assert "error" in result


# ---------------------------------------------------------------------------
# update_task
# ---------------------------------------------------------------------------


def test_update_task_pending_to_in_progress(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 0, "in_progress")
    assert result["success"] is True
    assert result["data"]["old_status"] == "pending"
    assert result["data"]["new_status"] == "in_progress"


def test_update_task_modifies_file(track_dir):
    update_task(track_dir, "my-track_20260101", 0, 0, "completed")
    plan_path = track_dir / "conductor" / "tracks" / "my-track_20260101" / "plan.md"
    content = plan_path.read_text()
    # The first task should now be [x]
    assert "[x] Task: Create initial structure" in content


def test_update_task_in_progress_to_completed(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 1, "completed")
    assert result["success"] is True
    assert result["data"]["old_status"] == "in_progress"
    assert result["data"]["new_status"] == "completed"


def test_update_task_completed_to_pending(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 2, "pending")
    assert result["success"] is True
    assert result["data"]["old_status"] == "completed"
    assert result["data"]["new_status"] == "pending"


def test_update_task_invalid_phase_index(track_dir):
    result = update_task(track_dir, "my-track_20260101", 99, 0, "completed")
    assert result["success"] is False
    assert "error" in result


def test_update_task_invalid_task_index(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 99, "completed")
    assert result["success"] is False
    assert "error" in result


def test_update_task_invalid_status(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 0, "invalid_status")
    assert result["success"] is False
    assert "error" in result


def test_update_task_missing_track(track_dir):
    result = update_task(track_dir, "nonexistent_20000101", 0, 0, "completed")
    assert result["success"] is False


def test_update_task_returns_line_number(track_dir):
    result = update_task(track_dir, "my-track_20260101", 0, 0, "completed")
    assert result["success"] is True
    assert "line_number" in result["data"]
    assert isinstance(result["data"]["line_number"], int)


def test_update_task_hyphenated_status(track_dir):
    """Accept both 'in_progress' and 'in-progress'."""
    result = update_task(track_dir, "my-track_20260101", 0, 0, "in-progress")
    assert result["success"] is True
    assert result["data"]["new_status"] == "in-progress"
    plan_path = track_dir / "conductor" / "tracks" / "my-track_20260101" / "plan.md"
    assert "[~] Task: Create initial structure" in plan_path.read_text()


# ---------------------------------------------------------------------------
# read_context
# ---------------------------------------------------------------------------


def test_read_context_all_sections(track_dir):
    result = read_context(track_dir, "my-track_20260101")
    assert result["success"] is True
    data = result["data"]
    assert "spec" in data
    assert "plan" in data
    assert "metadata" in data


def test_read_context_spec_content(track_dir):
    result = read_context(track_dir, "my-track_20260101")
    assert "# Spec" in result["data"]["spec"]


def test_read_context_plan_is_parsed(track_dir):
    result = read_context(track_dir, "my-track_20260101")
    plan = result["data"]["plan"]
    assert "raw" in plan
    assert "parsed" in plan
    assert isinstance(plan["parsed"], list)
    assert len(plan["parsed"]) == 2  # two phases


def test_read_context_metadata_content(track_dir):
    result = read_context(track_dir, "my-track_20260101")
    metadata = result["data"]["metadata"]
    assert metadata["track_id"] == "my-track_20260101"
    assert metadata["type"] == "feature"


def test_read_context_include_spec_only(track_dir):
    result = read_context(track_dir, "my-track_20260101", include="spec")
    assert result["success"] is True
    assert result["data"].get("spec") is not None
    # plan and metadata not requested
    assert "plan" not in result["data"]
    assert "metadata" not in result["data"]


def test_read_context_include_plan_metadata(track_dir):
    result = read_context(track_dir, "my-track_20260101", include="plan,metadata")
    assert result["success"] is True
    assert result["data"].get("plan") is not None
    assert result["data"].get("metadata") is not None
    assert "spec" not in result["data"]


def test_read_context_missing_track(track_dir):
    result = read_context(track_dir, "nonexistent_99990101")
    assert result["success"] is True  # returns success with None values
    # spec should be None since file doesn't exist
    assert result["data"].get("spec") is None


# ---------------------------------------------------------------------------
# _extract_keywords
# ---------------------------------------------------------------------------


def test_extract_keywords_removes_stop_words():
    text = "Create a new module with tests and add it to the CLI"
    keywords = _extract_keywords(text)
    assert "a" not in keywords
    assert "the" not in keywords
    assert "and" not in keywords
    assert "add" not in keywords
    assert "with" not in keywords


def test_extract_keywords_removes_short_tokens():
    text = "Add CLI to a module"
    keywords = _extract_keywords(text)
    assert "a" not in keywords
    # Short tokens < 3 chars removed
    for kw in keywords:
        assert len(kw) > 2


def test_extract_keywords_strips_backticks():
    text = "Create `scripts/commands/foo.py` module with CLI support"
    keywords = _extract_keywords(text)
    # Backtick content is stripped
    assert "scripts/commands/foo.py" not in keywords
    assert "module" in keywords


def test_extract_keywords_lowercases():
    text = "TypeScript Module JSON"
    keywords = _extract_keywords(text)
    assert "typescript" in keywords
    assert "TypeScript" not in keywords


def test_extract_keywords_empty():
    assert _extract_keywords("") == []


# ---------------------------------------------------------------------------
# batch_match_patterns
# ---------------------------------------------------------------------------


@pytest.fixture
def project_with_plan(tmp_path):
    """Project with a plan but no patterns (tests empty pattern matching)."""
    conductor = tmp_path / "conductor"
    conductor.mkdir()
    tracks = conductor / "tracks"
    tracks.mkdir()
    track = tracks / "batch-track_20260101"
    track.mkdir()

    (track / "plan.md").write_text(
        "## Phase 1: Core\n\n"
        "- [ ] Task: Build authentication module\n"
        "- [ ] Task: Write unit tests for login flow\n"
        "\n## Phase 2: UI\n\n"
        "- [ ] Task: Create React components\n"
    )
    (track / "metadata.json").write_text(
        json.dumps({"track_id": "batch-track_20260101", "type": "feature"})
    )

    # No patterns/index.md so match_patterns returns no matches gracefully
    (tmp_path / "patterns").mkdir()

    return tmp_path


def test_batch_match_patterns_missing_plan_arg(tmp_path):
    result = batch_match_patterns(tmp_path, tmp_path, None)
    assert result["success"] is False
    assert "--plan" in result["error"]


def test_batch_match_patterns_missing_track(tmp_path):
    (tmp_path / "conductor").mkdir()
    (tmp_path / "conductor" / "tracks").mkdir()
    result = batch_match_patterns(tmp_path, tmp_path, "nonexistent_20000101")
    assert result["success"] is False


def test_batch_match_patterns_returns_all_tasks(project_with_plan):
    result = batch_match_patterns(
        project_with_plan, project_with_plan, "batch-track_20260101"
    )
    assert result["success"] is True
    data = result["data"]
    assert data["summary"]["total_tasks"] == 3  # 2 + 1 tasks
    assert data["track_id"] == "batch-track_20260101"


def test_batch_match_patterns_task_structure(project_with_plan):
    result = batch_match_patterns(
        project_with_plan, project_with_plan, "batch-track_20260101"
    )
    assert result["success"] is True
    tasks = result["data"]["tasks"]
    assert len(tasks) == 3
    for task in tasks:
        assert "phase" in task
        assert "phase_index" in task
        assert "task_index" in task
        assert "task_content" in task
        assert "task_status" in task
        assert "keywords" in task
        assert "pattern_matches" in task
        assert isinstance(task["pattern_matches"], list)


def test_batch_match_patterns_summary_fields(project_with_plan):
    result = batch_match_patterns(
        project_with_plan, project_with_plan, "batch-track_20260101"
    )
    summary = result["data"]["summary"]
    assert "total_tasks" in summary
    assert "tasks_with_matches" in summary
    assert "total_pattern_matches" in summary
    assert isinstance(summary["total_tasks"], int)
    assert isinstance(summary["tasks_with_matches"], int)
