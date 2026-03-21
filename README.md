# Paper Formatter 🎓

[![Build Status](https://github.com/taobaoaz/paper-formatter/actions/workflows/build-windows.yml/badge.svg)](https://github.com/taobaoaz/paper-formatter/actions/workflows/build-windows.yml)
[![Test Status](https://github.com/taobaoaz/paper-formatter/actions/workflows/test.yml/badge.svg)](https://github.com/taobaoaz/paper-formatter/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/taobaoaz/paper-formatter)](https://github.com/taobaoaz/paper-formatter/releases)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://taobaoaz.github.io/paper-formatter/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-green)](https://taobaoaz.github.io/paper-formatter/installation)

A professional academic paper formatting tool that helps researchers and students format their papers with ease. Supports Chinese and English documents with advanced formatting features.

**📚 Documentation:** [https://taobaoaz.github.io/paper-formatter/](https://taobaoaz.github.io/paper-formatter/)

## ✨ Features

### 📘 Cover and Declaration Page Configuration
- Visual configuration interface
- Upload Word templates
- Select cover and declaration pages
- Save/load configurations

### 📄 Template Page Selection
- Pre-built templates for various paper formats
- Custom template support
- Easy template switching

### 📝 Document Formatting
- One-click formatting
- Support for multiple document formats
- Batch processing capability

### 📚 Reference Management
- Multiple citation styles support
- Automatic bibliography generation
- Reference formatting tools

### 🤖 AI Recognition
- Automatic format recognition
- Smart suggestions for formatting
- Learning-based improvements

### 🔤 Font Management (v2.2.2+)
- Online font search and download
- Chinese font priority search
- Multi-threaded font package downloads
- Real-time download progress display
- Automatic font installation
- Cross-platform support (Windows/macOS/Linux)

### 📦 Auto Backup (v2.1.8+)
- Automatic backup manager (configurable intervals)
- Smart cleanup strategies (importance/recent/time-based)
- Snapshot importance marking

### 🗂️ Document State Snapshot (v2.1.5+)
- Document state capture and restoration
- Configuration snapshots
- Snapshot management UI with keyboard shortcuts
- Automatic snapshot creation on document open and before formatting

## 🚀 Quick Start

### Installation

Choose your platform:

#### Windows
1. Download the latest `.exe` installer from [Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. Run the installer and follow the prompts
3. Launch Paper Formatter from Start Menu or Desktop

#### macOS
1. Download the `.dmg` file from [Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. Drag Paper Formatter to Applications folder
3. Launch from Applications

#### Linux
```bash
# For .deb packages (Ubuntu/Debian)
wget https://github.com/taobaoaz/paper-formatter/releases/download/v2.2.3/paper-formatter_v2.2.3_amd64.deb
sudo dpkg -i paper-formatter_v2.2.3_amd64.deb

# For AppImage (All Linux distributions)
wget https://github.com/taobaoaz/paper-formatter/releases/download/v2.2.3/paper-formatter-v2.2.3-x86_64.AppImage
chmod +x paper-formatter-v2.2.3-x86_64.AppImage
./paper-formatter-v2.2.3-x86_64.AppImage
```

### Basic Usage

1. **Open a Document**: Click "Open" and select your paper document
2. **Select Format**: Choose from pre-built templates or create custom format
3. **Format Document**: Click "Format" to apply formatting
4. **Save Result**: Save the formatted document

## 📖 Documentation

Comprehensive documentation is available at: [https://taobaoaz.github.io/paper-formatter/](https://taobaoaz.github.io/paper-formatter/)

### Documentation Sections:
- 📋 [Installation Guide](https://taobaoaz.github.io/paper-formatter/installation) - Detailed installation instructions for all platforms
- 🚀 Quick Start - Get started in minutes
- 📚 User Guide - Complete user manual
- 🔧 Development Guide - For contributors and developers
- 📝 API Reference - Technical documentation
- ❓ FAQ - Frequently Asked Questions
- 📋 Changelog - Version history and release notes

## 🛠️ Development

### Prerequisites
- Python 3.8+
- Git
- pip

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/taobaoaz/paper-formatter.git
cd paper-formatter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r launcher/requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 isort pre-commit

# Install pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run all tests
cd tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=.. --cov-report=html

# Run code quality checks
pre-commit run --all-files
```

### Building from Source
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

## 📁 Project Structure

```
paper-formatter/
├── .github/              # GitHub Actions workflows
├── core/                 # Core application logic
├── modules/              # Feature modules
├── launcher/            # Launcher scripts and requirements
├── templates/           # Document templates
├── releases/            # Release notes (organized)
├── docs/               # GitHub Pages documentation
├── tests/              # Test files
├── installer/          # Installer resources
├── .flake8             # Code style configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── CHANGELOG.md        # Version history
├── CONTRIBUTING.md     # Contribution guidelines
├── DEVELOPMENT.md      # Development guide
├── LICENSE             # MIT License
├── README.md           # Project documentation (this file)
└── README_简化版.md    # Simplified Chinese README
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use descriptive commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)
- **Documentation**: [GitHub Pages](https://taobaoaz.github.io/paper-formatter/)
- **Releases**: [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Built with Python and PyQt5
- Font search powered by Google Fonts API
- Icons from FontAwesome

---

**Development Assistant · Rigorous Professional Edition**  
**© 2024 All Rights Reserved**