#!/usr/bin/env python3
"""
Setup script for AWS Parameter Store Manager
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="aws-parameter-store-manager",
    version="1.0.0",
    author="AWS Parameter Store Manager Contributors",
    author_email="",
    description="A comprehensive GUI and CLI application for managing AWS Systems Manager Parameter Store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aws-parameter-store-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black",
            "flake8",
            "isort",
            "bandit",
            "safety",
        ],
    },
    entry_points={
        "console_scripts": [
            "aws-parameter-store-cli=cli_app:main",
            "aws-parameter-store-gui=gui_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.md", "*.txt", "*.bat", "*.sh"],
    },
    keywords="aws parameter-store systems-manager gui cli boto3 devops",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/aws-parameter-store-manager/issues",
        "Source": "https://github.com/yourusername/aws-parameter-store-manager",
        "Documentation": "https://github.com/yourusername/aws-parameter-store-manager#readme",
        "Contributing": "https://github.com/yourusername/aws-parameter-store-manager/blob/main/CONTRIBUTING.md",
    },
)
