import argparse
import time

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
from validators import ipv4, domain
from formatters.formatter import Formatter
from exporter.json_exporter import JSONExporter


enumeration_module_classs = {
    21: FE,     # FTP
    25: SNE,    # SMTP
    53: DE,     # DNS
    80: HE,     # HTTP
    123: NE,    # NTP
    137: SME,   # NetBIOS Name Service
    139: SME,   # SMB / NetBIOS Session Service
    161: SE,    # SNMP
    389: LE,    # LDAP
    443: HE,    # HTTP
    445: SME,   # SMB (Microsoft-DS)
    500: IE,    # IPsec/IKE
    636: LE,    # LDAPS
    4500: IE,   # IPsec NAT-T
}


formatter = Formatter()


def parse_args():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="CEH Enumeration Toolkit - automated network enumeration framework"
    )

    parser.add_argument(
        "-t", "--target",
        help="Target IP address or domain. If omitted, you will be prompted interactively."
    )

    parser.add_argument(
        "-p", "--ports",
        help="Comma-separated list of ports to enumerate directly, skipping the port scan "
             "(e.g. -p 21,80,443)."
    )

    parser.add_argument(
        "--start-port",
        type=int,
        default=1,
        help="Start port for the full scan when --ports is not given (default: 1)."
    )

    parser.add_argument(
        "--end-port",
        type=int,
        default=65535,
        help="End port for the full scan when --ports is not given (default: 65535)."
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export results to a timestamped JSON report."
    )

    parser.add_argument(
        "--output",
        default="reports",
        help="Directory to write the JSON report into (default: reports/)."
    )

    return parser.parse_args()


def validate_target(target):
    if not (ipv4(target) or domain(target)):
        formatter.print_warning("Invalid IP address or domain.")
        return False
    return True


def parse_port_list(ports_arg):
    ports = []

    for part in ports_arg.split(","):
        part = part.strip()

        if not part:
            continue

        if not part.isdigit():
            formatter.print_warning(f"Skipping invalid port: '{part}'")
            continue

        port = int(part)

        if not (1 <= port <= 65535):
            formatter.print_warning(f"Skipping out-of-range port: {port}")
            continue

        ports.append(port)

    return sorted(set(ports))


def get_basic_info(args):

    target = args.target or input("[+] Enter target: ").strip()

    if not validate_target(target):
        return None, None

    if args.ports:
        ports = parse_port_list(args.ports)

        if not ports:
            formatter.print_warning("No valid ports provided via --ports.")
            return None, None

        formatter.print_info(f"Skipping port scan, using provided ports: {ports}")
        return target, ports

    if args.start_port > args.end_port:
        formatter.print_warning("--start-port cannot be greater than --end-port.")
        return None, None

    scanner = PortScanner(target)
    open_ports = scanner.scan(args.start_port, args.end_port)

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

    args = parse_args()

    target, ports = get_basic_info(args)

    if target and ports:
        start = time.time()
        results = enumeration_executor(target, ports)
        end = time.time()

        formatter.print_header("Results")
        for module_class, output in results.items():
            print(f"\n[{module_class}]")
            print(output)

        if args.json:
            report_path = JSONExporter(output_dir=args.output).export(
                target, ports, results, scan_start=start, scan_end=end
            )
            formatter.print_info(f"JSON report saved to: {report_path}")