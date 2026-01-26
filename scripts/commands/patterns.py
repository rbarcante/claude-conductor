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
Patterns command - 85% scriptable.

Browse and search patterns from the Pattern Reference Layer.
Operations: list, show, search, ai_only
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import sys
import re

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.markdown_parser import MarkdownParser
from lib.formatters import Formatters


def handle(args) -> Dict[str, Any]:
    """Handle patterns subcommands."""
    project_root = args.project_root
    plugin_root = getattr(args, "plugin_root", None)

    if args.subcommand == "list":
        return list_patterns(plugin_root or project_root)
    elif args.subcommand == "show":
        # Check for --ai-only flag
        if getattr(args, "ai_only", False):
            return ai_only(plugin_root or project_root, args.name)
        return show_pattern(plugin_root or project_root, args.name)
    elif args.subcommand == "search":
        return search_patterns(plugin_root or project_root, args.query)
    else:
        # Default to list
        return list_patterns(plugin_root or project_root)


def list_patterns(project_root: Path) -> Dict[str, Any]:
    """
    List all available patterns from index.md.

    Returns JSON with:
    - patterns: List of pattern info dicts
    - summary: Count by category
    """
    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Read pattern registry
    index_path = resolver.resolve_project_file("pattern_registry")
    if not index_path:
        return {
            "success": False,
            "error": "Pattern registry not found at patterns/index.md",
        }

    content = index_path.read_text()

    # Parse the Core Patterns table
    core_section = md_parser.extract_section(content, "Core Patterns")
    core_patterns = []
    if core_section:
        core_patterns = _parse_pattern_table(core_section)

    # Parse Stack Patterns table (if any)
    stack_section = md_parser.extract_section(content, "Stack Patterns")
    stack_patterns = []
    if stack_section:
        stack_patterns = _parse_pattern_table(stack_section)

    # Enrich patterns with validation and frontmatter
    all_patterns = []
    for pattern in core_patterns:
        enriched = _enrich_pattern(project_root, pattern, "core")
        all_patterns.append(enriched)

    for pattern in stack_patterns:
        enriched = _enrich_pattern(project_root, pattern, "stack")
        all_patterns.append(enriched)

    # Summary by category
    categories = {}
    for p in all_patterns:
        cat = p.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "success": True,
        "data": {
            "patterns": all_patterns,
            "summary": {
                "total": len(all_patterns),
                "core": len(core_patterns),
                "stack": len(stack_patterns),
                "by_category": categories,
            },
        },
        "message": format_patterns_list(all_patterns),
    }


def show_pattern(project_root: Path, name: str) -> Dict[str, Any]:
    """
    Show detailed information about a pattern.

    Resolves path (core/ -> stack/ fallback), extracts sections.

    Returns JSON with:
    - name, category, tags, activation keywords
    - sections: full content of each section
    """
    if not name:
        return {"success": False, "error": "Pattern name is required"}

    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Resolve pattern path
    pattern_path = resolver.resolve_pattern(name)
    if not pattern_path:
        return {
            "success": False,
            "error": f"Pattern '{name}' not found in core/ or stack/ directories",
        }

    content = pattern_path.read_text()

    # Parse frontmatter
    frontmatter, body = md_parser.parse_frontmatter(content)

    # Extract key sections
    sections = {}
    for section_name in [
        "AI Quick Reference",
        "Human Documentation",
        "Anti-Patterns to Avoid",
        "Implementation Examples",
        "Best Practices",
        "Related Patterns",
    ]:
        section = md_parser.extract_section(body, section_name)
        if section:
            sections[section_name] = section

    # Get headers for overview
    headers = md_parser.extract_headers(body)

    result = {
        "name": frontmatter.get("name", name),
        "category": frontmatter.get("category", "Unknown"),
        "tags": frontmatter.get("tags", []),
        "version": frontmatter.get("version", "?"),
        "last_updated": frontmatter.get("last_updated"),
        "activation": frontmatter.get("activation", {}),
        "path": str(pattern_path.relative_to(project_root)),
        "sections": sections,
        "headers": headers,
    }

    return {"success": True, "data": result, "message": format_pattern_detail(result)}


def search_patterns(project_root: Path, query: str) -> Dict[str, Any]:
    """
    Search patterns by keyword across all pattern files.

    Returns ranked JSON results based on match relevance.
    """
    if not query:
        return {"success": False, "error": "Search query is required"}

    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Get pattern directories
    core_dir = project_root / "patterns" / "core"
    stack_dir = project_root / "patterns" / "stack"

    results = []
    query_lower = query.lower()
    query_terms = query_lower.split()

    # Search core patterns
    if core_dir.exists():
        for pattern_file in core_dir.glob("*.md"):
            if pattern_file.name == "TEMPLATE.md":
                continue
            score, matches = _score_pattern(pattern_file, query_terms, md_parser)
            if score > 0:
                results.append(
                    {
                        "name": pattern_file.stem,
                        "path": str(pattern_file.relative_to(project_root)),
                        "type": "core",
                        "score": score,
                        "matches": matches,
                    }
                )

    # Search stack patterns
    if stack_dir.exists():
        for pattern_file in stack_dir.rglob("*.md"):
            if pattern_file.name == "TEMPLATE.md":
                continue
            score, matches = _score_pattern(pattern_file, query_terms, md_parser)
            if score > 0:
                results.append(
                    {
                        "name": pattern_file.stem,
                        "path": str(pattern_file.relative_to(project_root)),
                        "type": "stack",
                        "score": score,
                        "matches": matches,
                    }
                )

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "success": True,
        "data": {"query": query, "results": results, "count": len(results)},
        "message": format_search_results(query, results),
    }


def ai_only(project_root: Path, name: str) -> Dict[str, Any]:
    """
    Extract only the AI Quick Reference section for a pattern.

    Returns minimal JSON for LLM consumption.
    """
    if not name:
        return {"success": False, "error": "Pattern name is required"}

    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Resolve pattern path
    pattern_path = resolver.resolve_pattern(name)
    if not pattern_path:
        return {"success": False, "error": f"Pattern '{name}' not found"}

    content = pattern_path.read_text()

    # Parse frontmatter for basic info
    frontmatter, body = md_parser.parse_frontmatter(content)

    # Extract AI Quick Reference section
    ai_reference = md_parser.extract_ai_reference(body)

    if not ai_reference:
        return {
            "success": False,
            "error": f"Pattern '{name}' has no AI Quick Reference section",
        }

    result = {
        "name": frontmatter.get("name", name),
        "category": frontmatter.get("category"),
        "keywords": frontmatter.get("activation", {}).get("keywords", []),
        "ai_reference": ai_reference,
    }

    return {"success": True, "data": result, "message": format_ai_reference(result)}


# Helper functions


def _parse_pattern_table(section: str) -> List[Dict[str, str]]:
    """Parse a markdown table from a section into pattern dicts."""
    patterns = []
    lines = section.strip().split("\n")

    # Find table lines
    table_lines = [l for l in lines if l.strip().startswith("|")]
    if len(table_lines) < 3:
        return patterns

    # Skip header and separator
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) >= 4:
            # Extract link from first cell
            link_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", cells[0])
            if link_match:
                name = link_match.group(1)
                path = link_match.group(2)
            else:
                name = cells[0]
                path = None

            patterns.append(
                {
                    "name": name,
                    "path": path,
                    "category": cells[1] if len(cells) > 1 else "",
                    "description": cells[2] if len(cells) > 2 else "",
                    "keywords": cells[3] if len(cells) > 3 else "",
                }
            )

    return patterns


def _enrich_pattern(
    project_root: Path, pattern: Dict[str, str], source: str
) -> Dict[str, Any]:
    """Enrich pattern data with file validation and frontmatter."""
    resolver = FileResolver(project_root)
    md_parser = MarkdownParser(project_root)

    # Validate file exists
    pattern_path = resolver.resolve_pattern(pattern.get("name", ""))
    exists = pattern_path is not None

    result = {
        "name": pattern.get("name", ""),
        "category": pattern.get("category", ""),
        "description": pattern.get("description", ""),
        "keywords": pattern.get("keywords", ""),
        "source": source,
        "exists": exists,
    }

    # If file exists, get additional metadata from frontmatter
    if pattern_path and exists:
        try:
            content = pattern_path.read_text()
            frontmatter, _ = md_parser.parse_frontmatter(content)
            result["tags"] = frontmatter.get("tags", [])
            result["version"] = frontmatter.get("version", "?")
            result["activation_keywords"] = frontmatter.get("activation", {}).get(
                "keywords", []
            )
        except Exception:
            pass

    return result


def _score_pattern(
    pattern_path: Path, query_terms: List[str], md_parser: MarkdownParser
) -> tuple:
    """
    Score a pattern file against search terms.

    Returns (score, matches) tuple.
    """
    try:
        content = pattern_path.read_text()
    except Exception:
        return 0, []

    frontmatter, body = md_parser.parse_frontmatter(content)

    score = 0
    matches = []

    # Check name match (highest weight)
    name = frontmatter.get("name", pattern_path.stem).lower()
    for term in query_terms:
        if term in name:
            score += 3.0
            matches.append(f"name: {name}")

    # Check tags match
    tags = frontmatter.get("tags", [])
    for tag in tags:
        tag_lower = tag.lower()
        for term in query_terms:
            if term in tag_lower or tag_lower in term:
                score += 2.0
                matches.append(f"tag: {tag}")

    # Check activation keywords (high weight - these are meant for matching)
    keywords = frontmatter.get("activation", {}).get("keywords", [])
    for keyword in keywords:
        keyword_lower = keyword.lower()
        for term in query_terms:
            if term == keyword_lower:
                score += 2.5
                matches.append(f"keyword: {keyword}")
            elif term in keyword_lower or keyword_lower in term:
                score += 1.5
                matches.append(f"keyword: {keyword}")

    # Check category match
    category = frontmatter.get("category", "").lower()
    for term in query_terms:
        if term in category:
            score += 1.5
            matches.append(f"category: {category}")

    # Check content match (lowest weight)
    body_lower = body.lower()
    for term in query_terms:
        if term in body_lower:
            # Count occurrences (capped contribution)
            count = body_lower.count(term)
            score += min(count * 0.1, 1.0)
            if f"content ({count} matches)" not in matches:
                matches.append(f"content ({count} matches)")

    return score, list(set(matches))


def format_patterns_list(patterns: List[Dict[str, Any]]) -> str:
    """Format patterns list for human-readable output."""
    if not patterns:
        return "No patterns found."

    columns = ["name", "category", "description"]
    headers = {"name": "Pattern", "category": "Category", "description": "Description"}

    # Truncate descriptions
    for p in patterns:
        p["description"] = Formatters.truncate(p.get("description", ""), 50)

    return Formatters.table(patterns, columns, headers)


def format_pattern_detail(pattern: Dict[str, Any]) -> str:
    """Format detailed pattern information."""
    lines = [
        f"{Formatters.COLORS['bold']}{pattern.get('name', 'Unknown')}{Formatters.COLORS['reset']}",
        "",
        f"  Category:    {pattern.get('category', '?')}",
        f"  Version:     {pattern.get('version', '?')}",
        f"  Path:        {pattern.get('path', '?')}",
    ]

    tags = pattern.get("tags", [])
    if tags:
        lines.append(f"  Tags:        {', '.join(tags)}")

    activation = pattern.get("activation", {})
    keywords = activation.get("keywords", [])
    if keywords:
        lines.append(f"  Keywords:    {', '.join(keywords[:8])}")

    file_patterns = activation.get("file_patterns", [])
    if file_patterns:
        lines.append(f"  File Patterns: {', '.join(file_patterns[:3])}")

    lines.append("")

    # List available sections
    sections = pattern.get("sections", {})
    if sections:
        lines.append("  Available Sections:")
        for section_name in sections.keys():
            lines.append(f"    - {section_name}")

    return "\n".join(lines)


def format_search_results(query: str, results: List[Dict[str, Any]]) -> str:
    """Format search results for human-readable output."""
    lines = [
        f"Search results for: '{query}'",
        f"Found {len(results)} matching pattern(s)",
        "",
    ]

    if not results:
        lines.append("  (no matches)")
    else:
        for i, result in enumerate(results[:10]):
            score = result.get("score", 0)
            symbol = (
                Formatters.status_symbol("completed")
                if score >= 2
                else Formatters.status_symbol("pending")
            )
            lines.append(f"  {symbol} {result['name']} (score: {score:.1f})")
            matches = result.get("matches", [])
            if matches:
                lines.append(f"      Matches: {', '.join(matches[:3])}")

    return "\n".join(lines)


def format_ai_reference(data: Dict[str, Any]) -> str:
    """Format AI Quick Reference for output."""
    lines = [
        f"{Formatters.COLORS['bold']}AI Quick Reference: {data.get('name', 'Unknown')}{Formatters.COLORS['reset']}",
        "",
    ]

    keywords = data.get("keywords", [])
    if keywords:
        lines.append(f"Keywords: {', '.join(keywords)}")
        lines.append("")

    ai_ref = data.get("ai_reference", "")
    if ai_ref:
        lines.append(ai_ref)

    return "\n".join(lines)
