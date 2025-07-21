# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2025-07-21

### Added
- Local git hooks for automated changelog updates
- Post-commit hook that detects release commits and updates CHANGELOG.md
- Hook installation script and documentation

### Changed
- Changelog updates now happen locally instead of in GitHub Actions
- Updated development setup to include git hook installation

## [0.6.1] - 2025-07-21

### Fixed
- Correct Docker base image reference in README from Alpine to Debian Linux

## [0.6.0] - 2025-07-21

### Added
- Comprehensive API documentation (`docs/api.md`)
- Testing guide with htmlcov explanation (`docs/testing.md`)
- Troubleshooting guide (`docs/troubleshooting.md`)
- Automated changelog generation tools (Python script and git-cliff config)

### Changed
- Reorganized documentation structure for clarity:
  - Renamed `SECURITY.md` to `vulnerability-reporting.md`
  - Renamed `security.md` to `deployment-security.md`
- Moved `CONTRIBUTING.md` to root directory

### Removed
- Unused `run_tests.py` file

## [0.5.2] - 2025-07-21

### Fixed
- Update CI workflow to use renamed Dockerfile (was referencing Dockerfile.secure)

## [0.5.1] - 2025-07-21

### Fixed
- Switch from Alpine to Debian base image to resolve libpcap compatibility issues

### Changed
- Consolidated to single Dockerfile (removed Dockerfile.secure)

## [0.5.0] - 2025-07-21

### Changed
- Consolidated multiple Docker compose files into single flexible configuration
- Simplified docker-entrypoint.sh to run as root with privileged mode
- Added environment variable support with defaults in compose.yaml

### Added
- `.env.example` file for environment configuration

## [0.4.2] - 2025-07-20

### Fixed
- Update release workflow to support both v-prefixed and plain semver tags

## [0.4.1] - 2025-07-20

### Fixed
- Resolve module import error in Docker container by setting PYTHONPATH
- Improve Dockerfile to use proper Python packaging instead of editable install

## [0.4.0] - 2025-07-20

### Added
- Integrated bumpr v0.3.0 for version management

## [0.3.0] - 2025-07-20

### Added
- Complete project restructuring with modular architecture
- Comprehensive security hardening:
  - Input validation for all configuration parameters
  - Rate limiting and packet size validation
  - Non-root Docker container execution
  - Security-focused Dockerfile with multi-stage build
- Full test suite with 62% code coverage
- CI/CD pipeline with GitHub Actions
- Health monitoring and Prometheus metrics
- Graceful shutdown handling
- Type hints throughout the codebase
- Pre-commit hooks for code quality
- Integrated bumpr for automated version management
- Created Makefile for common development tasks
- Added comprehensive improvement plan in .claude/PLAN.md
- Created project analysis documentation in .claude/README.md

### Changed
- Migrated from single file to modular architecture in src/
- Updated to Python 3.13 requirement
- Improved error handling with custom exceptions
- Enhanced logging with structured output
- Updated .gitignore to include development artifacts

### Security
- Implemented input validation for all user inputs
- Added rate limiting to prevent DoS attacks
- Created secure Docker image with non-root user
- Fixed all high/critical vulnerabilities in dependencies

## [0.1.0] - Initial Release

### Added
- Basic PLC packet sniffer functionality
- UDP packet capture and forwarding
- Docker container support
- Environment-based configuration
- Basic logging functionality