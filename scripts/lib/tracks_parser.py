"""
Tracks registry parsing and manipulation.

Parses tracks.md and plan.md files, extracting status markers and structure.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


@dataclass
class Track:
    """Represents a track in the registry."""
    description: str
    path: Optional[str]
    status: TaskStatus
    raw_line: str


@dataclass
class Task:
    """Represents a task in a plan."""
    content: str
    status: TaskStatus
    indent_level: int
    commit_sha: Optional[str] = None
    subtasks: List['Task'] = None

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
    """Parser for tracks.md and plan.md files."""

    # Regex patterns
    STATUS_PATTERN = re.compile(r'^\s*-\s*\[([ x~])\]')
    TRACK_PATTERN = re.compile(r'^\s*-\s*\[([ x~])\]\s*\*\*Track:\s*(.+?)\*\*')
    LINK_PATTERN = re.compile(r'\*Link:\s*\[([^\]]+)\]\(([^)]+)\)\*')
    PHASE_PATTERN = re.compile(r'^#\s+Phase\s+\d+:\s*(.+?)(?:\s*\[checkpoint:\s*([a-f0-9]+)\])?$', re.IGNORECASE)
    TASK_PATTERN = re.compile(r'^(\s*)-\s*\[([ x~])\]\s*(?:Task:\s*)?(.+?)(?:\s*\[commit:\s*([a-f0-9]+)\])?$')
    SUBTASK_PATTERN = re.compile(r'^(\s+)-\s*\[([ x~])\]\s*(.+?)(?:\s*\[commit:\s*([a-f0-9]+)\])?$')

    def __init__(self, project_root: Path):
        """Initialize parser with project root."""
        self.project_root = Path(project_root).resolve()

    def parse_tracks_registry(self, content: str = None) -> List[Track]:
        """
        Parse tracks.md file content.

        Args:
            content: File content (if None, reads from default location)

        Returns:
            List of Track objects
        """
        if content is None:
            tracks_path = self.project_root / 'conductor/tracks.md'
            if not tracks_path.exists():
                return []
            content = tracks_path.read_text()

        tracks = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]
            track_match = self.TRACK_PATTERN.match(line)

            if track_match:
                status_char = track_match.group(1)
                description = track_match.group(2).strip()
                status = self._char_to_status(status_char)

                # Look for link on next line
                path = None
                if i + 1 < len(lines):
                    link_match = self.LINK_PATTERN.search(lines[i + 1])
                    if link_match:
                        path = link_match.group(2)
                        i += 1

                tracks.append(Track(
                    description=description,
                    path=path,
                    status=status,
                    raw_line=line
                ))

            i += 1

        return tracks

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
        lines = content.split('\n')

        for line in lines:
            # Check for phase header
            phase_match = self.PHASE_PATTERN.match(line)
            if phase_match:
                if current_phase:
                    phases.append(current_phase)
                current_phase = Phase(
                    name=phase_match.group(1).strip(),
                    checkpoint_sha=phase_match.group(2),
                    tasks=[]
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
                    commit_sha=commit_sha
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
            total=total,
            completed=completed,
            in_progress=in_progress,
            pending=pending
        )

    def count_status_markers(self, content: str) -> Dict[str, int]:
        """
        Quick count of status markers in any markdown content.

        Args:
            content: Markdown content

        Returns:
            Dict with counts: {'completed': n, 'in_progress': n, 'pending': n}
        """
        completed = len(re.findall(r'\[x\]', content))
        in_progress = len(re.findall(r'\[~\]', content))
        pending = len(re.findall(r'\[ \]', content))

        return {
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'total': completed + in_progress + pending
        }

    def update_track_status(
        self,
        content: str,
        track_description: str,
        new_status: TaskStatus
    ) -> str:
        """
        Update a track's status in tracks.md content.

        Args:
            content: Current tracks.md content
            track_description: Track description to find
            new_status: New status to set

        Returns:
            Updated content
        """
        status_char = self._status_to_char(new_status)
        lines = content.split('\n')
        result = []

        for line in lines:
            if f'**Track: {track_description}**' in line or track_description in line:
                # Replace status marker
                line = re.sub(r'\[([ x~])\]', f'[{status_char}]', line, count=1)
            result.append(line)

        return '\n'.join(result)

    def update_task_status(
        self,
        content: str,
        task_content: str,
        new_status: TaskStatus,
        commit_sha: Optional[str] = None
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
        lines = content.split('\n')
        result = []

        for line in lines:
            if task_content in line:
                # Replace status marker
                line = re.sub(r'\[([ x~])\]', f'[{status_char}]', line, count=1)

                # Add commit SHA if provided and not already present
                if commit_sha and '[commit:' not in line:
                    line = line.rstrip() + f' [commit: {commit_sha}]'

            result.append(line)

        return '\n'.join(result)

    def extract_track_id_from_path(self, path: str) -> Optional[str]:
        """
        Extract track ID from a path like ./conductor/tracks/track_id/.

        Args:
            path: Track path

        Returns:
            Track ID or None
        """
        match = re.search(r'conductor/tracks/([^/]+)', path)
        if match:
            return match.group(1)
        return None

    def get_in_progress_items(self, content: str) -> List[Dict[str, Any]]:
        """
        Get all in-progress items from content.

        Args:
            content: Markdown content

        Returns:
            List of dicts with 'type' and 'content' keys
        """
        items = []
        lines = content.split('\n')

        for line in lines:
            if '[~]' in line:
                # Determine type
                if '**Track:' in line:
                    item_type = 'track'
                elif 'Phase' in line:
                    item_type = 'phase'
                elif 'Task:' in line:
                    item_type = 'task'
                else:
                    item_type = 'subtask'

                items.append({
                    'type': item_type,
                    'content': line.strip(),
                    'raw_line': line
                })

        return items

    def _char_to_status(self, char: str) -> TaskStatus:
        """Convert status character to TaskStatus enum."""
        if char == 'x':
            return TaskStatus.COMPLETED
        elif char == '~':
            return TaskStatus.IN_PROGRESS
        return TaskStatus.PENDING

    def _status_to_char(self, status: TaskStatus) -> str:
        """Convert TaskStatus enum to character."""
        if status == TaskStatus.COMPLETED:
            return 'x'
        elif status == TaskStatus.IN_PROGRESS:
            return '~'
        return ' '
