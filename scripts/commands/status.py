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
Status command - 85% scriptable.

Shows project status including setup verification, tracks, and progress metrics.
LLM only needed for narrative summary interpretation.
"""

from pathlib import Path
from typing import Dict, Any, List
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager
from lib.tracks_parser import TracksParser, TaskStatus
from lib.git_ops import GitOps
from lib.formatters import Formatters


def handle(args) -> Dict[str, Any]:
    """Handle status subcommands."""
    project_root = args.project_root

    if args.subcommand == 'verify':
        return verify_setup(project_root)
    elif args.subcommand == 'tracks':
        return parse_tracks(project_root)
    elif args.subcommand == 'progress':
        return calculate_progress(project_root)
    elif args.subcommand == 'full' or args.subcommand is None:
        return full_status(project_root)
    else:
        return full_status(project_root)


def verify_setup(project_root: Path) -> Dict[str, Any]:
    """
    Verify that conductor is properly set up.

    Checks for required files and directories.
    Returns structured data about what exists and what's missing.
    """
    resolver = FileResolver(project_root)

    # Required files
    required_files = {
        'product_definition': 'conductor/product.md',
        'tech_stack': 'conductor/tech-stack.md',
        'workflow': 'conductor/workflow.md',
        'tracks_registry': 'conductor/tracks.md',
    }

    # Optional files
    optional_files = {
        'product_guidelines': 'conductor/product-guidelines.md',
        'settings': 'conductor/settings.json',
        'setup_state': 'conductor/setup_state.json',
    }

    # Required directories
    required_dirs = {
        'tracks_directory': 'conductor/tracks',
    }

    # Check each
    results = {
        'required': {},
        'optional': {},
        'directories': {}
    }

    missing_required = []

    for key, path in required_files.items():
        exists = resolver.exists(key)
        results['required'][key] = {
            'path': path,
            'exists': exists
        }
        if not exists:
            missing_required.append(key)

    for key, path in optional_files.items():
        exists = resolver.exists(key)
        results['optional'][key] = {
            'path': path,
            'exists': exists
        }

    for key, path in required_dirs.items():
        full_path = project_root / path
        exists = full_path.exists() and full_path.is_dir()
        results['directories'][key] = {
            'path': path,
            'exists': exists
        }
        if not exists:
            missing_required.append(key)

    # Determine overall status
    is_valid = len(missing_required) == 0
    setup_complete = is_valid

    # Check setup state
    json_mgr = JsonManager(project_root)
    setup_state = json_mgr.read_setup_state()
    last_step = setup_state.get('last_successful_step')

    return {
        'success': True,
        'data': {
            'is_valid': is_valid,
            'setup_complete': setup_complete,
            'last_setup_step': last_step,
            'missing_required': missing_required,
            'checks': results
        },
        'message': format_verification(is_valid, missing_required, results)
    }


def parse_tracks(project_root: Path) -> Dict[str, Any]:
    """
    Parse all tracks from tracks.md.

    Returns structured data about each track with status.
    """
    resolver = FileResolver(project_root)
    parser = TracksParser(project_root)
    json_mgr = JsonManager(project_root)

    # Read tracks registry
    tracks_file = resolver.resolve_project_file('tracks_registry')
    if not tracks_file:
        return {
            'success': False,
            'error': 'Tracks registry (conductor/tracks.md) not found'
        }

    tracks = parser.parse_tracks_registry()

    # Enrich with metadata
    enriched_tracks = []
    for track in tracks:
        track_data = {
            'description': track.description,
            'status': track.status.value,
            'path': track.path
        }

        # Extract track ID and get metadata
        if track.path:
            track_id = parser.extract_track_id_from_path(track.path)
            if track_id:
                track_data['track_id'] = track_id

                # Read metadata
                metadata = json_mgr.read_track_metadata(track_id)
                if metadata:
                    track_data['type'] = metadata.get('type')
                    track_data['created_at'] = metadata.get('created_at')
                    track_data['updated_at'] = metadata.get('updated_at')

                # Check for plan and calculate task progress
                plan_file = resolver.resolve_track_file(track_id, 'implementation_plan')
                if plan_file:
                    plan_content = plan_file.read_text()
                    task_counts = parser.count_status_markers(plan_content)
                    track_data['tasks'] = task_counts

        enriched_tracks.append(track_data)

    # Summary by status
    summary = {
        'total': len(enriched_tracks),
        'completed': sum(1 for t in enriched_tracks if t['status'] == 'completed'),
        'in_progress': sum(1 for t in enriched_tracks if t['status'] == 'in_progress'),
        'pending': sum(1 for t in enriched_tracks if t['status'] == 'pending')
    }

    return {
        'success': True,
        'data': {
            'tracks': enriched_tracks,
            'summary': summary
        },
        'message': format_tracks_list(enriched_tracks, summary)
    }


def calculate_progress(project_root: Path) -> Dict[str, Any]:
    """
    Calculate overall project progress metrics.

    Aggregates task counts across all tracks.
    """
    resolver = FileResolver(project_root)
    parser = TracksParser(project_root)

    # Get all track directories
    tracks_dir = resolver.resolve_project_file('tracks_directory')
    if not tracks_dir or not tracks_dir.exists():
        return {
            'success': False,
            'error': 'Tracks directory not found'
        }

    total_tasks = 0
    completed_tasks = 0
    in_progress_tasks = 0
    pending_tasks = 0

    track_metrics = []

    for track_dir in tracks_dir.iterdir():
        if not track_dir.is_dir():
            continue

        plan_file = track_dir / 'plan.md'
        if not plan_file.exists():
            continue

        content = plan_file.read_text()
        counts = parser.count_status_markers(content)

        total_tasks += counts['total']
        completed_tasks += counts['completed']
        in_progress_tasks += counts['in_progress']
        pending_tasks += counts['pending']

        track_metrics.append({
            'track_id': track_dir.name,
            'total': counts['total'],
            'completed': counts['completed'],
            'in_progress': counts['in_progress'],
            'pending': counts['pending'],
            'progress_percent': (counts['completed'] / counts['total'] * 100) if counts['total'] > 0 else 0
        })

    overall = {
        'total': total_tasks,
        'completed': completed_tasks,
        'in_progress': in_progress_tasks,
        'pending': pending_tasks,
        'progress_percent': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }

    return {
        'success': True,
        'data': {
            'overall': overall,
            'by_track': track_metrics
        },
        'message': Formatters.metrics_summary(overall)
    }


def full_status(project_root: Path) -> Dict[str, Any]:
    """
    Get full status report combining all checks.

    This is the default operation that provides comprehensive status.
    """
    # Run all checks
    verification = verify_setup(project_root)
    tracks_result = parse_tracks(project_root)
    progress = calculate_progress(project_root)

    # Get git status
    git_ops = GitOps(project_root)
    git_status = git_ops.status() if git_ops.is_repo() else None

    # Combine results
    is_valid = verification.get('data', {}).get('is_valid', False)

    result = {
        'success': True,
        'data': {
            'setup': verification.get('data'),
            'tracks': tracks_result.get('data') if tracks_result.get('success') else None,
            'progress': progress.get('data') if progress.get('success') else None,
            'git': git_status
        }
    }

    # Format human-readable message
    lines = []

    lines.append('═══════════════════════════════════════════════')
    lines.append('             CONDUCTOR STATUS REPORT')
    lines.append('═══════════════════════════════════════════════')
    lines.append('')

    # Setup status
    if is_valid:
        lines.append(Formatters.success('Setup: Valid'))
    else:
        missing = verification.get('data', {}).get('missing_required', [])
        lines.append(Formatters.error(f'Setup: Missing {", ".join(missing)}'))

    lines.append('')

    # Git status
    if git_status:
        lines.append(f"Branch: {git_status.get('branch', '?')}")
        staged = git_status.get('staged', 0)
        modified = git_status.get('modified', 0)
        untracked = git_status.get('untracked', 0)
        if staged or modified or untracked:
            lines.append(f"Changes: {staged} staged, {modified} modified, {untracked} untracked")
        else:
            lines.append("Working tree clean")
    lines.append('')

    # Tracks summary
    if tracks_result.get('success'):
        tracks_data = tracks_result.get('data', {})
        summary = tracks_data.get('summary', {})
        lines.append(f"Tracks: {summary.get('total', 0)} total")
        lines.append(f"  {Formatters.status_symbol('completed')} Completed:   {summary.get('completed', 0)}")
        lines.append(f"  {Formatters.status_symbol('in_progress')} In Progress: {summary.get('in_progress', 0)}")
        lines.append(f"  {Formatters.status_symbol('pending')} Pending:     {summary.get('pending', 0)}")
    lines.append('')

    # Progress
    if progress.get('success'):
        overall = progress.get('data', {}).get('overall', {})
        if overall.get('total', 0) > 0:
            lines.append('Overall Task Progress:')
            lines.append(Formatters.progress_bar(overall.get('completed', 0), overall.get('total', 1)))
            lines.append(f"  {overall.get('completed', 0)}/{overall.get('total', 0)} tasks completed")

    lines.append('')
    lines.append('═══════════════════════════════════════════════')

    result['message'] = '\n'.join(lines)

    return result


def format_verification(is_valid: bool, missing: List[str], checks: Dict) -> str:
    """Format verification results for human output."""
    lines = []

    if is_valid:
        lines.append(Formatters.success('All required files present'))
    else:
        lines.append(Formatters.error(f'Missing required: {", ".join(missing)}'))

    lines.append('')
    lines.append('Required files:')
    for key, info in checks.get('required', {}).items():
        symbol = Formatters.status_symbol('completed' if info['exists'] else 'pending')
        lines.append(f"  {symbol} {info['path']}")

    lines.append('')
    lines.append('Optional files:')
    for key, info in checks.get('optional', {}).items():
        symbol = Formatters.status_symbol('completed' if info['exists'] else 'pending')
        lines.append(f"  {symbol} {info['path']}")

    return '\n'.join(lines)


def format_tracks_list(tracks: List[Dict], summary: Dict) -> str:
    """Format tracks list for human output."""
    lines = []

    lines.append(f"Total tracks: {summary['total']}")
    lines.append('')

    if tracks:
        for track in tracks:
            status = track.get('status', 'pending')
            symbol = Formatters.status_symbol(status)
            desc = Formatters.truncate(track.get('description', ''), 50)
            lines.append(f"  {symbol} {desc}")

            # Show task progress if available
            tasks = track.get('tasks')
            if tasks and tasks.get('total', 0) > 0:
                progress = Formatters.progress_bar(tasks['completed'], tasks['total'], width=15)
                lines.append(f"      {progress}")
    else:
        lines.append('  (no tracks)')

    return '\n'.join(lines)
