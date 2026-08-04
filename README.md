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
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    DNS Module     SMTP Module     LDAP Module
        ▼               ▼               ▼
     Parse Data     Parse Data     Parse Data
        └───────────────┼───────────────┘
                        ▼
                Unified Output Engine
                        ▼
             Final Enumeration Report
```

---

# 📂 Project Structure

```
Enumeration-Tool/

│
├── main.py
│
├── modules/
│   ├── dns.py
│   ├── smtp.py
│   ├── ldap.py
│   ├── snmp.py
│   ├── ntp.py
│   ├── netbios.py
│   ├── ipsec.py
│   
│
├── scanner/
│   └── parser.py
│
├── formatters/
│   ├── formatter.py
│
│
├── requirements.txt
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
| NTP       | Information disclosure                    |
| IPsec     | VPN endpoint detection                    |

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

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🚀 Usage

Scan an IP address

```bash
python main.py 

[+] Enter target: 192.168.1.10
```



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

### Upcoming Modules

- [ ] RPC
- [x] FTP
- [ ] HTTP
- [ ] SSH
- [ ] Kerberos
- [ ] MySQL
- [ ] PostgreSQL
- [ ] MSSQL
- [ ] RPC Null Session
- [ ] Banner Fingerprinting

---

# 📊 Future Features

- HTML Reports
- JSON Export
- XML Export
- Logging Engine
- CVE Lookup
- Vulnerability Detection
- Multi-threading
- Plugin Support
- Docker Support

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
