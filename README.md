# Markush Audit

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)

A comprehensive Android security audit framework combining ADB commands, deep-level security checks, and Mobile Verification Toolkit (MVT) for nation-state spyware detection.

![Security Overview](Data/1.png)

![Demo Video](Data/main.mp4)

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Workflow](#project-workflow)
- [Output Structure](#output-structure)
- [Security Features](#security-features)
- [MVT Integration](#mvt-integration)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Features

Markush_audit combines three distinct security analysis layers:

### ADB Security Audit
- Apps analysis: Complete package inventory and sideloaded app detection
- Permissions check: Camera, Microphone, Location, SMS, Calls, Contacts monitoring
- Security settings: Developer options, USB debugging, Unknown sources, Mock location
- Access control: Accessibility services, Device admins, Notification listeners
- System status: Overlay permissions, Running processes, VPN/Proxy status
- Enterprise detection: Work profile, MDM (Mobile Device Management) checks

### Deep-Level Security Check
- Kernel analysis: Version, Build date, Architecture, Compiler information
- Bootloader status: Verified boot, Build type, OEM unlock, Build tags
- SELinux policy: Enforcing status, Policy version, Domain configurations
- Process monitoring: Root processes, Suspicious process names, Privilege escalation
- Network security: Listening ports, Established connections, Backdoor detection
- Baseband/modem: Version, RIL implementation, Network type, Operator info
- Kernel modules: Loaded modules, Suspicious module detection, Module signatures
- System properties: Security-relevant properties, Debuggable status, Fingerprinting
- Filesystem integrity: Mount status, Remount flags, dm-verity mode, Filesystem types
- Tracing status: Kernel tracing, Surveillance detection, Performance monitoring

### MVT Integration
Detection against 16+ threat intelligence feeds including NSO Group Pegasus, Predator (Intellexa), RCS Lab, Stalkerware, Quadream KingSpawn, Operation Triangulation, WyrmSpy/DragonEgg, Wintego Helios, NoviSpy, Candiru, ResidentBat, Cellebrite, DarkSword, Coruna, Morpheus, BTMOB, and Spyrtacus.

## Technology Stack

### Core Technologies
- Python 3.7+
- ADB (Android Debug Bridge)
- Shell Scripting
- JSON

### Python Libraries
| Library | Purpose |
|---------|---------|
| cryptography | Encryption |
| requests | HTTP |
| rich | Terminal UI |
| click | CLI |
| pydantic | Validation |
| PyYAML | Configuration |

### Security Tools
- MVT (Mobile Verification Toolkit)
- 16+ IOC Feeds
- SELinux analysis
- Kernel inspection
- Network tools (netstat/ss, ps, getprop, dumpsys, pm)

## Quick Start

```bash
git clone https://github.com/Thunder9954/Audit.git
cd Audit
pip install -r Documents/requirements.txt
python3 Markush/manage.py
```

## Installation

### Install ADB

**Linux:**
```bash
sudo apt update
sudo apt install adb
```

**macOS:**
```bash
brew install android-platform-tools
```

**Windows:** Download from [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)

### Enable USB Debugging

1. Settings → About Phone → Tap "Build Number" 7 times
2. Settings → Developer Options → Enable "USB Debugging"
3. Connect device via USB and accept authorization popup
4. Verify connection: `adb devices`

### Install Dependencies

```bash
pip install -r Documents/requirements.txt
```

MVT will be auto-installed in a virtual environment when first used.

## Usage

Run the audit tool:

```bash
python3 Markush/manage.py
```

**CLI Options:**

```bash
python3 Markush/manage.py --version    # Show version information
python3 Markush/manage.py --about       # Display detailed project information
python3 Markush/manage.py --delay 1.0   # Set custom delay between commands
python3 Markush/manage.py --verify     # Verify release authenticity
```

The tool will prompt you to:
1. Enter delay between commands (default: 0.5s)
2. Confirm each audit section (ADB, Deep Check, MVT)
3. Review results and recommendations

## Project Workflow

1. Start audit and check ADB connection
2. Gather device information
3. Run ADB security audit (apps, permissions, settings)
4. Perform deep security check (kernel, network, system)
5. Execute MVT analysis (spyware detection)
6. Generate comprehensive reports
7. Assess risks and provide recommendations

## Output Structure

```
audit_runs/
└── run_YYYYMMDD_HHMMSS/
    ├── adb_audit_report_YYYYMMDD_HHMMSS.txt
    ├── deep_security_report_YYYYMMDD_HHMMSS.txt
    ├── mvt_report_YYYYMMDD_HHMMSS.txt
    ├── master_security_audit_YYYYMMDD_HHMMSS.txt
    ├── master_security_audit_YYYYMMDD_HHMMSS.json
    ├── bugreport_YYYYMMDD_HHMMSS.zip
    └── mvt_results/
        ├── alerts.json
        ├── alerts_timeline.csv
        └── dbinfo.json
```

## Security Features

- **Read-only operations** - No device modifications
- **Local analysis** - All processing performed locally
- **No external data transmission** - Except MVT IOC downloads from official sources
- **Personal data protection** - Contacts, messages, and personal content are NOT included in reports
- **Virtual environment isolation** - MVT installed in isolated environment
- **No root required** - Works on standard Android devices

![Compromised Phone Detection](Data/2.jpg)

![Lock Security Types](Data/3.png)

## MVT Integration

MVT (Mobile Verification Toolkit) is developed by Amnesty International's Security Lab to detect signs of nation-state spyware. The tool automatically:

1. Downloads IOC indicators from 16+ threat intelligence feeds
2. Generates Android bug report via `adb bugreport`
3. Analyzes system state against known spyware signatures
4. Produces detailed alerts with severity levels (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
5. Provides matched indicators of compromise when detected

## Troubleshooting

### ADB Connection Issues

**Device not found:**
- Check USB cable (use original or high-quality cable)
- Try different USB port (direct connection, not through hub)
- Re-enable USB debugging on device
- Restart ADB: `adb kill-server && adb start-server`
- Check authorization: `adb devices`

**Device offline:**
- Disconnect and reconnect USB cable
- Toggle USB debugging off and on
- Restart device

### MVT Installation Issues

**Installation fails:**
- Ensure Python 3.7+ is installed
- Check internet connection
- Verify virtual environment: `ls python-pip/`
- Manual install: `python3 -m venv python-pip && source python-pip/bin/activate && pip install mvt`

**IOC download fails:**
- Check internet connection
- Verify MVT installation: `source python-pip/bin/activate && mvt-android version`
- Retry download (may be temporary server issue)

### Permission Issues

**Permission denied:**
- Ensure ADB has proper permissions
- On Linux: `sudo usermod -aG plugdev $USER`
- Restart ADB server after group change

## Roadmap

### Version 1.0.0 (Current)
- ADB security audit module
- Deep-level security checks
- MVT integration
- Comprehensive reporting
- Risk assessment
- JSON export

### Version 2.0.0 (Planned)
- Web-based dashboard
- Automated scheduling
- Cloud report storage
- Multi-device support
- Real-time monitoring
- ML threat detection
- SIEM integration
- Mobile app companion

## Contributing

1. Understand security implications and privacy considerations
2. Test on multiple Android versions
3. Follow existing code style
4. Add documentation for new features
5. Maintain user privacy and secure data handling

## License

Licensed under the MIT License - see the [LICENSE](Documents/LICENSE) file for details.

## Contact

**Creator:** Purn Vadodariya  
**Email:** purn872008@gmail.com  
**GitHub:** https://github.com/Thunder9954/Audit

For bug reports, feature suggestions, or questions:
- Email with detailed description and logs
- Open an issue on GitHub
- Submit pull requests for documentation improvements

## Acknowledgements

- Amnesty International Security Lab - MVT development and threat intelligence
- Android Open Source Project - ADB tools and documentation
- Security Research Community - Threat intelligence and IOC feeds
- Python Community - Excellent libraries and tools

## Additional Resources

- [Android Security Documentation](https://source.android.com/security)
- [MVT Documentation](https://github.com/mvt-project/mvt)
- [ADB Guide](https://developer.android.com/studio/command-line/adb)
- [Amnesty Security Lab](https://securitylab.amnesty.org/)
- [Citizen Lab](https://citizenlab.ca/)
- [EFF Surveillance Self-Defense](https://ssd.eff.org/)

## Release Verification

Official releases are signed using Ed25519 cryptographic signatures to ensure authenticity and integrity. Each release includes:

- `manifest.json` - SHA-256 hashes of all project files
- `manifest.sig` - Ed25519 signature of the manifest
- `public_key.pem` - Public verification key

### Verify a Release

To verify that you have an authentic, unmodified release:

```bash
python3 Markush/manage.py --verify
```

This will display:
- Project information
- Signature status (VALID/INVALID)
- Manifest status (VALID/INVALID)
- Overall build status

### Verification Output

**Official Build:**
```
Project: Markush Audit
Version: 1.0.0
Author: Purn Vadodariya
GitHub: https://github.com/Thunder9954/Audit

Signature: VALID
Manifest: VALID

Overall Status: Official Build
```

**Modified/Unofficial Build:**
```
Signature: INVALID
Manifest: INVALID

Overall Status: Modified / Unofficial Build
```

### Development Builds

If verification files are not found, the tool will report a development build. This is normal when running from source code that hasn't been packaged as a release.

### Security Notes

- The private signing key is never committed to the repository
- Verification uses only the public key, which is safe to distribute
- The verification process is transparent and can be audited
- Modified or unofficial builds will still run with a warning

---

**This tool is for legitimate security auditing only. Unauthorized access to devices is illegal. Use only on devices you own or have explicit permission to audit.**
