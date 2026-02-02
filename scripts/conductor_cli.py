#!/usr/bin/env python3

# Copyright 2025 Ricardo Barcante
#
# Derived from Conductor for Gemini CLI (https://github.com/gemini-cli-extensions/conductor)
# Copyright 2024 Google LLC
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
#
# NOTICE: This file has been modified from the original.

"""
Conductor CLI - Token-efficient command dispatcher for Conductor plugin.

This CLI provides scriptable operations that reduce LLM token usage by
offloading mechanical tasks (file parsing, JSON manipulation, git operations)
to deterministic Python code.

Usage:
    python conductor_cli.py <command> [subcommand] [options]

Commands:
    skills      Manage and explore skills (list, info, enable, disable)
    status      Show project status and progress metrics
    patterns    Browse and search patterns (list, show, search)
    snippets    Browse and search code snippets
    newtrack    Create track structure (scaffold, metadata)
    setup       Project setup operations (detect, scaffold)
    revert      Git revert operations
    implement   Implementation helpers (parse, update-status)
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add lib to path for imports
SCRIPT_DIR = Path(__file__).parent
PLUGIN_ROOT = (
    SCRIPT_DIR.parent
)  # conductor_cli.py is in scripts/, plugin root is parent
sys.path.insert(0, str(SCRIPT_DIR))

from commands import (
    skills,
    status,
    patterns,
    snippets,
    newtrack,
    setup,
    revert,
    implement,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="conductor",
        description="Conductor CLI - Token-efficient command operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    # Plugin root: where plugin files (skills, patterns, snippets) are located
    # Defaults to: 1) CLAUDE_PLUGIN_ROOT env var, 2) parent of scripts/ directory
    default_plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", str(PLUGIN_ROOT)))
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=default_plugin_root,
        help="Plugin root directory for skills/patterns/snippets (default: CLAUDE_PLUGIN_ROOT or auto-detected)",
    )

    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Skills command
    skills_parser = subparsers.add_parser("skills", help="Manage and explore skills")
    skills_subparsers = skills_parser.add_subparsers(dest="subcommand")

    skills_list = skills_subparsers.add_parser("list", help="List all available skills")
    skills_list.add_argument(
        "--show-disabled", action="store_true", help="Include disabled skills"
    )

    skills_info = skills_subparsers.add_parser(
        "info", help="Show detailed skill information"
    )
    skills_info.add_argument("name", help="Skill name")

    skills_enable = skills_subparsers.add_parser("enable", help="Enable a skill")
    skills_enable.add_argument("name", help="Skill name to enable")

    skills_disable = skills_subparsers.add_parser("disable", help="Disable a skill")
    skills_disable.add_argument("name", help="Skill name to disable")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_subparsers = status_parser.add_subparsers(dest="subcommand")

    status_subparsers.add_parser("verify", help="Verify project setup")
    status_subparsers.add_parser("tracks", help="Parse all tracks with status")
    status_subparsers.add_parser("progress", help="Calculate progress metrics")
    status_subparsers.add_parser("full", help="Full status report (default)")

    # Patterns command
    patterns_parser = subparsers.add_parser(
        "patterns", help="Browse and search patterns"
    )
    patterns_subparsers = patterns_parser.add_subparsers(dest="subcommand")

    patterns_subparsers.add_parser("list", help="List all patterns")

    patterns_show = patterns_subparsers.add_parser("show", help="Show pattern content")
    patterns_show.add_argument("name", help="Pattern name")
    patterns_show.add_argument(
        "--ai-only", action="store_true", help="Extract AI Quick Reference only"
    )

    patterns_search = patterns_subparsers.add_parser("search", help="Search patterns")
    patterns_search.add_argument("query", help="Search query")

    # Snippets command
    snippets_parser = subparsers.add_parser(
        "snippets", help="Browse and search snippets"
    )
    snippets_subparsers = snippets_parser.add_subparsers(dest="subcommand")

    snippets_subparsers.add_parser("list", help="List all snippets")

    snippets_show = snippets_subparsers.add_parser("show", help="Show snippet content")
    snippets_show.add_argument("name", help="Snippet name (with or without extension)")
    snippets_show.add_argument("--language", "-l", help="Language hint")

    snippets_search = snippets_subparsers.add_parser("search", help="Search snippets")
    snippets_search.add_argument("query", help="Search query")

    # Newtrack command
    newtrack_parser = subparsers.add_parser("newtrack", help="Create track structure")
    newtrack_subparsers = newtrack_parser.add_subparsers(dest="subcommand")

    newtrack_id = newtrack_subparsers.add_parser(
        "generate-id", help="Generate track ID"
    )
    newtrack_id.add_argument("description", help="Track description")

    newtrack_scaffold = newtrack_subparsers.add_parser(
        "scaffold", help="Create track directory structure"
    )
    newtrack_scaffold.add_argument("track_id", help="Track ID")
    newtrack_scaffold.add_argument(
        "--type",
        choices=["feature", "bugfix", "refactor", "docs", "chore"],
        default="feature",
    )
    newtrack_scaffold.add_argument(
        "--description", required=True, help="Track description"
    )

    newtrack_register = newtrack_subparsers.add_parser(
        "register", help="Register track in tracks.md"
    )
    newtrack_register.add_argument("track_id", help="Track ID")
    newtrack_register.add_argument(
        "--description", required=True, help="Track description"
    )

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Project setup operations")
    setup_subparsers = setup_parser.add_subparsers(dest="subcommand")

    setup_subparsers.add_parser("detect", help="Detect project type and tech stack")
    setup_subparsers.add_parser("scaffold", help="Create conductor directory structure")

    setup_state = setup_subparsers.add_parser("state", help="Manage setup state")
    setup_state.add_argument("--get", action="store_true", help="Get current state")
    setup_state.add_argument("--set", metavar="STEP", help="Set state to step")

    setup_templates = setup_subparsers.add_parser(
        "copy-templates", help="Copy template files"
    )
    setup_templates.add_argument(
        "--languages", nargs="+", help="Languages to copy styleguides for"
    )

    # Revert command
    revert_parser = subparsers.add_parser("revert", help="Git revert operations")
    revert_subparsers = revert_parser.add_subparsers(dest="subcommand")

    revert_commits = revert_subparsers.add_parser(
        "find-commits", help="Find commits for a track"
    )
    revert_commits.add_argument("track_id", help="Track ID")

    revert_plan = revert_subparsers.add_parser(
        "plan-updates", help="Find plan file updates"
    )
    revert_plan.add_argument("sha", help="Commit SHA")

    revert_list = revert_subparsers.add_parser(
        "build-list", help="Build revert commit list"
    )
    revert_list.add_argument("target", help="Target (track_id, phase, or task)")

    revert_exec = revert_subparsers.add_parser(
        "execute", help="Execute revert sequence"
    )
    revert_exec.add_argument("shas", nargs="+", help="Commit SHAs to revert")
    revert_exec.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )

    revert_subparsers.add_parser(
        "parse-registry", help="Parse tracks registry for menu"
    )

    # Implement command
    implement_parser = subparsers.add_parser("implement", help="Implementation helpers")
    implement_subparsers = implement_parser.add_subparsers(dest="subcommand")

    impl_parse = implement_subparsers.add_parser("parse-tracks", help="Parse tracks registry")
    impl_parse.add_argument("--track-id", help="Filter to specific track ID")
    impl_parse.add_argument("--status", choices=["pending", "in-progress", "completed"], help="Filter by status")

    impl_update = implement_subparsers.add_parser(
        "update-status", help="Update track status"
    )
    impl_update.add_argument("track_id", help="Track ID")
    impl_update.add_argument("status", choices=["pending", "in-progress", "completed"])

    impl_archive = implement_subparsers.add_parser("archive", help="Archive a track")
    impl_archive.add_argument("track_id", help="Track ID")

    implement_subparsers.add_parser(
        "modified-files", help="Get modified files from git"
    )

    impl_coverage = implement_subparsers.add_parser(
        "parse-coverage", help="Parse coverage report"
    )
    impl_coverage.add_argument(
        "--format", choices=["lcov", "cobertura", "json"], default="lcov"
    )
    impl_coverage.add_argument("--path", help="Path to coverage file")

    impl_adr = implement_subparsers.add_parser(
        "next-adr-number", help="Get next ADR number"
    )
    impl_adr.add_argument("--path", default="docs/decisions", help="ADR directory path")

    impl_patterns = implement_subparsers.add_parser(
        "match-patterns", help="Match patterns for keywords"
    )
    impl_patterns.add_argument("keywords", nargs="+", help="Keywords to match")

    impl_suggest_branch = implement_subparsers.add_parser(
        "suggest-branch", help="Suggest branch name for track"
    )
    impl_suggest_branch.add_argument("track_id", help="Track ID")

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch to appropriate command handler
    try:
        if args.command == "skills":
            result = skills.handle(args)
        elif args.command == "status":
            result = status.handle(args)
        elif args.command == "patterns":
            result = patterns.handle(args)
        elif args.command == "snippets":
            result = snippets.handle(args)
        elif args.command == "newtrack":
            result = newtrack.handle(args)
        elif args.command == "setup":
            result = setup.handle(args)
        elif args.command == "revert":
            result = revert.handle(args)
        elif args.command == "implement":
            result = implement.handle(args)
        else:
            parser.print_help()
            sys.exit(1)

        # Output result
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            # Pretty print for humans
            if isinstance(result, dict):
                if result.get("success", True):
                    if "data" in result:
                        print_formatted(result["data"])
                    elif "message" in result:
                        print(result["message"])
                else:
                    print(
                        f"Error: {result.get('error', 'Unknown error')}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            else:
                print(result)

    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_formatted(data):
    """Pretty print data for human consumption."""
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for k, v in item.items():
                    print(f"  {k}: {v}")
                print()
            else:
                print(f"  - {item}")
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (list, dict)):
                print(f"{k}:")
                print_formatted(v)
            else:
                print(f"  {k}: {v}")
    else:
        print(data)


if __name__ == "__main__":
    main()
