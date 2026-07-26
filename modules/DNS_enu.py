from core.command_runner import CommandRunner


class DNSEnumeration:

    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()
        self.tool = None
        self.name_servers = []

    def version_enu(self):
        result = self.runner.run(["dig", f"@{self.target}", "version.bind", "txt", "chaos"])

        if result["success"]:
            self.tool = "dig"
            return result

        result = self.runner.run(["nslookup", "-type=NS", self.target])

        if result["success"]:
            self.tool = "nslookup"
            return result

        self.tool = None
        return result

    def name_server_enu(self):

        if self.tool == "dig":
            result = self.runner.run(["dig", "NS", self.target])

            if result["success"]:
                self.name_servers.clear()

                for line in result["stdout"].splitlines():
                    if " IN NS " in line:
                        self.name_servers.append(line.split()[-1].rstrip("."))

            return result

        elif self.tool == "nslookup":
            result = self.runner.run(["nslookup", "-type=NS", self.target])

            if result["success"]:
                self.name_servers.clear()

                for line in result["stdout"].splitlines():
                    if "nameserver =" in line.lower():
                        self.name_servers.append(line.split("=")[1].strip().rstrip("."))

            return result

        return {}

    def soa_enu(self):

        if self.tool == "dig":
            return self.runner.run(["dig", "SOA", self.target])

        elif self.tool == "nslookup":
            return self.runner.run(["nslookup", "-type=SOA", self.target])

        return {}

    def zone_transfer_enu(self, nameserver):

        if self.tool != "dig":
            return {}

        return self.runner.run(["dig", "AXFR", self.target, f"@{nameserver}"])

    def general_enu(self):

        results = {}

        if self.tool == "dig":

            records = [
                "A",
                "AAAA",
                "MX",
                "TXT",
                "CNAME"
            ]

            for record in records:
                results[record] = self.runner.run(["dig", record, self.target])

        elif self.tool == "nslookup":

            records = [
                "A",
                "AAAA",
                "MX",
                "TXT",
                "CNAME"
            ]

            for record in records:
                results[record] = self.runner.run(["nslookup", f"-type={record}", self.target])

        return results

    def run(self):

        results = {}

        if not self.version_enu()["success"]:
            return {}

        results["version"] = self.version_enu()
        results["name_servers"] = self.name_server_enu()
        results["soa"] = self.soa_enu()
        results["records"] = self.general_enu()

        results["zone_transfer"] = {}

        if self.tool == "dig":
            for ns in self.name_servers:
                results["zone_transfer"][ns] = self.zone_transfer_enu(ns)

        return results