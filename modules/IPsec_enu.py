from core.command_runner import CommandRunner

class IPsecEnumeration:

    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()


    def _ike_scan(self, extra_args=None):
        cmd = ["ike-scan"]
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(self.target)

        return self.runner.run(cmd)
        #TODO print(f"[+] running ike-scan {extra_args} ...")

    
    def ike_enu(self):
        return self._ike_scan()
    
    def fingerprinting_enu(self):
        return self._ike_scan(["--multiline"])

    def aggressive_mode_enu(self):
        #! work only if the gateway supports IKE aggressive mode
        return self._ike_scan(["--aggressive"])
    
    def ike_version_enu(self):
        return self.runner.run(["nmap", "-sU", "-p500", "--script", "ike-version", self.target])
    

    def run(self):
        results = {}

        enumerations = {
            "ike" : self.ike_enu,
            "ike_version" : self.ike_version_enu,
            "fingerprint" : self.fingerprinting_enu,
            "aggressive_mode" : self.aggressive_mode_enu
        }

        for name, func in enumerations.items():
            results[name] = func()

        return results