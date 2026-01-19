"""
Tests for the command modules.
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from commands import skills, status, patterns, snippets, newtrack, setup, revert, implement


class MockArgs:
    """Mock arguments object for testing."""

    def __init__(self, **kwargs):
        self.project_root = kwargs.get('project_root', Path.cwd())
        self.subcommand = kwargs.get('subcommand')
        self.json = kwargs.get('json', False)
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def conductor_project(tmp_path):
    """Create a mock conductor project structure."""
    # Create directories
    (tmp_path / 'conductor').mkdir()
    (tmp_path / 'conductor' / 'tracks').mkdir()
    (tmp_path / 'skills').mkdir()
    (tmp_path / 'patterns').mkdir()
    (tmp_path / 'patterns' / 'core').mkdir()
    (tmp_path / 'snippets').mkdir()
    (tmp_path / 'snippets' / 'python').mkdir()

    # Create basic files
    (tmp_path / 'conductor' / 'product.md').write_text('# Product\nTest product')
    (tmp_path / 'conductor' / 'tech-stack.md').write_text('# Tech Stack\nPython')
    (tmp_path / 'conductor' / 'workflow.md').write_text('# Workflow\nTDD')
    (tmp_path / 'conductor' / 'tracks.md').write_text("""# Project Tracks

- [ ] **Track: Test feature**
  *Link: [./conductor/tracks/test_20260121/](./conductor/tracks/test_20260121/)*
""")

    # Create skill registry
    (tmp_path / 'skills' / 'skill-registry.json').write_text(json.dumps({
        'version': '1.0.0',
        'skills': [
            {
                'name': 'test-skill',
                'version': '1.0.0',
                'path': './test-skill',
                'description': 'A test skill',
                'activation': {
                    'keywords': ['test'],
                    'file_patterns': ['**/*.test.ts']
                }
            },
            {
                'name': 'always-active-skill',
                'version': '1.0.0',
                'path': './always-active-skill',
                'description': 'Always active',
                'activation': {
                    'always_active': True
                }
            }
        ]
    }))

    # Create skill directories
    (tmp_path / 'skills' / 'test-skill').mkdir()
    (tmp_path / 'skills' / 'test-skill' / 'SKILL.md').write_text('# Test Skill')
    (tmp_path / 'skills' / 'always-active-skill').mkdir()
    (tmp_path / 'skills' / 'always-active-skill' / 'SKILL.md').write_text('# Always Active')

    # Create pattern index
    (tmp_path / 'patterns' / 'index.md').write_text("""# Pattern Registry

## Core Patterns

| Pattern | Category | Description |
|---------|----------|-------------|
| [Error Handling](./core/error-handling.md) | Resilience | Error handling patterns |
| [Validation](./core/validation.md) | Input | Input validation |
""")

    # Create a pattern file
    (tmp_path / 'patterns' / 'core' / 'error-handling.md').write_text("""---
name: Error Handling
category: Resilience
tags: [errors, exceptions]
activation:
  keywords: [error, exception, catch]
---
# Error Handling

## AI Quick Reference
Quick tips for error handling.

## Implementation
Detailed implementation guide.
""")

    # Create snippet
    (tmp_path / 'snippets' / 'index.md').write_text("""# Snippets

## Python
- [api-client](./python/api-client.py) - HTTP client
""")

    (tmp_path / 'snippets' / 'python' / 'api-client.py').write_text('''"""
USE: When building an API client
REQUIRES: httpx>=0.24
PATTERN: Error Handling
"""

import httpx

def make_request():
    pass
''')

    # Create track directory
    track_dir = tmp_path / 'conductor' / 'tracks' / 'test_20260121'
    track_dir.mkdir()
    (track_dir / 'metadata.json').write_text(json.dumps({
        'track_id': 'test_20260121',
        'type': 'feature',
        'status': 'new',
        'created_at': '2026-01-21T00:00:00Z',
        'updated_at': '2026-01-21T00:00:00Z',
        'description': 'Test feature'
    }))
    (track_dir / 'plan.md').write_text("""# Phase 1: Setup

- [x] Task: Setup project
- [ ] Task: Write tests
- [~] Task: Implement feature
""")

    return tmp_path


class TestSkillsCommand:
    """Tests for skills command."""

    def test_list_skills(self, conductor_project):
        """Test listing skills."""
        args = MockArgs(project_root=conductor_project, subcommand='list', show_disabled=False)
        result = skills.handle(args)

        assert result['success'] is True
        assert 'skills' in result['data']
        assert len(result['data']['skills']) == 2

    def test_skill_info(self, conductor_project):
        """Test getting skill info."""
        args = MockArgs(project_root=conductor_project, subcommand='info', name='test-skill')
        result = skills.handle(args)

        assert result['success'] is True
        assert result['data']['name'] == 'test-skill'

    def test_skill_not_found(self, conductor_project):
        """Test skill not found error."""
        args = MockArgs(project_root=conductor_project, subcommand='info', name='nonexistent')
        result = skills.handle(args)

        assert result['success'] is False
        assert 'not found' in result['error']

    def test_disable_skill(self, conductor_project):
        """Test disabling a skill."""
        args = MockArgs(project_root=conductor_project, subcommand='disable', name='test-skill')
        result = skills.handle(args)

        assert result['success'] is True
        assert 'test-skill' in result['data']['disabled_skills']

    def test_cannot_disable_always_active(self, conductor_project):
        """Test that always-active skills cannot be disabled."""
        args = MockArgs(project_root=conductor_project, subcommand='disable', name='always-active-skill')
        result = skills.handle(args)

        assert result['success'] is False
        assert 'cannot be disabled' in result['error']


class TestStatusCommand:
    """Tests for status command."""

    def test_verify_setup(self, conductor_project):
        """Test setup verification."""
        args = MockArgs(project_root=conductor_project, subcommand='verify')
        result = status.handle(args)

        assert result['success'] is True
        assert result['data']['is_valid'] is True
        assert len(result['data']['missing_required']) == 0

    def test_verify_missing_files(self, tmp_path):
        """Test verification with missing files."""
        args = MockArgs(project_root=tmp_path, subcommand='verify')
        result = status.handle(args)

        assert result['success'] is True
        assert result['data']['is_valid'] is False
        assert len(result['data']['missing_required']) > 0

    def test_parse_tracks(self, conductor_project):
        """Test track parsing."""
        args = MockArgs(project_root=conductor_project, subcommand='tracks')
        result = status.handle(args)

        assert result['success'] is True
        assert 'tracks' in result['data']
        assert len(result['data']['tracks']) == 1

    def test_calculate_progress(self, conductor_project):
        """Test progress calculation."""
        args = MockArgs(project_root=conductor_project, subcommand='progress')
        result = status.handle(args)

        assert result['success'] is True
        assert 'overall' in result['data']
        assert result['data']['overall']['total'] == 3
        assert result['data']['overall']['completed'] == 1


class TestPatternsCommand:
    """Tests for patterns command."""

    def test_list_patterns(self, conductor_project):
        """Test listing patterns."""
        args = MockArgs(project_root=conductor_project, subcommand='list')
        result = patterns.handle(args)

        assert result['success'] is True

    def test_show_pattern(self, conductor_project):
        """Test showing a pattern."""
        args = MockArgs(project_root=conductor_project, subcommand='show', name='error-handling', ai_only=False)
        result = patterns.handle(args)

        assert result['success'] is True
        assert 'Error Handling' in result['data'].get('name', result['data'].get('content', ''))

    def test_show_pattern_ai_only(self, conductor_project):
        """Test AI-only pattern extraction."""
        args = MockArgs(project_root=conductor_project, subcommand='show', name='error-handling', ai_only=True)
        result = patterns.handle(args)

        assert result['success'] is True


class TestSnippetsCommand:
    """Tests for snippets command."""

    def test_list_snippets(self, conductor_project):
        """Test listing snippets."""
        args = MockArgs(project_root=conductor_project, subcommand='list')
        result = snippets.handle(args)

        assert result['success'] is True

    def test_show_snippet(self, conductor_project):
        """Test showing a snippet."""
        args = MockArgs(project_root=conductor_project, subcommand='show', name='api-client', language='python')
        result = snippets.handle(args)

        assert result['success'] is True


class TestNewtrackCommand:
    """Tests for newtrack command."""

    def test_generate_id(self, conductor_project):
        """Test track ID generation."""
        args = MockArgs(project_root=conductor_project, subcommand='generate-id', description='Add user authentication')
        result = newtrack.handle(args)

        assert result['success'] is True
        assert 'track_id' in result['data']
        assert '_' in result['data']['track_id']  # Has date suffix

    def test_scaffold(self, conductor_project):
        """Test track scaffolding."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='scaffold',
            track_id='new_track_20260121',
            type='feature',
            description='New feature'
        )
        result = newtrack.handle(args)

        assert result['success'] is True
        track_dir = conductor_project / 'conductor' / 'tracks' / 'new_track_20260121'
        assert track_dir.exists()
        assert (track_dir / 'metadata.json').exists()
        assert (track_dir / 'spec.md').exists()
        assert (track_dir / 'plan.md').exists()

    def test_register_creates_correct_path_format(self, conductor_project):
        """Test that register creates tracks.md entries with ./conductor/tracks/ path format.

        This tests the fix for the bug where register used ./tracks/{track_id}/
        but implement update-status expects ./conductor/tracks/{track_id}/.
        """
        args = MockArgs(
            project_root=conductor_project,
            subcommand='register',
            track_id='test-register_20260122',
            description='Test register path format'
        )
        result = newtrack.handle(args)

        assert result['success'] is True

        # Read tracks.md and verify the path format
        tracks_file = conductor_project / 'conductor' / 'tracks.md'
        content = tracks_file.read_text()

        # The entry should use ./conductor/tracks/ path, NOT ./tracks/
        assert '(./conductor/tracks/test-register_20260122/)' in content, \
            f"Expected path format './conductor/tracks/test-register_20260122/' not found in tracks.md. Content:\n{content}"

        # The entry should NOT use the incorrect ./tracks/ path
        assert '(./tracks/test-register_20260122/)' not in content, \
            "Incorrect path format './tracks/test-register_20260122/' found in tracks.md"


class TestSetupCommand:
    """Tests for setup command."""

    def test_detect(self, tmp_path):
        """Test project detection."""
        # Create a package.json
        (tmp_path / 'package.json').write_text('{"name": "test", "dependencies": {"react": "^18.0.0"}}')

        args = MockArgs(project_root=tmp_path, subcommand='detect')
        result = setup.handle(args)

        assert result['success'] is True
        assert result['data']['project_type'] == 'brownfield'

    def test_detect_brownfield_with_python_source_only(self, tmp_path):
        """Test that detect returns brownfield for project with main.py but no requirements.txt."""
        # Create only a Python source file, no manifest
        (tmp_path / 'main.py').write_text('print("hello")')

        args = MockArgs(project_root=tmp_path, subcommand='detect')
        result = setup.handle(args)

        assert result['success'] is True
        assert result['data']['project_type'] == 'brownfield', \
            "Project with main.py should be detected as brownfield"
        assert 'python' in result['data']['languages'], \
            "Python should be inferred from .py file"

    def test_detect_brownfield_with_js_source_in_src_dir(self, tmp_path):
        """Test that detect returns brownfield for project with src/index.js but no package.json."""
        # Create only a JS source file in src/, no manifest
        (tmp_path / 'src').mkdir()
        (tmp_path / 'src' / 'index.js').write_text('console.log("hello");')

        args = MockArgs(project_root=tmp_path, subcommand='detect')
        result = setup.handle(args)

        assert result['success'] is True
        assert result['data']['project_type'] == 'brownfield', \
            "Project with src/index.js should be detected as brownfield"
        assert 'javascript' in result['data']['languages'], \
            "JavaScript should be inferred from .js file"

    def test_detect_greenfield_with_only_md_files(self, tmp_path):
        """Test that detect returns greenfield for project with only .md files."""
        # Create only markdown files
        (tmp_path / 'README.md').write_text('# My Project')
        (tmp_path / 'CONTRIBUTING.md').write_text('# Contributing')

        args = MockArgs(project_root=tmp_path, subcommand='detect')
        result = setup.handle(args)

        assert result['success'] is True
        assert result['data']['project_type'] == 'greenfield', \
            "Project with only .md files should be detected as greenfield"

    def test_detect_infers_language_from_source_files(self, tmp_path):
        """Test that detect infers language from source files when no manifest exists."""
        # Create TypeScript files without tsconfig.json
        (tmp_path / 'app.ts').write_text('const x: string = "hello";')
        (tmp_path / 'utils.ts').write_text('export const util = () => {};')

        args = MockArgs(project_root=tmp_path, subcommand='detect')
        result = setup.handle(args)

        assert result['success'] is True
        assert result['data']['project_type'] == 'brownfield', \
            "Project with .ts files should be detected as brownfield"
        assert 'typescript' in result['data']['languages'], \
            "TypeScript should be inferred from .ts files"

    def test_scaffold(self, tmp_path):
        """Test conductor scaffolding."""
        args = MockArgs(project_root=tmp_path, subcommand='scaffold')
        result = setup.handle(args)

        assert result['success'] is True
        assert (tmp_path / 'conductor').exists()
        assert (tmp_path / 'conductor' / 'tracks').exists()

    def test_state_get(self, conductor_project):
        """Test getting setup state."""
        args = MockArgs(project_root=conductor_project, subcommand='state', get=True, set=None)
        result = setup.handle(args)

        assert result['success'] is True


class TestImplementCommand:
    """Tests for implement command."""

    def test_parse_tracks(self, conductor_project):
        """Test parsing tracks."""
        args = MockArgs(project_root=conductor_project, subcommand='parse-tracks')
        result = implement.handle(args)

        assert result['success'] is True
        assert 'tracks' in result['data']

    def test_update_status(self, conductor_project):
        """Test updating track status."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='update-status',
            track_id='test_20260121',
            status='in-progress'
        )
        result = implement.handle(args)

        assert result['success'] is True

    def test_next_adr_number(self, conductor_project):
        """Test ADR number generation."""
        # Create decisions directory
        decisions_dir = conductor_project / 'docs' / 'decisions'
        decisions_dir.mkdir(parents=True)
        (decisions_dir / '0001-initial.md').write_text('# ADR 1')
        (decisions_dir / '0002-second.md').write_text('# ADR 2')

        args = MockArgs(project_root=conductor_project, subcommand='next-adr-number', path='docs/decisions')
        result = implement.handle(args)

        assert result['success'] is True
        assert result['data']['next_number'] == 3

    def test_suggest_branch_feature_track(self, conductor_project):
        """Test suggest_branch returns correct prefix for feature track."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='suggest-branch',
            track_id='test_20260121'
        )
        result = implement.handle(args)

        assert result['success'] is True
        assert result['data']['branch_prefix'] == 'feature/'
        assert result['data']['branch_name'] == 'feature/test'

    def test_suggest_branch_bugfix_track(self, conductor_project):
        """Test suggest_branch returns correct prefix for bugfix track."""
        # Create a bugfix track
        bugfix_track_dir = conductor_project / 'conductor' / 'tracks' / 'login-bug_20260121'
        bugfix_track_dir.mkdir()
        (bugfix_track_dir / 'metadata.json').write_text(json.dumps({
            'track_id': 'login-bug_20260121',
            'type': 'bugfix',
            'status': 'pending',
            'created_at': '2026-01-21T00:00:00Z',
            'updated_at': '2026-01-21T00:00:00Z',
            'description': 'Fix login bug'
        }))

        args = MockArgs(
            project_root=conductor_project,
            subcommand='suggest-branch',
            track_id='login-bug_20260121'
        )
        result = implement.handle(args)

        assert result['success'] is True
        assert result['data']['branch_prefix'] == 'fix/'
        assert result['data']['branch_name'] == 'fix/login-bug'

    def test_suggest_branch_extracts_shortname(self, conductor_project):
        """Test suggest_branch extracts shortname from track_id (removes date suffix)."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='suggest-branch',
            track_id='test_20260121'
        )
        result = implement.handle(args)

        assert result['success'] is True
        assert result['data']['track_id'] == 'test_20260121'
        # Shortname should not include the date suffix
        assert 'test' in result['data']['branch_name']
        assert '20260121' not in result['data']['branch_name']

    def test_suggest_branch_missing_track(self, conductor_project):
        """Test suggest_branch returns error for missing track."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='suggest-branch',
            track_id='nonexistent_20260121'
        )
        result = implement.handle(args)

        assert result['success'] is False
        assert 'not found' in result['error'].lower()

    def test_suggest_branch_returns_worktree_path(self, conductor_project):
        """Test suggest_branch returns suggested worktree path."""
        args = MockArgs(
            project_root=conductor_project,
            subcommand='suggest-branch',
            track_id='test_20260121'
        )
        result = implement.handle(args)

        assert result['success'] is True
        assert 'worktree_path' in result['data']
        # Worktree path should be relative to parent directory
        assert result['data']['worktree_path'].startswith('../')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
