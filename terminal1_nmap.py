#!/usr/bin/env python3
"""
TERMINAL 1: Nmap Comprehensive Scanner
Performs 3-phase scanning: Quick, Full, and Targeted Vulnerability Scans
"""

import nmap
import sys
import json
import os
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class NmapScanner:
    def __init__(self, target, workspace="/tmp"):
        self.target = target
        self.workspace = workspace
        self.results_file = f"{workspace}/results/nmap_scan.json"
        self.nm = nmap.PortScanner()
        self.all_results = {
            'target': target,
            'scan_time': datetime.now().isoformat(),
            'phases': {}
        }
        
        print(f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════╗
║              TERMINAL 1: NMAP COMPREHENSIVE SCANNER              ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")
        print(f"{Colors.OKBLUE}Target:{Colors.ENDC} {target}")
        print(f"{Colors.OKBLUE}Workspace:{Colors.ENDC} {workspace}\n")
    
    def phase1_quick_scan(self):
        """Phase 1: Quick scan of top 1000 ports"""
        print(f"{Colors.BOLD}[PHASE 1] Quick Scan - Top 1000 Ports{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Command: nmap -sS -sV -O --top-ports 1000 --open -T4{Colors.ENDC}\n")
        
        try:
            self.nm.scan(self.target, arguments='-sS -sV -O --top-ports 1000 --open -T4 --min-rate 1000')
            results = self._parse_results('quick')
            self.all_results['phases']['quick_scan'] = results
            return results
        except Exception as e:
            print(f"{Colors.FAIL}[-] Quick scan failed: {e}{Colors.ENDC}")
            return {}
    
    def phase2_full_scan(self):
        """Phase 2: Full port scan all 65535 ports"""
        print(f"\n{Colors.BOLD}[PHASE 2] Full Port Scan - All 65535 Ports{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Command: nmap -sS -sV -p- --open -T4{Colors.ENDC}\n")
        
        try:
            self.nm.scan(self.target, arguments='-sS -sV -p- --open -T4 --min-rate 1000')
            results = self._parse_results('full')
            self.all_results['phases']['full_scan'] = results
            return results
        except Exception as e:
            print(f"{Colors.FAIL}[-] Full scan failed: {e}{Colors.ENDC}")
            return {}
    
    def phase3_vuln_scan(self):
        """Phase 3: Vulnerability scanning with NSE scripts"""
        print(f"\n{Colors.BOLD}[PHASE 3] Vulnerability Scan - NSE Scripts{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Command: nmap -sV --script vuln,exploit,auth,discovery -p {self._get_ports()}{Colors.ENDC}\n")
        
        ports = self._get_ports()
        if not ports:
            print(f"{Colors.WARNING}[!] No open ports found for vulnerability scanning{Colors.ENDC}")
            return {}
        
        try:
            port_str = ','.join(map(str, ports[:20]))  # Limit to first 20 ports
            self.nm.scan(self.target, ports=port_str, arguments='-sV --script vuln,exploit,auth,discovery -T4')
            results = self._parse_results('vuln')
            self.all_results['phases']['vuln_scan'] = results
            return results
        except Exception as e:
            print(f"{Colors.FAIL}[-] Vulnerability scan failed: {e}{Colors.ENDC}")
            return {}
    
    def _parse_results(self, phase):
        """Parse and display Nmap results"""
        results = {'hosts': {}, 'ports': [], 'services': []}
        
        for host in self.nm.all_hosts():
            hostname = self.nm[host].hostname() or "N/A"
            state = self.nm[host].state()
            
            print(f"{Colors.OKGREEN}[+] Host:{Colors.ENDC} {host} ({hostname})")
            print(f"{Colors.OKBLUE}    State:{Colors.ENDC} {state}")
            
            # OS Detection
            if 'osmatch' in self.nm[host] and self.nm[host]['osmatch']:
                for osmatch in self.nm[host]['osmatch'][:3]:
                    print(f"{Colors.OKBLUE}    OS:{Colors.ENDC} {osmatch['name']} ({osmatch['accuracy']}%)")
            
            results['hosts'][host] = {
                'hostname': hostname,
                'state': state,
                'os': [o['name'] for o in self.nm[host].get('osmatch', [])]
            }
            
            for proto in self.nm[host].all_protocols():
                ports = sorted(self.nm[host][proto].keys())
                for port in ports:
                    port_data = self.nm[host][proto][port]
                    service = port_data.get('name', 'unknown')
                    product = port_data.get('product', '')
                    version = port_data.get('version', '')
                    extrainfo = port_data.get('extrainfo', '')
                    
                    port_info = f"{port}/{proto}"
                    service_info = service
                    if product:
                        service_info += f" - {product}"
                    if version:
                        service_info += f" {version}"
                    if extrainfo:
                        service_info += f" ({extrainfo})"
                    
                    print(f"{Colors.OKGREEN}    [OPEN]{Colors.ENDC} {port_info:<12} {service_info}")
                    
                    port_entry = {
                        'port': port,
                        'protocol': proto,
                        'service': service,
                        'product': product,
                        'version': version,
                        'extrainfo': extrainfo
                    }
                    results['ports'].append(port_entry)
                    
                    # Check for scripts output
                    if 'script' in port_data:
                        for script_name, output in port_data['script'].items():
                            if 'VULNERABLE' in str(output) or 'CVE' in str(output):
                                print(f"{Colors.FAIL}    [!] VULNERABILITY:{Colors.ENDC} {script_name}")
                                print(f"        {output[:200]}...")
                                results['services'].append({
                                    'type': 'vulnerability',
                                    'port': port,
                                    'script': script_name,
                                    'output': output
                                })
        
        return results
    
    def _get_ports(self):
        """Extract unique ports from scan results"""
        ports = set()
        for phase_results in self.all_results['phases'].values():
            if 'ports' in phase_results:
                for p in phase_results['ports']:
                    ports.add(p['port'])
        return sorted(list(ports))
    
    def save_results(self):
        """Save results to JSON file"""
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump(self.all_results, f, indent=2)
        print(f"\n{Colors.OKGREEN}[+] Results saved to: {self.results_file}{Colors.ENDC}")
        
        # Also save as text summary
        text_file = self.results_file.replace('.json', '.txt')
        with open(text_file, 'w') as f:
            f.write(f"NMAP SCAN RESULTS FOR {self.target}\n")
            f.write(f"Time: {self.all_results['scan_time']}\n")
            f.write("="*60 + "\n\n")
            
            for phase, data in self.all_results['phases'].items():
                f.write(f"\n{phase.upper()}:\n")
                f.write("-"*40 + "\n")
                for host, host_data in data.get('hosts', {}).items():
                    f.write(f"Host: {host}\n")
                for port in data.get('ports', []):
                    f.write(f"  {port['port']}/{port['protocol']} - {port['service']}\n")
        
        print(f"{Colors.OKGREEN}[+] Summary saved to: {text_file}{Colors.ENDC}")
    
    def run(self):
        """Execute all scan phases"""
        print(f"{Colors.OKBLUE}[*] Starting 3-phase Nmap scanning...{Colors.ENDC}\n")
        
        # Phase 1: Quick
        self.phase1_quick_scan()
        
        # Phase 2: Full
        self.phase2_full_scan()
        
        # Phase 3: Vulnerability
        self.phase3_vuln_scan()
        
        # Save results
        self.save_results()
        
        # Summary
        total_ports = len(self._get_ports())
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}SCAN COMPLETE{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+] Total Open Ports Found: {total_ports}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Results: {self.results_file}{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Terminal 1 finished - Waiting for other terminals...{Colors.ENDC}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: terminal1_nmap.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    workspace = sys.argv[2] if len(sys.argv) > 2 else "/tmp"
    
    scanner = NmapScanner(target, workspace)
    scanner.run()


if __name__ == '__main__':
    main()
