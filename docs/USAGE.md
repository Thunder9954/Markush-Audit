# Usage Guide

Complete usage instructions for Markush_audit.

## Basic Usage

```bash
python3 manage.py
```

## Configuration

When prompted, enter the delay between commands:
- **Default**: 0.5 seconds
- **Purpose**: Prevent overwhelming ADB connection
- **Recommendation**: Use default unless experiencing connection issues

## Interactive Prompts

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

## Advanced Usage

### Run with Custom Delay

```bash
python3 manage.py
# Enter custom delay when prompted
```

### Run Specific Audit Sections

The tool allows you to skip sections by responding 'n' to prompts.

### Re-run Failed Checks

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

## Audit Flow

1. **Start Audit** - Initialize tool and check ADB connection
2. **Device Info** - Gather basic device information
3. **ADB Audit** - Analyze apps, permissions, settings
4. **Deep Check** - Inspect kernel, network, system
5. **MVT Analysis** - Detect nation-state spyware
6. **Generate Reports** - Create comprehensive audit reports
7. **Risk Assessment** - Analyze findings and prioritize threats
8. **Display Results** - Show summary and recommendations

## Output Files

Each audit run creates a timestamped directory with organized results:

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

## Report Descriptions

### ADB Audit Report
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

### Deep Security Report
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

### MVT Report
- Total alerts count
- Alerts by severity (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
- Matched indicators of compromise
- Detailed alert timeline
- Module-specific findings
- IOC hit analysis

### Master Security Audit Report
- Consolidated summary of all audits
- Risk assessment overview
- Recommendations
- JSON export for programmatic access
