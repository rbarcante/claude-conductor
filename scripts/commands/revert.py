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
Revert command - 50% scriptable.

Provides git revert operations for tracks, including commit discovery,
plan update detection, and revert execution.
LLM needed for conflict resolution and revert strategy decisions.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.git_ops import GitOps, Commit
from lib.tracks_parser import TracksParser, TaskStatus
from lib.file_resolver import FileResolver
from lib.formatters import Formatters


def handle(args) -> Dict[str, Any]:
    """Handle revert subcommands."""
    project_root = args.project_root

    if args.subcommand == 'find-commits':
        return find_commits(project_root, args.track_id)
    elif args.subcommand == 'plan-updates':
        return plan_updates(project_root, args.sha)
    elif args.subcommand == 'build-list':
        return build_list(project_root, args.target)
    elif args.subcommand == 'execute':
        dry_run = getattr(args, 'dry_run', False)
        return execute(project_root, args.shas, dry_run)
    elif args.subcommand == 'parse-registry':
        return parse_registry(project_root)
    else:
        return {
            'success': False,
            'error': 'No subcommand specified. Use: find-commits, plan-updates, build-list, execute, parse-registry'
        }


def find_commits(project_root: Path, track_id: str) -> Dict[str, Any]:
    """
    Find all commits related to a track.

    Uses GitOps.find_commits_for_track to search by:
    - Commit messages mentioning the track ID
    - Files changed in the track's directory

    Args:
        project_root: Project root path
        track_id: Track identifier

    Returns:
        JSON with commits list and metadata
    """
    git_ops = GitOps(project_root)
    resolver = FileResolver(project_root)

    # Verify git repo
    if not git_ops.is_repo():
        return {
            'success': False,
            'error': 'Not a git repository'
        }

    # Verify track exists
    if not resolver.track_exists(track_id):
        return {
            'success': False,
            'error': f"Track '{track_id}' not found"
        }

    # Find commits
    commits = git_ops.find_commits_for_track(track_id)

    # Format for output
    commit_data = []
    for commit in commits:
        # Check for merge commits
        is_merge = git_ops.is_merge_commit(commit.sha)

        # Get files changed in commit
        files = git_ops.get_files_in_commit(commit.sha)

        # Check if this commit modified plan.md
        has_plan_update = any(f.endswith('plan.md') for f in files)

        commit_data.append({
            'sha': commit.sha,
            'short_sha': commit.short_sha,
            'message': Formatters.truncate(commit.message, 60),
            'author': commit.author,
            'date': commit.date,
            'is_merge': is_merge,
            'has_plan_update': has_plan_update,
            'files_count': len(files)
        })

    return {
        'success': True,
        'data': {
            'track_id': track_id,
            'commits': commit_data,
            'total': len(commit_data)
        },
        'message': format_commits_list(commit_data, track_id)
    }


def plan_updates(project_root: Path, sha: str) -> Dict[str, Any]:
    """
    Find plan file updates in a specific commit.

    Args:
        project_root: Project root path
        sha: Commit SHA

    Returns:
        JSON with list of plan.md files changed
    """
    git_ops = GitOps(project_root)

    # Verify git repo
    if not git_ops.is_repo():
        return {
            'success': False,
            'error': 'Not a git repository'
        }

    # Find plan updates
    plan_files = git_ops.find_plan_updates(sha)

    # Get commit info for context
    commits = git_ops.log(n=1)
    commit_info = None

    # Try to get specific commit info
    code, stdout, _ = git_ops._run(['show', '-s', '--format=%H|%h|%s|%an|%ai', sha])
    if code == 0 and stdout.strip():
        parts = stdout.strip().split('|')
        if len(parts) >= 5:
            commit_info = {
                'sha': parts[0],
                'short_sha': parts[1],
                'message': parts[2],
                'author': parts[3],
                'date': parts[4]
            }

    return {
        'success': True,
        'data': {
            'sha': sha,
            'plan_files': plan_files,
            'count': len(plan_files),
            'commit': commit_info
        },
        'message': format_plan_updates(plan_files, sha)
    }


def build_list(project_root: Path, target: str) -> Dict[str, Any]:
    """
    Build a reverse chronological list of SHAs to revert.

    Target can be:
    - track_id: All commits for a track
    - sha: Single commit
    - sha1..sha2: Range of commits

    Args:
        project_root: Project root path
        target: Target specification

    Returns:
        JSON with ordered list of SHAs to revert (newest first)
    """
    git_ops = GitOps(project_root)
    resolver = FileResolver(project_root)

    if not git_ops.is_repo():
        return {
            'success': False,
            'error': 'Not a git repository'
        }

    shas_to_revert = []
    target_type = 'unknown'

    # Check if target is a SHA range
    if '..' in target:
        target_type = 'range'
        start, end = target.split('..', 1)

        # Get commits in range
        code, stdout, _ = git_ops._run([
            'log', '--format=%H', '--reverse',
            f'{start}..{end}'
        ])

        if code == 0 and stdout.strip():
            # Reverse to get newest first
            shas_to_revert = list(reversed(stdout.strip().split('\n')))

    # Check if target is a single SHA (looks like hex)
    elif all(c in '0123456789abcdef' for c in target.lower()) and len(target) >= 7:
        target_type = 'single'
        # Verify SHA exists
        full_sha = git_ops.get_commit_sha(target)
        if full_sha:
            shas_to_revert = [full_sha]
        else:
            return {
                'success': False,
                'error': f"Commit '{target}' not found"
            }

    # Otherwise treat as track_id
    else:
        target_type = 'track'
        if not resolver.track_exists(target):
            return {
                'success': False,
                'error': f"Track '{target}' not found"
            }

        commits = git_ops.find_commits_for_track(target)
        # Already in reverse chronological order (newest first)
        shas_to_revert = [c.sha for c in commits]

    # Filter out merge commits (cannot be easily reverted)
    filtered_shas = []
    merge_commits = []

    for sha in shas_to_revert:
        if git_ops.is_merge_commit(sha):
            merge_commits.append(sha[:7])
        else:
            filtered_shas.append(sha)

    # Get commit info for each SHA
    commit_info = []
    for sha in filtered_shas:
        code, stdout, _ = git_ops._run(['show', '-s', '--format=%H|%h|%s', sha])
        if code == 0 and stdout.strip():
            parts = stdout.strip().split('|')
            if len(parts) >= 3:
                commit_info.append({
                    'sha': parts[0],
                    'short_sha': parts[1],
                    'message': Formatters.truncate(parts[2], 50)
                })

    return {
        'success': True,
        'data': {
            'target': target,
            'target_type': target_type,
            'shas': filtered_shas,
            'commits': commit_info,
            'count': len(filtered_shas),
            'skipped_merges': merge_commits
        },
        'message': format_revert_list(commit_info, merge_commits, target)
    }


def execute(project_root: Path, shas: List[str], dry_run: bool = False) -> Dict[str, Any]:
    """
    Execute git revert sequence.

    Reverts commits in the order provided (should be newest first).

    Args:
        project_root: Project root path
        shas: List of commit SHAs to revert
        dry_run: If True, only show what would be done

    Returns:
        JSON with execution results
    """
    git_ops = GitOps(project_root)

    if not git_ops.is_repo():
        return {
            'success': False,
            'error': 'Not a git repository'
        }

    if not shas:
        return {
            'success': False,
            'error': 'No SHAs provided'
        }

    # Validate all SHAs first
    validated_shas = []
    for sha in shas:
        full_sha = git_ops.get_commit_sha(sha)
        if not full_sha:
            return {
                'success': False,
                'error': f"Commit '{sha}' not found"
            }
        if git_ops.is_merge_commit(full_sha):
            return {
                'success': False,
                'error': f"Cannot revert merge commit '{sha[:7]}'. Use manual revert with -m flag."
            }
        validated_shas.append(full_sha)

    results = []

    if dry_run:
        # Just show what would be done
        for sha in validated_shas:
            code, stdout, _ = git_ops._run(['show', '-s', '--format=%h %s', sha])
            message = stdout.strip() if code == 0 else sha[:7]
            results.append({
                'sha': sha,
                'short_sha': sha[:7],
                'action': 'would_revert',
                'message': message
            })

        return {
            'success': True,
            'data': {
                'dry_run': True,
                'results': results,
                'count': len(results)
            },
            'message': format_dry_run_results(results)
        }

    # Execute reverts
    for sha in validated_shas:
        success, output = git_ops.revert(sha, no_commit=False)

        code, stdout, _ = git_ops._run(['show', '-s', '--format=%h %s', sha])
        message = stdout.strip() if code == 0 else sha[:7]

        if success:
            results.append({
                'sha': sha,
                'short_sha': sha[:7],
                'action': 'reverted',
                'message': message,
                'success': True
            })
        else:
            results.append({
                'sha': sha,
                'short_sha': sha[:7],
                'action': 'failed',
                'message': message,
                'success': False,
                'error': output
            })
            # Stop on first failure
            break

    all_success = all(r['success'] for r in results)

    return {
        'success': all_success,
        'data': {
            'dry_run': False,
            'results': results,
            'count': len(results),
            'successful': sum(1 for r in results if r['success']),
            'failed': sum(1 for r in results if not r['success'])
        },
        'message': format_execute_results(results),
        'error': None if all_success else 'One or more reverts failed'
    }


def parse_registry(project_root: Path) -> Dict[str, Any]:
    """
    Parse tracks registry for guided menu display.

    Returns tracks sorted with in-progress items first, then pending.
    Completed tracks are listed last.

    Args:
        project_root: Project root path

    Returns:
        JSON with tracks organized for menu display
    """
    parser = TracksParser(project_root)
    resolver = FileResolver(project_root)

    # Read tracks registry
    tracks_file = resolver.resolve_project_file('tracks_registry')
    if not tracks_file:
        return {
            'success': False,
            'error': 'Tracks registry (conductor/tracks.md) not found'
        }

    tracks = parser.parse_tracks_registry()

    # Organize by status
    in_progress = []
    pending = []
    completed = []

    for track in tracks:
        track_data = {
            'description': track.description,
            'status': track.status.value,
            'path': track.path
        }

        # Extract track ID
        if track.path:
            track_id = parser.extract_track_id_from_path(track.path)
            if track_id:
                track_data['track_id'] = track_id

                # Get task metrics if plan exists
                plan_file = resolver.resolve_track_file(track_id, 'implementation_plan')
                if plan_file:
                    content = plan_file.read_text()
                    counts = parser.count_status_markers(content)
                    track_data['tasks'] = counts

        if track.status == TaskStatus.IN_PROGRESS:
            in_progress.append(track_data)
        elif track.status == TaskStatus.PENDING:
            pending.append(track_data)
        else:
            completed.append(track_data)

    # Combine with priority order
    all_tracks = in_progress + pending + completed

    return {
        'success': True,
        'data': {
            'tracks': all_tracks,
            'by_status': {
                'in_progress': in_progress,
                'pending': pending,
                'completed': completed
            },
            'summary': {
                'total': len(all_tracks),
                'in_progress': len(in_progress),
                'pending': len(pending),
                'completed': len(completed)
            }
        },
        'message': format_registry_menu(in_progress, pending, completed)
    }


# Formatting helpers

def format_commits_list(commits: List[Dict], track_id: str) -> str:
    """Format commits list for human output."""
    if not commits:
        return f'No commits found for track: {track_id}'

    lines = [
        f'Commits for track: {track_id}',
        f'Total: {len(commits)}',
        ''
    ]

    for commit in commits:
        flags = []
        if commit['is_merge']:
            flags.append('merge')
        if commit['has_plan_update']:
            flags.append('plan')

        flags_str = f" [{', '.join(flags)}]" if flags else ''

        lines.append(f"  {commit['short_sha']} {commit['message']}{flags_str}")
        lines.append(f"           {commit['author']} - {commit['date'][:10]}")

    return '\n'.join(lines)


def format_plan_updates(plan_files: List[str], sha: str) -> str:
    """Format plan updates for human output."""
    if not plan_files:
        return f'No plan.md files changed in commit {sha[:7]}'

    lines = [
        f'Plan files changed in {sha[:7]}:',
        ''
    ]

    for path in plan_files:
        lines.append(f'  - {path}')

    return '\n'.join(lines)


def format_revert_list(commits: List[Dict], skipped: List[str], target: str) -> str:
    """Format revert list for human output."""
    lines = [
        f'Revert plan for: {target}',
        ''
    ]

    if commits:
        lines.append(f'Commits to revert ({len(commits)}):')
        for i, commit in enumerate(commits, 1):
            lines.append(f"  {i}. {commit['short_sha']} {commit['message']}")
    else:
        lines.append('No commits to revert')

    if skipped:
        lines.append('')
        lines.append(f'Skipped merge commits ({len(skipped)}):')
        for sha in skipped:
            lines.append(f'  - {sha} (cannot auto-revert)')

    return '\n'.join(lines)


def format_dry_run_results(results: List[Dict]) -> str:
    """Format dry run results for human output."""
    lines = [
        'Dry run - would perform the following reverts:',
        ''
    ]

    for i, result in enumerate(results, 1):
        lines.append(f"  {i}. Revert {result['message']}")

    return '\n'.join(lines)


def format_execute_results(results: List[Dict]) -> str:
    """Format execution results for human output."""
    lines = ['Revert results:', '']

    for result in results:
        if result['success']:
            symbol = Formatters.status_symbol('completed')
            lines.append(f"  {symbol} Reverted {result['message']}")
        else:
            symbol = Formatters.status_symbol('error')
            lines.append(f"  {symbol} Failed: {result['message']}")
            if 'error' in result:
                lines.append(f"        {result['error'][:60]}")

    return '\n'.join(lines)


def format_registry_menu(in_progress: List[Dict], pending: List[Dict], completed: List[Dict]) -> str:
    """Format registry for menu display."""
    lines = ['Tracks Registry:', '']

    if in_progress:
        lines.append(f"{Formatters.status_symbol('in_progress')} In Progress:")
        for track in in_progress:
            track_id = track.get('track_id', '?')
            desc = Formatters.truncate(track['description'], 40)
            lines.append(f"    [{track_id}] {desc}")
        lines.append('')

    if pending:
        lines.append(f"{Formatters.status_symbol('pending')} Pending:")
        for track in pending:
            track_id = track.get('track_id', '?')
            desc = Formatters.truncate(track['description'], 40)
            lines.append(f"    [{track_id}] {desc}")
        lines.append('')

    if completed:
        lines.append(f"{Formatters.status_symbol('completed')} Completed ({len(completed)} tracks)")

    return '\n'.join(lines)
