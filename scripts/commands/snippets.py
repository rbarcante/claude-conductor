"""
Snippets command - 90% scriptable.

Browse and search code snippets from the Snippet Library.
Operations: list, show, search, detect_language
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import sys
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.markdown_parser import MarkdownParser
from lib.formatters import Formatters


# Language extension mappings
LANGUAGE_EXTENSIONS = {
    'python': ['.py'],
    'typescript': ['.ts'],
    'javascript': ['.js'],
    'java': ['.java'],
    'go': ['.go'],
    'rust': ['.rs'],
    'markdown': ['.md'],
}

# Reverse mapping for extension to language
EXTENSION_TO_LANGUAGE = {}
for lang, exts in LANGUAGE_EXTENSIONS.items():
    for ext in exts:
        EXTENSION_TO_LANGUAGE[ext] = lang


def handle(args) -> Dict[str, Any]:
    """Handle snippets subcommands."""
    project_root = args.project_root

    if args.subcommand == 'list':
        return list_snippets(project_root)
    elif args.subcommand == 'show':
        language = getattr(args, 'language', None)
        return show_snippet(project_root, args.name, language)
    elif args.subcommand == 'search':
        return search_snippets(project_root, args.query)
    elif args.subcommand == 'detect_language':
        return detect_language(args.filename)
    else:
        # Default to list
        return list_snippets(project_root)


def list_snippets(project_root: Path) -> Dict[str, Any]:
    """
    List all available snippets organized by category.

    Returns JSON with:
    - snippets: List of snippet info dicts grouped by language
    - summary: Count by language
    """
    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Read snippets index
    index_path = resolver.resolve_project_file('snippet_index')
    if not index_path:
        return {
            'success': False,
            'error': 'Snippet index not found at snippets/index.md'
        }

    content = index_path.read_text()

    # Parse snippets by category from index
    categories = {}
    all_snippets = []

    # Categories to look for
    category_names = ['TypeScript', 'Python', 'Java', 'Patterns']

    for category in category_names:
        section = md_parser.extract_section(content, category, level=3)
        if section:
            snippets = _parse_snippet_table(section, category.lower())
            categories[category] = snippets
            all_snippets.extend(snippets)

    # Validate and enrich with file info
    # Paths in index.md are relative to the snippets directory (where index.md is)
    snippets_dir = project_root / 'snippets'
    for snippet in all_snippets:
        path = snippet.get('path', '')
        if path:
            full_path = snippets_dir / path.lstrip('./')
            snippet['exists'] = full_path.exists()
            if full_path.exists():
                snippet['size'] = full_path.stat().st_size
                # Extract header info
                header = _extract_snippet_header(full_path, md_parser)
                snippet.update(header)
        else:
            snippet['exists'] = False

    # Summary counts
    summary = {
        'total': len(all_snippets),
        'by_language': {cat: len(snips) for cat, snips in categories.items()},
        'valid': sum(1 for s in all_snippets if s.get('exists', False))
    }

    return {
        'success': True,
        'data': {
            'snippets': all_snippets,
            'categories': categories,
            'summary': summary
        },
        'message': format_snippets_list(categories)
    }


def show_snippet(project_root: Path, name: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Show a specific snippet with its AI header and content.

    Args:
        name: Snippet name (with or without extension)
        language: Optional language hint for disambiguation

    Returns JSON with:
    - name, language, path
    - header: AI header info (use, requires, pattern)
    - content: Full snippet content
    """
    if not name:
        return {
            'success': False,
            'error': 'Snippet name is required'
        }

    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Resolve snippet path
    snippet_path = resolver.resolve_snippet(name, language)
    if not snippet_path:
        # Try direct name match in all language directories
        snippet_path = _find_snippet_by_name(project_root, name, language)

    if not snippet_path:
        return {
            'success': False,
            'error': f"Snippet '{name}' not found" + (f" for language '{language}'" if language else "")
        }

    content = snippet_path.read_text()

    # Detect language from extension
    detected_language = detect_language_from_path(snippet_path)

    # Parse AI header
    header = md_parser.parse_snippet_header(content, detected_language)

    result = {
        'name': snippet_path.stem,
        'language': detected_language,
        'path': str(snippet_path.relative_to(project_root)),
        'header': header,
        'content': content
    }

    return {
        'success': True,
        'data': result,
        'message': format_snippet_detail(result)
    }


def search_snippets(project_root: Path, query: str) -> Dict[str, Any]:
    """
    Search snippets by keyword across all snippet files.

    Searches snippet names, headers, and content.

    Returns ranked JSON results.
    """
    if not query:
        return {
            'success': False,
            'error': 'Search query is required'
        }

    md_parser = MarkdownParser(project_root)
    snippets_dir = project_root / 'snippets'

    if not snippets_dir.exists():
        return {
            'success': False,
            'error': 'Snippets directory not found'
        }

    results = []
    query_lower = query.lower()
    query_terms = query_lower.split()

    # Search all language directories
    for lang_dir in snippets_dir.iterdir():
        if not lang_dir.is_dir():
            continue

        for snippet_file in lang_dir.iterdir():
            if snippet_file.is_dir():
                continue

            # Skip non-code files (except markdown)
            if snippet_file.suffix not in EXTENSION_TO_LANGUAGE:
                continue

            score, matches = _score_snippet(snippet_file, query_terms, md_parser)
            if score > 0:
                results.append({
                    'name': snippet_file.stem,
                    'language': lang_dir.name,
                    'path': str(snippet_file.relative_to(project_root)),
                    'score': score,
                    'matches': matches
                })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)

    return {
        'success': True,
        'data': {
            'query': query,
            'results': results,
            'count': len(results)
        },
        'message': format_search_results(query, results)
    }


def detect_language(filename: str) -> Dict[str, Any]:
    """
    Detect programming language from filename extension.

    Returns language name and associated extensions.
    """
    if not filename:
        return {
            'success': False,
            'error': 'Filename is required'
        }

    # Extract extension
    path = Path(filename)
    ext = path.suffix.lower()

    if ext in EXTENSION_TO_LANGUAGE:
        language = EXTENSION_TO_LANGUAGE[ext]
        return {
            'success': True,
            'data': {
                'filename': filename,
                'extension': ext,
                'language': language,
                'all_extensions': LANGUAGE_EXTENSIONS.get(language, [ext])
            },
            'message': f"Detected language: {language} (from {ext})"
        }
    else:
        return {
            'success': True,
            'data': {
                'filename': filename,
                'extension': ext,
                'language': 'unknown',
                'all_extensions': []
            },
            'message': f"Unknown language for extension: {ext}"
        }


# Helper functions

def detect_language_from_path(path: Path) -> str:
    """Detect language from file path."""
    ext = path.suffix.lower()
    return EXTENSION_TO_LANGUAGE.get(ext, 'unknown')


def _parse_snippet_table(section: str, category: str) -> List[Dict[str, Any]]:
    """Parse a markdown table from a section into snippet dicts."""
    snippets = []
    lines = section.strip().split('\n')

    # Find table lines
    table_lines = [l for l in lines if l.strip().startswith('|')]
    if len(table_lines) < 3:
        return snippets

    # Skip header and separator
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 2:
            # Extract link from first cell
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cells[0])
            if link_match:
                name = link_match.group(1)
                path = link_match.group(2)
            else:
                name = cells[0]
                path = None

            snippet = {
                'name': name,
                'path': path,
                'category': category,
                'description': cells[1] if len(cells) > 1 else ''
            }

            # Some tables have Pattern column
            if len(cells) > 2:
                snippet['pattern'] = cells[2]

            snippets.append(snippet)

    return snippets


def _extract_snippet_header(path: Path, md_parser: MarkdownParser) -> Dict[str, Any]:
    """Extract AI header from a snippet file."""
    try:
        content = path.read_text()
        language = detect_language_from_path(path)
        return md_parser.parse_snippet_header(content, language)
    except Exception:
        return {}


def _find_snippet_by_name(project_root: Path, name: str, language: Optional[str] = None) -> Optional[Path]:
    """Find a snippet file by name, optionally filtered by language."""
    snippets_dir = project_root / 'snippets'
    if not snippets_dir.exists():
        return None

    # Normalize name (remove extension if present)
    name_stem = Path(name).stem

    # If language specified, search that directory first
    if language:
        lang_dir = snippets_dir / language.lower()
        if lang_dir.exists():
            for f in lang_dir.iterdir():
                if f.stem == name_stem:
                    return f

    # Search all language directories
    for lang_dir in snippets_dir.iterdir():
        if not lang_dir.is_dir():
            continue
        for f in lang_dir.iterdir():
            if f.stem == name_stem:
                return f

    return None


def _score_snippet(snippet_path: Path, query_terms: List[str], md_parser: MarkdownParser) -> tuple:
    """
    Score a snippet file against search terms.

    Returns (score, matches) tuple.
    """
    try:
        content = snippet_path.read_text()
    except Exception:
        return 0, []

    language = detect_language_from_path(snippet_path)
    header = md_parser.parse_snippet_header(content, language)

    score = 0
    matches = []

    # Check name match (highest weight)
    name = snippet_path.stem.lower()
    for term in query_terms:
        if term in name:
            score += 3.0
            matches.append(f"name: {name}")

    # Check USE field (high weight - describes purpose)
    use_text = header.get('use', '').lower()
    for term in query_terms:
        if term in use_text:
            score += 2.5
            matches.append(f"use: {term}")

    # Check PATTERN field (patterns this implements)
    pattern_text = header.get('pattern', '').lower()
    for term in query_terms:
        if term in pattern_text:
            score += 2.0
            matches.append(f"pattern: {term}")

    # Check REQUIRES field
    requires_text = header.get('requires', '').lower()
    for term in query_terms:
        if term in requires_text:
            score += 1.0
            matches.append(f"requires: {term}")

    # Check language/directory match
    lang = snippet_path.parent.name.lower()
    for term in query_terms:
        if term in lang or lang in term:
            score += 1.5
            matches.append(f"language: {lang}")

    # Check content match (lowest weight)
    content_lower = content.lower()
    for term in query_terms:
        if term in content_lower:
            count = content_lower.count(term)
            score += min(count * 0.05, 0.5)
            if f"content ({count} matches)" not in matches:
                matches.append(f"content ({count} matches)")

    return score, list(set(matches))


def format_snippets_list(categories: Dict[str, List[Dict[str, Any]]]) -> str:
    """Format snippets list for human-readable output."""
    lines = []

    for category, snippets in categories.items():
        if not snippets:
            continue

        lines.append(f"\n{Formatters.COLORS['bold']}{category}{Formatters.COLORS['reset']} ({len(snippets)} snippets)")
        lines.append('-' * 40)

        for snippet in snippets:
            exists = snippet.get('exists', False)
            symbol = Formatters.status_symbol('completed' if exists else 'error')
            name = snippet.get('name', 'Unknown')
            desc = Formatters.truncate(snippet.get('description', ''), 45)
            lines.append(f"  {symbol} {name}")
            if desc:
                lines.append(f"      {desc}")

    if not lines:
        return 'No snippets found.'

    return '\n'.join(lines)


def format_snippet_detail(snippet: Dict[str, Any]) -> str:
    """Format detailed snippet information."""
    lines = [
        f"{Formatters.COLORS['bold']}{snippet.get('name', 'Unknown')}{Formatters.COLORS['reset']}",
        '',
        f"  Language:  {snippet.get('language', '?')}",
        f"  Path:      {snippet.get('path', '?')}",
    ]

    header = snippet.get('header', {})
    if header.get('use'):
        lines.append('')
        lines.append(f"  USE: {header['use']}")

    if header.get('requires'):
        lines.append(f"  REQUIRES: {header['requires']}")

    if header.get('pattern'):
        lines.append(f"  PATTERN: {header['pattern']}")

    lines.append('')
    lines.append('  Content Preview:')
    lines.append('  ' + '-' * 50)

    # Show first 15 lines of content
    content = snippet.get('content', '')
    content_lines = content.split('\n')[:15]
    for line in content_lines:
        lines.append(f"  {line[:70]}")

    if len(snippet.get('content', '').split('\n')) > 15:
        lines.append('  ... (truncated)')

    return '\n'.join(lines)


def format_search_results(query: str, results: List[Dict[str, Any]]) -> str:
    """Format search results for human-readable output."""
    lines = [
        f"Search results for: '{query}'",
        f"Found {len(results)} matching snippet(s)",
        ''
    ]

    if not results:
        lines.append('  (no matches)')
    else:
        for result in results[:10]:
            score = result.get('score', 0)
            symbol = Formatters.status_symbol('completed') if score >= 2 else Formatters.status_symbol('pending')
            lang = result.get('language', '?')
            lines.append(f"  {symbol} {result['name']} [{lang}] (score: {score:.1f})")
            matches = result.get('matches', [])
            if matches:
                lines.append(f"      Matches: {', '.join(matches[:3])}")

    return '\n'.join(lines)
