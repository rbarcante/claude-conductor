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
JSON file operations for Conductor CLI.

Provides safe read/write operations for JSON configuration files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class JsonManager:
    """Manages JSON file operations with safe read/write."""

    def __init__(self, project_root: Path, plugin_root: Optional[Path] = None):
        """
        Initialize with project root and optional plugin root.

        Args:
            project_root: Root directory of the user's project (conductor/ files)
            plugin_root: Root directory of the plugin (skills/ files)
                        If not provided, defaults to project_root for backward compatibility
        """
        self.project_root = Path(project_root).resolve()
        self.plugin_root = Path(plugin_root).resolve() if plugin_root else self.project_root

    def read(self, path: Path) -> Optional[Dict[str, Any]]:
        """
        Read a JSON file.

        Args:
            path: Path to JSON file (absolute or relative to project root)

        Returns:
            Parsed JSON as dict or None if file doesn't exist
        """
        full_path = self._resolve_path(path)
        if not full_path.exists():
            return None

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    def write(self, path: Path, data: Dict[str, Any], indent: int = 2) -> bool:
        """
        Write data to a JSON file.

        Args:
            path: Path to JSON file
            data: Data to write
            indent: JSON indentation level

        Returns:
            True if successful
        """
        full_path = self._resolve_path(path)

        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            return True
        except Exception:
            return False

    def read_skill_registry(self) -> Optional[Dict[str, Any]]:
        """Read the skill registry file (from plugin root)."""
        return self._read_plugin_file(Path('skills/skill-registry.json'))

    def read_skill_manifest(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Read a skill's manifest.json file (from plugin root)."""
        return self._read_plugin_file(Path(f'skills/{skill_name}/manifest.json'))

    def _read_plugin_file(self, path: Path) -> Optional[Dict[str, Any]]:
        """
        Read a JSON file from the plugin root.

        Args:
            path: Path relative to plugin root

        Returns:
            Parsed JSON as dict or None if file doesn't exist
        """
        full_path = self.plugin_root / path
        if not full_path.exists():
            return None

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    def read_settings(self) -> Dict[str, Any]:
        """
        Read conductor settings, creating default if missing.

        Returns:
            Settings dict with at least 'disabledSkills' array
        """
        settings = self.read(Path('conductor/settings.json'))
        if settings is None:
            settings = {
                'version': '1.0.0',
                'disabledSkills': []
            }
        return settings

    def write_settings(self, settings: Dict[str, Any]) -> bool:
        """Write conductor settings."""
        return self.write(Path('conductor/settings.json'), settings)

    def read_setup_state(self) -> Dict[str, Any]:
        """Read setup state file."""
        state = self.read(Path('conductor/setup_state.json'))
        if state is None:
            state = {'last_successful_step': None}
        return state

    def write_setup_state(self, state: Dict[str, Any]) -> bool:
        """Write setup state file."""
        return self.write(Path('conductor/setup_state.json'), state)

    def read_track_metadata(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Read a track's metadata.json file."""
        return self.read(Path(f'conductor/tracks/{track_id}/metadata.json'))

    def write_track_metadata(self, track_id: str, metadata: Dict[str, Any]) -> bool:
        """Write a track's metadata.json file."""
        return self.write(Path(f'conductor/tracks/{track_id}/metadata.json'), metadata)

    def create_track_metadata(
        self,
        track_id: str,
        track_type: str,
        description: str,
        status: str = 'new'
    ) -> Dict[str, Any]:
        """
        Create metadata structure for a new track.

        Args:
            track_id: Track identifier
            track_type: Type (feature, bugfix, refactor, docs, chore)
            description: Track description
            status: Initial status

        Returns:
            Metadata dict
        """
        now = datetime.utcnow().isoformat() + 'Z'
        return {
            'track_id': track_id,
            'type': track_type,
            'status': status,
            'created_at': now,
            'updated_at': now,
            'description': description
        }

    def update_disabled_skills(self, skill_name: str, disable: bool) -> Dict[str, Any]:
        """
        Update the disabled skills list.

        Args:
            skill_name: Skill to enable/disable
            disable: True to disable, False to enable

        Returns:
            Updated settings dict
        """
        settings = self.read_settings()
        disabled = settings.get('disabledSkills', [])

        if disable:
            # Add to disabled list if not already there
            if skill_name not in disabled:
                disabled.append(skill_name)
        else:
            # Remove from disabled list
            disabled = [s for s in disabled if s != skill_name]

        settings['disabledSkills'] = disabled
        self.write_settings(settings)
        return settings

    def _resolve_path(self, path: Path) -> Path:
        """Resolve path relative to project root."""
        path = Path(path)
        if path.is_absolute():
            return path
        return self.project_root / path
