import platform
from core.command_runner import CommandRunner
from formatters.formatter import Formatter

class SMBNetBIOSEnumeration:

    def __init__(self, target):
        self.target = target
        self.os = platform.system().lower()
        self.runner = CommandRunner()
        self.output = Formatter()
        self.enumeration_type = "NetBIOS Enumeration"

    def _execute(self, command):
        res = self.runner.run(command)
        self.output.print_display(res)
        return res

    def service_name_scan(self):

        if self.os == "windows":
            command = ["nbtstat", "-A", self.target]

        elif self.os == "linux":
            command = ["nmblookup", "-A", self.target]

        else:
            self.output.print_warning("Unsupported operating system")
            return None

        return self._execute(command)

    def smb_scan(self):
        return self._execute(["smbclient","-L", f"//{self.target}", "-N"])
    
    def rpc_enumeration(self):
        results = {}

        commands = [
            "lsaquery",
            "enumdomusers",
            "enumdomgroups",
            "querydispinfo"
        ]

        for command in commands:

            result = self._execute(
                [
                    "rpcclient",
                    "-U", "",
                    "-N",
                    self.target,
                    "-c",
                    command
                ]
            )

            results[command] = result

        return results

    def run(self, ports):
        results = {}
        self.output.print_header(self.enumeration_type)
        if 137 in ports:
            results['services_name'] = self.service_name_scan()

        if any(port in ports for port in (139, 445)):
            results['smb'] = self.smb_scan()
            results['rpc'] = self.rpc_enumeration()

        self.output.print_summary(results=results)
        self.output.print_footer()

        return results