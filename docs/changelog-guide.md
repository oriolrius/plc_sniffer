# Changelog Management Guide

This project uses automated changelog generation based on [Conventional Commits](https://www.conventionalcommits.org/).

## Commit Message Format

All commits should follow this format:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, etc)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files

### Examples
```bash
# Feature
git commit -m "feat: add rate limiting to packet forwarding"

# Bug fix with scope
git commit -m "fix(sniffer): resolve memory leak in packet processing"

# Breaking change
git commit -m "feat!: change configuration format to YAML

BREAKING CHANGE: Configuration files must now use YAML format instead of JSON"

# Commit with issue reference
git commit -m "fix: correct packet filtering logic

Closes #123"
```

## Generating the Changelog

### Option 1: Python Script (No Dependencies)
```bash
python scripts/generate_changelog.py
```

### Option 2: git-cliff (Rust Tool)
First install git-cliff:
```bash
cargo install git-cliff
```

Then run:
```bash
scripts/update-changelog.sh
```

### Option 3: Integrate with Release Process
The changelog can be automatically updated during the release process by modifying the bumpr tool.

## Pre-commit Hook
The project includes a commitizen pre-commit hook that validates commit messages:

```bash
# Install/update pre-commit hooks
pre-commit install --hook-type commit-msg
```

## Release Workflow Integration

To integrate changelog generation with your release process:

1. Ensure commits follow conventional format
2. Run changelog generation before creating a release
3. Include the updated CHANGELOG.md in the release commit

## Manual Changelog Updates

While automation is preferred, you can still manually edit CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

## [0.5.2] - 2025-07-20
### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Change description
```

## Best Practices

1. **Write meaningful commit messages** - They become your changelog entries
2. **Use scopes** - Help organize changes by component
3. **Mark breaking changes** - Use `!` or `BREAKING CHANGE:` footer
4. **Reference issues** - Use `Closes #123` in commit body
5. **Review before release** - Ensure the generated changelog is accurate

## Configuration Files

- `.cz.toml` - Commitizen configuration
- `cliff.toml` - git-cliff configuration
- `.gitmessage` - Git commit message template
- `.pre-commit-config.yaml` - Pre-commit hooks including commitizen