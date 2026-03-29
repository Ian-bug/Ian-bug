# Changelog

All notable changes to the Ian-bug profile updater project.

## [Unreleased]

### Added
- **Comprehensive Testing**: Expanded test coverage with 14 test cases covering edge cases, error handling, and integration scenarios
- **Development Tooling**:
  - Added `Makefile` with common development tasks (test, lint, format, etc.)
  - Added `.pre-commit-config.yaml` for automated code quality checks
  - Added `CONTRIBUTING.md` with detailed contribution guidelines
  - Added `SECURITY.md` with security best practices and policies
- **Continuous Integration**:
  - Added `.github/workflows/tests.yml` for automated testing on PRs and pushes
  - Multi-Python version testing (3.10, 3.11, 3.12)
  - Coverage reporting integration
- **Documentation Improvements**:
  - Updated `requirements-dev.txt` with comprehensive development dependencies
  - Enhanced `pyproject.toml` with mypy configuration
- **Code Quality Tools**:
  - Configured mypy for static type checking
  - Configured black for code formatting
  - Configured flake8 for linting

### Improved
- **Code Structure**:
  - Removed redundant environment variable handling in `run_command()`
  - Added constants section for maintainability (MAX_PINNED_REPOS, MAX_ACTIVITY_ITEMS, etc.)
  - Extracted helper functions: `normalize_url()` and `format_date()`
  - Better separation of concerns and reduced code duplication
- **Error Handling**:
  - Added specific exception handling for `URLError` and `JSONDecodeError`
  - Added timeout (30s) to GraphQL API requests
  - More descriptive error messages for debugging
- **Type Hints**:
  - Enhanced type hints throughout the codebase
  - Added mypy configuration in `pyproject.toml`
  - Improved type safety and IDE support
- **Testing**:
  - Fixed failing tests related to mock configuration
  - Improved test coverage for edge cases
  - Added tests for new helper functions

### Changed
- Updated `requirements-dev.txt` from placeholder to actual dependencies
- Improved GraphQL API error messages
- Changed test mock setup to properly test both run_command and fetch_pinned_repos

### Fixed
- Fixed test that was checking for "Top Repositories" instead of "Pinned Repositories"
- Fixed test mock parameter ordering issue
- Fixed test expectations for repository fetching

### Documentation
- Added comprehensive `CONTRIBUTING.md` with:
  - Development environment setup
  - Code standards and best practices
  - Testing guidelines
  - Pull request guidelines
- Added `SECURITY.md` with:
  - Token security best practices
  - Vulnerability reporting process
  - API rate limit considerations
  - Security guidelines for forking

---

## Previous Versions

For versions prior to this improvement cycle, see git commit history.

## Versioning

This project follows semantic versioning for releases:
- **MAJOR**: Incompatible changes
- **MINOR**: Backwards-compatible functionality
- **PATCH**: Backwards-compatible bug fixes
