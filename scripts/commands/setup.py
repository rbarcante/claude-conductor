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
Setup command - 50% scriptable.

Project setup operations including detection, scaffolding, and template management.
LLM still needed for product.md and tech-stack.md content generation.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.file_resolver import FileResolver
from lib.json_manager import JsonManager
from lib.formatters import Formatters

# Project type indicators (file -> detected stack info)
PROJECT_INDICATORS = {
    # Node.js / JavaScript
    "package.json": {"language": "javascript", "ecosystem": "node"},
    "package-lock.json": {"language": "javascript", "ecosystem": "node"},
    "yarn.lock": {"language": "javascript", "ecosystem": "node"},
    "pnpm-lock.yaml": {"language": "javascript", "ecosystem": "node"},
    # TypeScript
    "tsconfig.json": {"language": "typescript", "ecosystem": "node"},
    # Python
    "requirements.txt": {"language": "python", "ecosystem": "pip"},
    "pyproject.toml": {"language": "python", "ecosystem": "pip"},
    "setup.py": {"language": "python", "ecosystem": "pip"},
    "Pipfile": {"language": "python", "ecosystem": "pipenv"},
    "poetry.lock": {"language": "python", "ecosystem": "poetry"},
    # Go
    "go.mod": {"language": "go", "ecosystem": "go-modules"},
    "go.sum": {"language": "go", "ecosystem": "go-modules"},
    # Rust
    "Cargo.toml": {"language": "rust", "ecosystem": "cargo"},
    "Cargo.lock": {"language": "rust", "ecosystem": "cargo"},
    # Java / JVM
    "pom.xml": {"language": "java", "ecosystem": "maven"},
    "build.gradle": {"language": "java", "ecosystem": "gradle"},
    "build.gradle.kts": {"language": "kotlin", "ecosystem": "gradle"},
    # .NET
    "*.csproj": {"language": "csharp", "ecosystem": "dotnet"},
    "*.sln": {"language": "csharp", "ecosystem": "dotnet"},
    # Ruby
    "Gemfile": {"language": "ruby", "ecosystem": "bundler"},
    "Gemfile.lock": {"language": "ruby", "ecosystem": "bundler"},
    # PHP
    "composer.json": {"language": "php", "ecosystem": "composer"},
    # Dart/Flutter
    "pubspec.yaml": {"language": "dart", "ecosystem": "pub"},
}

# Framework detection patterns (file content or structure patterns)
FRAMEWORK_PATTERNS = {
    # Frontend
    "react": ["react", "react-dom", "next", "gatsby", "create-react-app"],
    "vue": ["vue", "nuxt", "vite"],
    "angular": ["@angular/core", "angular.json"],
    "svelte": ["svelte", "sveltekit"],
    # Backend (Node)
    "express": ["express"],
    "fastify": ["fastify"],
    "nestjs": ["@nestjs/core"],
    # Backend (Python)
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    # Backend (Go)
    "gin": ["github.com/gin-gonic/gin"],
    "echo": ["github.com/labstack/echo"],
    "fiber": ["github.com/gofiber/fiber"],
    # Backend (Java)
    "spring": ["spring-boot", "org.springframework"],
    # Mobile
    "react-native": ["react-native"],
    "flutter": ["flutter"],
}

# Source code file extensions to language mapping
# Used for brownfield detection when no manifest files are present
SOURCE_CODE_EXTENSIONS = {
    # Python
    ".py": "python",
    # JavaScript
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    # TypeScript
    ".ts": "typescript",
    ".tsx": "typescript",
    # Java
    ".java": "java",
    # Go
    ".go": "go",
    # Rust
    ".rs": "rust",
    # Ruby
    ".rb": "ruby",
    # PHP
    ".php": "php",
    # C#
    ".cs": "csharp",
    # Dart
    ".dart": "dart",
    # C/C++
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
}

# Language to styleguide mapping
LANGUAGE_STYLEGUIDES = {
    "javascript": "javascript.md",
    "typescript": "typescript.md",
    "python": "python.md",
    "go": "go.md",
    "java": "java.md",
    "csharp": "csharp.md",
    "dart": "dart.md",
    "html": "html-css.md",
    "css": "html-css.md",
    "general": "general.md",
}


def handle(args) -> Dict[str, Any]:
    """Handle setup subcommands."""
    project_root = args.project_root

    if args.subcommand == "detect":
        return detect(project_root)
    elif args.subcommand == "scaffold":
        return scaffold(project_root)
    elif args.subcommand == "state":
        if args.get:
            return get_state(project_root)
        elif args.set:
            return set_state(project_root, args.set)
        else:
            return get_state(project_root)
    elif args.subcommand == "copy-templates":
        languages = getattr(args, "languages", None) or []
        return copy_templates(project_root, languages)
    else:
        return {
            "success": False,
            "error": "No subcommand specified. Use: detect, scaffold, state, or copy-templates",
        }


def detect(project_root: Path) -> Dict[str, Any]:
    """
    Detect project type and tech stack.

    Scans for common project files to determine:
    - Project type (greenfield vs brownfield)
    - Primary language(s)
    - Package ecosystem
    - Detected frameworks

    Args:
        project_root: Project root directory

    Returns:
        Dict with detected stack information
    """
    project_root = Path(project_root)

    detected = {
        "project_type": "greenfield",  # Default to greenfield
        "languages": [],
        "ecosystems": [],
        "frameworks": [],
        "indicators_found": [],
    }

    # Check for project indicators
    for indicator, info in PROJECT_INDICATORS.items():
        if indicator.startswith("*"):
            # Glob pattern
            pattern = indicator
            matches = list(project_root.glob(pattern))
            if matches:
                detected["project_type"] = "brownfield"
                detected["indicators_found"].append(matches[0].name)
                if info["language"] not in detected["languages"]:
                    detected["languages"].append(info["language"])
                if info["ecosystem"] not in detected["ecosystems"]:
                    detected["ecosystems"].append(info["ecosystem"])
        else:
            # Exact file
            if (project_root / indicator).exists():
                detected["project_type"] = "brownfield"
                detected["indicators_found"].append(indicator)
                if info["language"] not in detected["languages"]:
                    detected["languages"].append(info["language"])
                if info["ecosystem"] not in detected["ecosystems"]:
                    detected["ecosystems"].append(info["ecosystem"])

    # Detect source code files (for brownfield detection without manifest files)
    if detected["project_type"] == "greenfield":
        source_languages = _detect_source_files(project_root)
        if source_languages:
            detected["project_type"] = "brownfield"
            detected["indicators_found"].append("source_code_files")
            for lang in source_languages:
                if lang not in detected["languages"]:
                    detected["languages"].append(lang)

    # Detect frameworks from package files
    frameworks = _detect_frameworks(project_root)
    detected["frameworks"] = frameworks

    # Add some source code metrics
    code_stats = _get_code_stats(project_root)
    detected["code_stats"] = code_stats

    # Determine primary language
    if detected["languages"]:
        detected["primary_language"] = detected["languages"][0]
    else:
        detected["primary_language"] = None

    # Check if conductor is already set up
    conductor_dir = project_root / "conductor"
    detected["conductor_exists"] = conductor_dir.exists()

    # Format message
    if detected["project_type"] == "greenfield":
        message = "Detected greenfield project (no existing project files found)"
    else:
        langs = ", ".join(detected["languages"]) if detected["languages"] else "unknown"
        message = f"Detected brownfield project: {langs}"
        if detected["frameworks"]:
            message += f" with {', '.join(detected['frameworks'])}"

    return {"success": True, "data": detected, "message": message}


def scaffold(project_root: Path) -> Dict[str, Any]:
    """
    Create conductor directory structure.

    Creates:
    - conductor/product.md (empty template)
    - conductor/tech-stack.md (empty template)
    - conductor/workflow.md (from templates/workflow.md if exists)
    - conductor/tracks.md (empty with header)
    - conductor/tracks/ directory

    Args:
        project_root: Project root directory

    Returns:
        Dict with created files list
    """
    project_root = Path(project_root)
    conductor_dir = project_root / "conductor"
    tracks_dir = conductor_dir / "tracks"

    created_files = []
    skipped_files = []

    # Create directories
    conductor_dir.mkdir(parents=True, exist_ok=True)
    tracks_dir.mkdir(parents=True, exist_ok=True)

    # Create product.md
    product_path = conductor_dir / "product.md"
    if not product_path.exists():
        product_path.write_text(_create_product_template())
        created_files.append("conductor/product.md")
    else:
        skipped_files.append("conductor/product.md")

    # Create tech-stack.md
    tech_stack_path = conductor_dir / "tech-stack.md"
    if not tech_stack_path.exists():
        tech_stack_path.write_text(_create_tech_stack_template())
        created_files.append("conductor/tech-stack.md")
    else:
        skipped_files.append("conductor/tech-stack.md")

    # Create workflow.md (copy from template if exists)
    workflow_path = conductor_dir / "workflow.md"
    if not workflow_path.exists():
        template_workflow = project_root / "templates" / "workflow.md"
        if template_workflow.exists():
            shutil.copy(template_workflow, workflow_path)
        else:
            workflow_path.write_text(_create_workflow_template())
        created_files.append("conductor/workflow.md")
    else:
        skipped_files.append("conductor/workflow.md")

    # Create tracks.md
    tracks_path = conductor_dir / "tracks.md"
    if not tracks_path.exists():
        tracks_path.write_text(_create_tracks_template())
        created_files.append("conductor/tracks.md")
    else:
        skipped_files.append("conductor/tracks.md")

    # Create index.md
    index_path = conductor_dir / "index.md"
    if not index_path.exists():
        index_path.write_text(_create_index_template())
        created_files.append("conductor/index.md")
    else:
        skipped_files.append("conductor/index.md")

    return {
        "success": True,
        "data": {
            "conductor_dir": "conductor/",
            "created_files": created_files,
            "skipped_files": skipped_files,
            "tracks_dir": "conductor/tracks/",
        },
        "message": Formatters.success(
            f"Scaffolded conductor directory with {len(created_files)} files"
            + (
                f" ({len(skipped_files)} skipped - already exist)"
                if skipped_files
                else ""
            )
        ),
    }


def get_state(project_root: Path) -> Dict[str, Any]:
    """
    Get current setup state.

    Args:
        project_root: Project root directory

    Returns:
        Dict with current state
    """
    json_mgr = JsonManager(project_root)
    state = json_mgr.read_setup_state()

    return {
        "success": True,
        "data": state,
        "message": f"Setup state: {state.get('last_successful_step', 'not started')}",
    }


def set_state(project_root: Path, step: str) -> Dict[str, Any]:
    """
    Set setup state to a specific step.

    Args:
        project_root: Project root directory
        step: Step name to set

    Returns:
        Dict with updated state
    """
    json_mgr = JsonManager(project_root)

    state = {"last_successful_step": step, "updated_at": _get_timestamp()}

    json_mgr.write_setup_state(state)

    return {
        "success": True,
        "data": state,
        "message": Formatters.success(f"Setup state updated to: {step}"),
    }


def copy_templates(project_root: Path, languages: List[str]) -> Dict[str, Any]:
    """
    Copy code styleguide templates for specified languages.

    Copies from templates/code_styleguides/ to conductor/code_styleguides/

    Args:
        project_root: Project root directory
        languages: List of language names

    Returns:
        Dict with copied files
    """
    project_root = Path(project_root)
    source_dir = project_root / "templates" / "code_styleguides"
    dest_dir = project_root / "conductor" / "code_styleguides"

    if not source_dir.exists():
        return {
            "success": False,
            "error": "Templates directory not found at templates/code_styleguides/",
        }

    if not languages:
        return {
            "success": False,
            "error": "No languages specified. Use --languages to specify which styleguides to copy.",
        }

    # Create destination directory
    dest_dir.mkdir(parents=True, exist_ok=True)

    copied_files = []
    not_found = []

    for lang in languages:
        lang_lower = lang.lower()

        # Get styleguide filename
        if lang_lower in LANGUAGE_STYLEGUIDES:
            filename = LANGUAGE_STYLEGUIDES[lang_lower]
        else:
            # Try direct match
            filename = f"{lang_lower}.md"

        source_file = source_dir / filename
        dest_file = dest_dir / filename

        if source_file.exists():
            if not dest_file.exists():
                shutil.copy(source_file, dest_file)
                copied_files.append(filename)
            else:
                # Already exists, skip but note it
                copied_files.append(f"{filename} (already exists)")
        else:
            not_found.append(lang)

    result = {
        "success": True,
        "data": {
            "copied": copied_files,
            "not_found": not_found,
            "dest_dir": "conductor/code_styleguides/",
        },
    }

    if not_found:
        result["message"] = Formatters.warning(
            f"Copied {len(copied_files)} styleguides. Not found: {', '.join(not_found)}"
        )
    else:
        result["message"] = Formatters.success(
            f"Copied {len(copied_files)} styleguides to conductor/code_styleguides/"
        )

    return result


def _detect_frameworks(project_root: Path) -> List[str]:
    """Detect frameworks from package files."""
    frameworks = []

    # Check package.json for Node.js projects
    package_json = project_root / "package.json"
    if package_json.exists():
        try:
            import json

            with open(package_json) as f:
                pkg = json.load(f)

            deps = {}
            deps.update(pkg.get("dependencies", {}))
            deps.update(pkg.get("devDependencies", {}))

            for framework, indicators in FRAMEWORK_PATTERNS.items():
                for indicator in indicators:
                    if indicator in deps:
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
        except Exception:
            pass

    # Check requirements.txt for Python projects
    requirements_txt = project_root / "requirements.txt"
    if requirements_txt.exists():
        try:
            content = requirements_txt.read_text().lower()
            for framework, indicators in FRAMEWORK_PATTERNS.items():
                for indicator in indicators:
                    if indicator.lower() in content:
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
        except Exception:
            pass

    # Check pyproject.toml for Python projects
    pyproject_toml = project_root / "pyproject.toml"
    if pyproject_toml.exists():
        try:
            content = pyproject_toml.read_text().lower()
            for framework, indicators in FRAMEWORK_PATTERNS.items():
                for indicator in indicators:
                    if indicator.lower() in content:
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
        except Exception:
            pass

    # Check go.mod for Go projects
    go_mod = project_root / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            for framework, indicators in FRAMEWORK_PATTERNS.items():
                for indicator in indicators:
                    if indicator in content:
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
        except Exception:
            pass

    # Check pom.xml for Java/Maven projects
    pom_xml = project_root / "pom.xml"
    if pom_xml.exists():
        try:
            content = pom_xml.read_text()
            for framework, indicators in FRAMEWORK_PATTERNS.items():
                for indicator in indicators:
                    if indicator in content:
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
        except Exception:
            pass

    return frameworks


def _get_code_stats(project_root: Path) -> Dict[str, Any]:
    """Get basic code statistics."""
    stats = {
        "directories": 0,
        "files": 0,
    }

    # Count directories and files (shallow, non-recursive for performance)
    try:
        for item in project_root.iterdir():
            if item.name.startswith("."):
                continue
            if item.name in (
                "node_modules",
                "venv",
                ".venv",
                "__pycache__",
                "target",
                "build",
                "dist",
            ):
                continue
            if item.is_dir():
                stats["directories"] += 1
            elif item.is_file():
                stats["files"] += 1
    except Exception:
        pass

    return stats


def _detect_source_files(project_root: Path) -> List[str]:
    """
    Detect source code files in the project.

    Scans top-level directory and src/ subdirectory for source code files.
    Returns list of detected languages based on file extensions.

    Args:
        project_root: Project root directory

    Returns:
        List of detected language names (e.g., ['python', 'javascript'])
    """
    detected_languages = []

    # Directories to skip
    skip_dirs = {
        "node_modules",
        "venv",
        ".venv",
        "__pycache__",
        "target",
        "build",
        "dist",
        "conductor",
    }

    def scan_directory(directory: Path, depth: int = 0):
        """Scan a directory for source files (max depth 1 for performance)."""
        if depth > 1:
            return
        try:
            for item in directory.iterdir():
                if item.name.startswith("."):
                    continue
                if item.is_file():
                    ext = item.suffix.lower()
                    if ext in SOURCE_CODE_EXTENSIONS:
                        lang = SOURCE_CODE_EXTENSIONS[ext]
                        if lang not in detected_languages:
                            detected_languages.append(lang)
                elif item.is_dir() and item.name not in skip_dirs:
                    # Scan subdirectories (only src/ and similar)
                    if item.name in ("src", "lib", "app", "source", "sources"):
                        scan_directory(item, depth + 1)
        except Exception:
            pass

    scan_directory(project_root)

    return detected_languages


def _create_product_template() -> str:
    """Create empty product.md template."""
    return """# Product Definition

> Define what you're building and why.

## Vision

<!-- One sentence describing the product vision -->

## Problem Statement

<!-- What problem does this solve? Who has this problem? -->

## Target Users

<!-- Who are the primary users? -->

## Success Criteria

<!-- How will we measure success? -->

## Core Features

<!-- List the main features -->

1. Feature 1
2. Feature 2
3. Feature 3

## Non-Goals

<!-- What is explicitly out of scope? -->

- Non-goal 1

## Constraints

<!-- Technical, business, or resource constraints -->

- Constraint 1

"""


def _create_tech_stack_template() -> str:
    """Create empty tech-stack.md template."""
    return """# Tech Stack

> Technical decisions and architecture for this project.

## Languages

<!-- Primary programming language(s) -->

- Language: (e.g., TypeScript, Python, Go)

## Frameworks

<!-- Main frameworks in use -->

- Framework: (e.g., React, Django, Gin)

## Database

<!-- Database choices -->

- Database: (e.g., PostgreSQL, MongoDB, SQLite)

## Infrastructure

<!-- Deployment and infrastructure -->

- Hosting: (e.g., Vercel, AWS, GCP)
- CI/CD: (e.g., GitHub Actions, CircleCI)

## Key Libraries

<!-- Important libraries and their purposes -->

| Library | Purpose |
|---------|---------|
| Library 1 | Purpose |

## Architecture Decisions

<!-- Document key architectural decisions -->

### Decision 1: [Title]

**Date:** YYYY-MM-DD

**Decision:** What was decided

**Rationale:** Why this decision was made

---

## Development Environment

### Prerequisites

- Prerequisite 1
- Prerequisite 2

### Setup

```bash
# Setup commands
```

"""


def _create_workflow_template() -> str:
    """Create basic workflow.md template."""
    return """# Project Workflow

## Task Workflow

1. Select task from plan.md
2. Mark as in-progress [~]
3. Write failing tests (TDD)
4. Implement to pass tests
5. Verify coverage
6. Commit with message
7. Mark as complete [x]

## Quality Gates

- All tests pass
- Code coverage >80%
- No linting errors
- Documentation updated

## Commit Format

```
<type>(<scope>): <description>
```

Types: feat, fix, docs, style, refactor, test, chore

"""


def _create_tracks_template() -> str:
    """Create empty tracks.md template."""
    return """# Tracks Registry

> This file tracks all development tracks (features, bugfixes, refactors, etc.)

## Active Tracks

_No active tracks._

---

## Completed Tracks

_No completed tracks._

"""


def _create_index_template() -> str:
    """Create conductor index.md template."""
    return """# Conductor Index

> Central navigation for all Conductor documentation.

## Project Documentation

- [Product Definition](./product.md) - What we're building and why
- [Tech Stack](./tech-stack.md) - Technical architecture and decisions
- [Workflow](./workflow.md) - Development processes and guidelines

## Tracks

- [Tracks Registry](./tracks.md) - All development tracks
- [Tracks Directory](./tracks/) - Individual track folders

## Settings

- [Settings](./settings.json) - Project-level Conductor settings

"""


def _get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    from datetime import datetime

    return datetime.utcnow().isoformat() + "Z"
