# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Centralized project metadata for Markush Audit.

This module contains all project information in one place to ensure
consistency across the entire codebase. All other modules should import
from here instead of hardcoding metadata strings.
"""

PROJECT_NAME = "Markush Audit"
PROJECT_DESCRIPTION = (
    "A comprehensive Android security audit framework combining ADB commands, "
    "deep-level security checks, and Mobile Verification Toolkit (MVT) "
    "for nation-state spyware detection."
)
AUTHOR = "Purn Vadodariya"
COPYRIGHT = "Copyright (c) 2026 Purn Vadodariya"
GITHUB_URL = "https://github.com/Thunder9954/Audit"
GITHUB_USERNAME = "Thunder9954"
LICENSE = "MIT"
VERSION = "1.0.0"
EMAIL = "purn872008@gmail.com"


def get_banner():
    """
    Generate a professional banner string from project metadata.

    Returns:
        str: Formatted banner string
    """
    banner = f"""
{'=' * 70}
{'MARKUSH AUDIT'.center(70)}
{'Android Security Audit Framework'.center(70)}
{'=' * 70}
{'Version : ' + VERSION}
{'Author  : ' + AUTHOR}
{'GitHub  : ' + GITHUB_URL}
{'=' * 70}
{COPYRIGHT}
{'=' * 70}
"""
    return banner


def get_version_info():
    """
    Get version information as a formatted string.

    Returns:
        str: Version information
    """
    return f"{PROJECT_NAME} v{VERSION}"


def get_about_info():
    """
    Get detailed about information as a formatted string.

    Returns:
        str: About information
    """
    about = f"""
{PROJECT_NAME}
{PROJECT_DESCRIPTION}

Version: {VERSION}
Author: {AUTHOR}
Email: {EMAIL}
GitHub: {GITHUB_URL}
License: {LICENSE}
{COPYRIGHT}
"""
    return about
