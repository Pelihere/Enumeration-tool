from core.command_runner import CommandRunner
from formatters.formatter import Formatter

class IPsecEnumeration:

    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()
        self.output = Formatter()
        self.enumeration_type = "IPsec Enumeration"

    def _execute(self, command):
        results = self.runner.run(command)
        self.output.print_display(results)
        return results
    
    def _ike_scan(self, extra_args=None):
        cmd = ["ike-scan"]
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(self.target)

        return self._execute(cmd)

    
    def ike_enu(self):
        return self._ike_scan()
    
    def fingerprinting_enu(self):
        return self._ike_scan(["--multiline"])

    def aggressive_mode_enu(self):
        #! only works when the target supports IKE Aggressive mode
        return self._ike_scan(["--aggressive"])
    
    def ike_version_enu(self):
        return self._execute(["nmap", "-sU", "-p500", "--script", "ike-version", self.target])
    

    def run(self):
        results = {}
        self.output.print_header(self.enumeration_type)

        enumerations = {
            "ike" : self.ike_enu,
            "fingerprint" : self.fingerprinting_enu,
            "ike_version" : self.ike_version_enu,
            "aggressive_mode" : self.aggressive_mode_enu
        }

        for name, func in enumerations.items():
            results[name] = func()

        self.output.print_summary(results)
        self.output.print_footer()

        return results