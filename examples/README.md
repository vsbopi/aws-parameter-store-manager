# Examples

This directory contains example scripts and usage patterns for the AWS Parameter Store Manager.

## Files

- `basic_usage.py` - Basic programmatic usage examples
- `README.md` - This file

## Running Examples

### Prerequisites

1. Ensure you have AWS credentials configured
2. Install the required dependencies: `pip install -r ../requirements.txt`
3. Have appropriate IAM permissions for Parameter Store operations

### Basic Usage Example

```bash
cd examples
python basic_usage.py
```

The basic usage example demonstrates:
- Different authentication methods
- Connecting to AWS Parameter Store
- Reading parameters from CSV
- Creating and updating parameters
- Exporting parameters to CSV

### Authentication Examples

The examples show how to use different authentication methods:

1. **Access Key Authentication**
2. **AWS Profile Authentication**
3. **Environment Variables Authentication**
4. **Default Credential Chain**

### Customizing Examples

Edit the `basic_usage.py` file to:
- Use your own AWS credentials
- Modify parameter names and values
- Add your own parameter operations
- Test different authentication methods

### Safety Notes

⚠️ **Important**: The examples are designed to be safe and use test parameters. However:

- Always test in a non-production environment first
- Review the code before running
- Ensure you have appropriate permissions
- Be careful with parameter names to avoid conflicts

## Contributing Examples

If you have useful examples or patterns, please consider contributing them:

1. Create a new Python file in this directory
2. Follow the existing code style
3. Add documentation and comments
4. Update this README
5. Submit a pull request

## Common Patterns

### Reading Configuration from Parameters

```python
# Get database configuration
db_host = manager.parameter_exists('/myapp/database/host')[1]['Value']
db_port = manager.parameter_exists('/myapp/database/port')[1]['Value']
db_password = manager.parameter_exists('/myapp/database/password')[1]['Value']
```

### Bulk Parameter Updates

```python
# Read from CSV and upload
parameters = manager.read_csv_parameters('config.csv')
for param in parameters:
    manager.create_or_update_parameter(param, overwrite=True)
```

### Environment-Specific Parameters

```python
# Use different parameter paths for different environments
env = os.getenv('ENVIRONMENT', 'dev')
param_path = f'/myapp/{env}/database/host'
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your AWS credentials are valid
2. **Permission Errors**: Check your IAM permissions
3. **Import Errors**: Make sure you're running from the correct directory
4. **Parameter Not Found**: Verify parameter names and paths

### Getting Help

- Check the main README.md for detailed documentation
- Review the CONTRIBUTING.md for development guidelines
- Open an issue on GitHub for bugs or questions
