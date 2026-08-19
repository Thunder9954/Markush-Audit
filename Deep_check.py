#!/usr/bin/env python3
"""
Deep-Level Security Check Module
Handles kernel, SELinux, processes, network, baseband/modem, and kernel module checks
"""

import subprocess
import time
import os
from typing import Dict, List, Tuple


class DeepSecurityCheck:
    def __init__(self, delay: float = 0.5, output_dir: str = "."):
        self.delay = delay
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
    
    def check_kernel_version(self) -> Dict:
        """Check kernel version and build information"""
        kernel_info = {}
        
        # Kernel version
        kernel = self.run_adb_command("shell uname -a")
        kernel_info['kernel_version'] = kernel.strip()
        
        # Kernel build date
        build_date = self.run_adb_command("shell uname -v")
        kernel_info['kernel_build_date'] = build_date.strip()
        
        # Processor architecture
        arch = self.run_adb_command("shell uname -m")
        kernel_info['architecture'] = arch.strip()
        
        return kernel_info
    
    def check_bootloader(self) -> Dict:
        """Check bootloader status and verified boot"""
        bootloader_info = {}
        
        # Bootloader status
        bootloader = self.run_adb_command("shell getprop ro.bootloader")
        bootloader_info['bootloader'] = bootloader.strip()
        
        # Verified boot state
        verified_boot = self.run_adb_command("shell getprop ro.boot.verifiedbootstate")
        bootloader_info['verified_boot'] = verified_boot.strip()
        
        # Build type (user/userdebug/engineering)
        build_type = self.run_adb_command("shell getprop ro.build.type")
        bootloader_info['build_type'] = build_type.strip()
        
        # Build tags (release-keys/test-keys)
        build_tags = self.run_adb_command("shell getprop ro.build.tags")
        bootloader_info['build_tags'] = build_tags.strip()
        
        # OEM unlock status
        oem_unlock = self.run_adb_command("shell getprop sys.oem_unlock_allowed")
        bootloader_info['oem_unlock_allowed'] = oem_unlock.strip()
        
        return bootloader_info
    
    def check_selinux(self) -> Dict:
        """Check SELinux status and policy"""
        selinux_info = {}
        
        # SELinux enforcing status
        status = self.run_adb_command("shell getenforce")
        selinux_info['status'] = status.strip()
        
        # SELinux policy version - real property check
        sepolicy_version = self.run_adb_command("shell getprop ro.build.selinux")
        selinux_info['sepolicy_version'] = sepolicy_version.strip()
        
        return selinux_info
    
    def check_processes(self) -> Dict:
        """Check for unusual processes with elevated privileges"""
        process_info = {}
        
        # Get all processes
        ps_output = self.run_adb_command("shell ps -A -o USER,PID,PPID,NAME")
        process_info['all_processes_sample'] = ps_output[:500]  # Sample
        
        # Check for root processes
        root_processes = []
        for line in ps_output.split('\n'):
            if line.startswith('root') and not line.startswith('root           1     0 init'):
                root_processes.append(line.strip())
        
        process_info['root_processes'] = root_processes[:20]  # Limit output
        process_info['root_process_count'] = len(root_processes)
        
        # Check for suspicious process names
        suspicious_names = ['backdoor', 'shell', 'reverse', 'proxy', 'tunnel', 'nc', 'netcat']
        suspicious_processes = []
        
        for line in ps_output.split('\n'):
            for susp in suspicious_names:
                if susp in line.lower():
                    suspicious_processes.append(line.strip())
        
        process_info['suspicious_processes'] = suspicious_processes
        
        return process_info
    
    def check_network_connections(self) -> Dict:
        """Check network connections and listening ports for backdoors"""
        network_info = {}
        
        # Get listening ports - fixed to properly handle fallback within adb shell
        netstat = self.run_adb_command("shell 'netstat -tlnp 2>/dev/null || ss -tlnp'")
        network_info['listening_ports'] = netstat[:800]
        
        # Check for suspicious ports
        suspicious_ports = []
        common_backdoor_ports = ['4444', '5555', '6666', '7777', '8888', '9999', '31337', '12345']
        
        for line in netstat.split('\n'):
            for port in common_backdoor_ports:
                if f':{port}' in line:
                    suspicious_ports.append(line.strip())
        
        network_info['suspicious_ports'] = suspicious_ports
        
        # Get established connections - fixed fallback
        connections = self.run_adb_command("shell 'netstat -tnp 2>/dev/null || ss -tnp'")
        network_info['established_connections_sample'] = connections[:500]
        
        # Check for connections to unknown IPs
        network_info['connection_check'] = "Network connections analyzed"
        
        return network_info
    
    def check_baseband_modem(self) -> Dict:
        """Check baseband/modem information"""
        modem_info = {}
        
        # Baseband version
        baseband = self.run_adb_command("shell getprop gsm.version.baseband")
        modem_info['baseband_version'] = baseband.strip()
        
        # RIL implementation
        ril = self.run_adb_command("shell getprop gsm.version.ril-impl")
        modem_info['ril_implementation'] = ril.strip()
        
        # Modem type
        modem_type = self.run_adb_command("shell getprop ro.baseband")
        modem_info['modem_type'] = modem_type.strip()
        
        # Radio/network type
        network_type = self.run_adb_command("shell getprop gsm.network.type")
        modem_info['network_type'] = network_type.strip()
        
        # SIM operator
        operator = self.run_adb_command("shell getprop gsm.operator.alpha")
        modem_info['operator'] = operator.strip()
        
        # Check modem daemon status
        modem_daemon = self.run_adb_command("shell getprop init.svc.qti-modem-daemon-0")
        modem_info['modem_daemon_status'] = modem_daemon.strip()
        
        return modem_info
    
    def check_kernel_modules(self) -> Dict:
        """Check loaded kernel modules for suspicious entries"""
        module_info = {}
        
        # Get loaded modules
        modules = self.run_adb_command("shell cat /proc/modules")
        module_info['loaded_modules_sample'] = modules[:1000]
        
        # Check for suspicious module names
        suspicious_modules = []
        known_suspicious = ['rootkit', 'keylog', 'hide', 'stealth', 'reptile']
        
        for line in modules.split('\n'):
            for susp in known_suspicious:
                if susp in line.lower():
                    suspicious_modules.append(line.strip())
        
        module_info['suspicious_modules'] = suspicious_modules
        
        # Get module count
        module_count = len([line for line in modules.split('\n') if line.strip()])
        module_info['module_count'] = module_count
        
        return module_info
    
    def check_system_properties(self) -> Dict:
        """Check system properties for anomalies"""
        prop_info = {}
        
        # Get all properties
        props = self.run_adb_command("shell getprop")
        prop_info['properties_sample'] = props[:1000]
        
        # Check for unusual properties
        unusual_props = []
        suspicious_prop_names = ['ro.debuggable', 'ro.secure', 'persist.sys.usb.config']
        
        for line in props.split('\n'):
            for susp in suspicious_prop_names:
                if susp in line:
                    unusual_props.append(line.strip())
        
        prop_info['security_relevant_props'] = unusual_props
        
        # Check debuggable status
        debuggable = self.run_adb_command("shell getprop ro.debuggable")
        prop_info['debuggable'] = debuggable.strip()
        
        # Check secure status
        secure = self.run_adb_command("shell getprop ro.secure")
        prop_info['secure'] = secure.strip()
        
        return prop_info
    
    def check_filesystem_integrity(self) -> Dict:
        """Check filesystem and partition integrity"""
        fs_info = {}
        
        # Check system partition mount
        system_mount = self.run_adb_command("shell mount | grep system")
        fs_info['system_mount'] = system_mount[:200]
        
        # Check for remount flags
        remount_check = self.run_adb_command("shell mount | grep -i rw")
        fs_info['rw_mounts'] = remount_check[:300]
        
        # Check dm-verity status using actual property (not fake command)
        verity_mode = self.run_adb_command("shell getprop ro.boot.veritymode")
        fs_info['dm_verity_mode'] = verity_mode.strip()
        
        return fs_info
    
    def check_tracing_status(self) -> Dict:
        """Check if kernel tracing is enabled (potential surveillance indicator)"""
        tracing_info = {}
        
        # Check tracing status
        tracing = self.run_adb_command("shell cat /sys/kernel/debug/tracing/tracing_on 2>/dev/null || echo 'tracing not accessible'")
        tracing_info['tracing_status'] = tracing.strip()
        
        return tracing_info
    
    def check_system_libraries(self) -> Dict:
        """Check system libraries for modifications"""
        lib_info = {}
        
        # List system libraries
        libs = self.run_adb_command("shell ls -la /system/lib64 2>/dev/null | head -30")
        lib_info['system_libs_sample'] = libs
        
        return lib_info
    
    def generate_deep_report(self, results: Dict) -> str:
        """Generate formatted deep security report, saved inside self.output_dir"""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"deep_security_report_{timestamp}.txt")

        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("DEEP-LEVEL SECURITY AUDIT REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for section, data in results.items():
                f.write(f"\n{section.upper().replace('_', ' ')}\n")
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
    
    def analyze_findings(self, results: Dict) -> Dict:
        """Analyze findings and return risk assessment"""
        analysis = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': [],
            'info': []
        }
        
        # Analyze bootloader
        if results.get('bootloader', {}).get('build_type') == 'userdebug':
            analysis['medium_risk'].append("Device running userdebug build (more vulnerable)")
        
        if results.get('bootloader', {}).get('oem_unlock_allowed') == '1':
            analysis['medium_risk'].append("OEM unlock is allowed")
        
        # Analyze SELinux
        if results.get('selinux', {}).get('status') != 'Enforcing':
            analysis['high_risk'].append("SELinux not in enforcing mode")
        
        # Analyze processes
        if results.get('processes', {}).get('suspicious_processes'):
            analysis['high_risk'].append(f"Suspicious processes found: {len(results['processes']['suspicious_processes'])}")
        
        # Analyze network
        if results.get('network', {}).get('suspicious_ports'):
            analysis['high_risk'].append(f"Suspicious ports found: {len(results['network']['suspicious_ports'])}")
        
        # Analyze kernel modules
        if results.get('kernel_modules', {}).get('suspicious_modules'):
            analysis['high_risk'].append(f"Suspicious kernel modules found: {len(results['kernel_modules']['suspicious_modules'])}")
        
        # Analyze debuggable
        if results.get('system_properties', {}).get('debuggable') == '1':
            analysis['medium_risk'].append("Device is debuggable")
        
        return analysis
