from core.port_scanner import PortScanner
from modules.SMTP_enu import SMTPEnumeration as SNE
from modules.SNMP_enu import SNMPEnumeration as SE
from modules.LDAP_enu import LDAPEnumeration as LE
from modules.smb_Netbios_enu import SMBNetBIOSEnumeration as SME
from modules.DNS_enu import DNSEnumeration as DE
from modules.NTP_enu import NTPEnumeration as NE
from modules.IPsec_enu import IPsecEnumeration as IE
from modules.FTP_enu import FTPEnumeration as FE
from modules.HTTP_enu import HTTPEnumeration as HE

from formatters.formatter import Formatter
from exporter.json_exporter import JSONExporter

from validators import ipv4, domain
import time


enumeration_module_classs = {
    21: FE,     # FTP
    25: SNE,    # SMTP
    53: DE,     # DNS
    80: HE,
    123: NE,    # NTP
    137: SME,   # NetBIOS Name Service
    139: SME,   # SMB / NetBIOS Session Service
    161: SE,    # SNMP
    389: LE,    # LDAP
    443: HE,
    445: SME,   # SMB (Microsoft-DS)
    500: IE,    # IPsec/IKE
    636: LE,    # LDAPS
    4500: IE,   # IPsec NAT-T
}


formatter = Formatter()


def get_basic_info():
    target = input("[+] Enter target: ").strip()

    if not (ipv4(target) or domain(target)):
        formatter.print_warning("Invalid IP address or domain.")
        return None, None

    scanner = PortScanner(target)
    open_ports = scanner.scan()

    return target, open_ports


def enumeration_executor(target, ports):
    results = {}
    executed = set()

    for port in ports:
        module_class = enumeration_module_classs.get(port)

        if module_class is None:
            continue

        if module_class in executed:
            continue

        executed.add(module_class)

        formatter.print_info(f"\nRunning {module_class.__name__}...")

        try:
            if module_class == SME:
                enum = module_class(target)
                results[module_class.__name__] = enum.run(ports)
            elif module_class == SNE:
                enum = module_class()
                results[module_class.__name__] = enum.run(target, port)
            elif module_class == FE:
                enum = module_class(target)
                results[module_class.__name__] = enum.run(port)
            else:
                enum = module_class(target)
                results[module_class.__name__] = enum.run()

        except Exception as e:
            print(f"[-] {module_class.__name__} failed.\nError: {e}")

    return results


if __name__ == "__main__":

    target, ports = get_basic_info()
    if target and ports:
        start = time.time()
        results = enumeration_executor(target, ports)
        end = time.time()

        formatter.print_header("Results")
        for module_class, output in results.items():
            print(f"\n[{module_class}]")
            print(output)

        report_path = JSONExporter().export(target, ports, results, scan_start=start, scan_end=end)
        formatter.print_info(f"JSON report saved to: {report_path}")