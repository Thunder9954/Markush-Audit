#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Release Creation Script
Automates the process of creating a signed release with manifest and verification files.
"""

import shutil
import subprocess
from pathlib import Path
from manifest import generate_manifest
from sign_release import load_manifest, load_private_key, sign_manifest
from verify_release import verify_release


def create_release_directory(release_dir: str = "release") -> Path:
    """
    Create and prepare release directory.

    Args:
        release_dir: Name of the release directory

    Returns:
        Path: Path to the release directory
    """
    release_path = Path(release_dir)
    
    # Remove existing release directory
    if release_path.exists():
        shutil.rmtree(release_path)
    
    # Create new release directory
    release_path.mkdir()
    return release_path


def copy_project_files(release_path: Path, exclude_dirs: list = None) -> None:
    """
    Copy project files to release directory.

    Args:
        release_path: Path to the release directory
        exclude_dirs: Directories to exclude from copying
    """
    if exclude_dirs is None:
        exclude_dirs = [".git", "__pycache__", "venv", "python-pip", ".idea", 
                       ".vscode", "keys", "audit_runs", "release"]

    root_path = Path(".")
    
    for item in root_path.iterdir():
        if item.name in exclude_dirs or item.name.startswith("."):
            continue
        
        if item.is_dir():
            shutil.copytree(item, release_path / item.name, 
                          ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(item, release_path / item.name)


def create_release(release_dir: str = "release") -> bool:
    """
    Complete release creation workflow.

    Args:
        release_dir: Name of the release directory

    Returns:
        bool: True if release created successfully
    """
    print("=" * 70)
    print("MARKUSH AUDIT - RELEASE CREATION")
    print("=" * 70)
    print()

    # Step 1: Generate Manifest
    print("Step 1: Generating manifest...")
    try:
        manifest = generate_manifest(output_file="manifest.json")
    except Exception as e:
        print(f"  ✗ Error generating manifest: {e}")
        return False

    # Step 2: Sign Manifest
    print("\nStep 2: Signing manifest...")
    try:
        manifest_data = load_manifest("manifest.json")
        private_key = load_private_key("keys/private_key.pem")
        sign_manifest(manifest_data, private_key, "manifest.sig")
        print("  ✓ Manifest signed successfully")
    except Exception as e:
        print(f"  ✗ Error signing manifest: {e}")
        return False

    # Step 3: Verify Signature
    print("\nStep 3: Verifying signature...")
    try:
        signature_valid, hashes_valid, details = verify_release()
        if signature_valid and hashes_valid:
            print("  ✓ Signature and manifest verified")
        else:
            print(f"  ✗ Verification failed: {details}")
            return False
    except Exception as e:
        print(f"  ✗ Error verifying: {e}")
        return False

    # Step 4: Create Release Directory
    print("\nStep 4: Creating release directory...")
    try:
        release_path = create_release_directory(release_dir)
        print(f"  ✓ Release directory created: {release_path}")
    except Exception as e:
        print(f"  ✗ Error creating release directory: {e}")
        return False

    # Step 5: Copy Project Files
    print("\nStep 5: Copying project files...")
    try:
        copy_project_files(release_path)
        print(f"  ✓ Project files copied")
    except Exception as e:
        print(f"  ✗ Error copying files: {e}")
        return False

    # Step 6: Copy Verification Files
    print("\nStep 6: Copying verification files...")
    try:
        shutil.copy2("manifest.json", release_path / "manifest.json")
        shutil.copy2("manifest.sig", release_path / "manifest.sig")
        shutil.copy2("keys/public_key.pem", release_path / "public_key.pem")
        print("  ✓ Verification files copied")
    except Exception as e:
        print(f"  ✗ Error copying verification files: {e}")
        return False

    # Step 7: Copy Documentation
    print("\nStep 7: Copying documentation...")
    try:
        if Path("README.md").exists():
            shutil.copy2("README.md", release_path / "README.md")
        if Path("LICENSE").exists():
            shutil.copy2("LICENSE", release_path / "LICENSE")
        print("  ✓ Documentation copied")
    except Exception as e:
        print(f"  ✗ Error copying documentation: {e}")
        return False

    print()
    print("=" * 70)
    print("RELEASE SUCCESSFULLY CREATED")
    print("=" * 70)
    print(f"Release directory: {release_path.absolute()}")
    print(f"Files included:")
    print(f"  - Project source code")
    print(f"  - manifest.json (SHA-256 hashes)")
    print(f"  - manifest.sig (Ed25519 signature)")
    print(f"  - public_key.pem (verification key)")
    print(f"  - README.md")
    print(f"  - LICENSE")
    print()
    print("Users can verify the release with:")
    print(f"  python manage.py --verify")
    print()

    return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Create a signed release")
    parser.add_argument(
        "--output",
        default="release",
        help="Release directory name (default: release)"
    )

    args = parser.parse_args()

    try:
        success = create_release(args.output)
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error creating release: {e}")
        exit(1)


if __name__ == "__main__":
    main()
