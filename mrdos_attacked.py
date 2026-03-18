#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ███╗██████╗ ██████╗  ██████╗ ███████╗                             ║
║   ████╗ ████║██╔══██╗██╔══██╗██╔═══██╗██╔════╝                             ║
║   ██╔████╔██║██████╔╝██║  ██║██║   ██║███████╗                             ║
║   ██║╚██╔╝██║██╔══██╗██║  ██║██║   ██║╚════██║                             ║
║   ██║ ╚═╝ ██║██║  ██║██████╔╝╚██████╔╝███████║                             ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝                             ║
║                                                                              ║
║                    PENETRATION TESTING FRAMEWORK v2.0                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

    AUTHORIZED PENETRATION TESTING TOOL
    =====================================
    
    ⚠️  WARNING: This tool is for authorized security testing only!
    
    By using this tool, you confirm that:
    ✓ You have explicit written permission to test the target
    ✓ You are the owner of the target system, OR
    ✓ You have a signed contract/authorization for penetration testing
    ✓ You understand that unauthorized access is illegal
    
    The author assumes NO liability for misuse of this tool.
    
    Press Ctrl+C within 5 seconds to cancel if you don't have permission...
"""

import os
import sys
import json
import time
import socket
import subprocess
import http.server
import socketserver
import webbrowser
import threading
from datetime import datetime
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class MrDosAttacked:
    def __init__(self, target):
        self.target = target
        self.workspace = f"/tmp/mrdos_{target.replace('.', '_')}"
        self.start_time = datetime.now()
        self.web_port = 8888
        self.results = {
            'tool': 'MrDos Attacked',
            'version': '2.0',
            'target': target,
            'start_time': self.start_time.isoformat(),
            'workspace': self.workspace,
            'terminals': {},
            'vulnerabilities': [],
            'status': 'running'
        }
        
        # Create workspace
        os.makedirs(self.workspace, exist_ok=True)
        os.makedirs(f"{self.workspace}/results", exist_ok=True)
        os.makedirs(f"{self.workspace}/logs", exist_ok=True)
        os.makedirs(f"{self.workspace}/web", exist_ok=True)
        
        self._print_banner()
        
    def _print_banner(self):
        banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ███╗██████╗ ██████╗  ██████╗ ███████╗                             ║
║   ████╗ ████║██╔══██╗██╔══██╗██╔═══██╗██╔════╝                             ║
║   ██╔████╔██║██████╔╝██║  ██║██║   ██║███████╗                             ║
║   ██║╚██╔╝██║██╔══██╗██║  ██║██║   ██║╚════██║                             ║
║   ██║ ╚═╝ ██║██║  ██║██████╔╝╚██████╔╝███████║                             ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝                             ║
║                                                                              ║
║                    PENETRATION TESTING FRAMEWORK v2.0                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.WARNING}⚠️  AUTHORIZED USE ONLY{Colors.ENDC}
{Colors.OKBLUE}Target:{Colors.ENDC} {self.target}
{Colors.OKBLUE}Workspace:{Colors.ENDC} {self.workspace}
{Colors.OKBLUE}Web Dashboard:{Colors.ENDC} http://localhost:{self.web_port}
{Colors.OKBLUE}Start Time:{Colors.ENDC} {self.start_time}
"""
        print(banner)
    
    def launch_terminal(self, term_id, title, command):
        """Launch a terminal with specific command"""
        log_file = f"{self.workspace}/logs/terminal_{term_id}.log"
        
        terminal_cmds = [
            f"gnome-terminal --title='{title}' -- bash -c 'echo -e \"\\033[95m=== {title} ===\\033[0m\\n\"; {command} 2>&1 | tee {log_file}; exec bash'",
            f"xfce4-terminal --title='{title}' -e 'bash -c \"echo -e \\\"\\033[95m=== {title} ===\\033[0m\\n\\\"; {command} 2>&1 | tee {log_file}; exec bash\"'",
            f"konsole --new-tab -p tabtitle='{title}' -e bash -c 'echo -e \"\\033[95m=== {title} ===\\033[0m\\n\"; {command} 2>&1 | tee {log_file}; exec bash'",
            f"xterm -title '{title}' -e bash -c 'echo -e \"\\033[95m=== {title} ===\\033[0m\\n\"; {command} 2>&1 | tee {log_file}; exec bash'"
        ]
        
        for term_cmd in terminal_cmds:
            try:
                result = subprocess.run(term_cmd, shell=True, capture_output=True, timeout=5)
                if result.returncode == 0:
                    self.results['terminals'][term_id] = {'title': title, 'log': log_file, 'status': 'running'}
                    print(f"{Colors.OKGREEN}[+] Terminal {term_id} launched: {title}{Colors.ENDC}")
                    return True
            except:
                continue
        
        # Fallback
        bg_cmd = f"nohup bash -c '{command}' > {log_file} 2>&1 &"
        os.system(bg_cmd)
        self.results['terminals'][term_id] = {'title': title, 'log': log_file, 'status': 'background'}
        print(f"{Colors.WARNING}[!] Terminal {term_id} in background: {title}{Colors.ENDC}")
        return True
    
    def start_web_dashboard(self):
        """Start web dashboard for results"""
        dashboard_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>MrDos Attacked - Pentest Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; margin: 0; padding: 20px; }}
        .header {{ text-align: center; border: 2px solid #00ff00; padding: 20px; margin-bottom: 20px; }}
        .terminal {{ border: 1px solid #00ff00; margin: 10px 0; padding: 15px; background: #111; }}
        .status-running {{ color: #ffff00; }}
        .status-complete {{ color: #00ff00; }}
        .status-error {{ color: #ff0000; }}
        .vuln-critical {{ color: #ff0000; font-weight: bold; }}
        .vuln-high {{ color: #ff6600; }}
        .vuln-medium {{ color: #ffff00; }}
        pre {{ background: #000; padding: 10px; overflow-x: auto; }}
        h1, h2 {{ color: #00ff00; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>☠️ MrDos Attacked ☠️</h1>
        <h2>Penetration Testing Framework v2.0</h2>
        <p>Target: <strong>{self.target}</strong> | Started: {self.start_time}</p>
        <p>⚠️ AUTHORIZED TESTING ONLY - All activities logged</p>
    </div>
    
    <div class="grid">
        <div class="terminal">
            <h2>🖥️ Terminal Status</h2>
            <div id="terminals">
                <p class="status-running">⏳ Loading terminal status...</p>
            </div>
        </div>
        
        <div class="terminal">
            <h2>🎯 Vulnerabilities</h2>
            <div id="vulns">
                <p>Scanning in progress...</p>
            </div>
        </div>
    </div>
    
    <div class="terminal">
        <h2>📊 Live Logs</h2>
        <pre id="logs">Waiting for scan data...</pre>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds
        setInterval(function() {{
            location.reload();
        }}, 5000);
    </script>
</body>
</html>"""
        
        dashboard_path = f"{self.workspace}/web/index.html"
        with open(dashboard_path, 'w') as f:
            f.write(dashboard_html)
        
        # Start simple HTTP server
        os.chdir(f"{self.workspace}/web")
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", self.web_port), handler)
        
        def serve():
            httpd.serve_forever()
        
        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        
        print(f"{Colors.OKGREEN}[+] Web Dashboard started: http://localhost:{self.web_port}{Colors.ENDC}")
        
        # Try to open browser
        try:
            webbrowser.open(f"http://localhost:{self.web_port}")
        except:
            pass
    
    def run_orchestrated_attack(self):
        """Launch all 5 terminals with coordinated attacks"""
        print(f"\n{Colors.BOLD}Launching 5-Terminal Attack Sequence...{Colors.ENDC}\n")
        
        # Terminal 1: Nmap Scanner
        self.launch_terminal(1, "T1: NMAP SCANNER", 
            f"python3 /home/user/terminal1_nmap.py '{self.target}' '{self.workspace}'")
        time.sleep(2)
        
        # Terminal 2: SQL Injection
        self.launch_terminal(2, "T2: SQL INJECTION",
            f"python3 /home/user/terminal2_sql.py '{self.target}' '{self.workspace}'")
        time.sleep(2)
        
        # Terminal 3: RCE Testing
        self.launch_terminal(3, "T3: RCE TESTING",
            f"python3 /home/user/terminal3_rce.py '{self.target}' '{self.workspace}'")
        time.sleep(2)
        
        # Terminal 4: SSRF Testing
        self.launch_terminal(4, "T4: SSRF TESTING",
            f"python3 /home/user/terminal4_ssrf.py '{self.target}' '{self.workspace}'")
        time.sleep(2)
        
        # Terminal 5: API & XSS
        self.launch_terminal(5, "T5: API & XSS",
            f"python3 /home/user/terminal5_api_xss.py '{self.target}' '{self.workspace}'")
        
        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}All 5 terminals launched successfully!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")
        
        print(f"{Colors.OKBLUE}Terminal Status:{Colors.ENDC}")
        for term_id, info in self.results['terminals'].items():
            print(f"  Terminal {term_id}: {info['title']}")
            print(f"    Log: {info['log']}")
        
        print(f"\n{Colors.WARNING}Monitor Commands:{Colors.ENDC}")
        print(f"  tail -f {self.workspace}/logs/terminal_*.log")
        print(f"  watch -n 2 'ls -la {self.workspace}/results/'")
        
        print(f"\n{Colors.OKCYAN}Workspace: {self.workspace}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Results: {self.workspace}/results/{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Dashboard: http://localhost:{self.web_port}{Colors.ENDC}\n")
        
        # Keep main script running
        print(f"{Colors.BOLD}Press Ctrl+C to stop the orchestrator...{Colors.ENDC}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[!] Stopping orchestrator...{Colors.ENDC}")
            self.generate_final_report()
    
    def generate_final_report(self):
        """Generate final HTML report"""
        report_file = f"{self.workspace}/web/final_report.html"
        
        # Collect all results
        all_vulns = []
        for result_file in os.listdir(f"{self.workspace}/results"):
            if result_file.endswith('.json'):
                try:
                    with open(f"{self.workspace}/results/{result_file}") as f:
                        data = json.load(f)
                        if 'vulns' in data:
                            all_vulns.extend(data['vulns'])
                        elif 'vulnerabilities' in data:
                            all_vulns.extend(data['vulnerabilities'])
                except:
                    pass
        
        # Generate HTML report
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>MrDos Attacked - Final Report</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; margin: 0; padding: 20px; }}
        .header {{ text-align: center; border: 3px solid #00ff00; padding: 30px; margin-bottom: 30px; background: #111; }}
        .header h1 {{ font-size: 3em; margin: 0; text-shadow: 0 0 10px #00ff00; }}
        .header h2 {{ font-size: 1.5em; color: #ffff00; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-box {{ border: 2px solid #00ff00; padding: 20px; text-align: center; background: #111; }}
        .stat-number {{ font-size: 3em; font-weight: bold; color: #ffff00; }}
        .vuln-critical {{ border-left: 5px solid #ff0000; background: #300; padding: 15px; margin: 10px 0; }}
        .vuln-high {{ border-left: 5px solid #ff6600; background: #310; padding: 15px; margin: 10px 0; }}
        .vuln-medium {{ border-left: 5px solid #ffff00; background: #330; padding: 15px; margin: 10px 0; }}
        .terminal-log {{ background: #000; border: 1px solid #00ff00; padding: 15px; overflow-x: auto; max-height: 300px; }}
        h3 {{ color: #00ffff; border-bottom: 2px solid #00ffff; padding-bottom: 10px; }}
        .footer {{ text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #00ff00; color: #888; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>☠️ MrDos Attacked ☠️</h1>
        <h2>Penetration Testing Final Report</h2>
        <p><strong>Target:</strong> {self.target} | <strong>Date:</strong> {self.start_time}</p>
        <p style="color: #ff6600;">⚠️ AUTHORIZED PENETRATION TEST - ALL ACTIVITIES LOGGED</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{len(all_vulns)}</div>
            <div>Vulnerabilities</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{len([v for v in all_vulns if v.get('severity') == 'Critical'])}</div>
            <div>Critical</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{len([v for v in all_vulns if v.get('severity') == 'High'])}</div>
            <div>High</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{len([v for v in all_vulns if v.get('severity') in ['Medium', 'Low']])}</div>
            <div>Medium/Low</div>
        </div>
    </div>
    
    <h3>🎯 Discovered Vulnerabilities</h3>
"""
        
        if all_vulns:
            for vuln in all_vulns:
                severity = vuln.get('severity', 'Medium')
                css_class = f"vuln-{severity.lower()}"
                html += f"""
    <div class="{css_class}">
        <strong>[{severity}] {vuln.get('type', 'Unknown')}</strong><br>
        <strong>URL:</strong> {vuln.get('url', 'N/A')}<br>
        <strong>Evidence:</strong> {vuln.get('evidence', 'N/A')[:200]}<br>
        <strong>Payload:</strong> <code>{vuln.get('payload', 'N/A')}</code>
    </div>
"""
        else:
            html += "<p>No vulnerabilities detected yet. Scan may still be in progress...</p>"
        
        html += f"""
    <h3>📡 Terminal Logs</h3>
    <div class="terminal-log">
        <pre>"""
        
        # Add recent logs
        for i in range(1, 6):
            log_file = f"{self.workspace}/logs/terminal_{i}.log"
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()[-20:]  # Last 20 lines
                        html += f"\n=== TERMINAL {i} ===\n"
                        html += ''.join(lines)
                except:
                    pass
        
        html += f"""</pre>
    </div>
    
    <div class="footer">
        <p>MrDos Attacked - Penetration Testing Framework v2.0</p>
        <p>Generated: {datetime.now()}</p>
        <p style="color: #ff6600;">⚠️ For Authorized Security Testing Only</p>
    </div>
</body>
</html>"""
        
        with open(report_file, 'w') as f:
            f.write(html)
        
        print(f"\n{Colors.OKGREEN}[+] Final report generated: {report_file}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}[*] View at: http://localhost:{self.web_port}/final_report.html{Colors.ENDC}")
        
        # Copy to index.html too
        index_file = f"{self.workspace}/web/index.html"
        with open(index_file, 'w') as f:
            f.write(html)
    
    def run(self):
        """Main execution"""
        # Countdown for authorization confirmation
        print(f"\n{Colors.WARNING}⚠️  AUTHORIZATION CHECK{Colors.ENDC}")
        print(f"{Colors.WARNING}This tool is for authorized penetration testing only!{Colors.ENDC}")
        print(f"{Colors.WARNING}Press Ctrl+C within 5 seconds if you don't have permission...{Colors.ENDC}\n")
        
        try:
            for i in range(5, 0, -1):
                print(f"Starting in {i} seconds...", end='\r')
                time.sleep(1)
            print("\n")
        except KeyboardInterrupt:
            print(f"\n{Colors.FAIL}[!] Cancelled by user{Colors.ENDC}")
            sys.exit(0)
        
        # Start web dashboard
        self.start_web_dashboard()
        
        # Launch all terminals
        self.run_orchestrated_attack()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python3 mrdos_attacked.py <target>")
        print("Example: python3 mrdos_attacked.py 192.168.1.1")
        print("Example: python3 mrdos_attacked.py target.com")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Validate target
    try:
        socket.gethostbyname(target)
    except:
        print(f"{Colors.FAIL}[-] Invalid target: {target}{Colors.ENDC}")
        sys.exit(1)
    
    tool = MrDosAttacked(target)
    tool.run()


if __name__ == '__main__':
    main()
EOF