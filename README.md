
MrDos Attacked - Multi-Terminal Penetration Testing Framework

SHORT DESCRIPTION (for repo header):
------------------------------------
Advanced multi-terminal pentesting orchestrator with 5 concurrent attack modules 
(Nmap, SQLMap, RCE, SSRF, API/XSS), real-time web dashboard, and automated 
reporting. Built for authorized security professionals.

TAGS/TOPICS:
------------
penetration-testing, cybersecurity, nmap, sqlmap, vulnerability-scanner, 
kali-linux, security-tools, ethical-hacking, web-security, red-team

EMOJI HEADER FOR README:
------------------------
☠️ MrDos Attacked ☠️ - Advanced Multi-Terminal Penetration Testing Framework

ONE-LINE DESCRIPTION:
---------------------
Orchestrate 5 synchronized attack terminals with real-time web dashboard 
for comprehensive security assessments.

FEATURES LIST (GitHub style):
-----------------------------
✨ 5 Concurrent Attack Terminals (Nmap, SQLi, RCE, SSRF, API/XSS)
📊 Real-time Web Dashboard (http://localhost:8888)
🤖 Automated SQLMap Integration
☁️ Cloud Metadata Exploitation (AWS/GCP/Azure)
🎯 20+ SQL Injection Payloads
⚡ Command Injection Detection
🔌 API Endpoint Discovery with IDOR Testing
📝 JSON + HTML Report Generation
🖥️ Auto-terminal Detection (GNOME/XFCE/KDE)
🎨 Dark-themed Responsive Dashboard

INSTALLATION ONE-LINER:
-----------------------
chmod +x *.py && sudo apt install sqlmap nmap -y && pip3 install python-nmap requests --break-system-packages

What Happens After Running:
✅ Authorization countdown (5 seconds)
✅ Web dashboard starts at http://localhost:8888
✅ Browser opens automatically
✅ 5 terminals launch:
Terminal 1: 🔍 Nmap Scanner
Terminal 2: 💉 SQL Injection
Terminal 3: ⚡ RCE Testing
Terminal 4: 🌐 SSRF Testing
Terminal 5: 🔌 API & XSS
✅ Results appear on dashboard in real-time

USAGE EXAMPLE:
--------------
sudo python3 mrdos_attacked.py target.com
# List all results
ls -la /tmp/mrdos_*/results/

# View Nmap results
cat /tmp/mrdos_*/results/nmap_scan.json | python3 -m json.tool

# View SQL injection results
cat /tmp/mrdos_*/results/sqli_scan.json | python3 -m json.tool

# View all vulnerabilities found
ACCESS DASHBOARD:
-----------------
http://localhost:8888
