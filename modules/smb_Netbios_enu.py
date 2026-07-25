import platform
from core.command_runner import CommandRunner

class SMBNetBIOSEnumeration:

    def __init__(self, target):
        self.target = target
        self.os = platform.system().lower()
        self.runner = CommandRunner()

    def service_name_scan(self):

        if self.os == "windows":
            command = ["nbtstat", "-A", self.target]

        elif self.os == "linux":
            command = ["nmblookup", "-A", self.target]

        else:
            print("[-] Unsupported operating system")
            return None

        return self.runner.run(command)

    def smb_scan(self):
        return self.runner.run(["smbclient","-L", f"//{self.target}", "-N"])
    
    def rpc_enumeration(self):
        results = {}

        commands = [
            "lsaquery",
            "enumdomusers",
            "enumdomgroups",
            "querydispinfo"
        ]

        for command in commands:
            results["command"] = self.runner.run(
                    [
                        "rpcclient",
                        "-U", "",
                        "-N",
                        self.target,
                        "-c",
                        command
                    ])

        return results

    def run(self, ports):
        results = {}
        if 137 in ports:
            results['services_name'] = self.service_name_scan()

        if any(port in ports for port in (139, 445)):
            results['smb'] = self.smb_scan()
            results['rpc'] = self.rpc_enumeration()

        return results