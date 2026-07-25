import subprocess

class SNMPEnumeration:
    def __init__(self, target, community="public"):
        self.target = target
        self.community = community
        self.version = None

    def version_detection(self):
        try:
            ver2_info = subprocess.run(
                ["snmpwalk", "-v2c", "-c", self.community, self.target, "1.3.6.1.2.1.1"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if ver2_info.returncode == 0:
                print("[+] SNMP version 2c detected successfully")
                self.version = "2c"
                return True

            print("[*] Version 2c failed, trying version 1...")

            ver1_info = subprocess.run(
                ["snmpwalk", "-v1", "-c", self.community, self.target, "1.3.6.1.2.1.1"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if ver1_info.returncode == 0:
                print("[+] SNMP version 1 detected successfully")
                self.version = "1"
                return True

            print(f"[-] SNMP scan failed with both versions. \nError: {ver1_info.stderr} \n {ver2_info.stderr}")
            return False

        except subprocess.TimeoutExpired:
            print("[-] SNMP version detection timed out")
            return False

        except FileNotFoundError:
            print("[-] snmpwalk is not installed!")
            return False

        except Exception as e:
            print(f"[-] Something went wrong: {e}")
            return False

    def snmp_walker(self, oid):
        if self.version is None:
            print("[-] SNMP version has not been detected yet!")
            return None

        try:
            info = subprocess.run(
                [
                    "snmpwalk",
                    f"-v{self.version}",
                    "-c",
                    self.community,
                    self.target,
                    oid
                ],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
               "tool": "snmpwalk",
                "success": info.returncode == 0,
                "stdout": info.stdout,
                "stderr": info.stderr,
                "returncode": info.returncode
            }

        except subprocess.TimeoutExpired:
            print(f"[-] SNMP timeout while querying {oid}")
            return None

        except FileNotFoundError:
            print("[-] snmpwalk is not installed!")
            return None

        except Exception as e:
            print(f"[-] Something went wrong: {e}")
            return None
    

    def system_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.1")

    def interface_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.2")

    def ip_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.4")

    def tcp_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.6")

    def udp_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.7")
    
    def icmp_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.5")

    def storage_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.25.2")

    def process_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.25.4")

    def software_enu(self):
        return self.snmp_walker("1.3.6.1.2.1.25.6")
    

    def run(self):
        results = {}
        if not self.version_detection():
            return None
        
        results['system'] = self.system_enu()
        results['interface'] = self.interface_enu()
        results['ip'] = self.ip_enu()
        results['tcp'] = self.tcp_enu()
        results['udp'] = self.udp_enu()
        results['icmp'] = self.icmp_enu()
        results['storage'] = self.storage_enu()
        results['process'] = self.process_enu()
        results['software'] = self.software_enu()

        return results