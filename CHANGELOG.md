# Changelog

All notable changes to Paper Formatter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline with UTF-8 encoding fixes
- Comprehensive documentation (README, CONTRIBUTING, ISSUE_TEMPLATE)
- MIT License
- Repository topics for better discoverability

### Changed
- Organized release notes into `releases/` directory
- Updated README with proper release notes references
- Improved GitHub Actions workflow configuration

## [v2.2.3] - 2026-03-21

### Fixed
- GitHub Actions UTF-8 encoding issues on Windows
- Workflow configuration for better cross-platform compatibility

### Changed
- Simplified UTF-8 configuration in CI/CD pipelines
- Updated documentation structure

## [v2.2.2] - 2026-03-20

### Added
- Font package search and download functionality
- Font manager with import/export capabilities
- Google Fonts API integration
- Chinese font priority search
- Multi-threaded font downloads
- Real-time download progress display
- Cross-platform font installation support

### Technical Details
- Added `modules/font_downloader.py` (~380 lines)
- Added `modules/font_manager_dialog.py` (~400 lines)
- Integrated font management into main application
- Updated dependencies with `fonttools>=4.40.0`

## [v2.2.1] - 2026-03-20

### Added
- Batch PDF export functionality
- Enhanced Chinese font support
- Improved PDF generation quality

### Fixed
- Font rendering issues in PDF exports
- Character encoding problems

## [v2.2.0] - 2026-03-20

### Added
- PDF export functionality
- Comprehensive help system
- User documentation

### Improved
- User interface for export options
- Error handling during PDF generation

## [v2.1.8] - 2026-03-20

### Added
- Auto backup manager with configurable intervals
- Smart cleanup strategies (importance/recent/time-based)
- Snapshot importance marking

### Improved
- Data protection and recovery options
- Backup management interface

## [v2.1.6] - 2026-03-19

### Added
- Document snapshot functionality
- Configuration snapshot UI integration
- State preservation features

## [v2.1.0] - [v2.1.5]

### Added
- Initial core functionality
- Basic document formatting
- Template management
- Reference management system

### Improved
- User interface
- Performance optimizations
- Bug fixes and stability improvements

---

## Release Notes Location

Detailed release notes for each version are available in the `releases/` directory:

- `releases/RELEASE_NOTES_v2.2.2.md` - Font management update
- `releases/RELEASE_NOTES_v2.2.1.md` - PDF export and Chinese fonts
- `releases/RELEASE_NOTES_v2.2.0.md` - PDF export and help system
- `releases/RELEASE_NOTES_v2.1.8.md` - Auto backup and cleanup
- `releases/RELEASE_NOTES_v2.1.6.md` - Document snapshot integration
- ... and other version-specific release notes

## Versioning Scheme

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

## Contributing to the Changelog

When adding new entries, please follow the format:
- Group changes under Added, Changed, Deprecated, Removed, Fixed, or Security
- Use present tense ("Add feature" not "Added feature")
- Reference issues and pull requests when applicable