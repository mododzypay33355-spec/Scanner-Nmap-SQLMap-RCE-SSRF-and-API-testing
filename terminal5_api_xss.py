#!/usr/bin/env python3
"""TERMINAL 5: API Discovery & XSS Testing"""
import requests, sys, json, os, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Colors:
    HEADER, OKBLUE, OKCYAN, OKGREEN, WARNING, FAIL, ENDC, BOLD = '\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m'

class APIXSSTester:
    def __init__(self, target, workspace="/tmp"):
        self.target, self.workspace = target, workspace
        self.results_file = f"{workspace}/results/api_xss_scan.json"
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.vulnerabilities, self.api_endpoints, self.paths = [], [], []
        self.xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>", "'\"><script>alert('XSS')</script>"]
        self.api_paths = ['/api', '/api/v1', '/graphql', '/swagger.json', '/wp-json',
            '/users', '/auth', '/products', '/health', '/actuator', '/metrics']
        self.fuzz_paths = ['admin', 'backup', '.env', '.git', 'phpmyadmin', 'test', 'config']
        print(f"""{Colors.HEADER}\n╔══════════════════════════════════════════════════════════════════╗\n║      TERMINAL 5: API DISCOVERY, FUZZING & XSS                    ║\n╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\nTarget: {target}""")

    def get_urls(self):
        urls = []
        for p in ['http', 'https']:
            urls.append(f"{p}://{self.target}")
        for port in [80, 443, 8080, 3000, 8000]:
            proto = 'https' if port in [443, 8443] else 'http'
            urls.append(f"{proto}://{self.target}:{port}")
        return urls

    def check(self, url, path):
        try:
            full = f"{url}/{path}" if not url.endswith('/') else f"{url}{path}"
            r = self.session.get(full, timeout=8, verify=False, allow_redirects=False)
            if r.status_code in [200, 401, 403, 500]:
                return {'url': full, 'status': r.status_code, 'size': len(r.content)}
        except: pass
        return None

    def discover_apis(self):
        print(f"\n{Colors.BOLD}[PHASE 1] API Discovery{Colors.ENDC}\n")
        for url in self.get_urls():
            for path in self.api_paths:
                r = self.check(url, path)
                if r:
                    self.api_endpoints.append(r)
                    print(f"{Colors.OKGREEN}[API] {r['url']} [{r['status']}]{Colors.ENDC}")

    def fuzz(self):
        print(f"\n{Colors.BOLD}[PHASE 2] Directory Fuzzing{Colors.ENDC}\n")
        for url in self.get_urls()[:5]:
            with ThreadPoolExecutor(max_workers=10) as ex:
                futures = {ex.submit(self.check, url, p): p for p in self.fuzz_paths}
                for f in as_completed(futures):
                    r = f.result()
                    if r:
                        self.paths.append(r)
                        print(f"{Colors.OKCYAN}[PATH] {r['url']} [{r['status']}]{Colors.ENDC}")

    def test_xss(self):
        print(f"\n{Colors.BOLD}[PHASE 3] XSS Testing{Colors.ENDC}\n")
        for url in self.get_urls()[:6]:
            for param in ['q', 'search', 'name']:
                for payload in self.xss_payloads:
                    try:
                        test = f"{url}?{param}={urllib.parse.quote(payload)}"
                        r = self.session.get(test, timeout=10, verify=False)
                        if payload in r.text:
                            self.vulnerabilities.append({'type': 'XSS', 'url': test, 'param': param,
                                'payload': payload, 'severity': 'Medium'})
                            print(f"{Colors.FAIL}[!] XSS: {test}{Colors.ENDC}")
                            break
                    except: pass

    def save(self):
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump({'target': self.target, 'time': datetime.now().isoformat(),
                'apis': self.api_endpoints, 'paths': self.paths, 'vulns': self.vulnerabilities}, f, indent=2)
        print(f"\n{Colors.OKGREEN}[+] Results: {self.results_file}{Colors.ENDC}")

    def run(self):
        self.discover_apis()
        self.fuzz()
        self.test_xss()
        self.save()
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n{Colors.BOLD}Scan Complete{Colors.ENDC} | APIs: {len(self.api_endpoints)} | Paths: {len(self.paths)} | Vulns: {len(self.vulnerabilities)}{Colors.ENDC}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: terminal5_api_xss.py <target>")
        sys.exit(1)
    APIXSSTester(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/tmp").run()
