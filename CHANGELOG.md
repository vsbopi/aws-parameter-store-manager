# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multiple AWS authentication methods support
- AWS Profile authentication
- AWS SSO (Single Sign-On) authentication
- IAM Role assumption authentication
- Environment variables authentication
- Default AWS credential chain support
- Profile listing functionality in both GUI and CLI
- Enhanced CLI with comprehensive authentication options
- Session caching for improved performance
- Scrollable configuration interface in GUI
- Dynamic form display based on authentication method
- Enhanced error handling and validation
- Comprehensive documentation updates

### Changed
- Refactored authentication system to support multiple methods
- Updated GUI with radio button selection for authentication methods
- Enhanced CLI argument structure for better usability
- Improved connection status display with authentication method info
- Updated README with comprehensive authentication documentation

### Fixed
- Better error handling for authentication failures
- Improved session management and credential validation

## [1.0.0] - 2024-01-XX

### Added
- Initial release of AWS Parameter Store Manager
- GUI application for parameter management
- Command-line interface (CLI)
- Bulk parameter upload from CSV files
- Parameter viewing with search and filter capabilities
- Secure string decryption support
- Parameter export to CSV
- Individual parameter deletion
- Support for Standard, Advanced, and Intelligent-Tiering
- KMS encryption support for SecureString parameters
- Real-time parameter refresh
- Conflict detection for existing parameters
- Context menu for parameter operations (copy, delete)
- Cross-platform support (Windows, macOS, Linux)

### Security
- Secure handling of AWS credentials
- Support for encrypted SecureString parameters
- Session token support for temporary credentials
