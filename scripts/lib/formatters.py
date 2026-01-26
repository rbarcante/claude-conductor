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
Output formatting utilities for Conductor CLI.

Provides consistent formatting for tables, status displays, and JSON output.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path


class Formatters:
    """Output formatting utilities."""

    # Status symbols
    STATUS_SYMBOLS = {
        "completed": "✓",
        "in_progress": "~",
        "pending": "○",
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ",
    }

    # Status colors (ANSI codes)
    COLORS = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "gray": "\033[90m",
        "reset": "\033[0m",
        "bold": "\033[1m",
    }

    @classmethod
    def status_symbol(cls, status: str, use_color: bool = True) -> str:
        """Get formatted status symbol."""
        symbol = cls.STATUS_SYMBOLS.get(status, "?")

        if not use_color:
            return symbol

        color = ""
        if status in ("completed", "success"):
            color = cls.COLORS["green"]
        elif status in ("in_progress", "warning"):
            color = cls.COLORS["yellow"]
        elif status == "error":
            color = cls.COLORS["red"]
        elif status == "pending":
            color = cls.COLORS["gray"]

        if color:
            return f"{color}{symbol}{cls.COLORS['reset']}"
        return symbol

    @classmethod
    def table(
        cls,
        data: List[Dict[str, Any]],
        columns: List[str] = None,
        headers: Dict[str, str] = None,
        max_width: int = 80,
    ) -> str:
        """
        Format data as an ASCII table.

        Args:
            data: List of row dicts
            columns: Column keys in order (default: all keys)
            headers: Display names for columns
            max_width: Maximum table width

        Returns:
            Formatted table string
        """
        if not data:
            return "(no data)"

        if columns is None:
            columns = list(data[0].keys())

        if headers is None:
            headers = {col: col.replace("_", " ").title() for col in columns}

        # Calculate column widths
        widths = {}
        for col in columns:
            header = headers.get(col, col)
            widths[col] = len(header)
            for row in data:
                val = str(row.get(col, ""))
                widths[col] = max(widths[col], len(val))

        # Build table
        lines = []

        # Header
        header_cells = [headers.get(col, col).ljust(widths[col]) for col in columns]
        lines.append("  ".join(header_cells))

        # Separator
        lines.append("  ".join("-" * widths[col] for col in columns))

        # Rows
        for row in data:
            cells = [str(row.get(col, "")).ljust(widths[col]) for col in columns]
            lines.append("  ".join(cells))

        return "\n".join(lines)

    @classmethod
    def progress_bar(cls, completed: int, total: int, width: int = 30) -> str:
        """
        Create an ASCII progress bar.

        Args:
            completed: Completed count
            total: Total count
            width: Bar width in characters

        Returns:
            Progress bar string like "[████████░░░░░░] 50%"
        """
        if total == 0:
            return f"[{'░' * width}] 0%"

        percent = (completed / total) * 100
        filled = int(width * completed / total)
        empty = width - filled

        return f"[{'█' * filled}{'░' * empty}] {percent:.0f}%"

    @classmethod
    def metrics_summary(cls, metrics: Dict[str, Any]) -> str:
        """
        Format metrics as a summary block.

        Args:
            metrics: Dict with 'total', 'completed', 'in_progress', 'pending'

        Returns:
            Formatted summary string
        """
        total = metrics.get("total", 0)
        completed = metrics.get("completed", 0)
        in_progress = metrics.get("in_progress", 0)
        pending = metrics.get("pending", 0)

        progress = cls.progress_bar(completed, total)
        percent = (completed / total * 100) if total > 0 else 0

        lines = [
            f"Progress: {progress}",
            f"",
            f"  {cls.status_symbol('completed')} Completed:   {completed}",
            f"  {cls.status_symbol('in_progress')} In Progress: {in_progress}",
            f"  {cls.status_symbol('pending')} Pending:     {pending}",
            f"  ─────────────",
            f"  Total:       {total}",
        ]

        return "\n".join(lines)

    @classmethod
    def track_list(cls, tracks: List[Dict[str, Any]]) -> str:
        """
        Format track list for display.

        Args:
            tracks: List of track dicts with 'description', 'status', 'path'

        Returns:
            Formatted track list
        """
        if not tracks:
            return "(no tracks)"

        lines = []
        for track in tracks:
            status = track.get("status", "pending")
            desc = track.get("description", "Unknown")
            symbol = cls.status_symbol(status)
            lines.append(f"  {symbol} {desc}")

        return "\n".join(lines)

    @classmethod
    def skill_info(cls, skill: Dict[str, Any], enabled: bool = True) -> str:
        """
        Format detailed skill information.

        Args:
            skill: Skill dict from registry
            enabled: Whether skill is enabled

        Returns:
            Formatted skill info
        """
        lines = [
            f"{cls.COLORS['bold']}{skill.get('name', 'Unknown')}{cls.COLORS['reset']}",
            f"",
            f"  Version:     {skill.get('version', '?')}",
            f"  Path:        {skill.get('path', '?')}",
            f"  Status:      {'Enabled' if enabled else 'Disabled'}",
            f"",
            f"  Description:",
            f"    {skill.get('description', 'No description')}",
        ]

        activation = skill.get("activation", {})
        if activation:
            lines.append("")
            lines.append("  Activation:")
            if activation.get("always_active"):
                lines.append("    Always active")
            else:
                if activation.get("keywords"):
                    lines.append(
                        f"    Keywords: {', '.join(activation['keywords'][:5])}"
                    )
                if activation.get("file_patterns"):
                    lines.append(
                        f"    Files:    {', '.join(activation['file_patterns'][:3])}"
                    )

        provides = skill.get("provides", {})
        if provides:
            lines.append("")
            lines.append("  Provides:")
            for key, values in provides.items():
                if values:
                    lines.append(f"    {key}: {', '.join(values[:5])}")

        return "\n".join(lines)

    @classmethod
    def error(cls, message: str) -> str:
        """Format error message."""
        return f"{cls.COLORS['red']}{cls.STATUS_SYMBOLS['error']} Error: {message}{cls.COLORS['reset']}"

    @classmethod
    def success(cls, message: str) -> str:
        """Format success message."""
        return f"{cls.COLORS['green']}{cls.STATUS_SYMBOLS['success']} {message}{cls.COLORS['reset']}"

    @classmethod
    def warning(cls, message: str) -> str:
        """Format warning message."""
        return f"{cls.COLORS['yellow']}{cls.STATUS_SYMBOLS['warning']} {message}{cls.COLORS['reset']}"

    @classmethod
    def json_output(
        cls, data: Any, success: bool = True, error: str = None
    ) -> Dict[str, Any]:
        """
        Create standardized JSON output structure.

        Args:
            data: Output data
            success: Whether operation succeeded
            error: Error message if any

        Returns:
            Standardized output dict
        """
        result = {"success": success}

        if error:
            result["error"] = error
        elif data is not None:
            result["data"] = data

        return result

    @classmethod
    def truncate(cls, text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncate text to max length with suffix."""
        if len(text) <= max_length:
            return text
        return text[: max_length - len(suffix)] + suffix

    @classmethod
    def indent(cls, text: str, spaces: int = 2) -> str:
        """Indent all lines of text."""
        prefix = " " * spaces
        return "\n".join(prefix + line for line in text.split("\n"))

    @classmethod
    def bullet_list(cls, items: List[str], bullet: str = "•") -> str:
        """Format items as a bullet list."""
        return "\n".join(f"  {bullet} {item}" for item in items)

    @classmethod
    def numbered_list(cls, items: List[str]) -> str:
        """Format items as a numbered list."""
        return "\n".join(f"  {i+1}. {item}" for i, item in enumerate(items))
