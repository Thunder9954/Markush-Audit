#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
Master Security Audit Manager
Main controller integrating ADB commands, Deep security checks, and MVT.
Handles user input, delays, permissions, connection management, and orchestration.
"""

import sys
import os
import time
import getpass
import subprocess
import argparse
from datetime import datetime
from typing import Tuple, Optional

from ADB_commands import ADBCommands
from Deep_check import DeepSecurityCheck
from MVT import MVTIntegration
from project_info import (
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
    AUTHOR,
    COPYRIGHT,
    GITHUB_URL,
    LICENSE,
    VERSION,
    EMAIL,
    get_banner,
    get_version_info,
    get_about_info
)


class SecurityAuditManager:
    def __init__(self, default_delay: float = 0.5):
        self.default_delay = default_delay

        # Single timestamped folder for this entire run - every report,
        # bugreport, and MVT result goes inside here instead of scattering
        # into whatever directory the script happened to be launched from.
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join("audit_runs", f"run_{self.run_timestamp}")
        os.makedirs(self.run_dir, exist_ok=True)

        self.adb = ADBCommands(delay=default_delay, output_dir=self.run_dir)
        self.deep_check = DeepSecurityCheck(delay=default_delay, output_dir=self.run_dir)
        self.mvt = MVTIntegration(delay=default_delay, output_dir=self.run_dir)
        self.audit_results = {}

        print(f"All output for this run will be saved to: {self.run_dir}/\n")
        
    def print_banner(self):
        """Print welcome banner"""
        print(get_banner())
    
    def print_section(self, title: str):
        """Print section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def delay(self, seconds: Optional[float] = None):
        """Execute delay with progress indicator"""
        delay_time = seconds if seconds else self.default_delay
        if delay_time > 1:
            for i in range(int(delay_time)):
                print(f"  Waiting... {i+1}/{int(delay_time)}", end='\r')
                time.sleep(1)
            print(" " * 50, end='\r')
        else:
            time.sleep(delay_time)
    
    def get_user_confirmation(self, prompt: str, default: bool = False) -> bool:
        """Get user confirmation with YES/NO input"""
        while True:
            default_str = "Y/n" if default else "y/N"
            response = input(f"{prompt} [{default_str}]: ").strip().lower()
            
            if not response:
                return default
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("  Please enter 'y' or 'n'")
    
    def get_password(self, prompt: str = "Enter password: ") -> str:
        """Get password input securely"""
        return getpass.getpass(prompt)
    
    def check_adb_connection(self) -> bool:
        """Check and establish ADB connection"""
        self.print_section("ADB CONNECTION CHECK")
        
        connected, message = self.adb.check_connection()
        
        if connected:
            print(f"✓ {message}")
            print(f"  Device ID: {self.adb.device_id}")
            return True
        else:
            print(f"✗ {message}")
            print("\n  Troubleshooting steps:")
            print("  1. Enable USB debugging on your device")
            print("  2. Accept the USB debugging authorization popup on your phone")
            print("  3. Try a different USB cable or port")
            print("  4. Restart ADB server: adb kill-server && adb start-server")
            
            if self.get_user_confirmation("  Try to reconnect?"):
                # Restart ADB server
                print("  Restarting ADB server...")
                subprocess.run("adb kill-server", shell=True)
                time.sleep(2)
                subprocess.run("adb start-server", shell=True)
                time.sleep(2)
                
                connected, message = self.adb.check_connection()
                if connected:
                    print(f"✓ Reconnected: {message}")
                    return True
                else:
                    print(f"✗ Reconnection failed: {message}")
                    return False
            else:
                return False
    
    def run_adb_audit(self) -> bool:
        """Run ADB-based security audit"""
        self.print_section("ADB SECURITY AUDIT")
        
        if not self.get_user_confirmation("  Run ADB security audit?"):
            print("  Skipping ADB audit...")
            return False
        
        print("\n  Running ADB audit checks...")
        print("  This may take several minutes...\n")
        
        results = {}
        
        # Device info
        print("  [1/12] Getting device information...")
        self.delay()
        results['device_info'] = self.adb.get_device_info()
        print(f"  ✓ Device: {results['device_info'].get('model', 'Unknown')}")
        
        # Developer settings
        print("  [2/12] Checking developer settings...")
        self.delay()
        results['developer_settings'] = self.adb.check_developer_settings()
        print("  ✓ Developer settings checked")
        
        # Installed packages
        print("  [3/12] Getting installed packages...")
        self.delay(2)
        results['installed_packages'] = self.adb.get_installed_packages()
        print(f"  ✓ Found {len(results['installed_packages'])} packages")
        
        # Sideloaded apps
        print("  [4/12] Checking for sideloaded apps...")
        self.delay(2)
        results['sideloaded_apps'] = self.adb.get_sideloaded_apps()
        print(f"  ✓ Found {len(results['sideloaded_apps'])} sideloaded apps")
        
        # Dangerous permissions
        print("  [5/12] Checking dangerous permissions...")
        self.delay(3)
        results['dangerous_permissions'] = self.adb.check_dangerous_permissions()
        print(f"  ✓ Found {len(results['dangerous_permissions'])} apps with dangerous permissions")
        
        # Accessibility services
        print("  [6/12] Checking accessibility services...")
        self.delay()
        results['accessibility_services'] = self.adb.check_accessibility_services()
        print(f"  ✓ Found {len(results['accessibility_services'])} accessibility services")
        
        # Device admins
        print("  [7/12] Checking device admin apps...")
        self.delay()
        results['device_admins'] = self.adb.check_device_admins()
        print("  ✓ Device admin check completed")
        
        # Notification listeners
        print("  [8/12] Checking notification listeners...")
        self.delay()
        results['notification_listeners'] = self.adb.check_notification_listeners()
        print(f"  ✓ Found {len(results['notification_listeners'])} notification listeners")
        
        # Overlay permissions
        print("  [9/12] Checking overlay permissions...")
        self.delay()
        results['overlay_permissions'] = self.adb.check_overlay_permissions()
        print("  ✓ Overlay permissions checked")
        
        # Running processes
        print("  [10/12] Checking running processes...")
        self.delay(2)
        results['running_processes'] = self.adb.check_running_processes()
        print(f"  ✓ Process check completed")
        
        # VPN status
        print("  [11/12] Checking VPN/proxy status...")
        self.delay()
        results['vpn_status'] = self.adb.check_vpn_status()
        print("  ✓ VPN status checked")
        
        # Work profile
        print("  [12/12] Checking work profile/MDM...")
        self.delay()
        results['work_profile'] = self.adb.check_work_profile()
        print("  ✓ Work profile check completed")
        
        # Generate report
        print("\n  Generating ADB audit report...")
        report_file = self.adb.generate_report(results)
        print(f"  ✓ Report saved: {report_file}")
        
        self.audit_results['adb'] = results
        return True
    
    def run_deep_security_check(self) -> bool:
        """Run deep-level security checks"""
        self.print_section("DEEP-LEVEL SECURITY CHECK")
        
        if not self.get_user_confirmation("  Run deep-level security check?"):
            print("  Skipping deep security check...")
            return False
        
        print("\n  Running deep security checks...")
        print("  This may take several minutes...\n")
        
        results = {}
        
        # Kernel version
        print("  [1/10] Checking kernel version...")
        self.delay()
        results['kernel'] = self.deep_check.check_kernel_version()
        print("  ✓ Kernel version checked")
        
        # Bootloader
        print("  [2/10] Checking bootloader status...")
        self.delay()
        results['bootloader'] = self.deep_check.check_bootloader()
        print("  ✓ Bootloader status checked")
        
        # SELinux
        print("  [3/10] Checking SELinux status...")
        self.delay()
        results['selinux'] = self.deep_check.check_selinux()
        print(f"  ✓ SELinux: {results['selinux'].get('status', 'Unknown')}")
        
        # Processes
        print("  [4/10] Checking processes...")
        self.delay(2)
        results['processes'] = self.deep_check.check_processes()
        print(f"  ✓ Process check completed")
        
        # Network
        print("  [5/10] Checking network connections...")
        self.delay(2)
        results['network'] = self.deep_check.check_network_connections()
        print("  ✓ Network connections checked")
        
        # Baseband/Modem
        print("  [6/10] Checking baseband/modem...")
        self.delay()
        results['baseband_modem'] = self.deep_check.check_baseband_modem()
        print("  ✓ Baseband/modem checked")
        
        # Kernel modules
        print("  [7/10] Checking kernel modules...")
        self.delay()
        results['kernel_modules'] = self.deep_check.check_kernel_modules()
        print(f"  ✓ Found {results['kernel_modules'].get('module_count', 0)} modules")
        
        # System properties
        print("  [8/10] Checking system properties...")
        self.delay()
        results['system_properties'] = self.deep_check.check_system_properties()
        print("  ✓ System properties checked")
        
        # Filesystem
        print("  [9/10] Checking filesystem integrity...")
        self.delay()
        results['filesystem'] = self.deep_check.check_filesystem_integrity()
        print("  ✓ Filesystem check completed")
        
        # Tracing
        print("  [10/10] Checking tracing status...")
        self.delay()
        results['tracing'] = self.deep_check.check_tracing_status()
        print("  ✓ Tracing status checked")
        
        # Analyze findings
        print("\n  Analyzing findings...")
        analysis = self.deep_check.analyze_findings(results)
        results['analysis'] = analysis
        
        print(f"\n  Risk Assessment:")
        print(f"    High Risk: {len(analysis['high_risk'])}")
        print(f"    Medium Risk: {len(analysis['medium_risk'])}")
        print(f"    Low Risk: {len(analysis['low_risk'])}")
        
        # Generate report
        print("\n  Generating deep security report...")
        report_file = self.deep_check.generate_deep_report(results)
        print(f"  ✓ Report saved: {report_file}")
        
        self.audit_results['deep'] = results
        return True
    
    def run_mvt_analysis(self) -> bool:
        """Run MVT analysis for nation-state spyware detection"""
        self.print_section("MOBILE VERIFICATION TOOLKIT (MVT)")
        
        if not self.get_user_confirmation("  Run MVT analysis for nation-state spyware detection?"):
            print("  Skipping MVT analysis...")
            return False
        
        print("\n  MVT Analysis Setup")
        print("  This will check against 16+ threat intelligence feeds")
        print("  including Pegasus, Predator, and other known spyware\n")
        
        # Check MVT installation
        print("  [1/4] Checking MVT installation...")
        if not self.mvt.check_mvt_installed():
            print("  ✗ MVT not installed")
            if self.get_user_confirmation("  Install MVT now?"):
                success, message = self.mvt.install_mvt()
                if success:
                    print(f"  ✓ {message}")
                else:
                    print(f"  ✗ {message}")
                    return False
            else:
                return False
        else:
            print("  ✓ MVT is installed")
            print(f"  Version: {self.mvt.get_mvt_version()}")
        
        # Download indicators
        print("\n  [2/4] Downloading IOC indicators...")
        if not self.mvt.indicators_downloaded:
            success, message = self.mvt.download_indicators()
            if success:
                print(f"  ✓ {message}")
            else:
                print(f"  ✗ {message}")
                return False
        else:
            print("  ✓ IOC indicators already downloaded")
        
        # Generate bug report
        print("\n  [3/4] Generating Android bug report...")
        print("  This may take 1-2 minutes...")
        success, bugreport_file = self.mvt.generate_bugreport()
        if success:
            print(f"  ✓ Bug report generated: {bugreport_file}")
        else:
            print(f"  ✗ {bugreport_file}")
            return False
        
        # Run MVT analysis
        print("\n  [4/4] Running MVT analysis...")
        print("  This comprehensive analysis may take several minutes...")
        success, results_dir = self.mvt.run_mvt_analysis(bugreport_file)
        if success:
            print(f"  ✓ MVT analysis completed")
            print(f"  Results directory: {results_dir}")
        else:
            print(f"  ✗ {results_dir}")
            return False
        
        # Parse results
        print("\n  Parsing MVT results...")
        mvt_results = self.mvt.parse_mvt_results(results_dir)
        
        if 'error' not in mvt_results:
            print(f"\n  MVT Alert Summary:")
            for severity, count in mvt_results['severity_counts'].items():
                print(f"    {severity}: {count}")
            
            if mvt_results['matched_indicators']:
                print(f"\n  ⚠ INDICATORS OF COMPROMISE DETECTED!")
                print(f"  {len(mvt_results['matched_indicators'])} IOC matches found")
            else:
                print(f"\n  ✓ No indicators of compromise matched")
                print(f"  This is a GOOD sign - no known spyware detected")
        
        # Generate report
        print("\n  Generating MVT report...")
        report_file = self.mvt.generate_mvt_report(mvt_results)
        print(f"  ✓ Report saved: {report_file}")
        
        # Cleanup
        if self.get_user_confirmation("  Clean up temporary bug report file?"):
            self.mvt.cleanup(bugreport_file)
        
        self.audit_results['mvt'] = mvt_results
        return True
    
    def generate_final_report(self):
        """Generate final comprehensive report with consolidated findings"""
        self.print_section("FINAL REPORT")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"master_security_audit_{timestamp}.txt"
        json_filename = f"master_security_audit_{timestamp}.json"
        
        # Save JSON export for structured access
        import json
        with open(json_filename, 'w') as json_f:
            json.dump(self.audit_results, json_f, indent=2, default=str)
        print(f"  ✓ JSON export saved: {json_filename}")
        
        with open(filename, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("MASTER SECURITY AUDIT - FINAL REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("AUDIT SECTIONS COMPLETED:\n")
            f.write("-" * 70 + "\n")
            f.write(f"ADB Security Audit: {'✓' if 'adb' in self.audit_results else '✗'}\n")
            f.write(f"Deep-Level Security Check: {'✓' if 'deep' in self.audit_results else '✗'}\n")
            f.write(f"MVT Analysis: {'✓' if 'mvt' in self.audit_results else '✗'}\n\n")
            
            if 'adb' in self.audit_results:
                f.write("\nADB AUDIT SUMMARY:\n")
                f.write("-" * 70 + "\n")
                adb = self.audit_results['adb']
                f.write(f"Device Model: {adb.get('device_info', {}).get('model', 'Unknown')}\n")
                f.write(f"Android Version: {adb.get('device_info', {}).get('android_version', 'Unknown')}\n")
                f.write(f"Security Patch: {adb.get('device_info', {}).get('security_patch', 'Unknown')}\n")
                f.write(f"Total Packages: {len(adb.get('installed_packages', []))}\n")
                f.write(f"Sideloaded Apps: {len(adb.get('sideloaded_apps', {}))}\n")
                f.write(f"Dangerous Permissions: {len(adb.get('dangerous_permissions', {}))}\n")
                f.write(f"Accessibility Services: {len(adb.get('accessibility_services', []))}\n")
                f.write(f"Device Admins: {len(adb.get('device_admins', {}).get('active_admins', []))}\n")
                
                # Include detailed sideloaded apps
                if adb.get('sideloaded_apps'):
                    f.write("\nSIDELOADED APPS (non-Play Store):\n")
                    for pkg, installer in adb['sideloaded_apps'].items():
                        f.write(f"  - {pkg} (installer: {installer})\n")
                
                # Include apps with dangerous permissions
                if adb.get('dangerous_permissions'):
                    f.write("\nAPPS WITH DANGEROUS PERMISSIONS:\n")
                    for pkg, perms in adb['dangerous_permissions'].items():
                        f.write(f"  - {pkg}: {', '.join(perms)}\n")
            
            if 'deep' in self.audit_results:
                f.write("\nDEEP SECURITY CHECK SUMMARY:\n")
                f.write("-" * 70 + "\n")
                deep = self.audit_results['deep']
                analysis = deep.get('analysis', {})
                f.write(f"High Risk Issues: {len(analysis.get('high_risk', []))}\n")
                f.write(f"Medium Risk Issues: {len(analysis.get('medium_risk', []))}\n")
                f.write(f"Low Risk Issues: {len(analysis.get('low_risk', []))}\n")
                f.write(f"SELinux Status: {deep.get('selinux', {}).get('status', 'Unknown')}\n")
                f.write(f"Verified Boot: {deep.get('bootloader', {}).get('verified_boot', 'Unknown')}\n")
                f.write(f"Build Type: {deep.get('bootloader', {}).get('build_type', 'Unknown')}\n")
                f.write(f"dm-verity Mode: {deep.get('filesystem', {}).get('dm_verity_mode', 'Unknown')}\n")
                
                if analysis.get('high_risk'):
                    f.write("\nHIGH RISK FINDINGS:\n")
                    for risk in analysis['high_risk']:
                        f.write(f"  - {risk}\n")
                
                if analysis.get('medium_risk'):
                    f.write("\nMEDIUM RISK FINDINGS:\n")
                    for risk in analysis['medium_risk']:
                        f.write(f"  - {risk}\n")
            
            if 'mvt' in self.audit_results:
                f.write("\nMVT ANALYSIS SUMMARY:\n")
                f.write("-" * 70 + "\n")
                mvt = self.audit_results['mvt']
                if 'error' not in mvt:
                    f.write(f"Total Alerts: {mvt.get('total_alerts', 0)}\n")
                    for severity, count in mvt.get('severity_counts', {}).items():
                        f.write(f"{severity}: {count}\n")
                    
                    if mvt.get('matched_indicators'):
                        f.write("\n⚠ INDICATORS OF COMPROMISE DETECTED:\n")
                        for indicator in mvt['matched_indicators']:
                            f.write(f"  - Severity: {indicator.get('severity')}\n")
                            f.write(f"    Module: {indicator.get('module')}\n")
                            f.write(f"    Message: {indicator.get('message')}\n")
                    else:
                        f.write("\n✓ No indicators of compromise matched\n")
                        f.write("  This is a GOOD sign - no known spyware detected\n")
                else:
                    f.write(f"Error: {mvt.get('error', 'Unknown')}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("RECOMMENDATIONS:\n")
            f.write("-" * 70 + "\n")
            f.write("1. Review all HIGH and MEDIUM risk findings\n")
            f.write("2. Remove any unfamiliar or suspicious apps\n")
            f.write("3. Revoke unnecessary permissions\n")
            f.write("4. Keep device updated with security patches\n")
            f.write("5. Enable Google Play Protect\n")
            f.write("6. Avoid sideloading apps from untrusted sources\n")
            f.write("7. If IOC matches were found, seek professional help\n")
            f.write("   https://securitylab.amnesty.org/get-help/\n")
            f.write("=" * 70 + "\n")
            f.write(f"\nFull JSON data available in: {json_filename}\n")
        
        print(f"\n  ✓ Final report saved: {filename}")
        return filename
    
    def run_full_audit(self):
        """Run complete security audit with all modules"""
        self.print_banner()
        
        print("This tool will perform a comprehensive security audit of your Android device.")
        print("It includes:")
        print("  1. ADB-based security audit (apps, permissions, settings)")
        print("  2. Deep-level security check (kernel, SELinux, network, modem)")
        print("  3. MVT analysis (nation-state spyware detection)")
        print()
        
        if not self.get_user_confirmation("Proceed with full security audit?"):
            print("Audit cancelled by user.")
            return
        
        # Check ADB connection
        if not self.check_adb_connection():
            print("\n✗ Cannot proceed without ADB connection")
            print("Please fix connection issues and try again.")
            return
        
        # Run ADB audit
        self.run_adb_audit()
        
        # Run deep security check
        self.run_deep_security_check()
        
        # Run MVT analysis
        self.run_mvt_analysis()
        
        # Generate final report
        self.generate_final_report()
        
        self.print_section("AUDIT COMPLETE")
        print("All security checks have been completed.")
        print("Please review the generated reports for detailed findings.")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description=PROJECT_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=get_version_info()
    )
    
    parser.add_argument(
        '--about',
        action='store_true',
        help='Display detailed project information'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between ADB commands in seconds (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    if args.about:
        print(get_about_info())
        sys.exit(0)
    
    try:
        # Create manager with delay from args or prompt
        delay = args.delay
        if delay == 0.5:
            print("Configuration:")
            delay_input = input("  Enter delay between commands (seconds, default 0.5): ").strip()
            delay = float(delay_input) if delay_input else 0.5
        
        # Create manager
        manager = SecurityAuditManager(default_delay=delay)
        
        # Run full audit
        manager.run_full_audit()
        
    except KeyboardInterrupt:
        print("\n\nAudit interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
