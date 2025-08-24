"""
AWS Parameter Store Manager
Handles CRUD operations for AWS Systems Manager Parameter Store
"""

import csv
import json
from typing import Dict, List, Optional, Tuple

import boto3
import pandas as pd
from botocore.exceptions import (ClientError, NoCredentialsError,
                                 ProfileNotFound)

from config import aws_config


class AWSParameterManager:
    """Main class for managing AWS Parameter Store operations"""

    def __init__(self):
        self.ssm_client = None
        self.current_parameters = {}

    def connect(self) -> bool:
        """Connect to AWS SSM using configured credentials"""
        try:
            if not aws_config.is_configured():
                raise ValueError("AWS credentials not configured")

            session = aws_config.get_session()
            self.ssm_client = session.client("ssm")

            # Test connection
            self.ssm_client.describe_parameters(MaxResults=1)
            return True

        except (ClientError, NoCredentialsError, ValueError, ProfileNotFound) as e:
            print(f"Failed to connect to AWS: {str(e)}")
            return False

    def read_csv_parameters(self, csv_file_path: str) -> List[Dict]:
        """Read parameters from CSV file"""
        parameters = []
        try:
            with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                required_columns = {"key", "value", "type"}

                if not required_columns.issubset(reader.fieldnames):
                    raise ValueError(f"CSV must contain columns: {required_columns}")

                for row_num, row in enumerate(reader, start=2):
                    if not row["key"] or not row["value"]:
                        print(f"Warning: Skipping row {row_num} - missing key or value")
                        continue

                    param = {
                        "key": row["key"].strip(),
                        "value": row["value"].strip(),
                        "type": row.get("type", "String").strip(),
                        "tier": row.get("tier", "Standard").strip(),
                        "kms_key": row.get("kms", aws_config.kms_key_alias).strip(),
                    }

                    # Validate parameter type
                    if param["type"] not in ["String", "StringList", "SecureString"]:
                        print(
                            f"Warning: Invalid type '{param['type']}' for {param['key']}, defaulting to String"
                        )
                        param["type"] = "String"

                    # Validate tier
                    if param["tier"] not in [
                        "Standard",
                        "Advanced",
                        "Intelligent-Tiering",
                    ]:
                        print(
                            f"Warning: Invalid tier '{param['tier']}' for {param['key']}, defaulting to Standard"
                        )
                        param["tier"] = "Standard"

                    parameters.append(param)

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV: {str(e)}")

        return parameters

    def parameter_exists(self, parameter_name: str) -> Tuple[bool, Optional[Dict]]:
        """Check if parameter exists and return its details"""
        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_name, WithDecryption=True
            )

            # Get additional parameter details
            details_response = self.ssm_client.describe_parameters(
                Filters=[{"Key": "Name", "Values": [parameter_name]}]
            )

            if details_response["Parameters"]:
                param_details = details_response["Parameters"][0]
                existing_param = {
                    "Name": response["Parameter"]["Name"],
                    "Value": response["Parameter"]["Value"],
                    "Type": response["Parameter"]["Type"],
                    "Tier": param_details.get("Tier", "Standard"),
                    "KeyId": param_details.get("KeyId", ""),
                    "LastModifiedDate": param_details.get("LastModifiedDate"),
                    "Version": response["Parameter"]["Version"],
                }
                return True, existing_param

        except ClientError as e:
            if e.response["Error"]["Code"] == "ParameterNotFound":
                return False, None
            else:
                raise e

        return False, None

    def create_or_update_parameter(self, param: Dict, overwrite: bool = False) -> bool:
        """Create or update a parameter in AWS Parameter Store"""
        try:
            put_params = {
                "Name": param["key"],
                "Value": param["value"],
                "Type": param["type"],
                "Tier": param["tier"],
                "Overwrite": overwrite,
            }

            # Add KMS key for SecureString
            if param["type"] == "SecureString" and param["kms_key"]:
                put_params["KeyId"] = param["kms_key"]

            self.ssm_client.put_parameter(**put_params)
            return True

        except ClientError as e:
            print(f"Error creating/updating parameter {param['key']}: {str(e)}")
            return False

    def get_all_parameters(self, decrypt: bool = True) -> List[Dict]:
        """Get all parameters from Parameter Store"""
        all_parameters = []
        next_token = None

        try:
            while True:
                # Get parameter names first
                describe_params = {"MaxResults": 50}
                if next_token:
                    describe_params["NextToken"] = next_token

                response = self.ssm_client.describe_parameters(**describe_params)

                # Get parameter values in batches
                parameter_names = [param["Name"] for param in response["Parameters"]]

                if parameter_names:
                    # Get parameters in batches of 10 (AWS limit)
                    for i in range(0, len(parameter_names), 10):
                        batch_names = parameter_names[i : i + 10]

                        try:
                            values_response = self.ssm_client.get_parameters(
                                Names=batch_names, WithDecryption=decrypt
                            )

                            # Create lookup for parameter values
                            values_lookup = {
                                p["Name"]: p for p in values_response["Parameters"]
                            }

                            # Combine metadata with values
                            for param_meta in response["Parameters"][i : i + 10]:
                                param_name = param_meta["Name"]
                                param_value = values_lookup.get(param_name, {})

                                combined_param = {
                                    "Name": param_name,
                                    "Value": param_value.get("Value", "N/A"),
                                    "Type": param_meta["Type"],
                                    "Tier": param_meta.get("Tier", "Standard"),
                                    "KeyId": param_meta.get("KeyId", ""),
                                    "LastModifiedDate": param_meta.get(
                                        "LastModifiedDate"
                                    ),
                                    "Version": param_value.get("Version", "N/A"),
                                    "Description": param_meta.get("Description", ""),
                                }
                                all_parameters.append(combined_param)

                        except ClientError as e:
                            print(f"Error getting parameter values for batch: {str(e)}")
                            # Add parameters without values if there's an error
                            for param_meta in response["Parameters"][i : i + 10]:
                                combined_param = {
                                    "Name": param_meta["Name"],
                                    "Value": "Error retrieving value",
                                    "Type": param_meta["Type"],
                                    "Tier": param_meta.get("Tier", "Standard"),
                                    "KeyId": param_meta.get("KeyId", ""),
                                    "LastModifiedDate": param_meta.get(
                                        "LastModifiedDate"
                                    ),
                                    "Version": "N/A",
                                    "Description": param_meta.get("Description", ""),
                                }
                                all_parameters.append(combined_param)

                next_token = response.get("NextToken")
                if not next_token:
                    break

        except ClientError as e:
            print(f"Error retrieving parameters: {str(e)}")

        # Cache the current parameters
        self.current_parameters = {param["Name"]: param for param in all_parameters}
        return all_parameters

    def delete_parameter(self, parameter_name: str) -> bool:
        """Delete a parameter from Parameter Store"""
        try:
            self.ssm_client.delete_parameter(Name=parameter_name)
            return True
        except ClientError as e:
            print(f"Error deleting parameter {parameter_name}: {str(e)}")
            return False

    def export_parameters_to_csv(
        self, output_file: str, parameters: List[Dict] = None
    ) -> bool:
        """Export parameters to CSV file"""
        if parameters is None:
            parameters = self.get_all_parameters()

        try:
            with open(output_file, "w", newline="", encoding="utf-8") as file:
                if parameters:
                    fieldnames = [
                        "Name",
                        "Value",
                        "Type",
                        "Tier",
                        "KeyId",
                        "LastModifiedDate",
                        "Version",
                        "Description",
                    ]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(parameters)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
