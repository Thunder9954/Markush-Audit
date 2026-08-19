# Git Signing Documentation

This document provides guidance on signing Git commits and tags for the Markush Audit project.

## Why Sign Commits?

Signing commits and tags provides cryptographic proof that:
- The commit was made by the claimed author
- The commit has not been tampered with
- The code comes from a trusted source

## Setting Up Git Signing

### Option 1: GPG Signing

#### Generate a GPG Key

```bash
gpg --full-generate-key
```

Select:
- Key type: RSA and RSA
- Key size: 4096
- Expiration: No expiration or your preference
- Real name: Purn Vadodariya
- Email: purn872008@gmail.com
- Passphrase: Choose a strong passphrase

#### List Your GPG Keys

```bash
gpg --list-secret-keys --keyid-format=LONG
```

Output example:
```
sec   rsa4096/3AA5C34371567BD2 2016-03-10 [expires: 2017-03-10]
ssb   rsa4096/42B317FD4BA89E7A 2016-03-10
```

The key ID is the part after the `/`: `3AA5C34371567BD2`

#### Configure Git to Use GPG

```bash
git config --global user.signingkey 3AA5C34371567BD2
git config --global commit.gpgsign true
git config --global gpg.program gpg
```

#### Upload Your Public Key to GitHub

```bash
gpg --armor --export 3AA5C34371567BD2
```

Copy the output and add it to GitHub:
1. Go to GitHub Settings → SSH and GPG keys
2. Click "New GPG key"
3. Paste your public key
4. Click "Add GPG key"

### Option 2: SSH Signing

#### Generate an SSH Key

```bash
ssh-keygen -t ed25519 -C "purn872008@gmail.com"
```

#### Configure Git to Use SSH

```bash
git config --global gpg.format ssh
git config --global commit.gpgsign true
git config --global user.signingkey ~/.ssh/id_ed25519.pub
```

#### Upload Your SSH Public Key to GitHub

Add your SSH public key to GitHub:
1. Go to GitHub Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

## Signing Commits

### Sign a Single Commit

```bash
git commit -S -m "Your commit message"
```

The `-S` flag signs the commit.

### Sign All Commits by Default

If you configured `commit.gpgsign true`, all commits will be signed automatically.

```bash
git commit -m "Your commit message"
```

### Sign Previous Commits

To sign the last commit:

```bash
git commit --amend --no-edit -S
```

To sign multiple previous commits (interactive rebase):

```bash
git rebase -i HEAD~3
```

Change `pick` to `edit` for commits you want to sign, then:

```bash
git commit --amend --no-edit -S
git rebase --continue
```

## Signing Tags

### Sign a Tag

```bash
git tag -s v1.0.0 -m "Release version 1.0.0"
```

### Sign an Existing Tag

```bash
git tag -s v1.0.0 -f -m "Release version 1.0.0"
```

### List Signed Tags

```bash
git tag -v v1.0.0
```

## Verifying Signatures

### Verify a Commit

```bash
git log --show-signature -1
```

### Verify a Tag

```bash
git verify-tag v1.0.0
```

### View All Signed Commits

```bash
git log --show-signature
```

## GitHub Display

Signed commits and tags will display a "Verified" badge on GitHub:
- Green checkmark for verified signatures
- The email address associated with the signing key
- The key type (GPG or SSH)

## Troubleshooting

### GPG Agent Not Running

```bash
gpgconf --launch gpg-agent
```

### GPG Passphrase Prompt

If you're repeatedly prompted for your passphrase:

```bash
# Configure gpg-agent to cache passphrase
echo "default-cache-ttl 3600" >> ~/.gnupg/gpg-agent.conf
echo "max-cache-ttl 7200" >> ~/.gnupg/gpg-agent.conf
gpgconf --reload gpg-agent
```

### SSH Key Not Recognized

Ensure your SSH key is added to the SSH agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

## Best Practices

1. **Always sign release tags** - This provides cryptographic proof of authenticity
2. **Sign important commits** - Security fixes, major features, etc.
3. **Keep your private keys secure** - Never share private keys
4. **Use strong passphrases** - Protect your GPG private key
5. **Backup your keys** - Store backups in a secure location
6. **Rotate keys periodically** - If a key is compromised, revoke and replace it

## Additional Resources

- [GitHub Documentation on GPG](https://docs.github.com/en/authentication/managing-commit-signature-verification/checking-for-existing-gpg-keys)
- [GitHub Documentation on SSH](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-ssh-key)
- [GPG Documentation](https://gnupg.org/documentation/)
