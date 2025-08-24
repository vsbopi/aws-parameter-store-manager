#!/usr/bin/env python3
"""
Command Line Interface for AWS Parameter Store Manager
"""
import argparse
import sys
import getpass
import os
from aws_parameter_manager import AWSParameterManager
from config import aws_config, AuthMethod


def main():
    parser = argparse.ArgumentParser(description="AWS Parameter Store Manager CLI")

    # Authentication method selection
    auth_group = parser.add_mutually_exclusive_group(required=False)
    auth_group.add_argument(
        "--auth-method",
        choices=["access-key", "profile", "sso", "role", "environment", "default"],
        default="default",
        help="Authentication method (default: default)",
    )

    # Access key authentication
    parser.add_argument(
        "--access-key", help="AWS Access Key ID (for access-key method)"
    )
    parser.add_argument(
        "--secret-key", help="AWS Secret Access Key (for access-key method)"
    )
    parser.add_argument(
        "--session-token", help="AWS Session Token (optional, for access-key method)"
    )

    # Profile authentication
    parser.add_argument("--profile", help="AWS Profile name (for profile method)")

    # SSO authentication
    parser.add_argument("--sso-start-url", help="SSO start URL (for sso method)")
    parser.add_argument("--sso-region", help="SSO region (for sso method)")
    parser.add_argument("--sso-account-id", help="SSO account ID (for sso method)")
    parser.add_argument("--sso-role-name", help="SSO role name (for sso method)")

    # Role assumption
    parser.add_argument("--role-arn", help="Role ARN to assume (for role method)")
    parser.add_argument(
        "--role-session-name", help="Role session name (optional, for role method)"
    )
    parser.add_argument("--external-id", help="External ID (optional, for role method)")
    parser.add_argument(
        "--mfa-serial", help="MFA device serial number (optional, for role method)"
    )
    parser.add_argument("--mfa-token", help="MFA token (optional, for role method)")

    # Common settings
    parser.add_argument(
        "--region", default="us-east-1", help="AWS Region (default: us-east-1)"
    )
    parser.add_argument(
        "--kms-key", default="alias/aws/ssm", help="Default KMS key alias"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload parameters from CSV")
    upload_parser.add_argument("csv_file", help="Path to CSV file")
    upload_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing parameters without asking",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all parameters")
    list_parser.add_argument(
        "--decrypt",
        action="store_true",
        default=True,
        help="Decrypt SecureString values",
    )
    list_parser.add_argument("--output", help="Output to CSV file")
    list_parser.add_argument("--filter", help="Filter parameters by name")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get specific parameter")
    get_parser.add_argument("parameter_name", help="Parameter name to retrieve")
    get_parser.add_argument(
        "--decrypt", action="store_true", default=True, help="Decrypt if SecureString"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete parameter")
    delete_parser.add_argument("parameter_name", help="Parameter name to delete")
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation")

    # List profiles command
    list_profiles_parser = subparsers.add_parser(
        "list-profiles", help="List available AWS profiles"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Handle list-profiles command early
    if args.command == "list-profiles":
        return list_profiles_command()

    # Configure AWS authentication
    try:
        configure_aws_auth(args)
    except Exception as e:
        print(f"Error configuring authentication: {str(e)}")
        return 1

    # Initialize manager
    manager = AWSParameterManager()

    # Connect to AWS
    print("Connecting to AWS...")
    if not manager.connect():
        print(
            "Failed to connect to AWS. Please check your credentials and permissions."
        )
        return 1

    auth_info = aws_config.get_auth_info()
    print(
        f"Connected to AWS using {auth_info['method']} method in region: {auth_info['region']}"
    )

    # Execute command
    if args.command == "upload":
        return upload_command(manager, args)
    elif args.command == "list":
        return list_command(manager, args)
    elif args.command == "get":
        return get_command(manager, args)
    elif args.command == "delete":
        return delete_command(manager, args)


def configure_aws_auth(args):
    """Configure AWS authentication based on command line arguments"""
    auth_method = args.auth_method

    if auth_method == "access-key":
        if not args.access_key or not args.secret_key:
            raise ValueError(
                "Access key and secret key are required for access-key authentication method"
            )

        aws_config.set_access_key_auth(
            access_key_id=args.access_key,
            secret_access_key=args.secret_key,
            session_token=args.session_token,
            region=args.region,
        )

    elif auth_method == "profile":
        if not args.profile:
            raise ValueError(
                "Profile name is required for profile authentication method"
            )

        aws_config.set_profile_auth(profile_name=args.profile, region=args.region)

    elif auth_method == "sso":
        if not all(
            [
                args.sso_start_url,
                args.sso_region,
                args.sso_account_id,
                args.sso_role_name,
            ]
        ):
            raise ValueError(
                "All SSO parameters are required for SSO authentication method"
            )

        aws_config.set_sso_auth(
            sso_start_url=args.sso_start_url,
            sso_region=args.sso_region,
            sso_account_id=args.sso_account_id,
            sso_role_name=args.sso_role_name,
            region=args.region,
        )

    elif auth_method == "role":
        if not args.role_arn:
            raise ValueError("Role ARN is required for role authentication method")

        aws_config.set_role_auth(
            role_arn=args.role_arn,
            role_session_name=args.role_session_name,
            external_id=args.external_id,
            mfa_serial=args.mfa_serial,
            mfa_token=args.mfa_token,
            region=args.region,
        )

    elif auth_method == "environment":
        aws_config.set_environment_auth(region=args.region)

    elif auth_method == "default":
        aws_config.set_default_auth(region=args.region)

    # Set KMS key
    aws_config.kms_key_alias = args.kms_key


def list_profiles_command():
    """List available AWS profiles"""
    try:
        import configparser

        profiles = []

        # Check AWS credentials file
        creds_file = os.path.expanduser("~/.aws/credentials")
        if os.path.exists(creds_file):
            config = configparser.ConfigParser()
            config.read(creds_file)
            profiles.extend(
                [section for section in config.sections() if section != "default"]
            )

        # Check AWS config file
        config_file = os.path.expanduser("~/.aws/config")
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            for section in config.sections():
                if section.startswith("profile "):
                    profile_name = section.replace("profile ", "")
                    if profile_name not in profiles:
                        profiles.append(profile_name)

        # Add default profile if credentials file exists
        if os.path.exists(creds_file):
            profiles.insert(0, "default")

        if profiles:
            print("Available AWS profiles:")
            for profile in profiles:
                print(f"  • {profile}")
        else:
            print("No AWS profiles found. Please configure AWS CLI first.")

        return 0

    except Exception as e:
        print(f"Error listing profiles: {str(e)}")
        return 1


def upload_command(manager, args):
    """Handle upload command"""
    try:
        print(f"Reading parameters from {args.csv_file}...")
        parameters = manager.read_csv_parameters(args.csv_file)

        if not parameters:
            print("No valid parameters found in CSV file.")
            return 1

        print(f"Found {len(parameters)} parameters to upload")

        uploaded_count = 0
        skipped_count = 0

        for param in parameters:
            print(f"Processing {param['key']}...")

            # Check if parameter exists
            exists, existing_param = manager.parameter_exists(param["key"])

            if exists and not args.overwrite:
                print(f"Parameter {param['key']} already exists:")
                print(
                    f"  Current: {existing_param['Value'][:50]}{'...' if len(existing_param['Value']) > 50 else ''}"
                )
                print(
                    f"  New: {param['value'][:50]}{'...' if len(param['value']) > 50 else ''}"
                )

                response = input("Replace? (y/n/q): ").lower().strip()
                if response == "q":
                    print("Upload cancelled by user.")
                    break
                elif response != "y":
                    skipped_count += 1
                    print(f"Skipped {param['key']}")
                    continue

            # Upload parameter
            if manager.create_or_update_parameter(param, overwrite=True):
                uploaded_count += 1
                print(f"✓ Uploaded {param['key']}")
            else:
                print(f"✗ Failed to upload {param['key']}")

        print(
            f"\\nUpload completed: {uploaded_count} uploaded, {skipped_count} skipped"
        )
        return 0

    except Exception as e:
        print(f"Error during upload: {str(e)}")
        return 1


def list_command(manager, args):
    """Handle list command"""
    try:
        print("Retrieving parameters...")
        parameters = manager.get_all_parameters(decrypt=args.decrypt)

        if args.filter:
            parameters = [
                p for p in parameters if args.filter.lower() in p["Name"].lower()
            ]

        if not parameters:
            print("No parameters found.")
            return 0

        if args.output:
            # Export to CSV
            if manager.export_parameters_to_csv(args.output, parameters):
                print(f"Exported {len(parameters)} parameters to {args.output}")
            else:
                print("Failed to export parameters")
                return 1
        else:
            # Print to console
            print(f"\\nFound {len(parameters)} parameters:")
            print("-" * 80)
            print(f"{'Name':<40} {'Type':<12} {'Value':<28}")
            print("-" * 80)

            for param in parameters:
                name = param["Name"][:39] if len(param["Name"]) > 39 else param["Name"]
                value = (
                    param["Value"][:27] if len(param["Value"]) > 27 else param["Value"]
                )
                print(f"{name:<40} {param['Type']:<12} {value:<28}")

        return 0

    except Exception as e:
        print(f"Error retrieving parameters: {str(e)}")
        return 1


def get_command(manager, args):
    """Handle get command"""
    try:
        exists, param = manager.parameter_exists(args.parameter_name)

        if not exists:
            print(f"Parameter '{args.parameter_name}' not found.")
            return 1

        print(f"Parameter: {param['Name']}")
        print(f"Type: {param['Type']}")
        print(f"Tier: {param.get('Tier', 'N/A')}")
        print(f"Version: {param.get('Version', 'N/A')}")
        print(f"Last Modified: {param.get('LastModifiedDate', 'N/A')}")
        if param.get("KeyId"):
            print(f"KMS Key: {param['KeyId']}")
        print(f"Value: {param['Value']}")

        return 0

    except Exception as e:
        print(f"Error retrieving parameter: {str(e)}")
        return 1


def delete_command(manager, args):
    """Handle delete command"""
    try:
        exists, param = manager.parameter_exists(args.parameter_name)

        if not exists:
            print(f"Parameter '{args.parameter_name}' not found.")
            return 1

        if not args.force:
            print(f"Parameter to delete: {args.parameter_name}")
            print(
                f"Current value: {param['Value'][:100]}{'...' if len(param['Value']) > 100 else ''}"
            )
            response = (
                input("Are you sure you want to delete this parameter? (y/N): ")
                .lower()
                .strip()
            )
            if response != "y":
                print("Delete cancelled.")
                return 0

        if manager.delete_parameter(args.parameter_name):
            print(f"✓ Deleted parameter: {args.parameter_name}")
            return 0
        else:
            print(f"✗ Failed to delete parameter: {args.parameter_name}")
            return 1

    except Exception as e:
        print(f"Error deleting parameter: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
