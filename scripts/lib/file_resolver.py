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
Universal File Resolution Protocol implementation.

Resolves file paths according to the Conductor file resolution protocol
defined in CLAUDE.md.
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any

# Only allow safe branch-name-like characters in track IDs
TRACK_ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def validate_track_id(track_id: str) -> None:
    """Validate that a track_id is safe for filesystem path construction.

    Raises:
        ValueError: If track_id contains path traversal or unsafe characters
    """
    if not track_id or ".." in track_id or "/" in track_id or "\\" in track_id:
        raise ValueError(f"Invalid track_id: {track_id!r}")
    if not TRACK_ID_PATTERN.match(track_id):
        raise ValueError(f"Invalid track_id: {track_id!r}")


class FileResolver:
    """Resolves files using the Universal File Resolution Protocol."""

    # Standard default paths for project context
    PROJECT_DEFAULTS = {
        "product_definition": "conductor/product.md",
        "tech_stack": "conductor/tech-stack.md",
        "workflow": "conductor/workflow.md",
        "product_guidelines": "conductor/product-guidelines.md",
        "tracks_directory": "conductor/tracks",
        "project_index": "conductor/index.md",
        "settings": "conductor/settings.json",
        "setup_state": "conductor/setup_state.json",
    }

    # Standard default paths for track context
    TRACK_DEFAULTS = {
        "specification": "spec.md",
        "implementation_plan": "plan.md",
        "metadata": "metadata.json",
        "index": "index.md",
        "decisions": "decisions.md",
    }

    # Pattern-related paths
    PATTERN_DEFAULTS = {
        "pattern_registry": "patterns/index.md",
        "core_patterns": "patterns/core",
        "stack_patterns": "patterns/stack",
        "pattern_template": "patterns/TEMPLATE.md",
    }

    # Skill-related paths
    SKILL_DEFAULTS = {
        "skill_registry": "skills/skill-registry.json",
        "skill_directory": "skills",
    }

    # Snippet-related paths
    SNIPPET_DEFAULTS = {
        "snippet_index": "snippets/index.md",
        "snippet_directory": "snippets",
    }

    def __init__(self, project_root: Path, plugin_root: Optional[Path] = None):
        """
        Initialize resolver with project root and optional plugin root.

        Args:
            project_root: Root directory of the user's project (conductor/ files)
            plugin_root: Root directory of the plugin (skills/, patterns/, snippets/)
                        If not provided, defaults to project_root for backward compatibility
        """
        self.project_root = Path(project_root).resolve()
        self.plugin_root = (
            Path(plugin_root).resolve() if plugin_root else self.project_root
        )

    def resolve_project_file(self, file_key: str) -> Optional[Path]:
        """
        Resolve a project-level file.

        Args:
            file_key: Key identifying the file (e.g., 'workflow', 'tech_stack')

        Returns:
            Resolved Path or None if not found
        """
        # First try reading from project index
        index_path = self.project_root / self.PROJECT_DEFAULTS["project_index"]
        if index_path.exists():
            link = self._find_link_in_index(index_path, file_key)
            if link:
                resolved = (index_path.parent / link).resolve()
                if resolved.exists():
                    return resolved

        # Fall back to default path
        # Project files use project_root, plugin files (patterns, skills, snippets) use plugin_root
        default_path = None
        if file_key in self.PROJECT_DEFAULTS:
            default_path = self.project_root / self.PROJECT_DEFAULTS[file_key]
        elif file_key in self.PATTERN_DEFAULTS:
            default_path = self.plugin_root / self.PATTERN_DEFAULTS[file_key]
        elif file_key in self.SKILL_DEFAULTS:
            default_path = self.plugin_root / self.SKILL_DEFAULTS[file_key]
        elif file_key in self.SNIPPET_DEFAULTS:
            default_path = self.plugin_root / self.SNIPPET_DEFAULTS[file_key]

        if default_path and default_path.exists():
            return default_path

        return None

    def resolve_track_file(self, track_id: str, file_key: str) -> Optional[Path]:
        """
        Resolve a track-level file.

        Args:
            track_id: Track identifier
            file_key: Key identifying the file (e.g., 'specification')

        Returns:
            Resolved Path or None if not found
        """
        track_dir = self.get_track_directory(track_id)
        if not track_dir:
            return None

        # Try reading from track index
        index_path = track_dir / "index.md"
        if index_path.exists():
            link = self._find_link_in_index(index_path, file_key)
            if link:
                resolved = (index_path.parent / link).resolve()
                if resolved.exists():
                    return resolved

        # Fall back to default path
        if file_key in self.TRACK_DEFAULTS:
            default_path = track_dir / self.TRACK_DEFAULTS[file_key]
            if default_path.exists():
                return default_path

        return None

    def get_track_directory(self, track_id: str) -> Optional[Path]:
        """
        Get the directory for a track.

        Args:
            track_id: Track identifier

        Returns:
            Path to track directory or None if not found

        Raises:
            ValueError: If track_id contains unsafe characters
        """
        validate_track_id(track_id)

        tracks_dir = self.resolve_project_file("tracks_directory")
        if not tracks_dir:
            tracks_dir = self.project_root / self.PROJECT_DEFAULTS["tracks_directory"]

        track_dir = tracks_dir / track_id
        if track_dir.exists():
            return track_dir

        return None

    def list_tracks(self) -> list[str]:
        """List all track IDs in the tracks directory."""
        tracks_dir = self.resolve_project_file("tracks_directory")
        if not tracks_dir or not tracks_dir.exists():
            return []

        return [d.name for d in tracks_dir.iterdir() if d.is_dir()]

    def _find_link_in_index(self, index_path: Path, key: str) -> Optional[str]:
        """
        Find a link in an index.md file by key.

        Looks for markdown links with labels matching the key.

        Args:
            index_path: Path to index.md
            key: Key to search for (will be converted to title case for matching)

        Returns:
            Link path or None
        """
        import re

        if not index_path.exists():
            return None

        content = index_path.read_text()

        # Convert key to various forms for matching
        search_terms = [
            key.replace("_", " ").title(),  # tracks_registry -> Tracks Registry
            key.replace("_", " "),  # tracks_registry -> tracks registry
            key,  # As-is
        ]

        # Look for markdown links: [Label](./path/to/file)
        for term in search_terms:
            pattern = rf"\[{re.escape(term)}\]\(([^)]+)\)"
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def resolve_pattern(self, pattern_name: str) -> Optional[Path]:
        """
        Resolve a pattern file path.

        Checks core/ first, then stack/ as fallback.
        Patterns are plugin files, so use plugin_root.

        Args:
            pattern_name: Pattern name (without .md extension)

        Returns:
            Path to pattern file or None
        """
        # Normalize name
        name = pattern_name.lower().replace(" ", "-")
        if not name.endswith(".md"):
            name = f"{name}.md"

        # Try core patterns first (plugin files use plugin_root)
        core_dir = self.plugin_root / self.PATTERN_DEFAULTS["core_patterns"]
        core_path = core_dir / name
        if core_path.exists():
            return core_path

        # Try stack patterns as fallback
        stack_dir = self.plugin_root / self.PATTERN_DEFAULTS["stack_patterns"]
        stack_path = stack_dir / name
        if stack_path.exists():
            return stack_path

        return None

    def resolve_skill(self, skill_name: str) -> Optional[Path]:
        """
        Resolve a skill directory path.

        Skills are plugin files, so use plugin_root.

        Args:
            skill_name: Skill name

        Returns:
            Path to skill directory or None
        """
        skills_dir = self.plugin_root / self.SKILL_DEFAULTS["skill_directory"]
        skill_dir = skills_dir / skill_name
        if skill_dir.exists():
            return skill_dir

        return None

    def resolve_snippet(
        self, snippet_name: str, language: Optional[str] = None
    ) -> Optional[Path]:
        """
        Resolve a snippet file path.

        Snippets are plugin files, so use plugin_root.

        Args:
            snippet_name: Snippet name (with or without extension)
            language: Optional language hint for disambiguation

        Returns:
            Path to snippet file or None
        """
        snippets_dir = self.plugin_root / self.SNIPPET_DEFAULTS["snippet_directory"]
        if not snippets_dir.exists():
            return None

        # If language specified, look in that subdirectory
        if language:
            lang_dir = snippets_dir / language.lower()
            if lang_dir.exists():
                # Try with and without extension
                for ext in ["", ".py", ".ts", ".js", ".java", ".go", ".md"]:
                    path = lang_dir / f"{snippet_name}{ext}"
                    if path.exists():
                        return path

        # Search all language directories
        for lang_dir in snippets_dir.iterdir():
            if lang_dir.is_dir():
                for file in lang_dir.iterdir():
                    if file.is_file() and file.stem == snippet_name:
                        return file

        return None

    def exists(self, file_key: str) -> bool:
        """Check if a project file exists."""
        return self.resolve_project_file(file_key) is not None

    def track_exists(self, track_id: str) -> bool:
        """Check if a track exists."""
        return self.get_track_directory(track_id) is not None
