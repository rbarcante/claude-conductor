"""
Implement command - 35% scriptable.

Provides implementation helpers including track status management,
coverage parsing, pattern matching, and file tracking.
LLM needed for implementation decisions, TDD workflow, and verification.
"""

import os
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.git_ops import GitOps
from lib.tracks_parser import TracksParser, TaskStatus
from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager
from lib.markdown_parser import MarkdownParser
from lib.formatters import Formatters


def handle(args) -> Dict[str, Any]:
    """Handle implement subcommands."""
    project_root = args.project_root
    plugin_root = getattr(args, 'plugin_root', None)

    if args.subcommand == 'parse-tracks':
        return parse_tracks(project_root)
    elif args.subcommand == 'update-status':
        return update_status(project_root, args.track_id, args.status)
    elif args.subcommand == 'archive':
        return archive(project_root, args.track_id)
    elif args.subcommand == 'modified-files':
        return modified_files(project_root)
    elif args.subcommand == 'parse-coverage':
        coverage_format = getattr(args, 'format', 'lcov')
        coverage_path = getattr(args, 'path', None)
        return parse_coverage(project_root, coverage_format, coverage_path)
    elif args.subcommand == 'next-adr-number':
        adr_path = getattr(args, 'path', 'docs/decisions')
        return next_adr_number(project_root, adr_path)
    elif args.subcommand == 'match-patterns':
        return match_patterns(plugin_root or project_root, args.keywords)
    else:
        return {
            'success': False,
            'error': 'No subcommand specified. Use: parse-tracks, update-status, archive, modified-files, parse-coverage, next-adr-number, match-patterns'
        }


def parse_tracks(project_root: Path) -> Dict[str, Any]:
    """
    Parse tracks registry and return structured JSON with status.

    Args:
        project_root: Project root path

    Returns:
        JSON with tracks data including status and progress metrics
    """
    parser = TracksParser(project_root)
    resolver = FileResolver(project_root)
    json_mgr = JsonManager(project_root)

    # Read tracks registry
    tracks_file = resolver.resolve_project_file('tracks_registry')
    if not tracks_file:
        return {
            'success': False,
            'error': 'Tracks registry (conductor/tracks.md) not found'
        }

    tracks = parser.parse_tracks_registry()

    # Enrich with metadata and progress
    enriched_tracks = []
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

                # Read metadata
                metadata = json_mgr.read_track_metadata(track_id)
                if metadata:
                    track_data['type'] = metadata.get('type')
                    track_data['created_at'] = metadata.get('created_at')
                    track_data['updated_at'] = metadata.get('updated_at')

                # Get task progress
                plan_file = resolver.resolve_track_file(track_id, 'implementation_plan')
                if plan_file:
                    content = plan_file.read_text()
                    counts = parser.count_status_markers(content)
                    track_data['tasks'] = counts
                    if counts['total'] > 0:
                        track_data['progress_percent'] = round(
                            (counts['completed'] / counts['total']) * 100, 1
                        )
                    else:
                        track_data['progress_percent'] = 0

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


def update_status(project_root: Path, track_id: str, status: str) -> Dict[str, Any]:
    """
    Update track status in tracks.md.

    Args:
        project_root: Project root path
        track_id: Track identifier
        status: New status (pending, in-progress, completed)

    Returns:
        JSON with update result
    """
    resolver = FileResolver(project_root)
    parser = TracksParser(project_root)
    json_mgr = JsonManager(project_root)

    # Verify track exists
    if not resolver.track_exists(track_id):
        return {
            'success': False,
            'error': f"Track '{track_id}' not found"
        }

    # Read tracks.md
    tracks_file = resolver.resolve_project_file('tracks_registry')
    if not tracks_file:
        return {
            'success': False,
            'error': 'Tracks registry (conductor/tracks.md) not found'
        }

    content = tracks_file.read_text()

    # Map status string to enum
    status_map = {
        'pending': TaskStatus.PENDING,
        'in-progress': TaskStatus.IN_PROGRESS,
        'completed': TaskStatus.COMPLETED
    }

    if status not in status_map:
        return {
            'success': False,
            'error': f"Invalid status '{status}'. Use: pending, in-progress, completed"
        }

    new_status = status_map[status]

    # Find and update the track line
    # Look for the track by ID in the path
    lines = content.split('\n')
    updated = False
    new_lines = []

    for line in lines:
        if f'conductor/tracks/{track_id}' in line or f'tracks/{track_id}' in line:
            # This is the link line, track status is on previous line
            new_lines.append(line)
        elif track_id in line and '**Track:' in line:
            # Update status marker
            status_char = ' '
            if new_status == TaskStatus.COMPLETED:
                status_char = 'x'
            elif new_status == TaskStatus.IN_PROGRESS:
                status_char = '~'

            updated_line = re.sub(r'\[([ x~])\]', f'[{status_char}]', line, count=1)
            new_lines.append(updated_line)
            updated = True
        else:
            # Check if line contains track info by checking if next line would have track_id
            # This handles cases where track_id isn't in the track line itself
            new_lines.append(line)

    # If not found by ID in track line, try finding by looking at the path pattern
    if not updated:
        new_lines = []
        for i, line in enumerate(lines):
            if i + 1 < len(lines) and f'conductor/tracks/{track_id}' in lines[i + 1]:
                # Current line should be the track line
                status_char = ' '
                if new_status == TaskStatus.COMPLETED:
                    status_char = 'x'
                elif new_status == TaskStatus.IN_PROGRESS:
                    status_char = '~'

                updated_line = re.sub(r'\[([ x~])\]', f'[{status_char}]', line, count=1)
                new_lines.append(updated_line)
                updated = True
            else:
                new_lines.append(line)

    if not updated:
        return {
            'success': False,
            'error': f"Could not find track '{track_id}' in tracks.md"
        }

    # Write updated content
    tracks_file.write_text('\n'.join(new_lines))

    # Update metadata
    metadata = json_mgr.read_track_metadata(track_id)
    if metadata:
        from datetime import datetime
        metadata['status'] = status
        metadata['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        json_mgr.write_track_metadata(track_id, metadata)

    return {
        'success': True,
        'data': {
            'track_id': track_id,
            'new_status': status,
            'updated': True
        },
        'message': Formatters.success(f"Track '{track_id}' status updated to {status}")
    }


def archive(project_root: Path, track_id: str) -> Dict[str, Any]:
    """
    Archive a completed track by moving to archive/ directory.

    Args:
        project_root: Project root path
        track_id: Track identifier

    Returns:
        JSON with archive result
    """
    resolver = FileResolver(project_root)

    # Verify track exists
    track_dir = resolver.get_track_directory(track_id)
    if not track_dir:
        return {
            'success': False,
            'error': f"Track '{track_id}' not found"
        }

    # Create archive directory
    archive_dir = project_root / 'conductor' / 'tracks' / 'archive'
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Check if archive destination already exists
    dest_dir = archive_dir / track_id
    if dest_dir.exists():
        return {
            'success': False,
            'error': f"Archive destination already exists: {dest_dir}"
        }

    # Move track directory
    try:
        shutil.move(str(track_dir), str(dest_dir))
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to archive track: {str(e)}"
        }

    return {
        'success': True,
        'data': {
            'track_id': track_id,
            'source': str(track_dir),
            'destination': str(dest_dir)
        },
        'message': Formatters.success(f"Track '{track_id}' archived to {dest_dir}")
    }


def modified_files(project_root: Path) -> Dict[str, Any]:
    """
    Get list of modified files from git diff.

    Returns both staged and unstaged modified files.

    Args:
        project_root: Project root path

    Returns:
        JSON with lists of modified files
    """
    git_ops = GitOps(project_root)

    if not git_ops.is_repo():
        return {
            'success': False,
            'error': 'Not a git repository'
        }

    # Get staged files
    staged = git_ops.get_modified_files(staged=True)

    # Get all modified (vs HEAD)
    all_modified = git_ops.get_modified_files(staged=False)

    # Get untracked files
    untracked = git_ops.get_untracked_files()

    # Calculate unstaged (modified but not staged)
    unstaged = [f for f in all_modified if f not in staged]

    return {
        'success': True,
        'data': {
            'staged': staged,
            'unstaged': unstaged,
            'untracked': untracked,
            'all_modified': all_modified,
            'counts': {
                'staged': len(staged),
                'unstaged': len(unstaged),
                'untracked': len(untracked),
                'total': len(all_modified) + len(untracked)
            }
        },
        'message': format_modified_files(staged, unstaged, untracked)
    }


def parse_coverage(project_root: Path, format_type: str, path: Optional[str]) -> Dict[str, Any]:
    """
    Parse coverage reports in various formats.

    Supported formats:
    - lcov: Parse LF/LH lines for line coverage
    - cobertura: Parse XML for line-rate attribute
    - json: Look for summary.lines.pct or similar

    Args:
        project_root: Project root path
        format_type: Coverage format (lcov, cobertura, json)
        path: Path to coverage file (auto-detected if not provided)

    Returns:
        JSON with coverage metrics
    """
    # Auto-detect path if not provided
    if not path:
        default_paths = {
            'lcov': ['coverage/lcov.info', 'lcov.info'],
            'cobertura': ['coverage/cobertura-coverage.xml', 'cobertura.xml', 'coverage.xml'],
            'json': ['coverage/coverage-summary.json', 'coverage-final.json', 'coverage.json']
        }

        for default in default_paths.get(format_type, []):
            test_path = project_root / default
            if test_path.exists():
                path = default
                break

    if not path:
        return {
            'success': False,
            'error': f'No coverage file found for format: {format_type}'
        }

    coverage_file = project_root / path
    if not coverage_file.exists():
        return {
            'success': False,
            'error': f'Coverage file not found: {path}'
        }

    try:
        if format_type == 'lcov':
            metrics = parse_lcov(coverage_file)
        elif format_type == 'cobertura':
            metrics = parse_cobertura(coverage_file)
        elif format_type == 'json':
            metrics = parse_json_coverage(coverage_file)
        else:
            return {
                'success': False,
                'error': f'Unknown format: {format_type}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to parse coverage: {str(e)}'
        }

    return {
        'success': True,
        'data': {
            'format': format_type,
            'path': str(path),
            'metrics': metrics
        },
        'message': format_coverage_metrics(metrics)
    }


def parse_lcov(path: Path) -> Dict[str, Any]:
    """Parse LCOV format coverage file."""
    content = path.read_text()

    lines_found = 0
    lines_hit = 0
    uncovered_files = []

    current_file = None
    file_lf = 0
    file_lh = 0

    for line in content.split('\n'):
        line = line.strip()

        if line.startswith('SF:'):
            current_file = line[3:]
            file_lf = 0
            file_lh = 0
        elif line.startswith('LF:'):
            file_lf = int(line[3:])
            lines_found += file_lf
        elif line.startswith('LH:'):
            file_lh = int(line[3:])
            lines_hit += file_lh
        elif line == 'end_of_record':
            if current_file and file_lf > 0 and file_lh < file_lf:
                coverage = (file_lh / file_lf) * 100
                if coverage < 80:  # Files with less than 80% coverage
                    uncovered_files.append({
                        'file': current_file,
                        'coverage': round(coverage, 1)
                    })
            current_file = None

    coverage_percent = (lines_hit / lines_found * 100) if lines_found > 0 else 0

    return {
        'lines_covered': lines_hit,
        'lines_total': lines_found,
        'coverage_percent': round(coverage_percent, 2),
        'uncovered_files': sorted(uncovered_files, key=lambda x: x['coverage'])[:10]
    }


def parse_cobertura(path: Path) -> Dict[str, Any]:
    """Parse Cobertura XML format coverage file."""
    tree = ET.parse(path)
    root = tree.getroot()

    # Get line-rate from root or coverage element
    line_rate = root.get('line-rate') or root.get('lines-covered')

    if line_rate is None:
        # Try finding coverage element
        coverage_elem = root.find('.//coverage')
        if coverage_elem is not None:
            line_rate = coverage_elem.get('line-rate')

    if line_rate is not None:
        coverage_percent = float(line_rate) * 100
    else:
        # Calculate from packages
        lines_covered = 0
        lines_valid = 0

        for line in root.iter('line'):
            lines_valid += 1
            if int(line.get('hits', '0')) > 0:
                lines_covered += 1

        coverage_percent = (lines_covered / lines_valid * 100) if lines_valid > 0 else 0

    # Find uncovered files
    uncovered_files = []
    for cls in root.iter('class'):
        filename = cls.get('filename', '')
        cls_line_rate = cls.get('line-rate')
        if cls_line_rate:
            file_coverage = float(cls_line_rate) * 100
            if file_coverage < 80:
                uncovered_files.append({
                    'file': filename,
                    'coverage': round(file_coverage, 1)
                })

    # Get total lines if available
    lines_covered_attr = root.get('lines-covered')
    lines_valid_attr = root.get('lines-valid')

    lines_covered = int(lines_covered_attr) if lines_covered_attr else 0
    lines_total = int(lines_valid_attr) if lines_valid_attr else 0

    return {
        'lines_covered': lines_covered,
        'lines_total': lines_total,
        'coverage_percent': round(coverage_percent, 2),
        'uncovered_files': sorted(uncovered_files, key=lambda x: x['coverage'])[:10]
    }


def parse_json_coverage(path: Path) -> Dict[str, Any]:
    """Parse JSON format coverage file (Istanbul/NYC style)."""
    data = json.loads(path.read_text())

    # Try different JSON structures
    # Istanbul summary format
    if 'total' in data and 'lines' in data['total']:
        lines = data['total']['lines']
        return {
            'lines_covered': lines.get('covered', 0),
            'lines_total': lines.get('total', 0),
            'coverage_percent': round(lines.get('pct', 0), 2),
            'uncovered_files': []
        }

    # Coverage-summary format
    if 'lines' in data:
        lines = data['lines']
        return {
            'lines_covered': lines.get('covered', 0),
            'lines_total': lines.get('total', 0),
            'coverage_percent': round(lines.get('pct', 0), 2),
            'uncovered_files': []
        }

    # Jest coverage format with file breakdown
    lines_covered = 0
    lines_total = 0
    uncovered_files = []

    for filename, file_data in data.items():
        if isinstance(file_data, dict) and 'lines' in file_data:
            file_lines = file_data['lines']
            file_covered = file_lines.get('covered', 0)
            file_total = file_lines.get('total', 0)
            lines_covered += file_covered
            lines_total += file_total

            if file_total > 0:
                file_pct = (file_covered / file_total) * 100
                if file_pct < 80:
                    uncovered_files.append({
                        'file': filename,
                        'coverage': round(file_pct, 1)
                    })

    coverage_percent = (lines_covered / lines_total * 100) if lines_total > 0 else 0

    return {
        'lines_covered': lines_covered,
        'lines_total': lines_total,
        'coverage_percent': round(coverage_percent, 2),
        'uncovered_files': sorted(uncovered_files, key=lambda x: x['coverage'])[:10]
    }


def next_adr_number(project_root: Path, adr_path: str) -> Dict[str, Any]:
    """
    Get the next ADR number by counting existing ADR files.

    Args:
        project_root: Project root path
        adr_path: Path to ADR directory

    Returns:
        JSON with next ADR number
    """
    adr_dir = project_root / adr_path

    if not adr_dir.exists():
        # Directory doesn't exist yet, start with 1
        return {
            'success': True,
            'data': {
                'next_number': 1,
                'padded': '0001',
                'existing_count': 0,
                'path': str(adr_dir)
            },
            'message': 'ADR directory does not exist. Next ADR: 0001'
        }

    # Find existing ADR files (format: NNNN-*.md)
    adr_pattern = re.compile(r'^(\d{4})-.*\.md$')
    existing_numbers = []

    for file in adr_dir.iterdir():
        if file.is_file():
            match = adr_pattern.match(file.name)
            if match:
                existing_numbers.append(int(match.group(1)))

    if not existing_numbers:
        next_num = 1
    else:
        next_num = max(existing_numbers) + 1

    return {
        'success': True,
        'data': {
            'next_number': next_num,
            'padded': f'{next_num:04d}',
            'existing_count': len(existing_numbers),
            'path': str(adr_dir)
        },
        'message': f'Next ADR number: {next_num:04d} ({len(existing_numbers)} existing)'
    }


def match_patterns(project_root: Path, keywords: List[str]) -> Dict[str, Any]:
    """
    Match keywords against patterns in patterns/index.md.

    Scoring:
    - Exact match: +1.0
    - Partial match (substring): +0.5

    Args:
        project_root: Project root path
        keywords: List of keywords to match

    Returns:
        JSON with ranked list of matching patterns
    """
    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Find patterns index
    patterns_index = resolver.resolve_project_file('pattern_registry')
    if not patterns_index:
        return {
            'success': False,
            'error': 'Patterns index (patterns/index.md) not found'
        }

    # Normalize keywords
    normalized_keywords = [k.lower().strip() for k in keywords]

    # Read patterns index and extract patterns
    content = patterns_index.read_text()

    # Find pattern links in index
    links = md_parser.parse_index_links(content)

    matched_patterns = []

    for link in links:
        pattern_name = link['label']
        pattern_path = link['path']

        # Resolve pattern file
        if pattern_path.startswith('./'):
            pattern_file = patterns_index.parent / pattern_path
        else:
            pattern_file = project_root / pattern_path

        if not pattern_file.exists():
            continue

        # Read pattern and extract activation keywords from frontmatter
        pattern_content = pattern_file.read_text()
        frontmatter, _ = md_parser.parse_frontmatter(pattern_content)

        activation = frontmatter.get('activation', {})
        if isinstance(activation, dict):
            activation_keywords = activation.get('keywords', [])
        else:
            activation_keywords = []

        # Also use pattern name words as implicit keywords
        name_words = pattern_name.lower().replace('-', ' ').replace('_', ' ').split()
        all_pattern_keywords = [k.lower() for k in activation_keywords] + name_words

        # Calculate score
        score = 0.0
        matched_keywords = []

        for keyword in normalized_keywords:
            for pattern_keyword in all_pattern_keywords:
                if keyword == pattern_keyword:
                    score += 1.0
                    matched_keywords.append(keyword)
                    break
                elif keyword in pattern_keyword or pattern_keyword in keyword:
                    score += 0.5
                    matched_keywords.append(keyword)
                    break

        if score > 0:
            # Extract description from pattern
            description = frontmatter.get('description', '')
            if not description:
                # Try to get first line of content
                for line in pattern_content.split('\n'):
                    if line.strip() and not line.startswith('#') and not line.startswith('---'):
                        description = line.strip()[:100]
                        break

            matched_patterns.append({
                'name': pattern_name,
                'path': str(pattern_file),
                'score': score,
                'matched_keywords': list(set(matched_keywords)),
                'description': Formatters.truncate(description, 80)
            })

    # Sort by score descending
    matched_patterns.sort(key=lambda x: x['score'], reverse=True)

    # Limit to top matches
    top_patterns = matched_patterns[:10]

    return {
        'success': True,
        'data': {
            'keywords': keywords,
            'matches': top_patterns,
            'total_matches': len(matched_patterns)
        },
        'message': format_pattern_matches(top_patterns, keywords)
    }


# Formatting helpers

def format_tracks_list(tracks: List[Dict], summary: Dict) -> str:
    """Format tracks list for human output."""
    lines = [
        f"Tracks: {summary['total']} total",
        f"  {Formatters.status_symbol('completed')} Completed:   {summary['completed']}",
        f"  {Formatters.status_symbol('in_progress')} In Progress: {summary['in_progress']}",
        f"  {Formatters.status_symbol('pending')} Pending:     {summary['pending']}",
        ''
    ]

    for track in tracks:
        status = track.get('status', 'pending')
        symbol = Formatters.status_symbol(status)
        desc = Formatters.truncate(track.get('description', ''), 45)
        track_id = track.get('track_id', '')

        lines.append(f"  {symbol} [{track_id}] {desc}")

        # Show progress if available
        if 'progress_percent' in track:
            progress = Formatters.progress_bar(
                track.get('tasks', {}).get('completed', 0),
                track.get('tasks', {}).get('total', 1),
                width=20
            )
            lines.append(f"      {progress}")

    return '\n'.join(lines)


def format_modified_files(staged: List[str], unstaged: List[str], untracked: List[str]) -> str:
    """Format modified files for human output."""
    lines = ['Modified Files:', '']

    if staged:
        lines.append(f'{Formatters.status_symbol("completed")} Staged ({len(staged)}):')
        for f in staged[:10]:
            lines.append(f'    {f}')
        if len(staged) > 10:
            lines.append(f'    ... and {len(staged) - 10} more')
        lines.append('')

    if unstaged:
        lines.append(f'{Formatters.status_symbol("in_progress")} Unstaged ({len(unstaged)}):')
        for f in unstaged[:10]:
            lines.append(f'    {f}')
        if len(unstaged) > 10:
            lines.append(f'    ... and {len(unstaged) - 10} more')
        lines.append('')

    if untracked:
        lines.append(f'{Formatters.status_symbol("pending")} Untracked ({len(untracked)}):')
        for f in untracked[:10]:
            lines.append(f'    {f}')
        if len(untracked) > 10:
            lines.append(f'    ... and {len(untracked) - 10} more')

    if not staged and not unstaged and not untracked:
        lines.append('  No changes detected')

    return '\n'.join(lines)


def format_coverage_metrics(metrics: Dict[str, Any]) -> str:
    """Format coverage metrics for human output."""
    lines = [
        'Coverage Report:',
        '',
        f"  Lines: {metrics['lines_covered']}/{metrics['lines_total']} ({metrics['coverage_percent']}%)",
        '',
        Formatters.progress_bar(metrics['lines_covered'], metrics['lines_total'])
    ]

    uncovered = metrics.get('uncovered_files', [])
    if uncovered:
        lines.append('')
        lines.append('Files needing coverage:')
        for f in uncovered[:5]:
            lines.append(f"  - {f['file']}: {f['coverage']}%")

    return '\n'.join(lines)


def format_pattern_matches(patterns: List[Dict], keywords: List[str]) -> str:
    """Format pattern matches for human output."""
    if not patterns:
        return f'No patterns matched for: {", ".join(keywords)}'

    lines = [
        f'Pattern matches for: {", ".join(keywords)}',
        ''
    ]

    for pattern in patterns:
        score_display = f"[{pattern['score']:.1f}]"
        lines.append(f"  {score_display} {pattern['name']}")
        if pattern.get('description'):
            lines.append(f"        {pattern['description']}")

    return '\n'.join(lines)
