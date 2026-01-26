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
Markdown parsing utilities for Conductor CLI.

Handles YAML frontmatter extraction, section parsing, and table formatting.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class MarkdownParser:
    """Parser for markdown files with YAML frontmatter."""

    # Frontmatter pattern
    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    # Header patterns
    H1_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)
    H2_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    H3_PATTERN = re.compile(r"^###\s+(.+)$", re.MULTILINE)

    def __init__(self, project_root: Path):
        """Initialize parser with project root."""
        self.project_root = Path(project_root).resolve()

    def parse_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """
        Extract YAML frontmatter from markdown content.

        Args:
            content: Markdown file content

        Returns:
            Tuple of (frontmatter dict, remaining content)
        """
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return {}, content

        frontmatter_text = match.group(1)
        remaining = content[match.end() :]

        # Simple YAML parsing (handles basic key: value pairs)
        frontmatter = self._parse_simple_yaml(frontmatter_text)

        return frontmatter, remaining

    def _parse_simple_yaml(self, yaml_text: str) -> Dict[str, Any]:
        """
        Parse simple YAML without external dependencies.

        Handles:
        - key: value
        - key: [list, items]
        - key:
            - item1
            - item2
        - Nested objects (one level deep)
        """
        result = {}
        lines = yaml_text.split("\n")
        current_key = None
        current_list = None
        current_object = None
        object_key = None

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Check for key: value
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                if current_list is not None and current_key:
                    result[current_key] = current_list
                    current_list = None
                if current_object is not None and object_key:
                    result[object_key] = current_object
                    current_object = None

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if value == "":
                    # Could be start of list or object
                    current_key = key
                    current_list = []
                elif value.startswith("[") and value.endswith("]"):
                    # Inline list
                    items = value[1:-1].split(",")
                    result[key] = [
                        item.strip().strip("\"'") for item in items if item.strip()
                    ]
                else:
                    # Simple value
                    result[key] = self._parse_value(value)

            elif line.startswith("  ") or line.startswith("\t"):
                # Indented content
                if stripped.startswith("-"):
                    # List item
                    item = stripped[1:].strip()
                    if current_list is not None:
                        current_list.append(self._parse_value(item))
                elif ":" in stripped and current_key:
                    # Nested object
                    if current_object is None:
                        current_object = {}
                        object_key = current_key
                        current_key = None
                        current_list = None

                    nested_key, nested_value = stripped.split(":", 1)
                    current_object[nested_key.strip()] = self._parse_value(
                        nested_value.strip()
                    )

        # Handle final pending items
        if current_list is not None and current_key:
            result[current_key] = current_list
        if current_object is not None and object_key:
            result[object_key] = current_object

        return result

    def _parse_value(self, value: str) -> Any:
        """Parse a YAML value string to appropriate Python type."""
        value = value.strip().strip("\"'")

        # Boolean
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False

        # Number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        return value

    def extract_section(
        self, content: str, header: str, level: int = 2
    ) -> Optional[str]:
        """
        Extract a section by header.

        Args:
            content: Markdown content
            header: Header text to find
            level: Header level (1-6)

        Returns:
            Section content (without header) or None
        """
        prefix = "#" * level
        pattern = rf"^{prefix}\s+{re.escape(header)}\s*$"
        next_header = rf"^#{{{1},{level}}}\s+"

        lines = content.split("\n")
        in_section = False
        section_lines = []

        for line in lines:
            if re.match(pattern, line, re.IGNORECASE):
                in_section = True
                continue

            if in_section:
                if re.match(next_header, line):
                    break
                section_lines.append(line)

        if not section_lines:
            return None

        return "\n".join(section_lines).strip()

    def extract_ai_reference(self, content: str) -> Optional[str]:
        """
        Extract AI Quick Reference section from pattern/skill content.

        Args:
            content: Full markdown content

        Returns:
            AI Quick Reference section or None
        """
        # Try common header variations
        headers = ["AI Quick Reference", "Quick Reference", "TL;DR", "Summary"]

        for header in headers:
            section = self.extract_section(content, header)
            if section:
                return section

        return None

    def extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract all headers from markdown content.

        Args:
            content: Markdown content

        Returns:
            List of dicts with 'level', 'text', and 'line_number'
        """
        headers = []
        lines = content.split("\n")

        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                headers.append(
                    {
                        "level": len(match.group(1)),
                        "text": match.group(2).strip(),
                        "line_number": i + 1,
                    }
                )

        return headers

    def parse_index_links(self, content: str) -> List[Dict[str, str]]:
        """
        Parse links from an index.md file.

        Args:
            content: Index file content

        Returns:
            List of dicts with 'label' and 'path'
        """
        links = []
        pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

        for match in pattern.finditer(content):
            links.append({"label": match.group(1), "path": match.group(2)})

        return links

    def parse_table(self, content: str) -> List[Dict[str, str]]:
        """
        Parse a markdown table into list of dicts.

        Args:
            content: Content containing a markdown table

        Returns:
            List of row dicts with column headers as keys
        """
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        table_lines = [l for l in lines if l.startswith("|")]

        if len(table_lines) < 3:  # Need header, separator, and at least one row
            return []

        # Parse header
        header_line = table_lines[0]
        headers = [h.strip() for h in header_line.split("|")[1:-1]]

        # Skip separator (line 1)
        # Parse data rows
        rows = []
        for line in table_lines[2:]:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))

        return rows

    def format_table(
        self, data: List[Dict[str, Any]], columns: List[str] = None
    ) -> str:
        """
        Format data as a markdown table.

        Args:
            data: List of dicts
            columns: Column order (default: all keys from first item)

        Returns:
            Markdown table string
        """
        if not data:
            return ""

        if columns is None:
            columns = list(data[0].keys())

        # Calculate column widths
        widths = {col: len(col) for col in columns}
        for row in data:
            for col in columns:
                val = str(row.get(col, ""))
                widths[col] = max(widths[col], len(val))

        # Build table
        lines = []

        # Header
        header = "| " + " | ".join(col.ljust(widths[col]) for col in columns) + " |"
        lines.append(header)

        # Separator
        sep = "| " + " | ".join("-" * widths[col] for col in columns) + " |"
        lines.append(sep)

        # Rows
        for row in data:
            cells = [str(row.get(col, "")).ljust(widths[col]) for col in columns]
            lines.append("| " + " | ".join(cells) + " |")

        return "\n".join(lines)

    def parse_snippet_header(self, content: str, language: str) -> Dict[str, Any]:
        """
        Parse AI-optimized snippet header based on language.

        Supports:
        - Python: Triple-quoted docstring at start
        - TypeScript/JavaScript: JSDoc comment
        - Java: JavaDoc comment
        - Other: YAML frontmatter

        Args:
            content: File content
            language: Programming language

        Returns:
            Dict with 'use', 'requires', 'pattern' keys
        """
        header = {}

        if language in ("python", "py"):
            # Python docstring
            match = re.match(r'^"""(.+?)"""', content, re.DOTALL)
            if match:
                header = self._parse_docstring_header(match.group(1))

        elif language in ("typescript", "ts", "javascript", "js"):
            # JSDoc
            match = re.match(r"^/\*\*(.+?)\*/", content, re.DOTALL)
            if match:
                header = self._parse_jsdoc_header(match.group(1))

        elif language == "java":
            # JavaDoc
            match = re.match(r"^/\*\*(.+?)\*/", content, re.DOTALL)
            if match:
                header = self._parse_jsdoc_header(match.group(1))

        elif language in ("go", "golang"):
            # Go comment block
            match = re.match(r"^//\s*(.+?)(?:\n(?!//)|$)", content, re.DOTALL)
            if match:
                lines = []
                for line in content.split("\n"):
                    if line.startswith("//"):
                        lines.append(line[2:].strip())
                    else:
                        break
                header = self._parse_docstring_header("\n".join(lines))

        else:
            # Try YAML frontmatter
            fm, _ = self.parse_frontmatter(content)
            if fm:
                header = fm

        return header

    def _parse_docstring_header(self, docstring: str) -> Dict[str, Any]:
        """Parse USE/REQUIRES/PATTERN from docstring."""
        header = {}
        for line in docstring.split("\n"):
            line = line.strip()
            if line.startswith("USE:"):
                header["use"] = line[4:].strip()
            elif line.startswith("REQUIRES:"):
                header["requires"] = line[9:].strip()
            elif line.startswith("PATTERN:"):
                header["pattern"] = line[8:].strip()
        return header

    def _parse_jsdoc_header(self, jsdoc: str) -> Dict[str, Any]:
        """Parse @use/@requires/@pattern from JSDoc."""
        header = {}
        for line in jsdoc.split("\n"):
            line = line.strip().lstrip("*").strip()
            if line.startswith("@use"):
                header["use"] = line[4:].strip()
            elif line.startswith("@requires"):
                header["requires"] = line[9:].strip()
            elif line.startswith("@pattern"):
                header["pattern"] = line[8:].strip()
        return header
