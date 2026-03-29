# Contributing to Ian-bug Profile

Thank you for your interest in contributing! This repository contains an automated GitHub profile README updater.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- GitHub CLI (`gh`) installed and authenticated
- Git

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ian-bug/Ian-bug.git
   cd Ian-bug
   ```

2. **Set up Python virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r .github/scripts/requirements-dev.txt
   ```

## Development Workflow

### Running Tasks (Windows PowerShell)

A `Make.ps1` script is provided for common development commands:
```powershell
.\Make.ps1 help          # Show all available commands
.\Make.ps1 test          # Run tests
.\Make.ps1 test-cov      # Run tests with coverage
.\Make.ps1 lint          # Run flake8 linting
.\Make.ps1 format        # Format code with black
.\Make.ps1 type-check    # Run mypy type checking
.\Make.ps1 clean         # Clean temporary files
.\Make.ps1 all           # Run format, lint, type-check, and test
```

### Running Tasks (Unix / Make)

On systems with GNU Make installed:
```bash
make help          # Show all available commands
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run flake8 linting
make format        # Format code with black
make type-check    # Run mypy type checking
make clean         # Clean temporary files
make all           # Run format, lint, type-check, and test
```

### Running Tests Directly

Run the test suite:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=.github/scripts/update_readme --cov-report=html
```

### Code Quality

Run linting:
```bash
flake8 .github/scripts/update_readme.py
```

Run type checking (if mypy is configured):
```bash
mypy .github/scripts/update_readme.py
```

Format code (if black is configured):
```bash
black .github/scripts/update_readme.py
```

### Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following existing code style and patterns.

3. **Add tests** for your changes if applicable.

4. **Run tests** to ensure everything passes:
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** with a clear description of your changes.

## Project Structure

```
Ian-bug/
├── .github/
│   ├── scripts/
│   │   ├── update_readme.py    # Main script that fetches GitHub data
│   │   ├── requirements.txt    # Runtime dependencies
│   │   └── requirements-dev.txt # Development dependencies
│   ├── workflows/
│   │   └── update-readme.yml   # GitHub Actions workflow
│   └── FUNDING.yml
├── tests/
│   └── test_update_readme.py   # Unit tests
├── .flake8                     # Flake8 configuration
├── .gitignore
├── GUIDE.md                    # Usage guide
├── pyproject.toml              # Project configuration
└── README.md                  # Auto-generated profile README
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and modular
- Use meaningful variable and function names

### Testing

- Write tests for new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Mock external API calls in tests
- Test edge cases and error conditions

### Documentation

- Keep documentation up-to-date
- Use clear, concise language
- Include examples in docstrings
- Update GUIDE.md if changing behavior

## Common Tasks

### Adding New Sections to README

1. Add data fetching logic in `fetch_github_data()`
2. Create a new generator function (e.g., `generate_new_section()`)
3. Call the new function in `generate_readme()`
4. Add tests for the new function

### Modifying Existing Sections

1. Locate the relevant function (e.g., `generate_repos_section()`)
2. Make your changes
3. Update tests accordingly
4. Run tests to verify

### Fixing Bugs

1. Add a test that reproduces the bug
2. Fix the issue
3. Verify the test passes
4. Check for any related issues

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code follows project style guidelines
- [ ] Added/updated tests for new functionality
- [ ] Updated documentation if needed
- [ ] Commits are clear and descriptive

### PR Description

Include:
- Brief description of changes
- Motivation for the change
- Any breaking changes
- Related issues (if any)
- Screenshots (for UI changes)

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Join discussions in existing issues

## License

This project is open source and available under the same terms as the repository.
