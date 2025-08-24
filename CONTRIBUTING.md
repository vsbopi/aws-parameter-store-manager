# Contributing to AWS Parameter Store Manager

Thank you for your interest in contributing to AWS Parameter Store Manager! We welcome contributions from the community and are pleased to have you join us.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes
5. Make your changes
6. Test your changes
7. Submit a pull request

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues reported in the GitHub Issues
- **Feature enhancements**: Add new functionality or improve existing features
- **Documentation**: Improve documentation, add examples, or fix typos
- **Testing**: Add or improve test coverage
- **Performance improvements**: Optimize code for better performance
- **UI/UX improvements**: Enhance the user interface and experience

### Areas for Contribution

- **Authentication methods**: Add support for new AWS authentication methods
- **Parameter management**: Enhance parameter CRUD operations
- **Export/Import formats**: Support for additional file formats (JSON, YAML, etc.)
- **Bulk operations**: Improve bulk parameter operations
- **Error handling**: Better error messages and recovery
- **Logging**: Enhanced logging and debugging capabilities
- **Cross-platform support**: Improve compatibility across different operating systems

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/aws-parameter-store-manager.git
   cd aws-parameter-store-manager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up AWS credentials** (for testing):
   - Configure AWS CLI: `aws configure`
   - Or set environment variables
   - Or use any other supported authentication method

5. **Test the setup**:
   ```bash
   python gui_app.py  # Test GUI
   python cli_app.py --help  # Test CLI
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting

We recommend using these tools:

- **Black** for code formatting: `pip install black`
- **Flake8** for linting: `pip install flake8`
- **isort** for import sorting: `pip install isort`

Example usage:
```bash
black .
flake8 .
isort .
```

### Documentation

- Update README.md if you add new features
- Add docstrings to new functions and classes
- Include examples in docstrings where helpful
- Update CLI help text for new command-line options

## Testing

### Manual Testing

Before submitting changes:

1. **Test GUI functionality**:
   - Test all authentication methods
   - Test parameter upload/download
   - Test parameter viewing and management
   - Test error scenarios

2. **Test CLI functionality**:
   - Test all commands with different authentication methods
   - Test edge cases and error conditions
   - Verify help text is accurate

3. **Cross-platform testing** (if possible):
   - Test on Windows, macOS, and Linux
   - Test with different Python versions

### Test Data

- Use the provided `sample_parameters.csv` for testing
- Create test parameters in a dedicated AWS account/region
- Clean up test resources after testing

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, well-documented code
   - Follow the coding standards
   - Test your changes thoroughly

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes
- **Breaking changes**: Clearly mark any breaking changes
- **Documentation**: Update documentation if needed

### Commit Message Format

Use clear, descriptive commit messages:

```
Add support for AWS SSO authentication

- Implement SSO authentication in config.py
- Add SSO configuration UI in GUI
- Add SSO command-line options
- Update documentation with SSO examples

Fixes #123
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Environment**: OS, Python version, dependency versions
- **Steps to reproduce**: Clear steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Screenshots**: If applicable
- **Error messages**: Full error messages and stack traces
- **Configuration**: Authentication method used (without sensitive data)

### Feature Requests

When requesting features:

- **Use case**: Describe the problem you're trying to solve
- **Proposed solution**: Your idea for how to solve it
- **Alternatives**: Other solutions you've considered
- **Additional context**: Any other relevant information

### Security Issues

For security-related issues:

- **Do not** create a public GitHub issue
- Email the maintainers directly
- Include details about the vulnerability
- Allow time for the issue to be addressed before public disclosure

## Questions and Support

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the README.md for usage information

## Recognition

Contributors will be recognized in:

- GitHub contributors list
- Release notes for significant contributions
- README.md acknowledgments section

Thank you for contributing to AWS Parameter Store Manager! 🎉
