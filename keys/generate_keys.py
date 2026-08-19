#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Ed25519 Key Generation Script
Generates an Ed25519 key pair for signing releases.

The private key is NEVER committed to Git and must be kept secure.
The public key can be distributed for verification.
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def generate_ed25519_keypair(keys_dir: str = "keys") -> tuple[Path, Path]:
    """
    Generate an Ed25519 key pair.

    Args:
        keys_dir: Directory to store the keys

    Returns:
        tuple: (private_key_path, public_key_path)
    """
    keys_path = Path(keys_dir)
    keys_path.mkdir(exist_ok=True)

    # Generate Ed25519 key pair
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write private key
    private_key_path = keys_path / "private_key.pem"
    private_key_path.write_bytes(private_pem)
    private_key_path.chmod(0o600)  # Restrict permissions

    # Write public key
    public_key_path = keys_path / "public_key.pem"
    public_key_path.write_bytes(public_pem)

    return private_key_path, public_key_path


def main():
    """Main entry point"""
    print("Generating Ed25519 key pair...")

    try:
        private_key_path, public_key_path = generate_ed25519_keypair()

        print(f"\n✓ Key pair generated successfully")
        print(f"\nPrivate key: {private_key_path}")
        print(f"  - Keep this file secure and NEVER share it")
        print(f"  - This file is automatically added to .gitignore")
        print(f"\nPublic key: {public_key_path}")
        print(f"  - This file can be distributed for verification")
        print(f"  - This file can be committed to the repository")

    except Exception as e:
        print(f"\n✗ Error generating keys: {e}")
        exit(1)


if __name__ == "__main__":
    main()
