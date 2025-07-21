#!/bin/bash
# Script to install git hooks

HOOKS_DIR="$(dirname "$0")"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

echo "Installing git hooks..."

# List of hooks to install
HOOKS=("post-commit")

for hook in "${HOOKS[@]}"; do
    if [ -f "$HOOKS_DIR/$hook" ]; then
        # Make the hook executable
        chmod +x "$HOOKS_DIR/$hook"
        
        # Copy to git hooks directory
        cp "$HOOKS_DIR/$hook" "$GIT_HOOKS_DIR/$hook"
        
        echo "✅ Installed $hook hook"
    else
        echo "⚠️  Hook $hook not found in $HOOKS_DIR"
    fi
done

echo "Done! Git hooks have been installed."
echo ""
echo "To test the changelog generation:"
echo "1. Make a change and commit it"
echo "2. Run: tools/bumpr patch"
echo "3. The CHANGELOG.md will be automatically updated"