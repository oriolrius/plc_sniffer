#!/usr/bin/env python3
"""Generate or update CHANGELOG.md from git commits using conventional commits."""

import re
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple
import sys


class ChangelogGenerator:
    """Generate changelog from conventional commits."""
    
    COMMIT_TYPES = {
        'feat': 'Added',
        'fix': 'Fixed',
        'docs': 'Documentation',
        'style': 'Changed',
        'refactor': 'Changed',
        'perf': 'Performance',
        'test': 'Testing',
        'build': 'Build',
        'ci': 'CI/CD',
        'chore': 'Miscellaneous',
        'revert': 'Reverted',
    }
    
    CHANGELOG_HEADER = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""

    def __init__(self):
        self.commit_pattern = re.compile(
            r'^(?P<type>\w+)(?:\((?P<scope>[\w\-]+)\))?:\s*(?P<message>.+)$'
        )
    
    def get_commits(self, from_tag: str = None, to_tag: str = 'HEAD') -> List[Dict[str, str]]:
        """Get commits between two tags/refs."""
        cmd = ['git', 'log', '--pretty=format:%H|%s|%b|%an|%ad', '--date=short']
        
        if from_tag:
            cmd.append(f'{from_tag}..{to_tag}')
        else:
            cmd.append(to_tag)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        commits = []
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|', 4)
            if len(parts) >= 5:
                commit = {
                    'hash': parts[0],
                    'subject': parts[1],
                    'body': parts[2],
                    'author': parts[3],
                    'date': parts[4],
                }
                commits.append(commit)
        
        return commits
    
    def parse_commit(self, commit: Dict[str, str]) -> Dict[str, str]:
        """Parse a commit message into conventional commit format."""
        match = self.commit_pattern.match(commit['subject'])
        if match:
            commit_type = match.group('type')
            scope = match.group('scope')
            message = match.group('message')
            
            # Check for breaking changes
            breaking = 'BREAKING CHANGE:' in commit['body'] or '!' in commit['subject']
            
            return {
                'type': commit_type,
                'scope': scope,
                'message': message,
                'breaking': breaking,
                'hash': commit['hash'][:7],
                'author': commit['author'],
                'date': commit['date'],
            }
        return None
    
    def group_commits(self, commits: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """Group commits by type."""
        grouped = {}
        
        for commit in commits:
            parsed = self.parse_commit(commit)
            if parsed:
                group = self.COMMIT_TYPES.get(parsed['type'], 'Other')
                if group not in grouped:
                    grouped[group] = []
                grouped[group].append(parsed)
        
        return grouped
    
    def format_version_section(self, version: str, date: str, grouped_commits: Dict[str, List[Dict[str, str]]]) -> str:
        """Format a version section of the changelog."""
        section = f"## [{version}] - {date}\n\n"
        
        # Order groups
        group_order = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security']
        other_groups = sorted(set(grouped_commits.keys()) - set(group_order))
        
        for group in group_order + other_groups:
            if group in grouped_commits:
                section += f"### {group}\n"
                for commit in grouped_commits[group]:
                    message = commit['message']
                    if commit['scope']:
                        message = f"**{commit['scope']}:** {message}"
                    if commit['breaking']:
                        message += " [**BREAKING**]"
                    section += f"- {message} ({commit['hash']})\n"
                section += "\n"
        
        return section
    
    def get_tags(self) -> List[Tuple[str, str]]:
        """Get all version tags with dates."""
        cmd = ['git', 'tag', '-l', '--format=%(refname:short)|%(creatordate:short)']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        tags = []
        for line in result.stdout.strip().split('\n'):
            if line and '|' in line:
                tag, date = line.split('|', 1)
                # Filter for version tags
                if re.match(r'^v?\d+\.\d+\.\d+', tag):
                    tags.append((tag, date))
        
        return sorted(tags, key=lambda x: x[0], reverse=True)
    
    def generate_changelog(self) -> str:
        """Generate the complete changelog."""
        changelog = self.CHANGELOG_HEADER
        tags = self.get_tags()
        
        # Add Unreleased section
        if tags:
            unreleased_commits = self.get_commits(from_tag=tags[0][0])
            if unreleased_commits:
                grouped = self.group_commits(unreleased_commits)
                if grouped:
                    changelog += "## [Unreleased]\n\n"
                    today = datetime.now().strftime('%Y-%m-%d')
                    section = self.format_version_section('Unreleased', today, grouped)
                    # Remove the duplicate header
                    section_lines = section.split('\n')[2:]  # Skip the version line
                    changelog += '\n'.join(section_lines)
        
        # Add version sections
        for i, (tag, date) in enumerate(tags):
            from_tag = tags[i + 1][0] if i + 1 < len(tags) else None
            commits = self.get_commits(from_tag=from_tag, to_tag=tag)
            grouped = self.group_commits(commits)
            
            if grouped:
                version = tag.lstrip('v')
                changelog += self.format_version_section(version, date, grouped)
        
        return changelog


def main():
    """Main entry point."""
    generator = ChangelogGenerator()
    
    try:
        changelog = generator.generate_changelog()
        
        # Write to file
        with open('CHANGELOG.md', 'w') as f:
            f.write(changelog)
        
        print("✅ CHANGELOG.md updated successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating changelog: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()