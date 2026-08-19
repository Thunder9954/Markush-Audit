#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
SHA-256 Manifest Generator
Computes SHA-256 hashes for all project files to create a manifest for release verification.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict


# Directories and files to ignore
IGNORE_PATTERNS = {
    ".git",
    "__pycache__",
    "venv",
    "python-pip",
    ".idea",
    ".vscode",
    "release",
    "keys",
    "audit_runs",
}

IGNORE_FILES = {
    "*.pyc",
    "*.log",
    "*.tmp",
    ".gitignore",
    "manifest.json",
    "manifest.sig",
}


def should_ignore(path: Path) -> bool:
    """
    Check if a path should be ignored.

    Args:
        path: Path to check

    Returns:
        bool: True if path should be ignored
    """
    # Check directory patterns
    for part in path.parts:
        if part in IGNORE_PATTERNS:
            return True

    # Check file patterns
    if path.is_file():
        for pattern in IGNORE_FILES:
            if path.match(pattern):
                return True

    return False


def compute_sha256(file_path: Path) -> str:
    """
    Compute SHA-256 hash of a file.

    Args:
        file_path: Path to the file

    Returns:
        str: Hexadecimal SHA-256 hash
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def generate_manifest(root_dir: str = ".", output_file: str = "manifest.json") -> Dict[str, Dict[str, str]]:
    """
    Generate a manifest of all project files with their SHA-256 hashes.

    Args:
        root_dir: Root directory to scan
        output_file: Output file for the manifest

    Returns:
        dict: Manifest dictionary
    """
    root_path = Path(root_dir).resolve()
    manifest = {}

    print(f"Scanning project directory: {root_path}")

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and not should_ignore(file_path):
            # Get relative path from root
            rel_path = file_path.relative_to(root_path)
            file_hash = compute_sha256(file_path)
            manifest[str(rel_path)] = {"sha256": file_hash}
            print(f"  Added: {rel_path}")

    # Write manifest to file
    manifest_path = Path(output_file)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    print(f"\n✓ Manifest generated: {manifest_path}")
    print(f"  Total files: {len(manifest)}")

    return manifest


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate SHA-256 manifest for release verification")
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="manifest.json",
        help="Output manifest file (default: manifest.json)"
    )

    args = parser.parse_args()

    try:
        generate_manifest(args.root, args.output)
    except Exception as e:
        print(f"\n✗ Error generating manifest: {e}")
        exit(1)


if __name__ == "__main__":
    main()
