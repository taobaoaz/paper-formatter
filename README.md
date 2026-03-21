# Paper Formatter 🎓

[![Build Status](https://github.com/taobaoaz/paper-formatter/actions/workflows/build-windows.yml/badge.svg)](https://github.com/taobaoaz/paper-formatter/actions/workflows/build-windows.yml)
[![Release](https://img.shields.io/github/v/release/taobaoaz/paper-formatter)](https://github.com/taobaoaz/paper-formatter/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

A professional academic paper formatting tool that helps researchers and students format their papers with ease. Supports Chinese and English documents with advanced formatting features.

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

## 🚀 Quick Start

### Prerequisites
- **Operating System:** Windows 7/8/10/11, Linux, macOS
- **Python:** 3.8+
- **Memory:** At least 2GB
- **Disk:** At least 100MB

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/taobaoaz/paper-formatter.git
   cd paper-formatter
   ```

2. **Navigate to the launcher folder:**
   ```bash
   cd 启动文件
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   **Windows:**
   ```
   Double-click 启动.bat
   ```

   **Linux/Mac:**
   ```bash
   ./启动.sh
   ```

   **Or via command line:**
   ```bash
   python launcher.py
   ```

## 📁 Project Structure

```
paper-formatter/
│
├── 🚀 启动文件/       # Launcher files (start here)
├── 🔧 核心模块/       # Core modules
├── ⚙️ 功能模块/       # Feature modules
├── 📚 文档资料/       # Documentation
└── 📝 临时文件/       # Temporary files
```

## 🛠️ Development

### Building from Source

The project uses GitHub Actions for automated builds. When you push a tag starting with 'v', it automatically:

1. **Builds Windows EXE** - Creates a portable executable
2. **Builds Installer** - Creates an installer package
3. **Creates Releases** - Publishes to GitHub Releases

### Running Tests

```bash
# Run test scripts
python temp/test_v2.2.2.py
```

## 📦 Releases

### Latest Release: v2.2.2

**Font Management Update** - Added online font search and download capabilities.

### Previous Releases

- **v2.2.1** - Batch PDF export and Chinese font support
- **v2.2.0** - PDF export and help system
- **v2.1.8** - Auto backup and smart cleanup
- **v2.1.6** - Document snapshot and configuration snapshot UI integration

Check the `releases/releases/RELEASE_NOTES_v*.md` files for detailed release information.

## 🔧 Font Management

### Features
- ✅ Online font library search
- ✅ Chinese font priority search
- ✅ Font package download (multi-threaded)
- ✅ Real-time download progress display
- ✅ Automatic font installation
- ✅ Cross-platform support (Windows/macOS/Linux)

### Usage
1. Click "Help" → "Font Management"
2. Or use shortcut Ctrl+Alt+F
3. Switch to "Search & Download" tab
4. Enter font name (optional)
5. Check "Search Chinese fonts only"
6. Click "Search"
7. Select fonts and click "Download Selected"

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)
- **Repository:** [GitHub](https://github.com/taobaoaz/paper-formatter)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to the Python community for excellent libraries
- Inspired by the needs of academic researchers and students

---

**Development Assistant · Rigorous Professional Edition**  
**© 2024 All Rights Reserved**