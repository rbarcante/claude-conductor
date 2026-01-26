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
Skills command - 100% scriptable.

Manages and explores skills from the skill registry.
Operations: list, info, enable, disable
"""

from pathlib import Path
from typing import Dict, Any, List
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.json_manager import JsonManager
from lib.file_resolver import FileResolver
from lib.formatters import Formatters


def handle(args) -> Dict[str, Any]:
    """Handle skills subcommands."""
    project_root = args.project_root
    plugin_root = getattr(args, "plugin_root", None)

    if args.subcommand == "list":
        return list_skills(project_root, plugin_root, show_disabled=args.show_disabled)
    elif args.subcommand == "info":
        return skill_info(project_root, plugin_root, args.name)
    elif args.subcommand == "enable":
        return enable_skill(project_root, plugin_root, args.name)
    elif args.subcommand == "disable":
        return disable_skill(project_root, plugin_root, args.name)
    else:
        # Default to list
        return list_skills(project_root, plugin_root, show_disabled=False)


def list_skills(
    project_root: Path, plugin_root: Path = None, show_disabled: bool = False
) -> Dict[str, Any]:
    """
    List all available skills.

    Args:
        project_root: Project root directory (for settings)
        plugin_root: Plugin root directory (for skills registry)
        show_disabled: Include disabled skills in output

    Returns JSON with:
    - skills: List of skill info dicts
    - disabled_skills: List of disabled skill names
    - summary: Count summary
    """
    json_mgr = JsonManager(project_root, plugin_root)
    resolver = FileResolver(project_root, plugin_root)

    # Read registry
    registry = json_mgr.read_skill_registry()
    if not registry:
        return {
            "success": False,
            "error": "Skill registry not found at skills/skill-registry.json",
        }

    # Read settings for disabled list
    settings = json_mgr.read_settings()
    disabled_skills = set(settings.get("disabledSkills", []))

    # Process skills
    skills_data = []
    for skill in registry.get("skills", []):
        name = skill.get("name", "")
        is_disabled = name in disabled_skills
        is_always_active = skill.get("activation", {}).get("always_active", False)

        # Skip disabled unless show_disabled is True
        if is_disabled and not show_disabled and not is_always_active:
            continue

        # Validate skill file exists
        skill_path = resolver.resolve_skill(name)
        skill_md_exists = False
        if skill_path:
            skill_md = skill_path / "SKILL.md"
            skill_md_exists = skill_md.exists()

        # Build activation summary
        activation = skill.get("activation", {})
        if is_always_active:
            activation_type = "always"
        elif activation.get("keywords") or activation.get("file_patterns"):
            activation_type = "auto"
        else:
            activation_type = "manual"

        # Determine effective status
        if is_always_active:
            status = "active"
        elif is_disabled:
            status = "disabled"
        else:
            status = "available"

        skills_data.append(
            {
                "name": name,
                "version": skill.get("version", "?"),
                "description": Formatters.truncate(skill.get("description", ""), 60),
                "status": status,
                "activation": activation_type,
                "valid": skill_md_exists,
                "always_active": is_always_active,
                "path": skill.get("path", ""),
            }
        )

    # Summary counts
    total = len(skills_data)
    active = sum(1 for s in skills_data if s["status"] == "active")
    available = sum(1 for s in skills_data if s["status"] == "available")
    disabled = sum(1 for s in skills_data if s["status"] == "disabled")

    return {
        "success": True,
        "data": {
            "skills": skills_data,
            "summary": {
                "total": total,
                "active": active,
                "available": available,
                "disabled": disabled,
            },
            "disabled_skills": list(disabled_skills),
        },
        "message": format_skills_list(skills_data),
    }


def skill_info(project_root: Path, plugin_root: Path, name: str) -> Dict[str, Any]:
    """
    Get detailed information about a skill.

    Args:
        project_root: Project root directory (for settings)
        plugin_root: Plugin root directory (for skills registry)
        name: Skill name to get info for

    Returns JSON with full skill data including manifest and SKILL.md content preview.
    """
    json_mgr = JsonManager(project_root, plugin_root)
    resolver = FileResolver(project_root, plugin_root)

    # Find skill in registry
    registry = json_mgr.read_skill_registry()
    if not registry:
        return {"success": False, "error": "Skill registry not found"}

    skill_data = None
    for skill in registry.get("skills", []):
        if skill.get("name") == name:
            skill_data = skill
            break

    if not skill_data:
        return {"success": False, "error": f"Skill '{name}' not found in registry"}

    # Check if disabled
    settings = json_mgr.read_settings()
    disabled_skills = settings.get("disabledSkills", [])
    is_disabled = name in disabled_skills
    is_always_active = skill_data.get("activation", {}).get("always_active", False)

    # Read manifest for full details
    manifest = json_mgr.read_skill_manifest(name)
    if manifest:
        # Merge registry data with manifest
        skill_data = {**skill_data, **manifest}

    # Check SKILL.md existence and get preview
    skill_path = resolver.resolve_skill(name)
    skill_md_preview = None
    if skill_path:
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()
            # Get first 500 chars as preview
            skill_md_preview = content[:500] + ("..." if len(content) > 500 else "")

    result = {
        "name": skill_data.get("name"),
        "version": skill_data.get("version"),
        "description": skill_data.get("description"),
        "path": skill_data.get("path"),
        "enabled": not is_disabled or is_always_active,
        "always_active": is_always_active,
        "activation": skill_data.get("activation", {}),
        "provides": skill_data.get("provides", {}),
        "dependencies": skill_data.get("dependencies", []),
        "skill_md_exists": skill_md_preview is not None,
        "preview": skill_md_preview,
    }

    return {
        "success": True,
        "data": result,
        "message": Formatters.skill_info(skill_data, enabled=not is_disabled),
    }


def enable_skill(project_root: Path, plugin_root: Path, name: str) -> Dict[str, Any]:
    """
    Enable a skill by removing from disabledSkills.

    Args:
        project_root: Project root directory (for settings)
        plugin_root: Plugin root directory (for skills registry)
        name: Skill name to enable

    Returns updated settings.
    """
    json_mgr = JsonManager(project_root, plugin_root)

    # Verify skill exists
    registry = json_mgr.read_skill_registry()
    if not registry:
        return {"success": False, "error": "Skill registry not found"}

    skill_exists = any(s.get("name") == name for s in registry.get("skills", []))
    if not skill_exists:
        return {"success": False, "error": f"Skill '{name}' not found in registry"}

    # Check if already enabled
    settings = json_mgr.read_settings()
    disabled = settings.get("disabledSkills", [])

    if name not in disabled:
        return {
            "success": True,
            "data": {"was_enabled": True},
            "message": f"Skill '{name}' is already enabled",
        }

    # Update settings
    updated = json_mgr.update_disabled_skills(name, disable=False)

    return {
        "success": True,
        "data": {
            "skill": name,
            "action": "enabled",
            "disabled_skills": updated.get("disabledSkills", []),
        },
        "message": Formatters.success(f"Skill '{name}' has been enabled"),
    }


def disable_skill(project_root: Path, plugin_root: Path, name: str) -> Dict[str, Any]:
    """
    Disable a skill by adding to disabledSkills.

    Args:
        project_root: Project root directory (for settings)
        plugin_root: Plugin root directory (for skills registry)
        name: Skill name to disable

    Returns updated settings. Note: always_active skills cannot be disabled.
    """
    json_mgr = JsonManager(project_root, plugin_root)

    # Verify skill exists and check if always_active
    registry = json_mgr.read_skill_registry()
    if not registry:
        return {"success": False, "error": "Skill registry not found"}

    skill_data = None
    for skill in registry.get("skills", []):
        if skill.get("name") == name:
            skill_data = skill
            break

    if not skill_data:
        return {"success": False, "error": f"Skill '{name}' not found in registry"}

    # Check if always_active
    if skill_data.get("activation", {}).get("always_active", False):
        return {
            "success": False,
            "error": f"Skill '{name}' is always-active and cannot be disabled",
        }

    # Check if already disabled
    settings = json_mgr.read_settings()
    disabled = settings.get("disabledSkills", [])

    if name in disabled:
        return {
            "success": True,
            "data": {"was_disabled": True},
            "message": f"Skill '{name}' is already disabled",
        }

    # Update settings
    updated = json_mgr.update_disabled_skills(name, disable=True)

    return {
        "success": True,
        "data": {
            "skill": name,
            "action": "disabled",
            "disabled_skills": updated.get("disabledSkills", []),
        },
        "message": Formatters.success(f"Skill '{name}' has been disabled"),
    }


def format_skills_list(skills: List[Dict[str, Any]]) -> str:
    """Format skills list for human-readable output."""
    if not skills:
        return "No skills found."

    columns = ["name", "status", "activation", "version"]
    headers = {
        "name": "Skill",
        "status": "Status",
        "activation": "Activation",
        "version": "Version",
    }

    return Formatters.table(skills, columns, headers)
