#!/usr/bin/env python3
# =============================================================================
# Markush Audit
# Copyright (c) 2026 Purn Vadodariya
# Author: Purn Vadodariya
# GitHub: https://github.com/Thunder9954
# License: MIT
# =============================================================================

"""
ADB Commands Module
Handles all ADB-based security audit operations.
"""

import subprocess
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

from project_info import PROJECT_NAME, AUTHOR, EMAIL, GITHUB_URL


class ADBCommands:
    def __init__(self, delay: float = 0.5, output_dir: str = "."):
        self.delay = delay
        self.device_id = None
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_adb_command(self, command: str, capture_output: bool = True) -> str:
        """Run ADB command with delay and error handling"""
        time.sleep(self.delay)
        try:
            full_command = f"adb {command}"
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            if capture_output:
                return result.stdout + result.stderr
            return ""
        except subprocess.TimeoutExpired:
            return "ERROR: Command timed out"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def check_connection(self) -> Tuple[bool, str]:
        """Check ADB device connection"""
        output = self.run_adb_command("devices")
        lines = output.strip().split('\n')
        
        if len(lines) < 2:
            return False, "No devices found"
        
        for line in lines[1:]:
            if 'device' in line and 'unauthorized' not in line and 'offline' not in line:
                self.device_id = line.split()[0]
                return True, f"Device connected: {self.device_id}"
        
        return False, "Device not authorized or offline"
    
    def get_device_info(self) -> Dict:
        """Get basic device information"""
        info = {}
        
        # Get device model
        model = self.run_adb_command("shell getprop ro.product.model")
        info['model'] = model.strip()
        
        # Get Android version
        version = self.run_adb_command("shell getprop ro.build.version.release")
        info['android_version'] = version.strip()
        
        # Get security patch
        patch = self.run_adb_command("shell getprop ro.build.version.security_patch")
        info['security_patch'] = patch.strip()
        
        # Get build fingerprint
        fingerprint = self.run_adb_command("shell getprop ro.build.fingerprint")
        info['build_fingerprint'] = fingerprint.strip()
        
        return info
    
    def check_developer_settings(self) -> Dict:
        """Check developer and security settings"""
        settings = {}
        
        # USB debugging - correct property for actual USB debugging status
        usb_debug = self.run_adb_command("shell settings get global adb_enabled")
        settings['usb_debugging'] = usb_debug.strip()
        
        # Developer options enabled - different from USB debugging
        dev_options = self.run_adb_command("shell settings get global development_settings_enabled")
        settings['developer_options_enabled'] = dev_options.strip()
        
        # Unknown sources
        unknown_sources = self.run_adb_command("shell settings get secure install_non_market_apps")
        settings['unknown_sources'] = unknown_sources.strip()
        
        # Mock location
        mock_location = self.run_adb_command("shell settings get secure mock_location")
        settings['mock_location'] = mock_location.strip()
        
        return settings
    
    def get_installed_packages(self) -> List[str]:
        """Get list of all installed packages"""
        output = self.run_adb_command("shell pm list packages")
        packages = []
        for line in output.split('\n'):
            if line.startswith('package:'):
                pkg = line.replace('package:', '').strip()
                packages.append(pkg)
        return packages
    
    def get_sideloaded_apps(self) -> Dict[str, str]:
        """Get apps not installed from Play Store"""
        output = self.run_adb_command("shell pm list packages -i")
        sideloaded = {}
        
        for line in output.split('\n'):
            if 'installer=' in line:
                parts = line.split()
                pkg = parts[0].replace('package:', '')
                installer = None
                for part in parts:
                    if part.startswith('installer='):
                        installer = part.replace('installer=', '')
                        break
                
                if installer and installer != 'com.android.vending':
                    sideloaded[pkg] = installer
        
        return sideloaded
    
    def check_dangerous_permissions(self) -> Dict:
        """Check apps with dangerous permissions"""
        dangerous_perms = {
            'android.permission.CAMERA': 'CAMERA',
            'android.permission.RECORD_AUDIO': 'RECORD_AUDIO',
            'android.permission.ACCESS_FINE_LOCATION': 'FINE_LOCATION',
            'android.permission.ACCESS_BACKGROUND_LOCATION': 'BACKGROUND_LOCATION',
            'android.permission.READ_SMS': 'READ_SMS',
            'android.permission.READ_CALL_LOG': 'READ_CALL_LOG',
            'android.permission.READ_CONTACTS': 'READ_CONTACTS',
            'android.permission.READ_PHONE_STATE': 'READ_PHONE_STATE',
        }
        
        results = {}
        packages = self.get_installed_packages()
        
        for pkg in packages:
            if pkg.startswith('com.android') or pkg.startswith('com.google.android'):
                continue
                
            perm_output = self.run_adb_command(f"shell dumpsys package {pkg}")
            pkg_perms = []
            
            # Fixed: Parse per-line to match permission name with its granted state on the same line
            for line in perm_output.split('\n'):
                for perm_name, perm_display in dangerous_perms.items():
                    if perm_name in line and 'granted=true' in line.lower():
                        pkg_perms.append(perm_display)
            
            if pkg_perms:
                results[pkg] = pkg_perms
        
        return results
    
    def check_accessibility_services(self) -> List[str]:
        """Check enabled accessibility services"""
        output = self.run_adb_command("shell settings get secure enabled_accessibility_services")
        services = []
        if output.strip():
            services = output.strip().split(':')
        return services
    
    def check_device_admins(self) -> Dict:
        """Check device admin apps"""
        output = self.run_adb_command("shell dumpsys device_policy")
        admins = []
        
        if 'Active Device Admins:' in output or 'Enabled Device Admins' in output:
            lines = output.split('\n')
            for line in lines:
                if 'Admin' in line or 'admin' in line.lower():
                    admins.append(line.strip())
        
        return {'active_admins': admins}
    
    def check_notification_listeners(self) -> List[str]:
        """Check notification listener access"""
        output = self.run_adb_command("shell settings get secure enabled_notification_listeners")
        listeners = []
        if output.strip():
            listeners = output.strip().split(':')
        return listeners
    
    def check_overlay_permissions(self) -> List[str]:
        """Check apps with overlay permissions"""
        output = self.run_adb_command("shell dumpsys appops | grep -A 5 SYSTEM_ALERT_WINDOW")
        apps = []
        
        for line in output.split('\n'):
            if 'package:' in line.lower() or 'uid=' in line:
                apps.append(line.strip())
        
        return apps
    
    def check_running_processes(self) -> List[str]:
        """Check running processes"""
        output = self.run_adb_command("shell ps -A")
        processes = []
        
        for line in output.split('\n'):
            if line.strip() and not line.startswith('USER'):
                processes.append(line.strip())
        
        return processes
    
    def check_vpn_status(self) -> Dict:
        """Check VPN/proxy configuration"""
        output = self.run_adb_command("shell dumpsys connectivity")
        vpn_info = {'vpn_enabled': False, 'vpn_details': ''}
        
        if 'VPN' in output or 'VpnNetworkProvider' in output:
            vpn_info['vpn_enabled'] = True
            vpn_info['vpn_details'] = output
        
        return vpn_info
    
    def check_battery_anomalies(self) -> Dict:
        """Check battery stats for anomalies"""
        output = self.run_adb_command("shell dumpsys batterystats")
        return {'battery_stats': output[:1000]}  # Truncated for brevity
    
    def get_system_apps(self) -> List[str]:
        """Get system/OEM apps list"""
        output = self.run_adb_command("shell pm list packages -s")
        apps = []
        for line in output.split('\n'):
            if line.startswith('package:'):
                apps.append(line.replace('package:', '').strip())
        return apps
    
    def check_work_profile(self) -> Dict:
        """Check for work profile/MDM"""
        output = self.run_adb_command("shell pm list users")
        users = []
        
        for line in output.split('\n'):
            if 'UserInfo' in line or 'Profile' in line:
                users.append(line.strip())
        
        # Check device owner
        device_owner = self.run_adb_command("shell dumpsys device_policy | grep -i owner")
        
        return {'users': users, 'device_owner': device_owner}
    
    def generate_report(self, results: Dict) -> str:
        """Generate formatted report, saved inside self.output_dir"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"adb_audit_report_{timestamp}.txt")

        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("ADB SECURITY AUDIT REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for section, data in results.items():
                f.write(f"\n{section.upper()}\n")
                f.write("-" * 60 + "\n")
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(data, list):
                    for item in data:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{data}\n")
        
        return filename
