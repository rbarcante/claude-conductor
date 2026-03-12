# Contributing to Claude Conductor for Claude Code

Thank you for your interest in contributing to the Claude Conductor for Claude Code!

## About This Project

Claude Conductor for Claude Code is a derivative work based on the [Conductor Extension for Gemini CLI](https://github.com/gemini-cli-extensions/conductor), originally released under the Apache License 2.0. This project extends Conductor's context-driven development methodology to work with Claude Code.

## How to Contribute

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/claude-conductor.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear, descriptive messages
7. Push to your fork
8. Create a Pull Request

### Contribution Guidelines

#### Code Quality
- Follow the project's existing code style and conventions
- Write clear, self-documenting code with appropriate comments
- Maintain or improve test coverage (target: >80%)
- Run all tests before submitting a PR: `npm test` (or appropriate for your language)

#### Testing
- Write tests for new features and bug fixes
- Ensure all tests pass before submitting
- Include both unit tests and integration tests where applicable

#### Documentation
- Update README.md if adding new features
- Document any new commands or skills
- Add comments to complex logic
- Update CHANGELOG if applicable

#### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `revert`, `test`, `chore`, `build`, `ci`

**Version bump rules** (enforced by Release Please):
- `feat:` → **minor** version bump (e.g., 1.0.1 → 1.1.0)
- `fix:` → **patch** version bump (e.g., 1.0.1 → 1.0.2)
- `feat!:` / `fix!:` / `BREAKING CHANGE:` → **major** version bump (e.g., 1.0.1 → 2.0.0)
- All other types → no version bump (may appear in changelog)

> **Important:** Only the types listed above are recognized by Release Please. Using
> non-standard types will cause commits to be **completely ignored** for both changelog
> generation and version bumping. Always use standard Conventional Commits types
> (e.g., `feat(<scope>):`, `fix(<scope>):`) to ensure proper semantic versioning.

Example:
```
feat(agents): Add specialist sub-agents for parallel analysis

Implement dedicated analysis agents that enable parallel processing
of code review tasks across multiple dimensions.

Closes #123
```

### Pull Request Process

1. Update documentation with details of your changes
2. Ensure your code follows the project's style guidelines
3. Include a clear description of the changes
4. Reference related issues
5. Ensure all CI checks pass

### Reporting Issues

When reporting bugs or issues:
- Include a clear, descriptive title
- Describe the exact steps to reproduce the issue
- Explain the expected vs actual behavior
- Include relevant logs or screenshots
- Specify your environment (OS, Node version, etc.)

## License

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0. See the LICENSE file for details.

This project is a derivative work of the Conductor Extension for Gemini CLI. Your contributions help maintain and improve both this plugin and the open-source ecosystem.

## Questions?

- Check existing issues and discussions first
- Create a new discussion for questions
- Refer to the documentation in `conductor/` directory

Thank you for helping make Claude Conductor better!
