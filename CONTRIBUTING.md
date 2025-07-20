# Contributing to PLC Sniffer

Thank you for your interest in contributing to PLC Sniffer! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use issue templates when available
3. Provide detailed information:
   - Environment details
   - Steps to reproduce
   - Expected vs actual behavior
   - Logs and error messages

### Submitting Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/plc_sniffer.git
   cd plc_sniffer
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   make dev-install
   pre-commit install
   ```

4. **Make Changes**
   - Follow the coding standards
   - Add tests for new features
   - Update documentation
   - Ensure all tests pass

5. **Run Tests**
   ```bash
   make test
   make lint
   make type-check
   ```

6. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

7. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Add type hints
- Write docstrings

### Testing

- Write unit tests for all new code
- Maintain 80%+ code coverage
- Use pytest for testing
- Mock external dependencies

### Commit Messages

Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build/maintenance tasks

### Version Bumping

Use bumpr for version management:
```bash
make bump-patch  # For bug fixes
make bump-minor  # For new features
make bump-major  # For breaking changes
```

## Development Workflow

1. **Pre-commit Checks**
   ```bash
   pre-commit run --all-files
   ```

2. **Local Testing**
   ```bash
   make test
   ```

3. **Type Checking**
   ```bash
   make type-check
   ```

4. **Linting**
   ```bash
   make lint
   ```

5. **Format Code**
   ```bash
   make format
   ```

## Release Process

1. Update CHANGELOG.md
2. Run tests: `make test`
3. Bump version: `make bump-[patch|minor|major]`
4. Push with tags: `git push && git push --tags`
5. CI/CD will handle the rest

## Getting Help

- Check documentation in `/docs`
- Review existing issues and PRs
- Ask questions in issues
- Read the source code

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Release notes

Thank you for contributing!