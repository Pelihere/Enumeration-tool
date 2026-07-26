from core.command_runner import CommandRunner

class SNMPEnumeration:
    def __init__(self, target, community="public"):
        self.target = target
        self.community = community
        self.version = None
        self.runner = CommandRunner()

    def version_detection(self):
        ver2_info = self.runner.run(["snmpwalk", "-v2c", "-c", self.community, self.target, "1.3.6.1.2.1.1"])

        if ver2_info["success"]:
            #TODO use formmatter module here for version 2 success
            self.version = "2c"
            return True

        #TODO use formmatter module here for version 2 failure

        ver1_info = self.runner.run(["snmpwalk", "-v1", "-c", self.community, self.target, "1.3.6.1.2.1.1"])

        if ver1_info["success"]:
            #TODO use formmatter module here for version 1 success
            self.version = "1"
            return True

        #TODO use formmatter module here for both version failure
        return False

    def _walker(self, oid):
        if self.version is None:
            #TODO use formmatter module here
            return {}

        return self.runner.run(
                [
                    "snmpwalk",
                    f"-v{self.version}",
                    "-c",
                    self.community,
                    self.target,
                    oid
                ])

    def system_enu(self):
        return self._walker("1.3.6.1.2.1.1")

    def interface_enu(self):
        return self._walker("1.3.6.1.2.1.2")

    def ip_enu(self):
        return self._walker("1.3.6.1.2.1.4")

    def tcp_enu(self):
        return self._walker("1.3.6.1.2.1.6")

    def udp_enu(self):
        return self._walker("1.3.6.1.2.1.7")
    
    def icmp_enu(self):
        return self._walker("1.3.6.1.2.1.5")

    def storage_enu(self):
        return self._walker("1.3.6.1.2.1.25.2")

    def process_enu(self):
        return self._walker("1.3.6.1.2.1.25.4")

    def software_enu(self):
        return self._walker("1.3.6.1.2.1.25.6")
    
    def run(self):
        results = {}
        if not self.version_detection():
            return {}
        
        enumerations = {
            "system": self.system_enu,
            "interface": self.interface_enu,
            "ip": self.ip_enu,
            "tcp": self.tcp_enu,
            "udp": self.udp_enu,
            "icmp": self.icmp_enu,
            "storage": self.storage_enu,
            "process": self.process_enu,
            "software": self.software_enu,
        }

        for name, func in enumerations.items():
            results[name] = func()

        return results