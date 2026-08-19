# Installation Guide

Complete installation instructions for Markush_audit.

## System Requirements

- **Operating System**: Linux, macOS, or Windows (WSL2)
- **Python**: 3.7 or higher
- **ADB**: Android Debug Bridge (system-wide installation)
- **USB Cable**: For device connection
- **Internet**: For MVT IOC downloads

## Step 1: Install ADB

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install adb
```

### macOS

```bash
brew install android-platform-tools
```

### Windows

Download from: [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)

## Step 2: Verify ADB Installation

```bash
adb version
# Should display: Android Debug Bridge version 1.0.41 or higher
```

## Step 3: Enable USB Debugging on Android

1. **Enable Developer Options:**
   - Settings → About Phone → Tap "Build Number" 7 times

2. **Enable USB Debugging:**
   - Settings → Developer Options → Enable "USB Debugging"
   - Enable "Stay Awake" (optional, for screen-on during audit)

3. **Connect Device:**
   ```bash
   adb devices
   # Accept the authorization popup on your phone
   ```

## Step 4: Clone Repository

```bash
git clone https://github.com/Thunder9954/Audit.git
cd Audit
```

## Step 5: Install Python Dependencies

```bash
# With specific versions (recommended for stability)
pip install -r requirements.txt

# Or with latest versions
pip install -r requirementsV.txt
```

**Note:** MVT will be auto-installed in a virtual environment when first used.

## Troubleshooting Installation

### ADB Connection Issues

**Device not found or unauthorized:**
1. Check USB cable (use original or high-quality cable)
2. Try different USB port (direct connection, not through hub)
3. Re-enable USB debugging on device
4. Restart ADB server:
   ```bash
   adb kill-server && adb start-server
   ```
5. Check device authorization:
   ```bash
   adb devices
   ```
6. Revoke USB debugging authorization and re-accept

**Device offline:**
1. Disconnect and reconnect USB cable
2. Toggle USB debugging off and on
3. Restart device
4. Check USB cable for damage

### Python Issues

**Python version too old:**
```bash
# Install Python 3.7+
sudo apt install python3.7  # Linux
brew install python3        # macOS
```

**Permission denied:**
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### MVT Installation Issues

**MVT installation fails:**
1. Ensure Python 3.7+ is installed:
   ```bash
   python3 --version
   ```
2. Check internet connection (required for package downloads)
3. Verify virtual environment creation:
   ```bash
   ls python-pip/
   ```
4. Manual installation:
   ```bash
   python3 -m venv python-pip
   source python-pip/bin/activate
   pip install mvt
   ```

**IOC download fails:**
1. Check internet connection
2. Verify MVT installation:
   ```bash
   source python-pip/bin/activate
   mvt-android version
   ```
3. Retry download (may be temporary server issue)
