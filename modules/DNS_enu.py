from core.command_runner import CommandRunner
from formatters.formatter import Formatter


class DNSEnumeration:

    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()
        self.tool = None
        self.name_servers = []
        self.output = Formatter()
        self.enumeration_type = "DNS Enumeration"

    def _execute(self, command):
        results = self.runner.run(command)
        self.output.print_display(results)
        return results

    def version_enu(self):
        result = self._execute(["dig", f"@{self.target}", "version.bind", "txt", "chaos"])

        if result["success"]:
            self.tool = "dig"
            return result

        result = self._execute(["nslookup", "-type=NS", self.target])

        if result["success"]:
            self.tool = "nslookup"
            return result

        self.tool = None
        return result

    def name_server_enu(self):

        if self.tool == "dig":
            result = self._execute(["dig", "NS", self.target])

            if result["success"]:
                self.name_servers.clear()

                for line in result["stdout"].splitlines():
                    if " IN NS " in line:
                        self.name_servers.append(line.split()[-1].rstrip("."))

            return result

        elif self.tool == "nslookup":
            result = self._execute(["nslookup", "-type=NS", self.target])

            if result["success"]:
                self.name_servers.clear()

                for line in result["stdout"].splitlines():
                    if "nameserver =" in line.lower():
                        self.name_servers.append(line.split("=")[1].strip().rstrip("."))

            return result

        return {}

    def soa_enu(self):

        if self.tool == "dig":
            return self._execute(["dig", "SOA", self.target])

        elif self.tool == "nslookup":
            return self._execute(["nslookup", "-type=SOA", self.target])

        return {}

    def zone_transfer_enu(self, nameserver):

        if self.tool != "dig":
            return {}

        return self._execute(["dig", "AXFR", self.target, f"@{nameserver}"])

    def general_enu(self):

        results = {}
        records = ["A", "AAAA", "MX", "TXT", "CNAME"]

        for record in records:
            if self.tool == "dig":
                cmd = ["dig", record, self.target]

            elif self.tool == "nslookup":
                cmd = ["nslookup", f"-type={record}", self.target]

            else:
                continue

            results[record] = self._execute(cmd)

        return results

    def run(self):

        results = {}
        self.output.print_header(self.enumeration_type)

        version_info = self.version_enu()

        if not version_info["success"]:
            self.output.print_summary(results)
            self.output.print_footer()
            return {}

        results["version"] = version_info
        results["name_servers"] = self.name_server_enu()
        results["soa"] = self.soa_enu()
        results["records"] = self.general_enu()

        results["zone_transfer"] = {}

        if self.tool == "dig":
            for ns in self.name_servers:
                results["zone_transfer"][ns] = self.zone_transfer_enu(ns)

        self.output.print_summary(results)
        self.output.print_footer()

        return results