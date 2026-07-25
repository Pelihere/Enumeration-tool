import subprocess

class NTPEnumeration:
    def __init__(self, target):
        self.target = target

    def _ntp_walker(self, args, timeout=5):
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
            return result
        except FileNotFoundError:
            print(f"[-] {args[0]} is not installed!")
        except subprocess.TimeoutExpired:
            print(f"[-] {args[0]} timed out on {self.target}")
        except Exception as e:
            print(f"[-] something went wrong while running {args[0]}. Error:\n{e}")
        return None

    def version_enu(self):
        print("[+] running ntpq for version detection ...")
        return self._ntp_walker(["ntpq", "-c", "rv 0 version", self.target])
    
    def peer_enu(self):
        print("[+] running ntpq for peer enumeration ...")
        return self._ntp_walker(["ntpq", "-c", "peers", self.target])

    def system_valriables_enu(self):
        print("[+] running ntpq for system variables detection ...")
        return self._ntp_walker(["ntpq", "-c", "readvar", self.target])

    def monlist_enu(self):
        print("[+] running ntpdc for Monlist enumeration ...")
        print("[*] monlist is old so it may be useless here.")
        return self._ntp_walker(["ntpdc", "-c", "monlist", self.target])

    def sysinfo_enu(self):
        print("[+] running ntpq ...")
        return self._ntp_walker(["ntpq", "-c", "sysinfo", self.target])


    def run(self):
        results = {}


        results["version"] = self.version_enu()
        results["Peer"] = self.peer_enu()
        results["SysVal"] = self.system_valriables_enu()
        results["Monlist"] = self.monlist_enu()
        results["SysInfo"] = self.sysinfo_enu()

        return results