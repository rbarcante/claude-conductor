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
Code review filtered-diff command.

Generates filtered, size-capped git diff with language statistics.
Replaces manual diff generation + file filtering + language detection with one call.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from commands.git_snapshot import (
    detect_base_branch,
    _run_git,
    filter_diff_content,
    filter_paths,
    _generate_untracked_diff,
)

# Language detection map: file extension -> language name
LANGUAGE_MAP = {
    "py": "Python",
    "ts": "TypeScript",
    "tsx": "TypeScript",
    "js": "JavaScript",
    "jsx": "JavaScript",
    "java": "Java",
    "go": "Go",
    "rs": "Rust",
    "rb": "Ruby",
    "php": "PHP",
    "cs": "C#",
    "cpp": "C++",
    "cc": "C++",
    "c": "C",
    "h": "C/C++",
    "hpp": "C++",
    "swift": "Swift",
    "kt": "Kotlin",
    "scala": "Scala",
    "md": "Markdown",
    "yml": "YAML",
    "yaml": "YAML",
    "json": "JSON",
    "toml": "TOML",
    "sh": "Shell",
    "bash": "Shell",
    "html": "HTML",
    "css": "CSS",
    "scss": "SCSS",
    "sass": "SCSS",
    "sql": "SQL",
    "tf": "Terraform",
    "dockerfile": "Docker",
}

DEFAULT_MAX_LINES = 5000
TRUNCATION_INDICATOR = (
    "\n\n... [DIFF TRUNCATED — use --max-lines N to increase limit] ...\n"
)


def handle(args: argparse.Namespace) -> Dict[str, Any]:
    """Handle codereview subcommands."""
    if args.subcommand == "filtered-diff":
        project_root = args.project_root
        exclude = getattr(args, "exclude", None) or []
        max_lines = getattr(args, "max_lines", DEFAULT_MAX_LINES) or DEFAULT_MAX_LINES
        base = getattr(args, "base", None)
        return filtered_diff(project_root, exclude, max_lines, base)
    return {
        "success": False,
        "error": "No subcommand specified. Use: filtered-diff",
    }


def filtered_diff(
    project_root: Path,
    exclude: Optional[List[str]] = None,
    max_lines: int = DEFAULT_MAX_LINES,
    base_branch: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a filtered, size-capped git diff with language statistics.

    Args:
        project_root: Project root directory
        exclude: Path patterns to exclude from the diff
        max_lines: Maximum number of diff lines to include (excess is truncated)
        base_branch: Base branch to diff against (auto-detected if not provided)

    Returns:
        JSON with stats, language_breakdown, file_stats, and diff_content
    """
    exclude = exclude or []
    if base_branch is None:
        base_branch = detect_base_branch(project_root)

    # Get raw diff
    raw_diff = _get_raw_diff(project_root, base_branch)
    if raw_diff is None:
        return {
            "success": False,
            "error": f"Failed to generate diff against '{base_branch}'",
        }

    # Filter excluded paths
    filtered = filter_diff_content(raw_diff, exclude) if exclude else raw_diff

    # Append untracked files as new-file diff entries
    untracked_diff = _generate_untracked_diff(project_root, exclude)
    if untracked_diff:
        filtered = filtered + "\n" + untracked_diff

    # Parse per-file stats (using --numstat for accuracy)
    # Also add untracked files to the stats
    file_stats = _parse_file_stats(project_root, base_branch, exclude)
    file_stats = _add_untracked_file_stats(project_root, exclude, file_stats)

    # Language breakdown
    language_stats = _compute_language_stats(file_stats)

    # Truncate if needed
    truncated = False
    diff_lines = filtered.split("\n")
    if len(diff_lines) > max_lines:
        filtered = "\n".join(diff_lines[:max_lines]) + TRUNCATION_INDICATOR
        truncated = True

    total_added = sum(f["lines_added"] for f in file_stats)
    total_removed = sum(f["lines_removed"] for f in file_stats)

    return {
        "success": True,
        "data": {
            "base_branch": base_branch,
            "stats": {
                "files_changed": len(file_stats),
                "lines_added": total_added,
                "lines_removed": total_removed,
                "truncated": truncated,
                "max_lines": max_lines,
            },
            "language_breakdown": language_stats,
            "file_stats": file_stats,
            "diff_content": filtered,
        },
        "message": _format_filtered_diff(
            base_branch, file_stats, language_stats, truncated
        ),
    }


def _get_raw_diff(project_root: Path, base_branch: str) -> Optional[str]:
    """Get raw diff content (tries origin/ first, then local)."""
    for ref in (f"origin/{base_branch}...HEAD", f"{base_branch}...HEAD"):
        out = _run_git(project_root, ["diff", ref])
        if out is not None:
            return out
    return None


def _parse_file_stats(
    project_root: Path, base_branch: str, exclude: List[str]
) -> List[Dict[str, Any]]:
    """Parse per-file diff statistics using git diff --numstat."""
    for ref in (f"origin/{base_branch}...HEAD", f"{base_branch}...HEAD"):
        out = _run_git(project_root, ["diff", "--numstat", ref])
        if out is None:
            continue

        file_stats = []
        for line in out.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue

            added_str, removed_str, filepath = parts[0], parts[1], parts[2]

            # Skip excluded paths
            if exclude and any(p in filepath for p in exclude):
                continue

            # Binary files show "-" in numstat
            is_binary = added_str == "-"
            added = int(added_str) if not is_binary else 0
            removed = int(removed_str) if not is_binary else 0

            ext = Path(filepath).suffix.lstrip(".").lower()
            language = LANGUAGE_MAP.get(ext, "Other")

            file_stats.append(
                {
                    "file": filepath,
                    "language": language,
                    "lines_added": added,
                    "lines_removed": removed,
                    "is_binary": is_binary,
                }
            )
        return file_stats

    return []


def _add_untracked_file_stats(
    project_root: Path,
    exclude: List[str],
    existing_stats: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Add per-file stats for untracked files to the existing file stats list.

    Args:
        project_root: Project root directory
        exclude: Path patterns to exclude
        existing_stats: Existing file stats from tracked diff

    Returns:
        Combined file stats list including untracked files
    """
    out = _run_git(project_root, ["ls-files", "--others", "--exclude-standard"])
    if not out:
        return existing_stats

    untracked = [f for f in out.strip().split("\n") if f]
    untracked = filter_paths(untracked, exclude)

    already_tracked = {s["file"] for s in existing_stats}
    new_stats = list(existing_stats)

    for filepath in untracked:
        if filepath in already_tracked:
            continue
        full_path = project_root / filepath
        if not full_path.is_file():
            continue
        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            lines_added = len(content.splitlines())
        except OSError:
            lines_added = 0

        ext = Path(filepath).suffix.lstrip(".").lower()
        new_stats.append(
            {
                "file": filepath,
                "language": LANGUAGE_MAP.get(ext, "Other"),
                "lines_added": lines_added,
                "lines_removed": 0,
                "is_binary": False,
                "untracked": True,
            }
        )

    return new_stats


def _compute_language_stats(
    file_stats: List[Dict[str, Any]],
) -> Dict[str, Dict[str, int]]:
    """Aggregate per-file stats into language-level totals."""
    lang_stats: Dict[str, Dict[str, int]] = {}
    for f in file_stats:
        lang = f["language"]
        if lang not in lang_stats:
            lang_stats[lang] = {"files": 0, "lines_added": 0, "lines_removed": 0}
        lang_stats[lang]["files"] += 1
        lang_stats[lang]["lines_added"] += f["lines_added"]
        lang_stats[lang]["lines_removed"] += f["lines_removed"]
    return lang_stats


def _format_filtered_diff(
    base_branch: str,
    file_stats: List[Dict[str, Any]],
    language_stats: Dict[str, Dict[str, int]],
    truncated: bool,
) -> str:
    """Format filtered diff summary for human-readable output."""
    total_added = sum(f["lines_added"] for f in file_stats)
    total_removed = sum(f["lines_removed"] for f in file_stats)
    lines = [
        f"Filtered Diff vs {base_branch}:",
        f"  Files changed: {len(file_stats)}",
        f"  Lines added:   +{total_added}",
        f"  Lines removed: -{total_removed}",
    ]
    if language_stats:
        lines.append("  Languages:")
        for lang, stats in sorted(language_stats.items(), key=lambda x: -x[1]["files"]):
            lines.append(
                f"    {lang}: {stats['files']} files "
                f"(+{stats['lines_added']}/-{stats['lines_removed']})"
            )
    if truncated:
        lines.append("  ⚠ Output truncated (use --max-lines to increase)")
    return "\n".join(lines)
