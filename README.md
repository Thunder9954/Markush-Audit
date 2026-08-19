<div align="center">

# Markush Audit

**Professional Android Security Audit Framework**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Thunder9954/Audit)
[![Python](https://img.shields.io/badge/python-3.7%2B-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/Thunder9954/Audit)
[![GitHub Stars](https://img.shields.io/github/stars/Thunder9954/Audit?style=social)](https://github.com/Thunder9954/Audit/stargazers)
[![Release](https://img.shields.io/badge/release-verified-brightgreen)](https://github.com/Thunder9954/Audit/releases)
[![Security](https://img.shields.io/badge/security-Ed25519-blue)](https://github.com/Thunder9954/Audit#release-verification)

A comprehensive Android security audit framework combining ADB commands, deep-level security checks, and Mobile Verification Toolkit (MVT) for nation-state spyware detection.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](-contributing)

</div>

---

![Security Overview](Data/1.png)

*Professional Android Security Audit Framework*

## Table of Contents

- [About](#about)
- [Features](#features)
- [Screenshots](#screenshots)
- [Video Demo](#video-demo)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Workflow](#project-workflow)
- [Output Structure](#output-structure)
- [Project Structure](#project-structure)
- [Security & Authenticity](#security--authenticity)
- [Screenshots Gallery](#screenshots-gallery)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About

Markush Audit is a comprehensive Android security audit framework designed for security professionals, researchers, and privacy advocates. It combines three powerful analysis layers:

- **ADB Security Analysis** - Complete device inspection via Android Debug Bridge
- **Deep Android Security Checks** - Kernel, bootloader, SELinux, and system-level analysis
- **Mobile Verification Toolkit (MVT)** - Nation-state spyware detection using threat intelligence feeds

### Who is it for?

- Security researchers and penetration testers
- Digital forensics investigators
- Privacy advocates and activists
- System administrators managing Android fleets
- Anyone concerned about mobile device security

### Security Focus

Markush Audit focuses on detecting:
- Nation-state spyware and surveillance tools
- Unauthorized access and compromise indicators
- Security misconfigurations
- Privacy violations
- Suspicious applications and permissions

### Privacy Focus

- **Read-only operations** - No device modifications
- **Local analysis** - All processing performed locally
- **No external data transmission** - Except official IOC downloads
- **Personal data protection** - Contacts, messages, and personal content are NOT included in reports

## Features

| Feature | Description |
|---------|-------------|
| **ADB Commands** | Complete device inspection via Android Debug Bridge |
| **Deep Security Analysis** | Kernel, bootloader, SELinux, and system-level checks |
| **MVT Integration** | Nation-state spyware detection with 16+ threat intelligence feeds |
| **Spyware Detection** | Detection against NSO Pegasus, Predator, RCS Lab, and more |
| **Report Generation** | Comprehensive HTML, text, and JSON reports |
| **Android Privacy Audit** | Permissions, accessibility services, and monitoring detection |
| **USB Debugging Analysis** | Security settings and developer options inspection |
| **Application Analysis** | Sideloaded app detection and dangerous permissions |
| **Security Recommendations** | Risk assessment and mitigation guidance |
| **Release Verification** | Ed25519 cryptographic signatures for authenticity |

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

## Screenshots

### Security Overview

![Compromised Device](Data/2.png)

*Example of a potentially compromised Android device under investigation*

### Android Device Protection

![Device Lock Methods](Data/3.png)

Markush Audit evaluates Android authentication mechanisms during device security assessment:

- **Face Unlock** - Biometric face recognition security
- **Pattern Lock** - Pattern-based screen lock
- **PIN Lock** - Numeric PIN code security
- **Fingerprint Lock** - Biometric fingerprint authentication

## 🎥 Video Demonstration

Watch the complete walkthrough of **Markush Audit**, including installation, setup, ADB connection, security analysis, MVT integration, threat detection, and report generation.

<p align="center">
  <a href="Data/main.mp4">
    <img src="Data/m.png"
         alt="Watch Markush Audit Demo"
         width="900">
  </a>
</p>

<p align="center">
<b>▶ Click the image above to watch or download the complete demonstration video.</b>
</p>

### What the video demonstrates

- Installation and setup
- ADB configuration
- Connecting an Android device
- Deep Security Analysis
- MVT Integration
- Spyware Detection
- Privacy Audit
- HTML Report Generation
- Complete workflow

**Direct Download**

[📥 Download Demo Video](Data/main.mp4)

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

### Prerequisites

- Python 3.7 or higher
- ADB (Android Debug Bridge)
- Android device with USB debugging enabled
- USB cable

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

**Windows:**
Download from [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)

### Enable USB Debugging

1. Go to **Settings → About Phone**
2. Tap **"Build Number"** 7 times to enable Developer Options
3. Go to **Settings → Developer Options**
4. Enable **"USB Debugging"**
5. Connect device via USB and accept authorization popup
6. Verify connection: `adb devices`

### Clone Repository

```bash
git clone https://github.com/Thunder9954/Audit.git
cd Audit
```

### Install Dependencies

```bash
pip install -r Documents/requirements.txt
```

MVT will be auto-installed in a virtual environment when first used.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Thunder9954/Audit.git
cd Audit

# Install dependencies
pip install -r Documents/requirements.txt

# Enable USB debugging on your Android device
# Connect device via USB

# Run the audit tool
python3 Markush/manage.py
```

That's it! The tool will guide you through the audit process.

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

```
Android Device
       │
       ▼
   ADB Connection
       │
       ▼
  Security Scan
       │
       ├─→ ADB Audit (Apps, Permissions, Settings)
       │
       ├─→ Deep Analysis (Kernel, Network, System)
       │
       └─→ MVT Execution (Spyware Detection)
              │
              ▼
         Threat Detection
              │
              ▼
         HTML Report
              │
              ▼
         JSON Export
              │
              ▼
      Risk Assessment
              │
              ▼
      Recommendations
```

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

All reports are organized in timestamped directories for easy tracking and comparison.

## Project Structure

```
Markush-Audit/
├── Markush/                    # Python source code
│   ├── __init__.py
│   ├── ADB_commands.py         # ADB security audit module
│   ├── Deep_check.py           # Deep-level security checks
│   ├── MVT.py                  # MVT integration
│   ├── manage.py               # Main orchestration script
│   ├── project_info.py         # Centralized metadata
│   ├── manifest.py             # SHA-256 manifest generator
│   ├── sign_release.py         # Release signing tool
│   ├── verify_release.py       # Release verification tool
│   └── release.py              # Release creation script
├── Documents/                  # Documentation
│   ├── GIT_SIGNING.md          # Git signing guide
│   ├── requirements.txt        # Python dependencies
│   └── requirementsV.txt       # Alternative requirements
├── Data/                       # Images and video
│   ├── 1.png                   # Security overview
│   ├── 2.jpg                   # Compromised device example
│   ├── 3.png                   # Device lock methods
│   └── main.mp4                # Video demonstration
├── keys/                       # Cryptographic keys
│   ├── generate_keys.py        # Key generation script
│   └── public_key.pem          # Public verification key
├── .github/                    # GitHub workflows
│   └── workflows/
│       └── release.yml         # Automated release workflow
├── docs/                       # Additional documentation
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── MVT.md
│   └── TROUBLESHOOTING.md
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

## Security & Authenticity

### Release Verification

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

### Security Features

- **Read-only operations** - No device modifications
- **Local analysis** - All processing performed locally
- **No external data transmission** - Except MVT IOC downloads from official sources
- **Personal data protection** - Contacts, messages, and personal content are NOT included in reports
- **Virtual environment isolation** - MVT installed in isolated environment
- **No root required** - Works on standard Android devices

## MVT Integration

MVT (Mobile Verification Toolkit) is developed by Amnesty International's Security Lab to detect signs of nation-state spyware. The tool automatically:

1. Downloads IOC indicators from 16+ threat intelligence feeds
2. Generates Android bug report via `adb bugreport`
3. Analyzes system state against known spyware signatures
4. Produces detailed alerts with severity levels (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
5. Provides matched indicators of compromise when detected

## Screenshots Gallery

<div align="center">

![Security Overview](Data/m.png)

*Markush Android Security Audit Framework*

</div>

---

<div align="center">

![Device Lock Methods](Data/3.png)

*Android authentication mechanisms evaluated during security assessment*

</div>

## FAQ

### Q: Does Markush Audit require root access?

**A:** No, Markush Audit works on standard Android devices without root access. It uses ADB (Android Debug Bridge) which requires USB debugging to be enabled, but does not require root privileges.

### Q: Is my personal data safe?

**A:** Yes. Markush Audit performs read-only operations and does not modify your device. Contacts, messages, and personal content are NOT included in reports. All analysis is performed locally on your machine.

### Q: Can this tool detect all spyware?

**A:** Markush Audit uses MVT (Mobile Verification Toolkit) which detects indicators of compromise from 16+ threat intelligence feeds, including NSO Group Pegasus, Predator, and other known spyware. However, no tool can guarantee detection of all possible threats.

### Q: Does this work on iOS devices?

**A:** No, Markush Audit is designed specifically for Android devices. MVT does have iOS support, but this implementation focuses on Android security auditing.

### Q: What Android versions are supported?

**A:** Markush Audit works on Android 5.0 (Lollipop) and later, as long as ADB is available and USB debugging can be enabled.

### Q: Can I use this on multiple devices?

**A:** Yes, you can run the audit on any number of Android devices. Each audit run creates a timestamped directory with separate reports for each device.

### Q: How long does an audit take?

**A:** A typical audit takes 5-15 minutes depending on:
- Device storage size
- Number of installed applications
- Network speed for IOC downloads
- MVT analysis complexity

### Q: What should I do if threats are detected?

**A:** If Markush Audit detects potential threats:
1. Review the detailed reports in the `audit_runs/` directory
2. Consider performing a factory reset of your device
3. Change all passwords on the device
4. Enable two-factor authentication where possible
5. Contact security professionals if you believe you are targeted

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

### Version 1.0.0 (Current) ✅
- [x] ADB security audit module
- [x] Deep-level security checks
- [x] MVT integration
- [x] Comprehensive reporting
- [x] Risk assessment
- [x] JSON export
- [x] Ed25519 release verification

### Version 2.0.0 (Planned)
- [ ] Web-based dashboard
- [ ] Automated scheduling
- [ ] Cloud report storage
- [ ] Multi-device support
- [ ] Real-time monitoring
- [ ] ML threat detection
- [ ] SIEM integration
- [ ] Mobile app companion


## Contributing

We welcome contributions from the security community! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Guidelines

- **Security implications** - Understand the security and privacy implications of your changes
- **Testing** - Test on multiple Android versions and devices
- **Code style** - Follow existing code style and PEP 8 guidelines
- **Documentation** - Add documentation for new features
- **Privacy** - Maintain user privacy and secure data handling practices
- **No malware** - Do not add any malicious code or backdoors

### Areas for Contribution

- Additional threat intelligence feeds
- New security checks
- Performance optimizations
- Documentation improvements
- Bug fixes
- Feature requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Purn Vadodariya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Author

<div align="center">

**Purn Vadodariya**

[![GitHub](https://img.shields.io/badge/GitHub-Thunder9954-blue)](https://github.com/Thunder9954)
[![Email](https://img.shields.io/badge/Email-purn872008@gmail.com-red)](mailto:purn872008@gmail.com)

**Project: Markush Audit**

*Professional Android Security Audit Framework*

</div>

## Contact

### Get in Touch

- **GitHub:** [https://github.com/Thunder9954/Audit](https://github.com/Thunder9954/Audit)
- **Email:** [purn872008@gmail.com](mailto:purn872008@gmail.com)

### Support

For bug reports, feature suggestions, or questions:

- 📧 Email with detailed description and logs
- 🐛 Open an issue on GitHub
- 📝 Submit pull requests for documentation improvements
- 💬 Join discussions in GitHub Issues

### Professional Inquiries

For professional inquiries, consulting, or collaboration opportunities, please contact via email with a detailed description of your requirements.

## Acknowledgements

This project would not be possible without the contributions of:

- **Amnesty International Security Lab** - MVT development and threat intelligence feeds
- **Android Open Source Project** - ADB tools and documentation
- **Security Research Community** - Threat intelligence and IOC feeds
- **Python Community** - Excellent libraries and tools
- **Open Source Contributors** - For making security tools accessible to everyone

## Additional Resources

- [Android Security Documentation](https://source.android.com/security)
- [MVT Documentation](https://github.com/mvt-project/mvt)
- [ADB Guide](https://developer.android.com/studio/command-line/adb)
- [Amnesty Security Lab](https://securitylab.amnesty.org/)
- [Citizen Lab](https://citizenlab.ca/)
- [EFF Surveillance Self-Defense](https://ssd.eff.org/)
- [Git Signing Guide](Documents/GIT_SIGNING.md)

---

<div align="center">

**⚠️ Disclaimer**

This tool is for legitimate security auditing only. Unauthorized access to devices is illegal. Use only on devices you own or have explicit permission to audit.

**Made with ❤️ by Purn Vadodariya**

[⭐ Star this project](https://github.com/Thunder9954/Audit) • [🐛 Report issues](https://github.com/Thunder9954/Audit/issues) • [📖 Documentation](https://github.com/Thunder9954/Audit)

</div>
