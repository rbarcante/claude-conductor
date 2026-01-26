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
Tests for GitHub Actions CI workflow configuration.

These tests validate that the CI workflow file exists and is properly configured
to run tests, linting, type checking, and security scans.
"""

import pytest
import yaml
from pathlib import Path


# Get the project root (parent of scripts/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestCIWorkflowExists:
    """Tests that verify the CI workflow file exists."""

    def test_github_workflows_directory_exists(self):
        """Test that .github/workflows directory exists."""
        workflows_dir = PROJECT_ROOT / '.github' / 'workflows'
        assert workflows_dir.exists(), \
            f"Expected .github/workflows directory at {workflows_dir}"

    def test_ci_workflow_file_exists(self):
        """Test that ci.yml workflow file exists."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        assert ci_file.exists(), \
            f"Expected ci.yml workflow file at {ci_file}"


class TestCIWorkflowStructure:
    """Tests that verify the CI workflow structure."""

    @pytest.fixture
    def workflow(self):
        """Load the CI workflow YAML file."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        if not ci_file.exists():
            pytest.skip("CI workflow file does not exist yet")
        with open(ci_file) as f:
            return yaml.safe_load(f)

    def test_workflow_has_name(self, workflow):
        """Test that workflow has a name."""
        assert 'name' in workflow, "Workflow must have a 'name' field"
        assert workflow['name'], "Workflow name must not be empty"

    def test_workflow_triggers_on_pull_request(self, workflow):
        """Test that workflow triggers on pull_request events."""
        assert 'on' in workflow, "Workflow must have 'on' trigger configuration"
        triggers = workflow['on']

        # Handle both dict and list formats
        if isinstance(triggers, dict):
            assert 'pull_request' in triggers, \
                "Workflow must trigger on pull_request events"
        elif isinstance(triggers, list):
            assert 'pull_request' in triggers, \
                "Workflow must trigger on pull_request events"
        else:
            pytest.fail(f"Unexpected 'on' format: {type(triggers)}")

    def test_workflow_has_jobs(self, workflow):
        """Test that workflow defines jobs."""
        assert 'jobs' in workflow, "Workflow must define 'jobs'"
        assert workflow['jobs'], "Workflow must have at least one job"


class TestCIWorkflowJobs:
    """Tests that verify CI workflow jobs configuration."""

    @pytest.fixture
    def workflow(self):
        """Load the CI workflow YAML file."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        if not ci_file.exists():
            pytest.skip("CI workflow file does not exist yet")
        with open(ci_file) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def test_job(self, workflow):
        """Get the test job from the workflow."""
        jobs = workflow.get('jobs', {})
        # Look for a job that runs tests (could be named 'test', 'tests', 'ci', etc.)
        for job_name in ['test', 'tests', 'ci', 'build']:
            if job_name in jobs:
                return jobs[job_name]
        # If no standard name, just return the first job
        if jobs:
            return list(jobs.values())[0]
        pytest.fail("No jobs found in workflow")

    def test_job_runs_on_ubuntu(self, test_job):
        """Test that job runs on Ubuntu."""
        assert 'runs-on' in test_job, "Job must specify 'runs-on'"
        runs_on = test_job['runs-on']
        assert 'ubuntu' in runs_on.lower(), \
            f"Job should run on Ubuntu, got: {runs_on}"

    def test_job_has_steps(self, test_job):
        """Test that job has steps defined."""
        assert 'steps' in test_job, "Job must have 'steps'"
        assert len(test_job['steps']) > 0, "Job must have at least one step"

    def test_job_uses_checkout_action(self, test_job):
        """Test that job uses actions/checkout."""
        steps = test_job.get('steps', [])
        checkout_found = any(
            step.get('uses', '').startswith('actions/checkout')
            for step in steps
        )
        assert checkout_found, "Job must use actions/checkout action"

    def test_job_uses_setup_python_action(self, test_job):
        """Test that job uses actions/setup-python."""
        steps = test_job.get('steps', [])
        setup_python_found = any(
            step.get('uses', '').startswith('actions/setup-python')
            for step in steps
        )
        assert setup_python_found, "Job must use actions/setup-python action"

    def test_job_uses_python_312(self, test_job):
        """Test that job uses Python 3.12."""
        steps = test_job.get('steps', [])
        for step in steps:
            if step.get('uses', '').startswith('actions/setup-python'):
                with_config = step.get('with', {})
                python_version = str(with_config.get('python-version', ''))
                assert '3.12' in python_version, \
                    f"Python version should be 3.12, got: {python_version}"
                return
        pytest.fail("Could not find setup-python step to verify Python version")


class TestCIWorkflowTestStep:
    """Tests that verify test execution in the workflow."""

    @pytest.fixture
    def workflow(self):
        """Load the CI workflow YAML file."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        if not ci_file.exists():
            pytest.skip("CI workflow file does not exist yet")
        with open(ci_file) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def all_steps(self, workflow):
        """Get all steps from all jobs."""
        steps = []
        for job in workflow.get('jobs', {}).values():
            steps.extend(job.get('steps', []))
        return steps

    def test_workflow_runs_pytest(self, all_steps):
        """Test that workflow runs pytest."""
        pytest_found = any(
            'pytest' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert pytest_found, "Workflow must run pytest"

    def test_workflow_installs_dependencies(self, all_steps):
        """Test that workflow installs dependencies."""
        install_found = any(
            'pip install' in step.get('run', '') or
            'requirements' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert install_found, "Workflow must install dependencies"


class TestCIWorkflowCodeQuality:
    """Tests that verify code quality checks in the workflow."""

    @pytest.fixture
    def workflow(self):
        """Load the CI workflow YAML file."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        if not ci_file.exists():
            pytest.skip("CI workflow file does not exist yet")
        with open(ci_file) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def all_steps(self, workflow):
        """Get all steps from all jobs."""
        steps = []
        for job in workflow.get('jobs', {}).values():
            steps.extend(job.get('steps', []))
        return steps

    def test_workflow_runs_linting(self, all_steps):
        """Test that workflow runs linting (pylint or flake8)."""
        linting_found = any(
            'pylint' in step.get('run', '') or
            'flake8' in step.get('run', '') or
            'ruff' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert linting_found, "Workflow must run linting (pylint, flake8, or ruff)"

    def test_workflow_runs_black(self, all_steps):
        """Test that workflow runs black formatter check."""
        black_found = any(
            'black' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert black_found, "Workflow must run black formatter check"

    def test_workflow_runs_mypy(self, all_steps):
        """Test that workflow runs mypy type checking."""
        mypy_found = any(
            'mypy' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert mypy_found, "Workflow must run mypy type checking"


class TestCIWorkflowSecurity:
    """Tests that verify security scanning in the workflow."""

    @pytest.fixture
    def workflow(self):
        """Load the CI workflow YAML file."""
        ci_file = PROJECT_ROOT / '.github' / 'workflows' / 'ci.yml'
        if not ci_file.exists():
            pytest.skip("CI workflow file does not exist yet")
        with open(ci_file) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def all_steps(self, workflow):
        """Get all steps from all jobs."""
        steps = []
        for job in workflow.get('jobs', {}).values():
            steps.extend(job.get('steps', []))
        return steps

    def test_workflow_runs_security_scan(self, all_steps):
        """Test that workflow runs security scanning (pip-audit or safety)."""
        security_found = any(
            'pip-audit' in step.get('run', '') or
            'safety' in step.get('run', '')
            for step in all_steps
            if 'run' in step
        )
        assert security_found, "Workflow must run security scanning (pip-audit or safety)"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
