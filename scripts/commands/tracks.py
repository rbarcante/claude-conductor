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
Track operations commands: parse-plan, update-task, read-context.

Consolidates multiple file reads and plan manipulations into structured JSON responses,
reducing per-task tool calls when loading or modifying track context.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager


def handle(args: argparse.Namespace) -> Dict[str, Any]:
    """Handle tracks subcommands."""
    project_root = args.project_root

    if args.subcommand == "parse-plan":
        return parse_plan(project_root, args.track_id)
    elif args.subcommand == "update-task":
        return update_task(
            project_root,
            args.track_id,
            args.phase_index,
            args.task_index,
            args.status,
        )
    elif args.subcommand == "read-context":
        include = getattr(args, "include", None)
        return read_context(project_root, args.track_id, include)

    return {
        "success": False,
        "error": "No subcommand specified. Use: parse-plan, update-task, read-context",
    }


def parse_plan(project_root: Path, track_id: str) -> Dict[str, Any]:
    """
    Parse a track's plan.md into structured JSON.

    Returns phase hierarchy, tasks with status and line numbers,
    summary counts, and the next pending task.

    Args:
        project_root: Project root directory
        track_id: Track identifier

    Returns:
        JSON with phases, summary counts, and next_pending_task
    """
    resolver = FileResolver(project_root)
    plan_file = resolver.resolve_track_file(track_id, "implementation_plan")
    if not plan_file:
        return {
            "success": False,
            "error": f"Plan file not found for track: {track_id}",
        }

    content = plan_file.read_text()
    phases = parse_plan_content(content)

    # Compute summary and find next pending task
    total = completed = in_progress = pending = 0
    next_pending: Optional[Dict[str, Any]] = None

    for phase in phases:
        for task in phase["tasks"]:
            total += 1
            s = task["status"]
            if s == "completed":
                completed += 1
            elif s == "in_progress":
                in_progress += 1
            else:
                pending += 1
                if next_pending is None:
                    next_pending = {
                        "phase_index": phase["index"],
                        "phase_name": phase["name"],
                        "task_index": task["index"],
                        "content": task["content"],
                        "line_number": task["line_number"],
                    }

    summary = {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "pending": pending,
    }

    return {
        "success": True,
        "data": {
            "track_id": track_id,
            "phases": phases,
            "summary": summary,
            "next_pending_task": next_pending,
        },
        "message": _format_parse_plan(phases, summary),
    }


def parse_plan_content(content: str) -> List[Dict[str, Any]]:
    """
    Parse plan.md content into a list of phase dicts with tasks and line numbers.

    Args:
        content: Raw plan.md content

    Returns:
        List of phase dicts with structure:
        {name, index, checkpoint_sha, line_number, tasks: [{index, content, status, commit_sha, line_number}]}
    """
    phases: List[Dict[str, Any]] = []
    current_phase: Optional[Dict[str, Any]] = None

    # Matches: ## Phase N: Name [checkpoint: abc1234]
    PHASE_RE = re.compile(
        r"^##?\s+Phase\s+\d+[:.]\s*(.+?)(?:\s*\[checkpoint:\s*([a-f0-9]+)\])?$",
        re.IGNORECASE,
    )
    # Matches: - [ ] Task: description [commit: abc1234]
    TASK_RE = re.compile(
        r"^(\s*)-\s*\[([ x~])\]\s*(?:Task:\s*)?(.+?)(?:\s*\[(?:commit|uncommitted):\s*([a-f0-9]+)\])?$"
    )
    STATUS_MAP = {" ": "pending", "~": "in_progress", "x": "completed"}

    for line_no, line in enumerate(content.split("\n"), start=1):
        phase_m = PHASE_RE.match(line)
        if phase_m:
            if current_phase:
                phases.append(current_phase)
            current_phase = {
                "name": phase_m.group(1).strip(),
                "index": len(phases),
                "checkpoint_sha": phase_m.group(2),
                "line_number": line_no,
                "tasks": [],
            }
            continue

        if not current_phase:
            continue

        task_m = TASK_RE.match(line)
        if task_m:
            indent = len(task_m.group(1))
            status_char = task_m.group(2)
            task_content = task_m.group(3).strip()
            commit_sha = task_m.group(4)

            # Only capture top-level tasks (no indentation)
            if indent == 0:
                current_phase["tasks"].append(
                    {
                        "index": len(current_phase["tasks"]),
                        "content": task_content,
                        "status": STATUS_MAP.get(status_char, "pending"),
                        "commit_sha": commit_sha,
                        "line_number": line_no,
                    }
                )

    if current_phase:
        phases.append(current_phase)

    return phases


def update_task(
    project_root: Path,
    track_id: str,
    phase_index: int,
    task_index: int,
    new_status: str,
) -> Dict[str, Any]:
    """
    Update a task's status marker in plan.md by phase index and task index.

    Args:
        project_root: Project root directory
        track_id: Track identifier
        phase_index: 0-based phase index
        task_index: 0-based task index within the phase
        new_status: New status ('pending', 'in_progress', 'in-progress', 'completed')

    Returns:
        JSON with old_status, new_status, line_number, and task details
    """
    resolver = FileResolver(project_root)
    plan_file = resolver.resolve_track_file(track_id, "implementation_plan")
    if not plan_file:
        return {
            "success": False,
            "error": f"Plan file not found for track: {track_id}",
        }

    STATUS_CHAR_MAP = {
        "pending": " ",
        "in_progress": "~",
        "in-progress": "~",
        "completed": "x",
    }

    if new_status not in STATUS_CHAR_MAP:
        return {
            "success": False,
            "error": (
                f"Invalid status '{new_status}'. "
                "Use: pending, in_progress, in-progress, completed"
            ),
        }

    content = plan_file.read_text()
    phases = parse_plan_content(content)

    if phase_index >= len(phases):
        return {
            "success": False,
            "error": f"Phase index {phase_index} out of range (0–{len(phases) - 1})",
        }

    phase = phases[phase_index]
    if task_index >= len(phase["tasks"]):
        return {
            "success": False,
            "error": (
                f"Task index {task_index} out of range "
                f"(0–{len(phase['tasks']) - 1})"
            ),
        }

    task = phase["tasks"][task_index]
    old_status = task["status"]
    target_line_idx = task["line_number"] - 1  # 0-based index

    lines = content.split("\n")
    old_line = lines[target_line_idx]
    new_char = STATUS_CHAR_MAP[new_status]
    new_line = re.sub(r"\[([ x~])\]", f"[{new_char}]", old_line, count=1)
    lines[target_line_idx] = new_line

    plan_file.write_text("\n".join(lines))

    return {
        "success": True,
        "data": {
            "track_id": track_id,
            "phase_index": phase_index,
            "phase_name": phase["name"],
            "task_index": task_index,
            "task_content": task["content"],
            "old_status": old_status,
            "new_status": new_status,
            "line_number": task["line_number"],
        },
        "message": (
            f"Updated [{phase['name']}] task {task_index}: "
            f"{old_status} → {new_status}"
        ),
    }


def read_context(
    project_root: Path,
    track_id: str,
    include: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Consolidate spec.md, plan.md, and metadata.json into a single JSON response.

    Replaces 3–5 individual file reads with one call, reducing token overhead
    for context loading at the start of each track session.

    Args:
        project_root: Project root directory
        track_id: Track identifier
        include: Comma-separated list of sections to include: spec,plan,metadata
                 (default: all three)

    Returns:
        JSON with requested track context sections
    """
    resolver = FileResolver(project_root)
    json_mgr = JsonManager(project_root)

    include_set = {"spec", "plan", "metadata"}
    if include:
        include_set = {i.strip().lower() for i in include.split(",")}

    data: Dict[str, Any] = {"track_id": track_id}
    loaded: List[str] = []

    if "spec" in include_set:
        spec_file = resolver.resolve_track_file(track_id, "specification")
        if spec_file:
            data["spec"] = spec_file.read_text()
            loaded.append("spec")
        else:
            data["spec"] = None

    if "plan" in include_set:
        plan_file = resolver.resolve_track_file(track_id, "implementation_plan")
        if plan_file:
            plan_content = plan_file.read_text()
            data["plan"] = {
                "raw": plan_content,
                "parsed": parse_plan_content(plan_content),
            }
            loaded.append("plan")
        else:
            data["plan"] = None

    if "metadata" in include_set:
        metadata = json_mgr.read_track_metadata(track_id)
        data["metadata"] = metadata
        if metadata:
            loaded.append("metadata")

    return {
        "success": True,
        "data": data,
        "message": f"Context loaded for track '{track_id}': {', '.join(loaded)}",
    }


def _format_parse_plan(phases: List[Dict], summary: Dict) -> str:
    """Format parse-plan output for human-readable display."""
    lines = [
        f"Plan: {summary['total']} tasks "
        f"({summary['completed']} done, "
        f"{summary['in_progress']} in-progress, "
        f"{summary['pending']} pending)",
        "",
    ]
    for phase in phases:
        done = sum(1 for t in phase["tasks"] if t["status"] == "completed")
        total = len(phase["tasks"])
        lines.append(f"  Phase {phase['index']}: {phase['name']} [{done}/{total}]")
        for task in phase["tasks"]:
            symbol = {"completed": "x", "in_progress": "~", "pending": " "}.get(
                task["status"], " "
            )
            lines.append(f"    [{symbol}] {task['content'][:60]}")
    return "\n".join(lines)
