# Git Hooks

This directory contains git hooks for the PLC Sniffer project.

## Installation

Run the installation script to set up the hooks:

```bash
./hooks/install.sh
```

## Available Hooks

### post-commit

Automatically updates `CHANGELOG.md` after a release commit created by `bumpr`.

**How it works:**
1. Detects commits with message pattern "releasing X.Y.Z"
2. Runs the changelog generation script
3. Amends the commit to include the updated CHANGELOG.md

**Note:** This hook only activates for release commits created by bumpr.

## Manual Changelog Generation

If you need to regenerate the changelog manually:

```bash
python scripts/generate_changelog.py
```

## Troubleshooting

If the hook doesn't work:
1. Ensure you've run `./hooks/install.sh`
2. Check that Python is available in your environment
3. Verify the hook is executable: `ls -la .git/hooks/post-commit`