# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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