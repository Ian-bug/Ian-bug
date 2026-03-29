param(
    [Parameter(Position=0)]
    [string]$Task = "help"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsDir = Join-Path $ProjectRoot ".github/scripts"

function Show-Help {
    Write-Host ""
    Write-Host "Ian-bug Profile Updater - Development Commands" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\Make.ps1 <task>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available tasks:" -ForegroundColor White
    Write-Host "  help                Show this help message"
    Write-Host "  install             Install runtime dependencies"
    Write-Host "  install-dev         Install development dependencies"
    Write-Host "  test                Run tests"
    Write-Host "  test-cov            Run tests with coverage report"
    Write-Host "  lint                Run flake8 linting"
    Write-Host "  format              Format code with black"
    Write-Host "  type-check          Run mypy type checking"
    Write-Host "  clean               Clean up temporary files"
    Write-Host "  run                 Run the update_readme.py script"
    Write-Host "  all                 Run format, lint, type-check, and test"
    Write-Host ""
}

function Install-Deps {
    Write-Host "Installing runtime dependencies..." -ForegroundColor Yellow
    pip install -r "$ScriptsDir\requirements.txt"
}

function Install-DevDeps {
    Write-Host "Installing development dependencies..." -ForegroundColor Yellow
    pip install -r "$ScriptsDir\requirements-dev.txt"
    pip install pre-commit
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Yellow
    pytest tests/ -v
}

function Run-TestCov {
    Write-Host "Running tests with coverage..." -ForegroundColor Yellow
    pytest tests/ --cov=.github/scripts/update_readme --cov-report=html --cov-report=term
}

function Run-Lint {
    Write-Host "Running flake8..." -ForegroundColor Yellow
    flake8 "$ScriptsDir\update_readme.py"
}

function Run-Format {
    Write-Host "Formatting code with black..." -ForegroundColor Yellow
    black "$ScriptsDir\update_readme.py"
}

function Run-TypeCheck {
    Write-Host "Running mypy..." -ForegroundColor Yellow
    mypy "$ScriptsDir\update_readme.py" --ignore-missing-imports
}

function Clean-Project {
    Write-Host "Cleaning up temporary files..." -ForegroundColor Yellow
    Get-ChildItem -Path $ProjectRoot -Recurse -Include "__pycache__" -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $ProjectRoot -Recurse -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
    if (Test-Path "$ProjectRoot\.pytest_cache") { Remove-Item "$ProjectRoot\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue }
    if (Test-Path "$ProjectRoot\.coverage") { Remove-Item "$ProjectRoot\.coverage" -Force -ErrorAction SilentlyContinue }
    if (Test-Path "$ProjectRoot\htmlcov") { Remove-Item "$ProjectRoot\htmlcov" -Recurse -Force -ErrorAction SilentlyContinue }
    if (Test-Path "$ProjectRoot\.mypy_cache") { Remove-Item "$ProjectRoot\.mypy_cache" -Recurse -Force -ErrorAction SilentlyContinue }
    Write-Host "Done." -ForegroundColor Green
}

function Run-Script {
    Write-Host "Running update_readme.py..." -ForegroundColor Yellow
    python "$ScriptsDir\update_readme.py"
}

function Run-All {
    Write-Host "Running all checks..." -ForegroundColor Yellow
    Run-Format
    Run-Lint
    Run-TypeCheck
    Run-Tests
    Write-Host ""
    Write-Host "All checks passed!" -ForegroundColor Green
}

switch ($Task) {
    "help"        { Show-Help }
    "install"     { Install-Deps }
    "install-dev" { Install-DevDeps }
    "test"        { Run-Tests }
    "test-cov"    { Run-TestCov }
    "lint"        { Run-Lint }
    "format"      { Run-Format }
    "type-check"  { Run-TypeCheck }
    "clean"       { Clean-Project }
    "run"         { Run-Script }
    "all"         { Run-All }
    default {
        Write-Host "Unknown task: $Task" -ForegroundColor Red
        Write-Host "Run '.\Make.ps1 help' for available commands." -ForegroundColor Yellow
        exit 1
    }
}
