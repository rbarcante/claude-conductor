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
Tracks directory scanning and plan parsing.

Scans conductor/tracks/*/metadata.json for track status and structure.
Parses plan.md files, extracting status markers and structure.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Track:
    """Represents a track discovered via directory scan."""

    description: str
    path: Optional[str]
    status: TaskStatus


@dataclass
class Task:
    """Represents a task in a plan."""

    content: str
    status: TaskStatus
    indent_level: int
    commit_sha: Optional[str] = None
    subtasks: List["Task"] = None

    def __post_init__(self):
        if self.subtasks is None:
            self.subtasks = []


@dataclass
class Phase:
    """Represents a phase in a plan."""

    name: str
    checkpoint_sha: Optional[str]
    tasks: List[Task]


@dataclass
class PlanMetrics:
    """Aggregated metrics from a plan."""

    total: int
    completed: int
    in_progress: int
    pending: int

    @property
    def progress_percent(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100


class TracksParser:
    """Parser for plan.md files and directory-based track scanning."""

    # Plan-related regex patterns (kept)
    PHASE_PATTERN = re.compile(
        r"^#\s+Phase\s+\d+:\s*(.+?)(?:\s*\[checkpoint:\s*([a-f0-9]+)\])?$",
        re.IGNORECASE,
    )
    TASK_PATTERN = re.compile(
        r"^(\s*)-\s*\[([ x~])\]\s*(?:Task:\s*)?(.+?)(?:\s*\[commit:\s*([a-f0-9]+)\])?$"
    )
    SUBTASK_PATTERN = re.compile(
        r"^(\s+)-\s*\[([ x~])\]\s*(.+?)(?:\s*\[commit:\s*([a-f0-9]+)\])?$"
    )

    def __init__(self, project_root: Path):
        """Initialize parser with project root."""
        self.project_root = Path(project_root).resolve()

    def scan_tracks_directory(self, include_archived: bool = True) -> List[Track]:
        """
        Scan conductor/tracks/ for subdirectories containing metadata.json.

        Args:
            include_archived: If True, also scan conductor/tracks/archive/

        Returns:
            List of Track objects, ordered by track_id (directory name)
        """
        tracks: List[Track] = []
        tracks_dir = self.project_root / "conductor" / "tracks"

        if not tracks_dir.exists():
            return []

        # Scan active track directories (skip archive/ itself)
        self._scan_directory(tracks_dir, tracks, path_prefix="./conductor/tracks", default_status="pending", skip_dirs={"archive"})

        # Optionally scan archive directory
        if include_archived:
            archive_dir = tracks_dir / "archive"
            if archive_dir.exists():
                self._scan_directory(archive_dir, tracks, path_prefix="./conductor/tracks/archive", default_status="completed")

        return tracks

    def _scan_directory(
        self,
        directory: Path,
        tracks: List[Track],
        path_prefix: str,
        default_status: str = "pending",
        skip_dirs: Optional[set] = None,
    ) -> None:
        """
        Scan a directory for subdirectories containing metadata.json.

        Args:
            directory: Directory to scan
            tracks: List to append Track objects to
            path_prefix: Path prefix for track paths (e.g. ./conductor/tracks)
            default_status: Default status if not specified in metadata
            skip_dirs: Set of directory names to skip
        """
        for subdir in sorted(directory.iterdir()):
            if not subdir.is_dir():
                continue
            if skip_dirs and subdir.name in skip_dirs:
                continue

            metadata_file = subdir / "metadata.json"
            if not metadata_file.exists():
                continue

            try:
                metadata = json.loads(metadata_file.read_text())
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Skipping %s: %s", metadata_file, e)
                continue

            description = metadata.get("description", "")
            status_str = str(metadata.get("status", default_status))
            status = self._string_to_status(status_str)
            path = f"{path_prefix}/{subdir.name}/"

            tracks.append(
                Track(
                    description=description,
                    path=path,
                    status=status,
                )
            )

    def parse_plan(self, content: str) -> List[Phase]:
        """
        Parse a plan.md file content.

        Args:
            content: Plan file content

        Returns:
            List of Phase objects
        """
        phases = []
        current_phase = None
        lines = content.split("\n")

        for line in lines:
            # Check for phase header
            phase_match = self.PHASE_PATTERN.match(line)
            if phase_match:
                if current_phase:
                    phases.append(current_phase)
                current_phase = Phase(
                    name=phase_match.group(1).strip(),
                    checkpoint_sha=phase_match.group(2),
                    tasks=[],
                )
                continue

            if not current_phase:
                continue

            # Check for task
            task_match = self.TASK_PATTERN.match(line)
            if task_match:
                indent = len(task_match.group(1))
                status_char = task_match.group(2)
                content_text = task_match.group(3).strip()
                commit_sha = task_match.group(4)

                task = Task(
                    content=content_text,
                    status=self._char_to_status(status_char),
                    indent_level=indent,
                    commit_sha=commit_sha,
                )

                # Determine if this is a subtask or main task
                if indent <= 0:
                    current_phase.tasks.append(task)
                elif current_phase.tasks:
                    # Add as subtask to last task
                    current_phase.tasks[-1].subtasks.append(task)

        if current_phase:
            phases.append(current_phase)

        return phases

    def calculate_metrics(self, phases: List[Phase]) -> PlanMetrics:
        """
        Calculate metrics from parsed phases.

        Args:
            phases: List of Phase objects

        Returns:
            PlanMetrics with counts
        """
        total = 0
        completed = 0
        in_progress = 0
        pending = 0

        def count_task(task: Task):
            nonlocal total, completed, in_progress, pending
            total += 1
            if task.status == TaskStatus.COMPLETED:
                completed += 1
            elif task.status == TaskStatus.IN_PROGRESS:
                in_progress += 1
            else:
                pending += 1

            for subtask in task.subtasks:
                count_task(subtask)

        for phase in phases:
            for task in phase.tasks:
                count_task(task)

        return PlanMetrics(
            total=total, completed=completed, in_progress=in_progress, pending=pending
        )

    def count_status_markers(self, content: str) -> Dict[str, int]:
        """
        Quick count of status markers in any markdown content.

        Args:
            content: Markdown content

        Returns:
            Dict with counts: {'completed': n, 'in_progress': n, 'pending': n}
        """
        completed = len(re.findall(r"\[x\]", content))
        in_progress = len(re.findall(r"\[~\]", content))
        pending = len(re.findall(r"\[ \]", content))

        return {
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "total": completed + in_progress + pending,
        }

    def update_task_status(
        self,
        content: str,
        task_content: str,
        new_status: TaskStatus,
        commit_sha: Optional[str] = None,
    ) -> str:
        """
        Update a task's status in plan.md content.

        Args:
            content: Current plan.md content
            task_content: Task content to find
            new_status: New status to set
            commit_sha: Optional commit SHA to add

        Returns:
            Updated content
        """
        status_char = self._status_to_char(new_status)
        lines = content.split("\n")
        result = []

        for line in lines:
            if task_content in line:
                # Replace status marker
                line = re.sub(r"\[([ x~])\]", f"[{status_char}]", line, count=1)

                # Add commit SHA if provided and not already present
                if commit_sha and "[commit:" not in line:
                    line = line.rstrip() + f" [commit: {commit_sha}]"

            result.append(line)

        return "\n".join(result)

    def extract_track_id_from_path(self, path: str) -> Optional[str]:
        """
        Extract track ID from a path like ./conductor/tracks/track_id/.

        Args:
            path: Track path

        Returns:
            Track ID or None
        """
        match = re.search(r"conductor/tracks/(?:archive/)?([^/]+)", path)
        if match:
            return match.group(1)
        return None

    def _string_to_status(self, status_str: str) -> TaskStatus:
        """Convert a status string to TaskStatus enum."""
        if status_str in ("completed", "done"):
            return TaskStatus.COMPLETED
        elif status_str in ("in-progress", "in_progress", "active"):
            return TaskStatus.IN_PROGRESS
        return TaskStatus.PENDING  # handles "new", "pending", anything else

    def _char_to_status(self, char: str) -> TaskStatus:
        """Convert status character to TaskStatus enum."""
        if char == "x":
            return TaskStatus.COMPLETED
        elif char == "~":
            return TaskStatus.IN_PROGRESS
        return TaskStatus.PENDING

    def _status_to_char(self, status: TaskStatus) -> str:
        """Convert TaskStatus enum to character."""
        if status == TaskStatus.COMPLETED:
            return "x"
        elif status == TaskStatus.IN_PROGRESS:
            return "~"
        return " "
