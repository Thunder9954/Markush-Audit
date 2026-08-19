#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Release Verification Script
Verifies the Ed25519 signature and SHA-256 hashes of a release to confirm authenticity.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def load_public_key(key_path: str = "keys/public_key.pem") -> ed25519.Ed25519PublicKey:
    """
    Load Ed25519 public key from PEM file.

    Args:
        key_path: Path to the public key file

    Returns:
        Ed25519PublicKey: Loaded public key
    """
    key_file = Path(key_path)
    if not key_file.exists():
        raise FileNotFoundError(f"Public key not found: {key_path}")

    with open(key_file, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

    if not isinstance(public_key, ed25519.Ed25519PublicKey):
        raise ValueError("Key is not an Ed25519 public key")

    return public_key


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


def load_signature(sig_path: str = "manifest.sig") -> bytes:
    """
    Load signature file.

    Args:
        sig_path: Path to the signature file

    Returns:
        bytes: Signature data
    """
    sig_file = Path(sig_path)
    if not sig_file.exists():
        raise FileNotFoundError(f"Signature not found: {sig_path}")

    return sig_file.read_bytes()


def verify_signature(
    manifest: dict,
    signature: bytes,
    public_key: ed25519.Ed25519PublicKey
) -> bool:
    """
    Verify the Ed25519 signature of the manifest.

    Args:
        manifest: Manifest dictionary
        signature: Signature bytes
        public_key: Ed25519 public key

    Returns:
        bool: True if signature is valid
    """
    # Serialize manifest to canonical JSON (same format as signing)
    manifest_json = json.dumps(manifest, sort_keys=True, separators=(',', ':'))
    manifest_bytes = manifest_json.encode('utf-8')

    try:
        public_key.verify(signature, manifest_bytes)
        return True
    except Exception:
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


def verify_file_hashes(manifest: dict, root_dir: str = ".") -> Tuple[bool, Dict[str, str]]:
    """
    Verify all file hashes in the manifest.

    Args:
        manifest: Manifest dictionary
        root_dir: Root directory for file paths

    Returns:
        tuple: (all_valid, results_dict)
    """
    root_path = Path(root_dir).resolve()
    results = {}
    all_valid = True

    for rel_path, file_data in manifest.items():
        file_path = root_path / rel_path

        if not file_path.exists():
            results[rel_path] = "MISSING"
            all_valid = False
            continue

        computed_hash = compute_sha256(file_path)
        expected_hash = file_data["sha256"]

        if computed_hash == expected_hash:
            results[rel_path] = "VALID"
        else:
            results[rel_path] = f"MODIFIED (expected: {expected_hash[:16]}..., got: {computed_hash[:16]}...)"
            all_valid = False

    return all_valid, results


def verify_release(
    manifest_path: str = "manifest.json",
    sig_path: str = "manifest.sig",
    key_path: str = "keys/public_key.pem",
    root_dir: str = "."
) -> Tuple[bool, bool, Dict]:
    """
    Perform complete release verification.

    Args:
        manifest_path: Path to manifest.json
        sig_path: Path to manifest.sig
        key_path: Path to public key
        root_dir: Root directory for file verification

    Returns:
        tuple: (signature_valid, hashes_valid, details)
    """
    details = {}

    # Load files
    try:
        manifest = load_manifest(manifest_path)
        signature = load_signature(sig_path)
        public_key = load_public_key(key_path)
    except Exception as e:
        details["error"] = str(e)
        return False, False, details

    # Verify signature
    signature_valid = verify_signature(manifest, signature, public_key)
    details["signature"] = "VALID" if signature_valid else "INVALID"

    # Verify file hashes
    hashes_valid, hash_results = verify_file_hashes(manifest, root_dir)
    details["hashes"] = hash_results
    details["hashes_valid"] = hashes_valid

    return signature_valid, hashes_valid, details


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Verify release authenticity")
    parser.add_argument(
        "--manifest",
        default="manifest.json",
        help="Path to manifest.json (default: manifest.json)"
    )
    parser.add_argument(
        "--signature",
        default="manifest.sig",
        help="Path to manifest.sig (default: manifest.sig)"
    )
    parser.add_argument(
        "--key",
        default="keys/public_key.pem",
        help="Path to public key (default: keys/public_key.pem)"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory for file verification (default: current directory)"
    )

    args = parser.parse_args()

    try:
        print("Verifying release authenticity...\n")

        signature_valid, hashes_valid, details = verify_release(
            args.manifest,
            args.signature,
            args.key,
            args.root
        )

        print(f"Signature: {details.get('signature', 'UNKNOWN')}")
        print(f"Manifest: {'VALID' if hashes_valid else 'INVALID'}")

        if not hashes_valid and "hashes" in details:
            print("\nFile verification results:")
            for file_path, status in details["hashes"].items():
                if status != "VALID":
                    print(f"  {file_path}: {status}")

        overall_valid = signature_valid and hashes_valid

        if overall_valid:
            print("\n✓ Official Build")
            print("  This release is authentic and unmodified.")
        else:
            print("\n✗ Modified / Unofficial Build")
            print("  This copy has been modified or is not an official release.")
            print(f"  Repository: https://github.com/Thunder9954/Audit")

        exit(0 if overall_valid else 1)

    except Exception as e:
        print(f"\n✗ Error during verification: {e}")
        exit(1)


if __name__ == "__main__":
    main()
