from core.command_runner import CommandRunner

class NTPEnumeration:
    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()

    def _walker(self, args):
        return self.runner.run(args)


    def version_enu(self):
        #TODO print("[+] running ntpq for version detection ...")
        return self._walker(["ntpq", "-c", "rv 0 version", self.target])
    
    def peer_enu(self):
        #TODO print("[+] running ntpq for peer enumeration ...")
        return self._walker(["ntpq", "-c", "peers", self.target])

    def system_variables_enu(self):
        #TODO print("[+] running ntpq for system variables detection ...")
        return self._walker(["ntpq", "-c", "readvar", self.target])

    def monlist_enu(self):
        #TODO print("[+] running ntpdc for Monlist enumeration ...")
        #TODO print("[*] monlist is old so it may be useless here.")
        return self._walker(["ntpdc", "-c", "monlist", self.target])

    def system_info_enu(self):
        #TODO print("[+] running ntpq ...")
        return self._walker(["ntpq", "-c", "sysinfo", self.target])


    def run(self):
        results = {}

        enumerations = {            
            "version" : self.version_enu,
            "peer" : self.peer_enu,
            "system_variables" : self.system_variables_enu,
            "monlist" : self.monlist_enu,
            "system_information" : self.system_info_enu
        }

        for name, func in enumerations.items():
            results[name] = func()

        return results