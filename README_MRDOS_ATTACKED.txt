================================================================================
           ☠️ MrDos Attacked - Penetration Testing Framework v2.0 ☠️
================================================================================

AUTHORIZED USE ONLY - FOR PROFESSIONAL PENETRATION TESTERS

================================================================================
                         KALI LINUX SETUP GUIDE
================================================================================

STEP 1: SYSTEM REQUIREMENTS
-----------------------------
- Kali Linux 2023.x or newer
- Python 3.x (pre-installed)
- Nmap (pre-installed)
- SQLMap (pre-installed: apt install sqlmap)
- gnome-terminal, xfce4-terminal, or konsole
- Network access to target

STEP 2: FILE INSTALLATION
-----------------------------
All files should be in /home/user/:
  - mrdos_attacked.py      (Main launcher + web dashboard)
  - terminal1_nmap.py      (Nmap scanner module)
  - terminal2_sql.py       (SQL Injection + SQLMap)
  - terminal3_rce.py       (RCE/Command Injection)
  - terminal4_ssrf.py      (SSRF/Cloud Metadata)
  - terminal5_api_xss.py  (API Discovery + XSS)

STEP 3: MAKE EXECUTABLE
-----------------------------
chmod +x /home/user/*.py

STEP 4: INSTALL PYTHON DEPENDENCIES
-----------------------------
pip3 install python-nmap requests urllib3 --break-system-packages

Or use:
apt install python3-nmap python3-requests -y

STEP 5: VERIFY SQLMAP
-----------------------------
sqlmap --version

================================================================================
                              USAGE
================================================================================

MAIN LAUNCHER (RECOMMENDED):
-----------------------------
python3 /home/user/mrdos_attacked.py <target>

Example:
  python3 /home/user/mrdos_attacked.py 192.168.1.1
  python3 /home/user/mrdos_attacked.py target.com
  python3 /home/user/mrdos_attacked.py 10.0.0.5

This will:
  1. Show authorization warning with 5-second countdown
  2. Launch web dashboard at http://localhost:8888
  3. Open 5 attack terminals automatically
  4. Generate real-time results
  5. Create final HTML report

ACCESSING RESULTS:
-----------------------------
1. Web Dashboard: http://localhost:8888
   - Live terminal status
   - Real-time vulnerability discovery
   - Auto-refresh every 5 seconds

2. Results Files: /tmp/mrdos_<target>/results/
   - nmap_scan.json      (Port scan results)
   - sqli_scan.json      (SQL injection findings)
   - rce_scan.json       (RCE vulnerabilities)
   - ssrf_scan.json      (SSRF test results)
   - api_xss_scan.json   (API endpoints & XSS)

3. Terminal Logs: /tmp/mrdos_<target>/logs/
   - terminal_1.log      (Nmap output)
   - terminal_2.log      (SQLi testing)
   - terminal_3.log      (RCE testing)
   - terminal_4.log      (SSRF testing)
   - terminal_5.log      (API/XSS testing)

INDIVIDUAL TERMINAL USAGE:
-----------------------------
# Terminal 1 - Nmap Scanner (3 phases)
python3 /home/user/terminal1_nmap.py <target> /tmp/mrdos_<target>

# Terminal 2 - SQL Injection
python3 /home/user/terminal2_sql.py <target> /tmp/mrdos_<target>

# Terminal 3 - RCE Testing
python3 /home/user/terminal3_rce.py <target> /tmp/mrdos_<target>

# Terminal 4 - SSRF Testing
python3 /home/user/terminal4_ssrf.py <target> /tmp/mrdos_<target>

# Terminal 5 - API & XSS
python3 /home/user/terminal5_api_xss.py <target> /tmp/mrdos_<target>

================================================================================
                        TERMINAL BREAKDOWN
================================================================================

TERMINAL 1: NMAP SCANNER
  - Quick Scan: Top 1000 ports
  - Full Scan: All 65535 ports  
  - Vuln Scan: NSE scripts for CVEs
  - OS Detection & Service fingerprinting
  - Outputs: JSON + TXT reports

TERMINAL 2: SQL INJECTION
  - 20+ payloads (Error/Time/Union-based)
  - Automatic SQLMap exploitation
  - Database banner extraction
  - Supports: MySQL, MSSQL, PostgreSQL, Oracle, SQLite
  - Outputs: Confirmed vulnerabilities + DB info

TERMINAL 3: RCE / COMMAND INJECTION
  - Command injection payloads (|, ;, `, $)
  - Web shell detection (c99, r57, wso, etc.)
  - Blind RCE detection (timing-based)
  - System info extraction (whoami, id, uname)
  - Critical severity alerts

TERMINAL 4: SSRF (Server-Side Request Forgery)
  - Cloud metadata endpoints (AWS, GCP, Azure)
  - Internal IP access (127.0.0.1, 192.168.x.x)
  - File wrapper tests (/etc/passwd, win.ini)
  - Protocol bypasses (dict, gopher, ftp)
  - Cloud metadata extraction alerts

TERMINAL 5: API DISCOVERY & XSS
  - 25+ API endpoint discovery
  - Directory/file fuzzing (multi-threaded)
  - 8 XSS payloads (reflected detection)
  - IDOR/BOLA testing on APIs
  - Hidden path discovery (admin, .git, .env)

================================================================================
                    MONITORING COMMANDS
================================================================================

# Watch all terminal outputs in real-time
tail -f /tmp/mrdos_*/logs/terminal_*.log

# Watch specific terminal
tail -f /tmp/mrdos_192_168_1_1/logs/terminal_1.log

# Auto-refresh directory listing
watch -n 5 'ls -la /tmp/mrdos_*/results/'

# Monitor process status
ps aux | grep -E "nmap|sqlmap|python.*terminal"

# View JSON results
cat /tmp/mrdos_*/results/nmap_scan.json | python3 -m json.tool

================================================================================
                         LEGAL DISCLAIMER
================================================================================

⚠️ WARNING - AUTHORIZED USE ONLY ⚠️

By using this tool, you confirm that:

1. You have EXPLICIT WRITTEN PERMISSION to test the target
2. You are the OWNER of the target system, OR
3. You have a signed CONTRACT/AUTHORIZATION for penetration testing
4. You understand that unauthorized access is ILLEGAL
5. You assume FULL RESPONSIBILITY for your actions

The author (MrDos) assumes NO LIABILITY for:
- Misuse of this tool
- Damage to systems
- Legal consequences of unauthorized testing
- Any criminal charges resulting from misuse

This tool is for:
✓ Authorized penetration testing
✓ Security research with permission
✓ Educational purposes in controlled environments
✓ Bug bounty programs (with permission)

This tool is NOT for:
✗ Unauthorized system access
✗ Attacking systems without permission
✗ Criminal activity
✗ Denial of Service attacks
✗ Data theft or espionage

================================================================================
                          TROUBLESHOOTING
================================================================================

ISSUE: Terminals don't open
SOLUTION: Install terminal emulator
  apt install gnome-terminal xfce4-terminal konsole xterm

ISSUE: SQLMap not found
SOLUTION: Install SQLMap
  apt install sqlmap

ISSUE: Python modules missing
SOLUTION: Install dependencies
  pip3 install python-nmap requests --break-system-packages

ISSUE: Permission denied
SOLUTION: Make scripts executable
  chmod +x /home/user/*.py

ISSUE: Nmap requires root
SOLUTION: Run with sudo
  sudo python3 /home/user/mrdos_attacked.py <target>

================================================================================
                           QUICK START
================================================================================

1. Open Kali Linux terminal
2. Navigate to scripts:
   cd /home/user

3. Run main launcher:
   python3 mrdos_attacked.py TARGET_IP

4. Wait 5 seconds for authorization confirmation

5. Access web dashboard:
   http://localhost:8888

6. Monitor 5 terminals automatically opening

7. View results in real-time on dashboard

8. Check saved results:
   ls /tmp/mrdos_TARGET/results/

================================================================================
                          REPORT GENERATION
================================================================================

The framework automatically generates:

1. Real-time web dashboard (auto-refresh)
2. Final HTML report with all vulnerabilities
3. Individual JSON files per test type
4. Terminal log files for detailed output
5. Vulnerability summary with severity levels

All reports are saved in:
/tmp/mrdos_<target>/
  ├── results/      (JSON data)
  ├── logs/         (Terminal outputs)
  ├── web/          (HTML reports)
  └── final_report.html

================================================================================
                           CONTACT & INFO
================================================================================

Tool: MrDos Attacked v2.0
Type: Multi-Terminal Penetration Testing Framework
Terminals: 5 (Nmap, SQLi, RCE, SSRF, API/XSS)
Dashboard: Web-based with auto-refresh
Reports: HTML + JSON formats

REMEMBER: Always have proper authorization before testing!

================================================================================
                          END OF DOCUMENT
================================================================================
