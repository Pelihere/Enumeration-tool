from core.port_scanner import PortScanner
from modules.SMTP_enu import SMTPEnumeration as SNE
from modules.SNMP_enu import SNMPEnumeration as SE
from modules.LDAP_enu import LDAPEnumeration as LE
from modules.smb_Netbios_enu import SMBNetBIOSEnumeration as SME
from modules.DNS_enu import DNSEnumeration as DE
from modules.NTP_enu import NTPEnumeration as NE
from modules.IPsec_enu import IPsecEnumeration as IE
from validators import ipv4, domain
from formatters.formatter import Formatter


enumeration_module_classs = {
    25: SME,
    53: DE,
    123: NE,
    139: SNE,
    161: SE,
    389: LE,
    445: SNE,
    500: IE,
    636: LE,
    4500: IE,
}


def get_basic_info():
    target = input("[+] Enter target: ").strip()

    if not (ipv4(target) or domain(target)):
        Formatter.print_warning("Invalid IP address or domain.")
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

        Formatter.print_info(f"\nRunning {module_class.__name__}...")

        try:
            if module_class == SME:
                enum = module_class()
                results[module_class.__name__] = enum.enumerate(target, port)
            else:
                enum = module_class(target)
                results[module_class.__name__] = enum.run()

        except Exception as e:
            print(f"[-] {module_class.__name__} failed.\nError: {e}")

    return results


if __name__ == "__main__":

    target, ports = get_basic_info()
    if target and ports:
        results = enumeration_executor(target, ports)
        Formatter.print_header("Results")
        for module_class, output in results.items():
            print(f"\n[{module_class}]")
            print(output)