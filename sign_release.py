#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Release Signature Script
Signs the manifest.json with Ed25519 private key to create manifest.sig
"""

import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def load_private_key(key_path: str = "keys/private_key.pem") -> ed25519.Ed25519PrivateKey:
    """
    Load Ed25519 private key from PEM file.

    Args:
        key_path: Path to the private key file

    Returns:
        Ed25519PrivateKey: Loaded private key
    """
    key_file = Path(key_path)
    if not key_file.exists():
        raise FileNotFoundError(f"Private key not found: {key_path}")

    with open(key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    if not isinstance(private_key, ed25519.Ed25519PrivateKey):
        raise ValueError("Key is not an Ed25519 private key")

    return private_key


def load_manifest(manifest_path: str = "manifest.json") -> dict:
    """
    Load manifest.json file.

    Args:
        manifest_path: Path to the manifest file

    Returns:
        dict: Manifest data
    """
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_file, "r") as f:
        return json.load(f)


def sign_manifest(
    manifest: dict,
    private_key: ed25519.Ed25519PrivateKey,
    output_path: str = "manifest.sig"
) -> Path:
    """
    Sign the manifest with Ed25519 private key.

    Args:
        manifest: Manifest dictionary
        private_key: Ed25519 private key
        output_path: Output signature file path

    Returns:
        Path: Path to the signature file
    """
    # Serialize manifest to canonical JSON (sorted keys, no extra whitespace)
    manifest_json = json.dumps(manifest, sort_keys=True, separators=(',', ':'))
    manifest_bytes = manifest_json.encode('utf-8')

    # Sign the manifest
    signature = private_key.sign(manifest_bytes)

    # Write signature to file
    sig_path = Path(output_path)
    sig_path.write_bytes(signature)

    return sig_path


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Sign release manifest with Ed25519")
    parser.add_argument(
        "--manifest",
        default="manifest.json",
        help="Path to manifest.json (default: manifest.json)"
    )
    parser.add_argument(
        "--key",
        default="keys/private_key.pem",
        help="Path to private key (default: keys/private_key.pem)"
    )
    parser.add_argument(
        "--output",
        default="manifest.sig",
        help="Output signature file (default: manifest.sig)"
    )

    args = parser.parse_args()

    try:
        print("Loading manifest...")
        manifest = load_manifest(args.manifest)

        print("Loading private key...")
        private_key = load_private_key(args.key)

        print("Signing manifest...")
        sig_path = sign_manifest(manifest, private_key, args.output)

        print(f"\n✓ Manifest signed successfully")
        print(f"  Signature: {sig_path}")
        print(f"  Manifest: {args.manifest}")
        print(f"  Private key: {args.key}")

    except Exception as e:
        print(f"\n✗ Error signing manifest: {e}")
        exit(1)


if __name__ == "__main__":
    main()
