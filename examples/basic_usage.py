#!/usr/bin/env python3
"""
Basic usage examples for AWS Parameter Store Manager

This script demonstrates how to use the AWS Parameter Store Manager
programmatically in your own Python applications.
"""

import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_parameter_manager import AWSParameterManager
from config import AuthMethod, aws_config


def example_access_key_auth():
    """Example using access key authentication"""
    print("=== Access Key Authentication Example ===")

    # Configure authentication (replace with your credentials)
    aws_config.set_access_key_auth(
        access_key_id="YOUR_ACCESS_KEY",
        secret_access_key="YOUR_SECRET_KEY",
        region="us-east-1",
    )

    # Create manager and connect
    manager = AWSParameterManager()
    if manager.connect():
        print("✅ Connected successfully!")

        # Get all parameters
        parameters = manager.get_all_parameters()
        print(f"Found {len(parameters)} parameters")

        # Display first few parameters
        for param in parameters[:5]:
            print(f"  - {param['Name']}: {param['Type']}")
    else:
        print("❌ Failed to connect")


def example_profile_auth():
    """Example using AWS profile authentication"""
    print("\n=== AWS Profile Authentication Example ===")

    # Configure authentication using AWS profile
    aws_config.set_profile_auth(
        profile_name="default", region="us-east-1"  # Replace with your profile name
    )

    # Create manager and connect
    manager = AWSParameterManager()
    if manager.connect():
        print("✅ Connected successfully using profile!")

        # Example: Create a test parameter
        test_param = {
            "key": "/example/test-parameter",
            "value": "Hello from Python!",
            "type": "String",
            "tier": "Standard",
            "kms_key": "",
        }

        if manager.create_or_update_parameter(test_param, overwrite=True):
            print(f"✅ Created parameter: {test_param['key']}")
        else:
            print(f"❌ Failed to create parameter: {test_param['key']}")
    else:
        print("❌ Failed to connect")


def example_environment_auth():
    """Example using environment variables authentication"""
    print("\n=== Environment Variables Authentication Example ===")

    # Configure authentication using environment variables
    aws_config.set_environment_auth(region="us-east-1")

    # Create manager and connect
    manager = AWSParameterManager()
    if manager.connect():
        print("✅ Connected successfully using environment variables!")

        # Example: Get a specific parameter
        exists, param = manager.parameter_exists("/example/test-parameter")
        if exists:
            print(f"✅ Found parameter: {param['Name']} = {param['Value']}")
        else:
            print("❌ Parameter not found")
    else:
        print(
            "❌ Failed to connect (make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set)"
        )


def example_csv_operations():
    """Example CSV operations"""
    print("\n=== CSV Operations Example ===")

    # Use default authentication
    aws_config.set_default_auth(region="us-east-1")

    manager = AWSParameterManager()
    if manager.connect():
        print("✅ Connected successfully!")

        # Read parameters from CSV (using the sample file)
        try:
            csv_file = os.path.join(
                os.path.dirname(__file__), "..", "sample_parameters.csv"
            )
            parameters = manager.read_csv_parameters(csv_file)
            print(f"✅ Read {len(parameters)} parameters from CSV")

            # Display first few parameters
            for param in parameters[:3]:
                print(f"  - {param['key']}: {param['type']} ({param['tier']})")

        except Exception as e:
            print(f"❌ Error reading CSV: {e}")

        # Export current parameters to CSV
        try:
            output_file = "exported_parameters.csv"
            if manager.export_parameters_to_csv(output_file):
                print(f"✅ Exported parameters to {output_file}")
            else:
                print("❌ Failed to export parameters")
        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")
    else:
        print("❌ Failed to connect")


def main():
    """Main function to run examples"""
    print("AWS Parameter Store Manager - Usage Examples")
    print("=" * 50)

    # Note: These examples require valid AWS credentials
    # Uncomment the examples you want to run:

    # example_access_key_auth()
    # example_profile_auth()
    # example_environment_auth()
    # example_csv_operations()

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nNote: Uncomment the example functions in main() to run them.")
    print("Make sure you have valid AWS credentials configured.")


if __name__ == "__main__":
    main()
