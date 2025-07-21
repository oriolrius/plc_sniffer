#!/bin/bash
# Update CHANGELOG.md using git-cliff

set -e

# Check if git-cliff is installed
if ! command -v git-cliff &> /dev/null; then
    echo "git-cliff is not installed. Installing..."
    cargo install git-cliff || {
        echo "Failed to install git-cliff. Please install Rust/Cargo first."
        exit 1
    }
fi

# Get the latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Generate changelog
if [ -z "$LATEST_TAG" ]; then
    echo "Generating full changelog..."
    git-cliff --output CHANGELOG.md
else
    echo "Updating changelog from $LATEST_TAG..."
    # Generate changelog for unreleased changes
    git-cliff --output CHANGELOG.new.md --unreleased
    
    # Combine with existing changelog
    if [ -f CHANGELOG.md ]; then
        # Find the line with [Unreleased] and insert new content after it
        awk '/^## \[Unreleased\]/{print; getline; print ""; system("cat CHANGELOG.new.md"); next} 1' CHANGELOG.md > CHANGELOG.tmp.md
        mv CHANGELOG.tmp.md CHANGELOG.md
        rm CHANGELOG.new.md
    else
        mv CHANGELOG.new.md CHANGELOG.md
    fi
fi

echo "CHANGELOG.md updated successfully!"