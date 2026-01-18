"""
Git operations wrapper for Conductor CLI.

Provides safe git command execution and output parsing.
"""

import subprocess
import re
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class Commit:
    """Represents a git commit."""
    sha: str
    short_sha: str
    message: str
    author: str
    date: str
    files_changed: List[str] = None

    def __post_init__(self):
        if self.files_changed is None:
            self.files_changed = []


class GitOps:
    """Git command wrapper with parsing utilities."""

    def __init__(self, project_root: Path):
        """Initialize with project root."""
        self.project_root = Path(project_root).resolve()

    def _run(self, args: List[str], capture: bool = True) -> Tuple[int, str, str]:
        """
        Run a git command.

        Args:
            args: Git command arguments (without 'git' prefix)
            capture: Whether to capture output

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.project_root,
                capture_output=capture,
                text=True
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return 1, '', 'git not found'

    def is_repo(self) -> bool:
        """Check if project root is a git repository."""
        code, _, _ = self._run(['rev-parse', '--git-dir'])
        return code == 0

    def get_current_branch(self) -> Optional[str]:
        """Get current branch name."""
        code, stdout, _ = self._run(['rev-parse', '--abbrev-ref', 'HEAD'])
        if code == 0:
            return stdout.strip()
        return None

    def get_modified_files(self, staged: bool = False) -> List[str]:
        """
        Get list of modified files.

        Args:
            staged: If True, only return staged files

        Returns:
            List of file paths
        """
        if staged:
            args = ['diff', '--cached', '--name-only']
        else:
            args = ['diff', '--name-only', 'HEAD']

        code, stdout, _ = self._run(args)
        if code == 0:
            return [f for f in stdout.strip().split('\n') if f]
        return []

    def get_untracked_files(self) -> List[str]:
        """Get list of untracked files."""
        code, stdout, _ = self._run(['ls-files', '--others', '--exclude-standard'])
        if code == 0:
            return [f for f in stdout.strip().split('\n') if f]
        return []

    def log(
        self,
        n: int = 10,
        path: Optional[str] = None,
        grep: Optional[str] = None,
        format_str: str = '%H|%h|%s|%an|%ai'
    ) -> List[Commit]:
        """
        Get commit log.

        Args:
            n: Number of commits
            path: Optional path filter
            grep: Optional message grep pattern
            format_str: Git format string

        Returns:
            List of Commit objects
        """
        args = ['log', f'-n{n}', f'--format={format_str}']

        if grep:
            args.append(f'--grep={grep}')

        if path:
            args.extend(['--', path])

        code, stdout, _ = self._run(args)
        if code != 0:
            return []

        commits = []
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 5:
                commits.append(Commit(
                    sha=parts[0],
                    short_sha=parts[1],
                    message=parts[2],
                    author=parts[3],
                    date=parts[4]
                ))

        return commits

    def find_commits_for_track(self, track_id: str) -> List[Commit]:
        """
        Find all commits related to a track.

        Searches for commits that mention the track ID or modify track files.

        Args:
            track_id: Track identifier

        Returns:
            List of related commits
        """
        # Find commits by message
        message_commits = self.log(n=100, grep=track_id)

        # Find commits by path
        track_path = f'conductor/tracks/{track_id}'
        path_commits = self.log(n=100, path=track_path)

        # Merge and deduplicate
        seen = set()
        all_commits = []

        for commit in message_commits + path_commits:
            if commit.sha not in seen:
                seen.add(commit.sha)
                all_commits.append(commit)

        return all_commits

    def find_plan_updates(self, sha: str) -> List[str]:
        """
        Find plan file changes in a commit.

        Args:
            sha: Commit SHA

        Returns:
            List of plan.md file paths changed
        """
        code, stdout, _ = self._run(['show', '--name-only', '--format=', sha])
        if code != 0:
            return []

        return [f for f in stdout.strip().split('\n') if f.endswith('plan.md')]

    def get_files_in_commit(self, sha: str) -> List[str]:
        """Get list of files changed in a commit."""
        code, stdout, _ = self._run(['show', '--name-only', '--format=', sha])
        if code == 0:
            return [f for f in stdout.strip().split('\n') if f]
        return []

    def is_merge_commit(self, sha: str) -> bool:
        """Check if a commit is a merge commit."""
        code, stdout, _ = self._run(['cat-file', '-p', sha])
        if code != 0:
            return False

        # Merge commits have multiple 'parent' lines
        parent_count = len(re.findall(r'^parent ', stdout, re.MULTILINE))
        return parent_count > 1

    def revert(self, sha: str, no_commit: bool = False) -> Tuple[bool, str]:
        """
        Revert a commit.

        Args:
            sha: Commit SHA to revert
            no_commit: If True, don't commit the revert

        Returns:
            Tuple of (success, message)
        """
        args = ['revert']
        if no_commit:
            args.append('--no-commit')
        args.append(sha)

        code, stdout, stderr = self._run(args)

        if code == 0:
            return True, stdout
        else:
            return False, stderr

    def get_diff_stat(self, sha: str = None) -> Dict[str, Any]:
        """
        Get diff statistics.

        Args:
            sha: Optional commit SHA (default: unstaged changes)

        Returns:
            Dict with 'files_changed', 'insertions', 'deletions'
        """
        if sha:
            args = ['show', '--stat', '--format=', sha]
        else:
            args = ['diff', '--stat']

        code, stdout, _ = self._run(args)
        if code != 0:
            return {'files_changed': 0, 'insertions': 0, 'deletions': 0}

        # Parse the summary line like "5 files changed, 100 insertions(+), 50 deletions(-)"
        match = re.search(r'(\d+) files? changed', stdout)
        files_changed = int(match.group(1)) if match else 0

        match = re.search(r'(\d+) insertions?\(\+\)', stdout)
        insertions = int(match.group(1)) if match else 0

        match = re.search(r'(\d+) deletions?\(-\)', stdout)
        deletions = int(match.group(1)) if match else 0

        return {
            'files_changed': files_changed,
            'insertions': insertions,
            'deletions': deletions
        }

    def status(self) -> Dict[str, Any]:
        """
        Get git status summary.

        Returns:
            Dict with 'branch', 'staged', 'modified', 'untracked' counts
        """
        code, stdout, _ = self._run(['status', '--porcelain', '-b'])
        if code != 0:
            return {}

        lines = stdout.strip().split('\n')

        branch = None
        staged = 0
        modified = 0
        untracked = 0

        for line in lines:
            if line.startswith('## '):
                # Branch line
                match = re.match(r'## (.+?)(?:\.\.\.|$)', line)
                if match:
                    branch = match.group(1)
            elif line.startswith('??'):
                untracked += 1
            elif line[0] != ' ':
                staged += 1
            elif line[1] != ' ':
                modified += 1

        return {
            'branch': branch,
            'staged': staged,
            'modified': modified,
            'untracked': untracked
        }

    def init(self) -> bool:
        """Initialize a new git repository."""
        code, _, _ = self._run(['init'])
        return code == 0

    def add(self, paths: List[str]) -> bool:
        """Stage files for commit."""
        code, _, _ = self._run(['add'] + paths)
        return code == 0

    def commit(self, message: str) -> Tuple[bool, str]:
        """
        Create a commit.

        Args:
            message: Commit message

        Returns:
            Tuple of (success, commit_sha or error)
        """
        code, stdout, stderr = self._run(['commit', '-m', message])
        if code == 0:
            # Extract commit SHA
            match = re.search(r'\[.+ ([a-f0-9]+)\]', stdout)
            sha = match.group(1) if match else ''
            return True, sha
        return False, stderr

    def get_commit_sha(self, ref: str = 'HEAD') -> Optional[str]:
        """Get full SHA for a ref."""
        code, stdout, _ = self._run(['rev-parse', ref])
        if code == 0:
            return stdout.strip()
        return None
