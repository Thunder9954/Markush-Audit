# 🔐 Markush_audit - Master Security Audit Tool

A comprehensive Android security audit tool combining ADB commands, deep-level security checks, and Mobile Verification Toolkit (MVT) for nation-state spyware detection.

**Creator:** Purn Vadodariya  
**Email:** purn872008@gmail.com  
**GitHub:** https://github.com/Thunder9954/Audit

## 📸 Project Overview

![Security Overview](d/1.png)

*Figure 1: Comprehensive security audit covering multiple layers of Android device protection*

---

## 🚨 Compromised Device Detection

![Compromised Phone](d/2.jpg)

*Figure 2: Visual representation of compromised phone detection and security analysis*

---

## 🔒 Device Lock Security Analysis

![Lock Types](d/3.png)

*Figure 3: Four types of device lock security - Face Recognition, Pattern Lock, PIN/Number Lock, and Fingerprint Authentication*

---

## 🎥 Complete Usage Tutorial

[![Watch Tutorial](d/main.mp4)](d/main.mp4)

*Click to watch the complete video tutorial demonstrating full code usage and workflow*

---

## ✨ Features

### 🔍 ADB Security Audit
- **Apps Analysis**: Complete package inventory and sideloaded app detection
- **Permissions Check**: Dangerous permissions monitoring (Camera, Microphone, Location, SMS, Calls, Contacts)
- **Security Settings**: Developer options, USB debugging, unknown sources, mock location
- **Access Control**: Accessibility services, device admins, notification listeners
- **System Status**: Overlay permissions, running processes, VPN/proxy status
- **Enterprise Detection**: Work profile and MDM (Mobile Device Management) checks

### 🛡️ Deep-Level Security Check
- **Kernel Analysis**: Version, build date, architecture information
- **Bootloader Status**: Verified boot, build type, OEM unlock, build tags
- **SELinux Policy**: Enforcing status and policy version
- **Process Monitoring**: Root processes, suspicious process names, privilege escalation
- **Network Security**: Listening ports, established connections, backdoor detection
- **Baseband/Modem**: Version, RIL implementation, network type, operator info
- **Kernel Modules**: Loaded modules, suspicious module detection
- **System Properties**: Security-relevant properties, debuggable status
- **Filesystem Integrity**: Mount status, remount flags, dm-verity mode
- **Tracing Status**: Kernel tracing surveillance detection

### 🦠 MVT Integration (Nation-State Spyware Detection)
Detection against 16+ threat intelligence feeds:
- **NSO Group Pegasus** - iOS/Android spyware
- **Predator Spyware** (Intellexa) - Advanced surveillance
- **RCS Lab** - Italian spyware
- **Stalkerware Indicators** - Domestic surveillance tools
- **Quadream KingSpawn** - iOS exploit
- **Operation Triangulation** - Zero-click exploit
- **WyrmSpy/DragonEgg** - Android spyware
- **Wintego Helios** - Mobile surveillance
- **NoviSpy** (Serbia) - Balkan region spyware
- **Candiru** (DevilsTongue) - Mercenary spyware
- **ResidentBat** - Advanced persistent threat
- **Cellebrite** - Forensic tool detection
- **DarkSword** - Surveillance malware
- **Coruna** - Mobile threat
- **Morpheus** - Spyware framework
- **BTMOB** - Bluetooth-based threats
- **Spyrtacus** - Emerging threats

---

## 📁 Project Structure

```
Android Security Audit Tool/
├── ADB_commands.py              # ADB-based security audit module
├── Deep_check.py               # Deep-level security checks (kernel, SELinux, network)
├── MVT.py                      # MVT integration for spyware detection
├── manage.py                   # Main controller and orchestration
├── requirements.txt            # Python dependencies with version constraints
├── requirementsV.txt           # Python dependencies (latest versions)
├── README.md                   # This file
├── python-pip/                 # Virtual environment for MVT (auto-created)
├── audit_runs/                 # Audit output directory
│   └── run_YYYYMMDD_HHMMSS/   # Timestamped audit results
│       ├── adb_audit_report_YYYYMMDD_HHMMSS.txt
│       ├── deep_security_report_YYYYMMDD_HHMMSS.txt
│       ├── mvt_report_YYYYMMDD_HHMMSS.txt
│       ├── master_security_audit_YYYYMMDD_HHMMSS.txt
│       ├── master_security_audit_YYYYMMDD_HHMMSS.json
│       ├── bugreport_YYYYMMDD_HHMMSS.zip
│       └── mvt_results/
│           ├── alerts.json
│           ├── alerts_timeline.csv
│           └── dbinfo.json
└── d/                          # Documentation media
    ├── 1.png                   # Security overview
    ├── 2.jpg                   # Compromised phone visualization
    ├── 3.png                   # Lock security types
    └── main.mp4               # Complete usage tutorial
```

---

## 🔧 Technologies & Tools Used

### Core Technologies
- **Python 3.7+** - Primary programming language
- **ADB (Android Debug Bridge)** - Android device communication
- **Subprocess** - System command execution
- **JSON** - Data serialization and export
- **Virtual Environment (venv)** - Isolated Python environment

### Security Tools
- **MVT (Mobile Verification Toolkit)** - Nation-state spyware detection
- **IOC (Indicators of Compromise)** - Threat intelligence feeds
- **SELinux** - Security-Enhanced Linux policy analysis
- **Kernel Analysis** - Low-level system inspection

### Python Libraries
- **cryptography** - Cryptographic operations
- **requests** - HTTP requests for IOC downloads
- **pydantic** - Data validation
- **rich** - Terminal formatting
- **click** - Command-line interface
- **PyYAML** - YAML configuration parsing

### System Tools
- **netstat/ss** - Network connection analysis
- **ps** - Process monitoring
- **getprop** - Android system properties
- **dumpsys** - Android system service dumps
- **pm** - Package manager commands

---

## 📋 Requirements

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL
- **Python Version**: 3.7 or higher
- **ADB**: Android Debug Bridge (system-wide installation)
- **Android Device**: With USB debugging enabled
- **USB Cable**: For device connection
- **Internet Connection**: For MVT IOC downloads

### Hardware Requirements
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space for reports and bug reports
- **USB Port**: For device connection

---

## 🚀 Installation

### Step 1: Install ADB

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install adb
```

**macOS:**
```bash
brew install android-platform-tools
```

**Windows:**
Download from: https://developer.android.com/studio/releases/platform-tools

### Step 2: Verify ADB Installation
```bash
adb version
```

### Step 3: Enable USB Debugging on Android Device

1. **Enable Developer Options:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Developer Options will be enabled

2. **Enable USB Debugging:**
   - Go to Settings > Developer Options
   - Enable "USB Debugging"
   - Enable "Stay Awake" (optional, keeps screen on)

3. **Connect Device:**
   - Connect via USB cable
   - Accept the authorization popup on your phone
   - Verify connection: `adb devices`

### Step 4: Clone or Download Project
```bash
cd /path/to/your/workspace
# Clone or extract the project files
```

### Step 5: (Optional) Install Python Dependencies
```bash
# With specific versions (recommended for stability)
pip install -r requirements.txt

# Or with latest versions
pip install -r requirementsV.txt
```

**Note:** MVT will be auto-installed in a virtual environment when first used.

---

## 💻 Usage

### Basic Usage

Run the master security audit tool:

```bash
python3 manage.py
```

### Configuration

When prompted, enter the delay between commands:
- **Default**: 0.5 seconds
- **Purpose**: Prevent overwhelming ADB connection
- **Recommendation**: Use default unless experiencing connection issues

### Interactive Prompts

The tool will ask for confirmation before each major section:

```
[1/3] ADB SECURITY AUDIT
  Run ADB security audit? [Y/n]: y

[2/3] DEEP-LEVEL SECURITY CHECK
  Run deep-level security check? [Y/n]: y

[3/3] MOBILE VERIFICATION TOOLKIT (MVT)
  Run MVT analysis for nation-state spyware detection? [Y/n]: y
```

**Response Options:**
- `y` or `yes` - Proceed with the section
- `n` or `no` - Skip the section
- Press Enter - Use default option

### Advanced Usage

#### Run with Custom Delay
```bash
python3 manage.py
# Enter custom delay when prompted
```

#### Run Specific Audit Sections
The tool allows you to skip sections by responding 'n' to prompts.

#### Re-run Failed Checks
If ADB connection fails, the tool offers automatic reconnection:
```
✗ Device not authorized or offline
  Troubleshooting steps:
  1. Enable USB debugging on your device
  2. Accept the USB debugging authorization popup on your phone
  3. Try a different USB cable or port
  4. Restart ADB server: adb kill-server && adb start-server
  
  Try to reconnect? [Y/n]: y
```

---

## 📊 Output Files

Each audit run creates a timestamped directory with organized results:

### Directory Structure
```
audit_runs/
└── run_20260819_191147/
    ├── adb_audit_report_20260819_191446.txt
    ├── deep_security_report_20260819_191512.txt
    ├── mvt_report_20260819_191925.txt
    ├── master_security_audit_20260819_191932.txt
    ├── master_security_audit_20260819_191932.json
    ├── bugreport_20260819_191800.zip
    └── mvt_results/
        ├── alerts.json
        ├── alerts_timeline.csv
        └── dbinfo.json
```

### Report Descriptions

#### ADB Audit Report
- Device information (model, Android version, security patch)
- Developer settings status
- Complete package list
- Sideloaded apps (non-Play Store)
- Apps with dangerous permissions
- Accessibility services
- Device administrators
- Notification listeners
- Overlay permissions
- Running processes
- VPN/proxy status
- Work profile/MDM status

#### Deep Security Report
- Kernel version and build information
- Bootloader status and verified boot
- SELinux status and policy
- Process analysis (root/suspicious processes)
- Network connections and listening ports
- Baseband/modem information
- Kernel modules analysis
- System properties security check
- Filesystem integrity
- Tracing status
- Risk assessment (High/Medium/Low)

#### MVT Report
- Total alerts count
- Alerts by severity (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
- Matched indicators of compromise
- Detailed alert timeline
- Module-specific findings
- IOC hit analysis

#### Master Security Audit Report
- Consolidated summary of all audits
- Risk assessment overview
- Recommendations
- JSON export for programmatic access

---

## 🔍 MVT Details

### What is MVT?
MVT (Mobile Verification Toolkit) is an open-source tool developed by Amnesty International's Security Lab to detect signs of compromise on mobile devices.

### IOC Sources
MVT downloads indicators from 16+ threat intelligence feeds:

| Threat Intel Feed | Type | Target |
|-------------------|------|--------|
| NSO Group Pegasus | Spyware | iOS/Android |
| Predator (Intellexa) | Spyware | Android |
| RCS Lab | Spyware | Android |
| Stalkerware | Domestic Abuse | Android |
| Quadream KingSpawn | Exploit | iOS |
| Operation Triangulation | Zero-click | iOS |
| WyrmSpy/DragonEgg | Spyware | Android |
| Wintego Helios | Surveillance | Mobile |
| NoviSpy | Spyware | Android |
| Candiru (DevilsTongue) | Mercenary | Mobile |
| ResidentBat | APT | Mobile |
| Cellebrite | Forensic | Mobile |
| DarkSword | Malware | Mobile |
| Coruna | Threat | Mobile |
| Morpheus | Spyware | Mobile |
| BTMOB | Bluetooth | Mobile |
| Spyrtacus | Emerging | Mobile |

### MVT Installation
The tool automatically installs MVT in a virtual environment:
```bash
python-pip/  # Virtual environment directory
```

### Bug Report Generation
MVT requires an Android bug report for analysis:
- Generated via `adb bugreport`
- Takes 1-5 minutes depending on device
- Requires screen to be ON and UNLOCKED
- Contains comprehensive system state

---

## 🛠️ Troubleshooting

### ADB Connection Issues

**Problem:** Device not found or unauthorized

**Solutions:**
1. Check USB cable (use original or high-quality cable)
2. Try different USB port (direct connection, not through hub)
3. Re-enable USB debugging on device
4. Restart ADB server:
   ```bash
   adb kill-server
   adb start-server
   ```
5. Check device authorization:
   ```bash
   adb devices
   ```
6. Revoke USB debugging authorization and re-accept

**Problem:** Device offline

**Solutions:**
1. Disconnect and reconnect USB cable
2. Toggle USB debugging off and on
3. Restart device
4. Check USB cable for damage

### MVT Installation Issues

**Problem:** MVT installation fails

**Solutions:**
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

**Problem:** IOC download fails

**Solutions:**
1. Check internet connection
2. Verify MVT installation:
   ```bash
   source python-pip/bin/activate
   mvt-android version
   ```
3. Retry download (may be temporary server issue)

### Permission Issues

**Problem:** Permission denied errors

**Solutions:**
1. Ensure ADB has proper permissions
2. On Linux, add user to plugdev group:
   ```bash
   sudo usermod -aG plugdev $USER
   ```
3. Restart ADB server after group change

### Memory/Storage Issues

**Problem:** Out of memory during bug report generation

**Solutions:**
1. Close other applications
2. Ensure sufficient disk space (500MB+)
3. Use smaller delay between commands

---

## 🔒 Security Notes

### Data Privacy
- **Read-Only Operations**: Tool performs only read checks, no device modifications
- **Local Analysis**: All analysis performed locally on your computer
- **No External Data Transmission**: No data sent to external servers (except MVT IOC downloads from official sources)
- **Report Content**: Reports contain package names, permissions, and system information only
- **Personal Data Protection**: Contacts, messages, and personal content are NOT included in reports

### Safe Usage
- Tool does not install any malware or spyware
- Virtual environment isolates MVT installation
- No persistent changes to device
- No root or modification required

### Limitations
The tool cannot detect:
- Kernel/firmware-level nation-state spyware that leaves no traces
- Zero-click exploits that only exist in RAM
- Hardware-level compromises
- Baseband/modem implants
- Advanced persistent threats with sophisticated evasion

For these advanced threats, seek professional forensic analysis.

---

## 🚨 Professional Help

If MVT detects indicators of compromise or you suspect targeted surveillance:

### Amnesty International Security Lab
- **Website**: https://securitylab.amnesty.org/get-help/
- **Services**: Free forensic analysis for human rights defenders
- **Contact**: securitylab@amnesty.org

### Digital Defenders Partnership
- **Website**: https://digitaldefenders.org/
- **Services**: Emergency response for digital attacks
- **Hotline**: Available for urgent cases

### Access Now
- **Website**: https://www.accessnow.org/help/
- **Services**: Digital security support for at-risk users
- **Helpline**: 24/7 emergency response

### Citizen Lab
- **Website**: https://citizenlab.ca/
- **Services**: Research and analysis of digital threats

---

## 📜 License

This tool is provided for educational and security auditing purposes. Use responsibly and in accordance with applicable laws and regulations.

**Disclaimer**: This tool is provided as-is without warranty. It cannot guarantee detection of all threats. For high-risk situations, consult professional security researchers.

---

## 🤝 Contributing

Before making changes to this security audit tool:

1. **Understand Security Implications**
   - Changes could affect detection capabilities
   - Consider privacy implications
   - Test thoroughly before deployment

2. **Testing Requirements**
   - Test on multiple Android versions
   - Verify no data leakage
   - Ensure backward compatibility

3. **Code Standards**
   - Follow existing code style
   - Add documentation for new features
   - Update README accordingly

4. **Privacy Protection**
   - Maintain user privacy
   - No data collection without consent
   - Secure handling of sensitive information

---

## 📞 Support & Contact

**Creator**: Purn Vadodariya  
**Email**: purn872008@gmail.com

For issues, questions, or contributions:
- Report bugs via email
- Suggest features via email
- Submit pull requests (if repository is public)

---

## 🙏 Acknowledgments

- **Amnesty International Security Lab** - MVT development and threat intelligence
- **Android Open Source Project** - ADB tools and documentation
- **Security Research Community** - Threat intelligence and IOC feeds
- **Python Community** - Excellent libraries and tools

---

## 📈 Version History

### Current Version: 1.0.0
- Initial release
- ADB security audit module
- Deep-level security checks
- MVT integration
- Comprehensive reporting
- Risk assessment
- JSON export

---

## 🔮 Future Enhancements

Planned features for future versions:
- Web-based dashboard
- Automated scheduling
- Cloud report storage
- Multi-device support
- Real-time monitoring
- Machine learning threat detection
- Integration with SIEM systems
- Mobile app companion

---

## 📚 Additional Resources

### Learning Resources
- [Android Security Documentation](https://source.android.com/security)
- [MVT Documentation](https://github.com/mvt-project/mvt)
- [ADB Guide](https://developer.android.com/studio/command-line/adb)

### Security Communities
- [Amnesty Security Lab](https://securitylab.amnesty.org/)
- [Citizen Lab](https://citizenlab.ca/)
- [EFF Surveillance Self-Defense](https://ssd.eff.org/)

### Related Tools
- [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
- [AndroBugs](https://github.com/AndroBugs/)
- [QARK](https://github.com/linkedin/qark)

---

**⚠️ Important**: This tool is for legitimate security auditing only. Unauthorized access to devices is illegal. Use only on devices you own or have explicit permission to audit.
