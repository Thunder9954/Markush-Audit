#!/usr/bin/env python3
"""
MVT (Mobile Verification Toolkit) Module
Handles MVT integration for nation-state spyware detection
"""

import subprocess
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class MVTIntegration:
    def __init__(self, delay: float = 0.5, venv_path: str = "python-pip", output_dir: str = "."):
        self.delay = delay
        self.venv_path = venv_path
        self.mvt_installed = False
        self.indicators_downloaded = False
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_command(self, command: str, capture_output: bool = True, executable: str = None, timeout: int = 120) -> Tuple[int, str]:
        """Run shell command with delay and error handling. Returns (returncode, output)."""
        time.sleep(self.delay)
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                executable=executable
            )
            if capture_output:
                return result.returncode, result.stdout + result.stderr
            return result.returncode, ""
        except subprocess.TimeoutExpired:
            return -1, "ERROR: Command timed out"
        except Exception as e:
            return -1, f"ERROR: {str(e)}"
    
    def check_mvt_installed(self) -> bool:
        """Check if MVT is installed"""
        try:
            # Check if mvt-android command exists - use POSIX-compatible '.' instead of bash-specific 'source'
            returncode, result = self.run_command(f". {self.venv_path}/bin/activate && which mvt-android", executable="/bin/bash")
            if returncode == 0 and "mvt-android" in result and "not found" not in result:
                self.mvt_installed = True
                return True
            
            # Alternative check via pip
            returncode, pip_check = self.run_command(f". {self.venv_path}/bin/activate && pip list | grep mvt", executable="/bin/bash")
            if returncode == 0 and "mvt" in pip_check.lower():
                self.mvt_installed = True
                return True
                
            return False
        except Exception:
            return False
    
    def install_mvt(self) -> Tuple[bool, str]:
        """Install MVT using pip in virtual environment"""
        print("Installing MVT (Mobile Verification Toolkit)...")
        print("This may take a few minutes...")
        
        try:
            # Create virtual environment if it doesn't exist
            if not os.path.exists(self.venv_path):
                returncode, venv_create = self.run_command(f"python3 -m venv {self.venv_path}")
                if returncode != 0:
                    return False, f"Failed to create virtual environment: {venv_create}"
            
            # Install MVT - use POSIX-compatible '.'
            install_cmd = f". {self.venv_path}/bin/activate && pip install mvt"
            returncode, result = self.run_command(install_cmd, executable="/bin/bash")
            
            if returncode != 0:
                return False, f"Installation failed (returncode {returncode}): {result}"
            
            self.mvt_installed = True
            return True, "MVT installed successfully"
            
        except Exception as e:
            return False, f"Installation error: {str(e)}"
    
    def download_indicators(self) -> Tuple[bool, str]:
        """Download IOC indicators for MVT"""
        if not self.mvt_installed:
            return False, "MVT not installed"
        
        print("Downloading IOC indicators (this may take a moment)...")
        
        try:
            download_cmd = f". {self.venv_path}/bin/activate && mvt-android download-iocs"
            returncode, result = self.run_command(download_cmd, executable="/bin/bash")
            
            if returncode != 0:
                return False, f"Failed to download indicators (returncode {returncode}): {result}"
            
            self.indicators_downloaded = True
            return True, "IOC indicators downloaded successfully"
            
        except Exception as e:
            return False, f"Download error: {str(e)}"
    
    def generate_bugreport(self) -> Tuple[bool, str]:
        """Generate Android bug report for MVT analysis"""
        print("Generating Android bug report...")
        print("This may take 1-2 minutes...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"bugreport_{timestamp}.zip")

            # Generate bug report with extended timeout (5 minutes) and user warning
            print("  IMPORTANT: Keep your phone screen ON and UNLOCKED during bug report generation")
            print("  This may take 2-5 minutes depending on your device...")

            bugreport_cmd = f"adb bugreport {filename}"
            returncode, result = self.run_command(bugreport_cmd, timeout=300)
            
            if returncode != 0 or "pulled" not in result.lower():
                return False, f"Failed to generate bug report (returncode {returncode}): {result}"
            
            return True, filename
            
        except Exception as e:
            return False, f"Bug report generation error: {str(e)}"
    
    def run_mvt_analysis(self, bugreport_path: str, output_dir: str = None) -> Tuple[bool, str]:
        """Run MVT analysis against bug report. Results land inside self.output_dir
        (i.e. this run's folder) unless a different output_dir is explicitly passed."""
        if not self.mvt_installed:
            return False, "MVT not installed"

        if not self.indicators_downloaded:
            return False, "IOC indicators not downloaded"

        if output_dir is None:
            output_dir = os.path.join(self.output_dir, "mvt_results")

        print(f"Running MVT analysis on {bugreport_path}...")
        print("This comprehensive analysis may take several minutes...")

        try:
            # Create output directory
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Run MVT analysis - use POSIX-compatible '.' with extended timeout
            analysis_cmd = f". {self.venv_path}/bin/activate && mvt-android check-bugreport -o {output_dir} {bugreport_path}"
            returncode, result = self.run_command(analysis_cmd, executable="/bin/bash", timeout=300)
            
            if returncode != 0:
                return False, f"MVT analysis failed (returncode {returncode}): {result}"
            
            return True, output_dir
            
        except Exception as e:
            return False, f"Analysis error: {str(e)}"
    
    def parse_mvt_results(self, results_dir: str) -> Dict:
        """Parse MVT analysis results"""
        alerts_file = os.path.join(results_dir, "alerts.json")
        
        if not os.path.exists(alerts_file):
            return {'error': 'Alerts file not found'}
        
        try:
            with open(alerts_file, 'r') as f:
                alerts = json.load(f)
            
            # Count alerts by severity
            severity_counts = {
                'CRITICAL': 0,
                'HIGH': 0,
                'MEDIUM': 0,
                'LOW': 0,
                'INFORMATIONAL': 0
            }
            
            for alert in alerts:
                severity = alert.get('level', 'UNKNOWN')
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            # Extract matched indicators
            matched_indicators = []
            for alert in alerts:
                if alert.get('matched_indicator'):
                    matched_indicators.append({
                        'severity': alert.get('level'),
                        'indicator': alert.get('matched_indicator'),
                        'module': alert.get('module'),
                        'message': alert.get('message')
                    })
            
            return {
                'total_alerts': len(alerts),
                'severity_counts': severity_counts,
                'matched_indicators': matched_indicators,
                'alerts': alerts
            }
            
        except Exception as e:
            return {'error': f'Failed to parse results: {str(e)}'}
    
    def get_mvt_version(self) -> str:
        """Get MVT version"""
        if not self.mvt_installed:
            return "MVT not installed"
        
        try:
            version_cmd = f". {self.venv_path}/bin/activate && mvt-android version"
            returncode, result = self.run_command(version_cmd, executable="/bin/bash")
            return result.strip()
        except Exception as e:
            return f"Error getting version: {str(e)}"
    
    def list_available_modules(self) -> List[str]:
        """List available MVT modules"""
        if not self.mvt_installed:
            return []
        
        try:
            modules_cmd = f". {self.venv_path}/bin/activate && mvt-android check-bugreport --list-modules"
            returncode, result = self.run_command(modules_cmd, executable="/bin/bash")
            
            modules = []
            for line in result.split('\n'):
                if line.strip() and not line.startswith('Usage') and 'MVT' not in line:
                    modules.append(line.strip())
            
            return modules
        except Exception as e:
            return []
    
    def generate_mvt_report(self, results: Dict, output_file: str = None) -> str:
        """Generate formatted MVT report, saved inside self.output_dir"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir, f"mvt_report_{timestamp}.txt")

        with open(output_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("MOBILE VERIFICATION TOOLKIT (MVT) REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            if 'error' in results:
                f.write(f"ERROR: {results['error']}\n")
                return output_file
            
            f.write("SUMMARY\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total Alerts: {results['total_alerts']}\n\n")
            
            f.write("ALERTS BY SEVERITY\n")
            f.write("-" * 60 + "\n")
            for severity, count in results['severity_counts'].items():
                f.write(f"{severity}: {count}\n")
            
            f.write("\nMATCHED INDICATORS (IOC HITS)\n")
            f.write("-" * 60 + "\n")
            if results['matched_indicators']:
                for indicator in results['matched_indicators']:
                    f.write(f"Severity: {indicator['severity']}\n")
                    f.write(f"Module: {indicator['module']}\n")
                    f.write(f"Message: {indicator['message']}\n")
                    f.write(f"Indicator: {indicator['indicator']}\n\n")
            else:
                f.write("No indicators of compromise matched.\n")
                f.write("This is a GOOD sign - no known spyware detected.\n")
            
            f.write("\nDETAILED ALERTS\n")
            f.write("-" * 60 + "\n")
            for alert in results['alerts']:
                f.write(f"Severity: {alert.get('level')}\n")
                f.write(f"Module: {alert.get('module')}\n")
                f.write(f"Message: {alert.get('message')}\n")
                f.write(f"Time: {alert.get('event_time')}\n\n")
        
        return output_file
    
    def cleanup(self, bugreport_path: str = None):
        """Clean up temporary files"""
        if bugreport_path and os.path.exists(bugreport_path):
            try:
                os.remove(bugreport_path)
                print(f"Cleaned up: {bugreport_path}")
            except Exception as e:
                print(f"Failed to cleanup {bugreport_path}: {str(e)}")
