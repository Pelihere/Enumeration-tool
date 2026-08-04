<div align="center">

# 🛡️ CEH Enumeration Toolkit

### Modular Python Framework for Network Enumeration & Reconnaissance

*A Python-based enumeration framework built for penetration testing, cybersecurity education, and reconnaissance automation.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-green)
![License](https://img.shields.io/badge/License-MIT-red)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

# 📖 Overview

The **CEH Enumeration Toolkit** is a modular Python framework designed to automate common enumeration tasks performed during penetration testing and security assessments.

Instead of manually executing multiple reconnaissance tools one by one, this framework detects available services, launches the appropriate enumeration modules automatically, parses their outputs, and presents the results in a clean and organized format.

---

# ✨ Features

- 🔍 Automatic service detection
- ⚡ Port-based module execution
- 🧩 Modular architecture
- 🐍 Pure Python implementation
- 📄 Clean terminal output
- 🖥 Cross-platform support
- ➕ Easily extendable
- 🚀 Fast execution
- 📦 Plugin-oriented design
- 🛠 Integration with common security tools
- 💻 Full CLI support via `argparse`
- 📤 JSON report export

---

# 🏗 Architecture

```
                     Target
                        │
                        ▼
                Initial Port Scan
                        │
                        ▼
              Detect Open Services
                        │
    ┌──────────┬────────┼────────┬──────────┐
    ▼          ▼        ▼        ▼          ▼
  DNS        SMTP     LDAP     HTTP        FTP     ... (SNMP, NTP, IPsec, SMB/NetBIOS)
    ▼          ▼        ▼        ▼          ▼
 Parse Data Parse Data Parse Data Parse Data Parse Data
    └──────────┴────────┼────────┴──────────┘
                        ▼
                Unified Output Engine
                        │
                ┌───────┴───────┐
                ▼               ▼
          Console Report   JSON Report
```

---

# 📂 Project Structure

```
Enumeration-Tool/

│
├── main.py
│
├── core/
│   ├── command_runner.py
│   └── port_scanner.py
│
├── modules/
│   ├── DNS_enu.py
│   ├── SMTP_enu.py
│   ├── SNMP_enu.py
│   ├── LDAP_enu.py
│   ├── NTP_enu.py
│   ├── IPsec_enu.py
│   ├── smb_Netbios_enu.py
│   ├── FTP_enu.py
│   └── HTTP_enu.py
│
├── exporter/
│   └── json_exporter.py
│
├── formatters/
│   └── formatter.py
│
├── reports/              # generated JSON reports (git-ignored)
│
├── REQIERMENTS.txt
│
└── README.md
```

---

# 🔬 Supported Enumeration Modules

| Module    | Description                               |
|---------  |-------------------------------------------|
| DNS       | DNS version, records, zone transfer       |
| SMTP      | Banner grabbing, VRFY, EXPN               |
| SNMP      | Community strings, system information     |
| LDAP      | Naming contexts, directory information    |
| NetBIOS   | Machine names, workgroups                 |
| SMB       | Share, user, and group enumeration via RPC|
| NTP       | Information disclosure, monlist           |
| IPsec     | VPN endpoint / IKE detection              |
| FTP       | Banner grabbing, anonymous login test     |
| HTTP/S    | Headers, OPTIONS, robots.txt, common paths|

---

# ⚙ Requirements

Python 3.10+

External tools:

- Nmap
- Dig
- ldapsearch
- snmpwalk
- rpcclient
- smbclient
- nmblookup
- curl

Install Python dependencies:

```bash
pip install -r REQIERMENTS.txt
```

---

# 🚀 Usage

### Interactive mode (no arguments)

```bash
python main.py

[+] Enter target: 192.168.1.10
```

### CLI mode (via argparse)

```bash
# Full scan + JSON report
python main.py -t 192.168.1.10 --json

# Skip the port scan, enumerate specific ports directly
python main.py -t 192.168.1.10 -p 21,53,80,443 --json

# Limit the scan range (faster than the full 1-65535 sweep)
python main.py -t test.local --start-port 1 --end-port 1024 --json --output my_reports/

# Show all available options
python main.py --help
```

### CLI options

| Flag | Description | Default |
|---|---|---|
| `-t`, `--target` | Target IP address or domain | prompts interactively if omitted |
| `-p`, `--ports` | Comma-separated list of ports to enumerate directly, skipping the port scan | none |
| `--start-port` | Start port for the full scan (used only when `--ports` is not given) | 1 |
| `--end-port` | End port for the full scan (used only when `--ports` is not given) | 65535 |
| `--json` | Export results to a timestamped JSON report | disabled |
| `--output` | Directory to write the JSON report into | `reports/` |

---

# 📤 JSON Reports

When run with `--json`, a report is written to the output directory with the following structure:

```json
{
  "target": "192.168.1.10",
  "open_ports": [21, 53, 80],
  "scan_start": "2026-08-04 09:00:00",
  "scan_end": "2026-08-04 09:02:15",
  "total_scan_time": 135.42,
  "results": { ... }
}
```

Reports are named `<target>_<unix_timestamp>.json` so repeated scans of the same target never overwrite each other.

---

# 🧠 Design Principles

The project follows several software engineering principles:

- Separation of Concerns
- Single Responsibility Principle
- Modular Design
- Code Reusability
- Easy Maintenance
- Extensibility
- Clean Output Formatting

---

# 🔧 Roadmap

### Core Modules

- [x] DNS
- [x] SMTP
- [x] LDAP
- [x] SNMP
- [x] NetBIOS
- [x] NTP
- [x] IPsec
- [x] FTP
- [x] HTTP

### Upcoming Modules

- [ ] RPC (standalone)
- [ ] SSH
- [ ] Kerberos
- [ ] MySQL
- [ ] PostgreSQL
- [ ] MSSQL
- [ ] RPC Null Session
- [ ] Banner Fingerprinting

---

# 📊 Future Features

- [x] JSON Export
- [x] CLI support (argparse)
- [ ] CVE Lookup
- [ ] HTML Reports
- [ ] XML Export
- [ ] Logging Engine
- [ ] Vulnerability Detection
- [ ] Multi-threading (parallel module execution)
- [ ] Plugin Support
- [ ] Docker Support
- [ ] Unit Tests (pytest)
- [ ] Config file support (default community strings, timeouts, wordlists)

---

# 🤝 Contributing

Contributions are welcome.

Feel free to:

- Report bugs
- Improve documentation
- Add new enumeration modules
- Optimize existing code
- Suggest new features

---

# ⚠ Disclaimer

This project is intended **strictly for authorized security testing**.

Do **NOT** use this tool against systems without explicit authorization.

The author assumes no responsibility for misuse or any damage caused by this software.

---

# 📜 License

MIT License

---