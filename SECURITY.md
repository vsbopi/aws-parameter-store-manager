# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

The AWS Parameter Store Manager team and community take security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report a Security Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to the project maintainers. You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

### What to Expect

After you submit a report, we will:

1. **Acknowledge receipt** of your vulnerability report within 48 hours
2. **Confirm the problem** and determine the affected versions
3. **Audit code** to find any potential similar problems
4. **Prepare fixes** for all supported releases
5. **Release patched versions** as soon as possible
6. **Publicly disclose** the vulnerability after fixes are available

## Security Best Practices

When using AWS Parameter Store Manager, please follow these security best practices:

### Credential Management

- **Never commit AWS credentials** to version control
- **Use IAM roles** when running on AWS infrastructure (EC2, ECS, Lambda)
- **Use temporary credentials** (STS tokens) when possible
- **Rotate credentials regularly**
- **Use least privilege principle** - grant only necessary permissions

### Authentication Methods

- **Prefer IAM roles** over access keys when possible
- **Use AWS SSO** for centralized authentication management
- **Enable MFA** for sensitive operations when using role assumption
- **Use environment variables** or AWS credential files instead of hardcoding credentials

### Parameter Store Security

- **Use SecureString** for sensitive data (passwords, API keys, etc.)
- **Use appropriate KMS keys** with proper key policies
- **Regularly audit parameter access** using CloudTrail
- **Use parameter hierarchies** to organize and control access
- **Implement least privilege** IAM policies for parameter access

### Network Security

- **Use VPC endpoints** when running in AWS VPC
- **Enable CloudTrail logging** for audit trails
- **Monitor unusual access patterns**
- **Use secure networks** when accessing parameters

### Application Security

- **Keep dependencies updated** - regularly update Python packages
- **Validate input data** - especially CSV files and parameter names
- **Handle errors securely** - don't expose sensitive information in error messages
- **Log security events** appropriately without logging sensitive data

## Security Features

This application includes several security features:

- **Credential encryption** - SecureString parameters are encrypted at rest
- **Session management** - Secure handling of temporary credentials
- **Input validation** - Validation of parameter names and values
- **Error handling** - Secure error messages that don't expose sensitive data
- **Audit logging** - Integration with AWS CloudTrail for access logging

## Known Security Considerations

- **GUI credential storage** - The GUI does not persist credentials between sessions
- **Memory handling** - Credentials are cleared from memory when possible
- **File permissions** - Ensure CSV files containing sensitive data have appropriate permissions
- **Network traffic** - All communication with AWS uses HTTPS/TLS

## Security Updates

Security updates will be released as patch versions and will be clearly marked in the changelog. We recommend:

- **Subscribe to releases** to be notified of security updates
- **Update promptly** when security patches are available
- **Review changelogs** for security-related changes

## Responsible Disclosure

We kindly ask that you:

- **Give us reasonable time** to fix the issue before public disclosure
- **Avoid accessing or modifying data** that doesn't belong to you
- **Don't perform actions** that could harm the service or other users
- **Don't publicly disclose** the vulnerability until we've had a chance to address it

## Recognition

We appreciate security researchers and users who help keep AWS Parameter Store Manager secure. Contributors who report valid security issues will be acknowledged in our security advisories (unless they prefer to remain anonymous).

Thank you for helping keep AWS Parameter Store Manager and our users safe!
