from core.port_scanner import port_scan
from modules.SMTP_enu import SMTPEnumeration as SNE
from modules.SNMP_enu import SNMPEnumeration as SE
from modules.LDAP_enu import LDAPEnumeration as LE
from modules.SMTP_enu import SMTPEnumeration as SME
from modules.DNS_enu import DNSEnumeration as DE
from modules.NTP_enu import NTPEnumeration as NE
from modules.IPsec_enu import IPsecEnumeration as IE
from validators import ipv4, domain


enumeration_modules = {
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
        print("[-] Invalid IP address or domain.")
        return None, None

    scanner = port_scan(target)
    open_ports = scanner.scan()

    return target, open_ports


def enumeration_executor(target, ports):
    results = {}
    executed = set()

    for port in ports:

        module = enumeration_modules.get(port)

        if module is None:
            continue

        if module in executed:
            continue

        executed.add(module)

        print(f"\n[#] Running {module.__name__}...")

        try:
            if module == SME:
                enum = module()
                results[module.__name__] = enum.enumerate(target, port)

            else:
                enum = module(target)
                results[module.__name__] = enum.run(ports)

        except Exception as e:
            print(f"[-] {module.__name__} failed.\nError: {e}")

    return results


if __name__ == "__main__":

    target, ports = get_basic_info()

    if target and ports:

        results = enumeration_executor(target, ports)

        print("\n========== RESULTS ==========")

        for module, output in results.items():
            print(f"\n[{module}]")
            print(output)