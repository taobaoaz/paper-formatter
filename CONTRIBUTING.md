# Contributing to Paper Formatter

Thank you for considering contributing to Paper Formatter! This document provides guidelines and instructions for contributing to this project.

## 🎯 How to Contribute

### 1. Reporting Issues
If you find a bug or have a feature request, please create an issue with the following information:
- **Bug Report:** Describe the bug, steps to reproduce, expected behavior, and actual behavior
- **Feature Request:** Describe the feature, why it's needed, and how it should work
- **Enhancement:** Suggest improvements to existing features

### 2. Submitting Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Open a Pull Request

### 3. Development Setup
```bash
# Clone the repository
git clone https://github.com/taobaoaz/paper-formatter.git
cd paper-formatter

# Install dependencies
cd 启动文件
pip install -r requirements.txt

# Run the application
python launcher.py
```

## 📝 Code Style

### Python Code
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Commit Messages
- Use conventional commit format
- Start with type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`
- Keep the first line under 50 characters
- Provide detailed description in the body if needed

Example:
```
feat: add font management feature

- Add online font search and download
- Implement font manager dialog
- Add API key management for Google Fonts
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_font_downloader.py

# Run with coverage
python -m pytest --cov=modules tests/
```

### Writing Tests
- Write unit tests for new features
- Test edge cases and error conditions
- Mock external dependencies
- Ensure tests are independent and repeatable

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include type hints where appropriate

### User Documentation
- Update README.md for new features
- Add usage examples
- Update release notes in RELEASE_NOTES_v*.md files

## 🚀 Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

### Creating a Release
1. Update version in relevant files
2. Update `RELEASE_NOTES_v*.md` with changes
3. Create a git tag: `git tag vX.Y.Z`
4. Push the tag: `git push origin vX.Y.Z`
5. GitHub Actions will automatically build and create a draft release
6. Review and publish the release

## 🐛 Bug Fixes
- Include tests that reproduce the bug
- Fix the root cause, not just symptoms
- Add comments explaining the fix if it's not obvious

## ✨ Feature Development
- Discuss major features in an issue first
- Keep features focused and single-purpose
- Consider backward compatibility
- Update documentation and tests

## 📦 Dependencies
- Keep dependencies up to date
- Use specific versions in requirements.txt
- Document why each dependency is needed
- Consider security implications of new dependencies

## 🔒 Security
- Never commit secrets or API keys
- Use environment variables for sensitive data
- Report security vulnerabilities privately
- Follow secure coding practices

## 🤝 Code Review
- Be respectful and constructive
- Focus on the code, not the person
- Explain why changes are suggested
- Respond to review comments promptly

## 📞 Getting Help
- Check existing documentation first
- Search for similar issues
- Ask questions in issue discussions
- Be patient and respectful

## 📄 License
By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make Paper Formatter better! 🎉