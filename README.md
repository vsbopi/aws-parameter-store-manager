# AWS Parameter Store Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Parameter%20Store-orange.svg)](https://aws.amazon.com/systems-manager/features/#Parameter_Store)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/aws-parameter-store-manager)

A comprehensive GUI and CLI application for managing AWS Systems Manager Parameter Store entries with support for multiple authentication methods, bulk uploads, parameter viewing, and secure string decryption.

![AWS Parameter Store Manager](https://img.shields.io/badge/Status-Production%20Ready-green.svg)

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Authentication Methods](#authentication-methods)
- [Required AWS IAM Permissions](#required-aws-iam-permissions)
- [Usage](#usage)
  - [GUI Application](#gui-application)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
- [CSV File Examples](#csv-file-examples)
- [Parameter Types](#parameter-types)
- [Parameter Tiers](#parameter-tiers)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multiple Authentication Methods**: Support for Access Keys, AWS Profiles, SSO, IAM Role Assumption, Environment Variables, and Default Credential Chain
- **Bulk Parameter Upload**: Upload multiple parameters from CSV files
- **Conflict Detection**: Automatically detects existing parameters and asks for confirmation before overwriting
- **Secure String Support**: Full support for SecureString parameters with KMS encryption
- **Parameter Viewing**: View all current parameters with decryption of secure strings
- **Search and Filter**: Search through parameters by name or value
- **Export Functionality**: Export current parameters to CSV format
- **Parameter Management**: Delete individual parameters with confirmation
- **Multiple Tiers**: Support for Standard, Advanced, and Intelligent-Tiering
- **Real-time Refresh**: Refresh parameter list to see latest changes
- **Command Line Interface**: Full CLI support with all authentication methods

## Screenshots
<img width="1052" height="822" alt="AWS Authentication" src="https://github.com/user-attachments/assets/c74478e8-6f50-4b76-9d26-1a14690d6e72" />

<img width="1052" height="825" alt="Upload Parameters" src="https://github.com/user-attachments/assets/253c46bf-8b10-414a-974e-abf99f56053f" />

<img width="1051" height="822" alt="Visualize or Download Parameters" src="https://github.com/user-attachments/assets/e0bafb2d-1aad-4b34-ae74-90ef721f5b2a" />

### GUI Application
*Screenshots will be added soon showing the main interface, authentication methods, and parameter management features.*

### CLI Usage
```bash
$ python cli_app.py --help
usage: cli_app.py [-h] [--auth-method {access-key,profile,sso,role,environment,default}]
                  [--access-key ACCESS_KEY] [--secret-key SECRET_KEY]
                  ...

AWS Parameter Store Manager CLI
```

## Prerequisites

- Python 3.7 or higher
- AWS account with appropriate IAM permissions for Parameter Store
- AWS credentials configured using one of the supported authentication methods (see Authentication Methods section)

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Authentication Methods

This application supports multiple AWS authentication methods to accommodate different use cases and security requirements:

### 1. Access Key & Secret Key
Traditional AWS access key authentication with optional session token for temporary credentials.

**GUI Configuration:**
- Select "Access Key & Secret" authentication method
- Enter AWS Access Key ID
- Enter AWS Secret Access Key
- Optionally enter Session Token (for temporary credentials)

**CLI Usage:**
```bash
python cli_app.py --auth-method access-key --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY [--session-token YOUR_TOKEN] list
```

### 2. AWS Profile
Use AWS CLI configured profiles from `~/.aws/credentials` and `~/.aws/config`.

**Setup:**
```bash
aws configure --profile myprofile
```

**GUI Configuration:**
- Select "AWS Profile" authentication method
- Enter profile name or click "List Available Profiles" to see configured profiles

**CLI Usage:**
```bash
python cli_app.py --auth-method profile --profile myprofile list
```

### 3. AWS SSO (Single Sign-On)
Use AWS SSO for centralized authentication management.

**Prerequisites:**
- AWS SSO configured in your organization
- AWS CLI v2 installed and configured for SSO

**Setup:**
```bash
aws configure sso
```

**GUI Configuration:**
- Select "AWS SSO" authentication method
- Enter SSO Start URL
- Enter SSO Region
- Enter Account ID
- Enter Role Name

**CLI Usage:**
```bash
python cli_app.py --auth-method sso --sso-start-url https://my-sso-portal.awsapps.com/start --sso-region us-east-1 --sso-account-id 123456789012 --sso-role-name MyRole list
```

### 4. IAM Role Assumption
Assume an IAM role using existing credentials.

**GUI Configuration:**
- Select "IAM Role Assumption" authentication method
- Enter Role ARN (required)
- Optionally enter Session Name, External ID, MFA Serial, and MFA Token

**CLI Usage:**
```bash
python cli_app.py --auth-method role --role-arn arn:aws:iam::123456789012:role/MyRole [--external-id EXTERNAL_ID] [--mfa-serial MFA_SERIAL --mfa-token MFA_TOKEN] list
```

### 5. Environment Variables
Use environment variables for credential configuration.

**Setup:**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_SESSION_TOKEN=your_session_token  # Optional
export AWS_DEFAULT_REGION=us-east-1  # Optional
```

**GUI Configuration:**
- Select "Environment Variables" authentication method
- No additional configuration needed

**CLI Usage:**
```bash
python cli_app.py --auth-method environment list
```

### 6. Default Credential Chain
Use AWS default credential provider chain (recommended for EC2, ECS, Lambda, etc.).

**Credential Chain Order:**
1. Environment variables
2. AWS credentials file (`~/.aws/credentials`)
3. AWS config file (`~/.aws/config`)
4. IAM roles for Amazon EC2
5. IAM roles for tasks (ECS)
6. IAM roles for Lambda functions

**GUI Configuration:**
- Select "Default Credential Chain" authentication method
- No additional configuration needed

**CLI Usage:**
```bash
python cli_app.py --auth-method default list
# or simply (default is 'default')
python cli_app.py list
```

## Required AWS IAM Permissions

Your AWS user/role needs the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:PutParameter",
                "ssm:DeleteParameter",
                "ssm:DescribeParameters",
                "ssm:GetParameterHistory"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:DescribeKey"
            ],
            "Resource": "arn:aws:kms:*:*:key/*"
        }
    ]
}
```

## Usage

### GUI Application

#### Starting the Application

Run the main application:

```bash
python gui_app.py
```

Or use the provided launcher scripts:
- **Windows**: Double-click `run_gui.bat`
- **Unix/Linux/macOS**: Run `./run_gui.sh`

#### Configuration Tab

1. **Authentication Method**: Select your preferred authentication method:
   - Access Key & Secret
   - AWS Profile
   - AWS SSO
   - IAM Role Assumption
   - Environment Variables
   - Default Credential Chain

2. **Method-Specific Configuration**: Fill in the required fields based on your selected authentication method

3. **Common Settings**:
   - AWS Region (default: us-east-1)
   - Default KMS Key (default: alias/aws/ssm)

4. **Connect**: Click "Connect to AWS" to establish connection

### Upload Parameters Tab

1. **CSV File Selection**: Browse and select your CSV file containing parameters

2. **CSV Format**: Your CSV file must have the following structure:

```csv
key,value,type,tier,kms
/app/database/host,localhost,String,Standard,
/app/database/password,secret123,SecureString,Standard,alias/aws/ssm
/app/features,feature1;feature2,StringList,Standard,
```

**Required Columns:**
- `key`: Parameter name (must start with /)
- `value`: Parameter value
- `type`: String, StringList, or SecureString

**Optional Columns:**
- `tier`: Standard (default), Advanced, or Intelligent-Tiering
- `kms`: KMS key alias (only used for SecureString, defaults to alias/aws/ssm)

3. **Upload Options**:
   - Check "Overwrite existing parameters without asking" to skip confirmation dialogs
   - Click "Upload Parameters" to start the process

4. **Upload Log**: Monitor the upload progress and results in the log area

### View Parameters Tab

1. **Refresh Parameters**: Click to load all current parameters from AWS
2. **Decrypt SecureString values**: Toggle to decrypt secure strings (enabled by default)
3. **Search**: Filter parameters by name or value
4. **Export to CSV**: Export current parameter list to a CSV file

**Parameter Actions** (right-click on parameter):
- Copy parameter name to clipboard
- Copy parameter value to clipboard
- Delete parameter (with confirmation)

## Command Line Interface (CLI)

The application also provides a comprehensive command-line interface for automation and scripting.

### Basic Usage

```bash
python cli_app.py [authentication options] <command> [command options]
```

### Available Commands

#### List Parameters
```bash
# List all parameters
python cli_app.py list

# List parameters with filtering
python cli_app.py list --filter database

# Export to CSV
python cli_app.py list --output parameters.csv

# List without decryption
python cli_app.py list --no-decrypt
```

#### Upload Parameters
```bash
# Upload from CSV file
python cli_app.py upload parameters.csv

# Upload with automatic overwrite
python cli_app.py upload parameters.csv --overwrite
```

#### Get Specific Parameter
```bash
# Get a single parameter
python cli_app.py get /app/database/host

# Get parameter without decryption
python cli_app.py get /app/database/password --no-decrypt
```

#### Delete Parameter
```bash
# Delete with confirmation
python cli_app.py delete /app/old/parameter

# Force delete without confirmation
python cli_app.py delete /app/old/parameter --force
```

#### List Available Profiles
```bash
# Show configured AWS profiles
python cli_app.py list-profiles
```

### CLI Authentication Examples

```bash
# Using access keys
python cli_app.py --auth-method access-key --access-key AKIAIOSFODNN7EXAMPLE --secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY list

# Using AWS profile
python cli_app.py --auth-method profile --profile production list

# Using environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
python cli_app.py --auth-method environment list

# Using default credential chain (default)
python cli_app.py list

# Using IAM role assumption
python cli_app.py --auth-method role --role-arn arn:aws:iam::123456789012:role/ParameterStoreRole list

# Using SSO
python cli_app.py --auth-method sso --sso-start-url https://my-sso.awsapps.com/start --sso-region us-east-1 --sso-account-id 123456789012 --sso-role-name PowerUserAccess list
```

## CSV File Examples

### Basic Example
```csv
key,value,type
/app/name,MyApplication,String
/app/version,1.0.0,String
/app/debug,false,String
```

### Advanced Example with All Columns
```csv
key,value,type,tier,kms
/app/database/host,db.example.com,String,Standard,
/app/database/password,mySecretPassword,SecureString,Standard,alias/aws/ssm
/app/features/enabled,feature1;feature2;feature3,StringList,Advanced,
/app/encryption/key,superSecretKey123,SecureString,Standard,alias/my-custom-key
```

## Parameter Types

- **String**: Plain text parameter
- **StringList**: Comma-separated list of values (use semicolon in CSV to avoid conflicts)
- **SecureString**: Encrypted parameter using KMS

## Parameter Tiers

- **Standard**: Up to 4KB, standard rate limits
- **Advanced**: Up to 8KB, higher rate limits, additional charges apply
- **Intelligent-Tiering**: Automatically moves between Standard and Advanced based on usage

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify AWS credentials are correct
   - Check if your account has the required IAM permissions
   - Ensure the specified region is correct

2. **Parameter Upload Fails**
   - Check CSV file format and encoding (should be UTF-8)
   - Verify parameter names start with '/'
   - Ensure KMS key exists and you have access to it

3. **Cannot Decrypt SecureString**
   - Verify you have KMS decrypt permissions
   - Check if the KMS key exists and is accessible

4. **Large Parameter Lists Loading Slowly**
   - Use search/filter to narrow down results
   - Consider using AWS CLI for very large parameter stores

### Error Messages

- **"Parameter name must start with /"**: Parameter names must begin with a forward slash
- **"Invalid parameter type"**: Use only String, StringList, or SecureString
- **"Access Denied"**: Check your IAM permissions
- **"Invalid KMS key"**: Verify the KMS key alias exists and you have access

## Security Considerations

- **Credentials**: Never hard-code AWS credentials in your code
- **Session Tokens**: Use temporary credentials when possible
- **KMS Keys**: Use appropriate KMS key policies to control access
- **SecureString**: Always use SecureString for sensitive data like passwords and API keys
- **Network**: Ensure you're connecting from a secure network

## File Structure

```
aws-parameter-store/
├── gui_app.py              # Main GUI application
├── cli_app.py              # Command line interface
├── aws_parameter_manager.py # Core AWS Parameter Store operations
├── config.py               # Configuration and authentication management
├── requirements.txt        # Python dependencies
├── sample_parameters.csv   # Example CSV file
├── run_gui.bat            # Windows GUI launcher
├── run_gui.sh             # Unix/Linux GUI launcher
└── README.md              # This file
```

## Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report bugs** - Found a bug? Please create an issue with details
- 💡 **Suggest features** - Have an idea? We'd love to hear it
- 📖 **Improve documentation** - Help make our docs better
- 🔧 **Submit code** - Fix bugs or add new features
- 🧪 **Test the application** - Help us test on different platforms

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for detailed information about our development process, coding standards, and how to submit pull requests.

### Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. By participating, you agree to abide by its terms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ **Commercial use** - You can use this software commercially
- ✅ **Modification** - You can modify the software
- ✅ **Distribution** - You can distribute the software
- ✅ **Private use** - You can use the software privately
- ❌ **Liability** - The authors are not liable for any damages
- ❌ **Warranty** - The software is provided "as is"

## Acknowledgments

- Thanks to the AWS team for providing the Systems Manager Parameter Store service
- Thanks to the Python community for the excellent libraries used in this project
- Thanks to all contributors who help improve this project

## Support

- 📖 **Documentation**: Check this README and the [Contributing Guide](CONTRIBUTING.md)
- 🐛 **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/aws-parameter-store-manager/issues)
- 💬 **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/yourusername/aws-parameter-store-manager/discussions)
- 🔒 **Security**: Report security issues via our [Security Policy](SECURITY.md)

---

**Made with ❤️ for the AWS community**
