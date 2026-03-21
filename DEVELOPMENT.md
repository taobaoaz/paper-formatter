# Development Guide

This guide provides instructions for setting up the development environment, running tests, and contributing to the Paper Formatter project.

## 🛠️ Development Setup

### Prerequisites

- **Python 3.8+**
- **Git**
- **GitHub Account** (for contributing)

### 1. Clone the Repository

```bash
git clone https://github.com/taobaoaz/paper-formatter.git
cd paper-formatter
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r launcher/requirements.txt

# Development dependencies
pip install pytest pytest-cov black flake8 isort pre-commit
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

## 🧪 Running Tests

### Run All Tests

```bash
cd tests
python -m pytest -v
```

### Run Specific Test File

```bash
cd tests
python -m pytest test_basic.py -v
```

### Run Tests with Coverage

```bash
cd tests
python -m pytest --cov=.. --cov-report=html
```

### Run Code Quality Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific checks
black . --check
flake8 .
isort . --check-only
```

## 📁 Project Structure

```
paper-formatter/
├── .github/              # GitHub Actions workflows
├── core/                 # Core application logic
├── modules/              # Feature modules
├── launcher/            # Launcher scripts and requirements
├── templates/           # Document templates
├── releases/            # Release notes
├── tests/               # Test files
├── installer/           # Installer resources
├── 文档资料/            # Documentation (Chinese)
├── .flake8              # Flake8 configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── CHANGELOG.md         # Version history
├── CONTRIBUTING.md      # Contribution guidelines
├── LICENSE              # MIT License
├── README.md            # Project documentation
└── README_简化版.md     # Simplified Chinese README
```

## 🔧 Code Style

### Python Code Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length:** 127 characters
- **Import order:** Standard library → Third-party → Local
- **Formatting:** Use Black for automatic formatting
- **Linting:** Use Flake8 for code quality

### Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

```bash
# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run hooks on staged files (default)
git commit -m "Your message"
```

Available hooks:
- **black:** Code formatting
- **isort:** Import sorting
- **flake8:** Code linting
- **mypy:** Type checking (optional)
- **bandit:** Security scanning
- **pydocstyle:** Docstring checking

## 🚀 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the code style guidelines and write tests for new functionality.

### 3. Run Tests

```bash
cd tests
python -m pytest -v
```

### 4. Run Code Quality Checks

```bash
pre-commit run --all-files
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add your feature"
```

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 🧪 Testing Guidelines

### Unit Tests

- Place unit tests in `tests/unit/`
- Test one thing per test function
- Use descriptive test names
- Mock external dependencies

### Integration Tests

- Place integration tests in `tests/integration/`
- Test interactions between components
- Use real dependencies when possible

### Test Structure

```python
def test_functionality():
    # Arrange: Setup test data
    # Act: Execute the code
    # Assert: Verify results
    pass
```

### Test Coverage

Aim for at least 80% test coverage for new code.

## 📦 Building and Packaging

### Build EXE (Windows)

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed \
  --name="paper-formatter" \
  --add-data "modules/parsers:parsers" \
  --paths modules \
  --paths core \
  --hidden-import parsers \
  ./core/main.py
```

### Create Release

1. Update version in relevant files
2. Update `CHANGELOG.md`
3. Create git tag: `git tag vX.Y.Z`
4. Push tag: `git push origin vX.Y.Z`
5. GitHub Actions will automatically build and create a draft release

## 🔍 Debugging

### Enable Debug Mode

Set environment variable:

```bash
export PAPER_FORMATTER_DEBUG=1
```

### Logging

The application uses Python's logging module. Log levels:
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

### Common Issues

1. **Import errors:** Check Python path and virtual environment
2. **Dependency issues:** Update requirements.txt
3. **Build failures:** Check PyInstaller configuration
4. **Encoding problems:** Ensure UTF-8 encoding

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)
- **Discussions:** [GitHub Discussions](https://github.com/taobaoaz/paper-formatter/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.