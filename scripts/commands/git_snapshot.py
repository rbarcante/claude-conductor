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
Git Snapshot command — consolidates 6-8 git commands into a single structured JSON response.

Replaces individual calls for branch detection, status, diff stats, changed files,
and diff content with one CLI invocation.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.git_ops import GitOps


def handle(args: argparse.Namespace) -> Dict[str, Any]:
    """Handle git-snapshot subcommand."""
    project_root = args.project_root
    exclude = getattr(args, "exclude", None) or []
    diff_stat_only = getattr(args, "diff_stat_only", False)
    return git_snapshot(project_root, exclude, diff_stat_only)


def git_snapshot(
    project_root: Path,
    exclude: Optional[List[str]] = None,
    diff_stat_only: bool = False,
) -> Dict[str, Any]:
    """
    Consolidate git state into a single structured JSON response.

    Args:
        project_root: Project root directory
        exclude: Path patterns to exclude from diff content and changed files list
        diff_stat_only: If True, skip full diff content (faster for stat-only queries)

    Returns:
        JSON with current_branch, base_branch, uncommitted_changes, diff_stats,
        changed_files, and optionally diff_content
    """
    git = GitOps(project_root)
    exclude = exclude or []

    if not git.is_repo():
        return {"success": False, "error": "Not a git repository"}

    current_branch = git.get_current_branch() or "HEAD"
    base_branch = detect_base_branch(project_root)
    uncommitted = _get_uncommitted_summary(git)
    diff_stats = _get_diff_stats(project_root, base_branch)
    changed_files = _get_changed_files(project_root, base_branch, exclude)

    data: Dict[str, Any] = {
        "current_branch": current_branch,
        "base_branch": base_branch,
        "uncommitted_changes": uncommitted,
        "diff_stats": diff_stats,
        "changed_files": changed_files,
    }

    if not diff_stat_only:
        data["diff_content"] = _get_filtered_diff(project_root, base_branch, exclude)

    return {
        "success": True,
        "data": data,
        "message": _format_snapshot(data),
    }


def detect_base_branch(project_root: Path) -> str:
    """
    Auto-detect base branch via reflog, remote tracking, or default.

    Algorithm:
    1. Check git reflog for 'branch: Created from' entry
    2. Check git reflog for 'checkout: moving from X to <current-branch>'
       (catches branches created with 'git checkout -b' or switched into)
    3. Check remote tracking refs on HEAD
    4. Try common default branches (master, main, develop)
    5. Default to 'master'
    """

    # Get current branch name for checkout-pattern matching
    current_branch: Optional[str] = None
    cb_out = _run_git(project_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if cb_out is not None:
        current_branch = cb_out.strip()

    stdout = _run_git(project_root, ["reflog", "show", "HEAD"])
    if stdout is not None:
        for line in stdout.splitlines():
            # Pattern 1a: explicit branch creation — "branch: Created from X"
            if "branch: Created from" in line:
                m = re.search(r"Created from (?:refs/heads/|origin/)?(.+)$", line)
                if m:
                    branch = m.group(1).strip()
                    if _valid_branch(branch) and _branch_exists_remote(
                        project_root, branch
                    ):
                        return branch

            # Pattern 1b: checkout to this branch — "checkout: moving from X to <current>"
            if (
                current_branch
                and "moving from" in line
                and f"to {current_branch}" in line
            ):
                m = re.search(r"moving from ([^\s]+) to ", line)
                if m:
                    branch = m.group(1).strip()
                    # Strip refs/heads/ prefix if present
                    branch = re.sub(r"^refs/heads/", "", branch)
                    if _valid_branch(branch) and _branch_exists_remote(
                        project_root, branch
                    ):
                        return branch

    # Step 2 (legacy): remote tracking refs on HEAD
    stdout = _run_git(project_root, ["log", "-1", "--format=%D", "HEAD"])
    if stdout is not None:
        for ref in stdout.split(","):
            ref = ref.strip()
            if ref.startswith("origin/") and not ref.startswith("origin/HEAD"):
                branch = ref[7:]
                if _valid_branch(branch) and _branch_exists_remote(
                    project_root, branch
                ):
                    return branch

    # Step 3: try common defaults
    for candidate in ("master", "main", "develop"):
        if (
            _run_git(project_root, ["rev-parse", "--verify", f"origin/{candidate}"])
            is not None
        ):
            return candidate

    return "master"


def _valid_branch(branch: str) -> bool:
    """Check that branch name only contains safe characters."""
    return bool(re.match(r"^[a-zA-Z0-9._/-]+$", branch))


def _branch_exists_remote(project_root: Path, branch: str) -> bool:
    """Check if a branch exists on the remote."""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"origin/{branch}"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _run_git(project_root: Path, args: List[str]) -> Optional[str]:
    """Run a git command and return stdout, or None on failure."""
    result = subprocess.run(
        ["git"] + args, cwd=project_root, capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout
    return None


def _get_uncommitted_summary(git: GitOps) -> Dict[str, Any]:
    """Get count of staged, modified, and untracked files."""
    status = git.status()
    staged = status.get("staged", 0)
    modified = status.get("modified", 0)
    untracked = status.get("untracked", 0)
    return {
        "staged": staged,
        "modified": modified,
        "untracked": untracked,
        "has_changes": staged > 0 or modified > 0 or untracked > 0,
    }


def _get_diff_stats(project_root: Path, base_branch: str) -> Dict[str, int]:
    """Get diff statistics between current branch and base (tries origin/ first)."""
    for ref in (f"origin/{base_branch}...HEAD", f"{base_branch}...HEAD"):
        out = _run_git(project_root, ["diff", "--stat", ref])
        if out is not None:
            fc = re.search(r"(\d+) files? changed", out)
            ins = re.search(r"(\d+) insertions?\(\+\)", out)
            dels = re.search(r"(\d+) deletions?\(-\)", out)
            return {
                "files_changed": int(fc.group(1)) if fc else 0,
                "lines_added": int(ins.group(1)) if ins else 0,
                "lines_removed": int(dels.group(1)) if dels else 0,
            }
    return {"files_changed": 0, "lines_added": 0, "lines_removed": 0}


def _get_changed_files(
    project_root: Path, base_branch: str, exclude: List[str]
) -> List[str]:
    """Get list of changed files, filtered by exclude patterns."""
    for ref in (f"origin/{base_branch}...HEAD", f"{base_branch}...HEAD"):
        out = _run_git(project_root, ["diff", "--name-only", ref])
        if out is not None:
            files = [f for f in out.strip().split("\n") if f]
            return filter_paths(files, exclude)
    return []


def _get_filtered_diff(project_root: Path, base_branch: str, exclude: List[str]) -> str:
    """
    Get diff content between current branch and base, with path filtering.

    Includes untracked files as new-file diff entries so the full working-tree
    state is visible, not just committed changes.
    """
    committed_diff = ""
    for ref in (f"origin/{base_branch}...HEAD", f"{base_branch}...HEAD"):
        out = _run_git(project_root, ["diff", ref])
        if out is not None:
            committed_diff = filter_diff_content(out, exclude) if exclude else out
            break

    untracked_diff = _generate_untracked_diff(project_root, exclude)

    return committed_diff + untracked_diff


def _generate_untracked_diff(project_root: Path, exclude: List[str]) -> str:
    """
    Generate unified-diff entries for untracked files.

    Untracked files are not shown by `git diff`, so we read them directly
    and format them as new-file diff hunks for completeness.

    Args:
        project_root: Project root directory
        exclude: Path patterns to exclude

    Returns:
        Unified diff string with one new-file entry per untracked file
    """
    out = _run_git(project_root, ["ls-files", "--others", "--exclude-standard"])
    if not out:
        return ""

    untracked = [f for f in out.strip().split("\n") if f]
    untracked = filter_paths(untracked, exclude)

    if not untracked:
        return ""

    parts: List[str] = []
    for filepath in untracked:
        full_path = project_root / filepath
        if not full_path.is_file():
            continue
        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        file_lines = content.splitlines()
        n = len(file_lines)
        hunk_lines = "\n".join(f"+{line}" for line in file_lines)

        parts.append(
            f"diff --git a/{filepath} b/{filepath}\n"
            f"new file mode 100644\n"
            f"--- /dev/null\n"
            f"+++ b/{filepath}\n"
            f"@@ -0,0 +1,{n} @@\n"
            f"{hunk_lines}\n"
        )

    return "\n".join(parts)


def filter_diff_content(diff: str, exclude: List[str]) -> str:
    """
    Filter diff content to remove hunks for excluded paths.

    Args:
        diff: Full git diff output
        exclude: Path patterns to exclude (substring match)

    Returns:
        Filtered diff content
    """
    if not exclude:
        return diff

    lines = diff.split("\n")
    result = []
    skip = False

    for line in lines:
        if line.startswith("diff --git"):
            skip = any(pattern in line for pattern in exclude)
        if not skip:
            result.append(line)

    return "\n".join(result)


def filter_paths(paths: List[str], exclude: List[str]) -> List[str]:
    """Filter file paths by exclude patterns (substring match)."""
    if not exclude:
        return paths
    return [p for p in paths if not any(pattern in p for pattern in exclude)]


def _format_snapshot(data: Dict[str, Any]) -> str:
    """Format git snapshot for human-readable output."""
    stats = data["diff_stats"]
    lines = [
        "Git Snapshot:",
        f"  Current branch: {data['current_branch']}",
        f"  Base branch:    {data['base_branch']}",
        f"  Files changed:  {stats['files_changed']}",
        f"  Lines added:    +{stats['lines_added']}",
        f"  Lines removed:  -{stats['lines_removed']}",
        f"  Changed files:  {len(data['changed_files'])}",
    ]
    uc = data.get("uncommitted_changes", {})
    if uc.get("has_changes"):
        lines += [
            "",
            "  Uncommitted:",
            f"    Staged:    {uc['staged']}",
            f"    Modified:  {uc['modified']}",
            f"    Untracked: {uc['untracked']}",
        ]
    return "\n".join(lines)
