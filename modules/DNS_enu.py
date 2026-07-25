import subprocess

class DNSEnumeration:

    def __init__(self, target):
        self.target = target
        self.tool = None
        self.name_servers = []

    def version_enu(self):
        dnsVersionInfo = None
        try:
            dnsVersionInfo = subprocess.run(["dig", f"@{self.target}", "version.bind", "txt", "chaos"],
                                            capture_output=True, 
                                            text=True,
                                            timeout=10)
            self.tool = "dig"
            print("[+] running dig for version enumeration ...")
        except FileNotFoundError:
            self.tool = "nslookup"
            print("[*] dig is not installed! trying nslookup")
        except Exception as e:
            print(f"[-] something went wrong while running dig. Error \n {e}")
            return None
        
        try:
            dnsVersionInfo = subprocess.run(["nslookup", "-type=NS", self.target], 
                                            capture_output=True,
                                            text=True,
                                            timeout=10)
            
            print("[+] running nslookup for version enumeration ...")

        except FileNotFoundError:
            self.tool = None
            print("[-] nslookup is not installed!")
        except Exception as e:
            print(f"[-] something went wrong while running nslookup. Error :\n{e}")

        return dnsVersionInfo

    def name_server_enu(self):
        try:
            nameServerInfo = subprocess.run(["dig", "NS", self.target],
                                            capture_output=True,
                                            text=True,
                                            timeout=10)
            print("[+] running dig for name server enumeration ...")
        except FileNotFoundError:
            print("[-] dig is not installed !")
            return None
        except Exception as e:
            print(f"[-] something went wrong while running dig. Error \n {e}") 
            return None
        
        for line in nameServerInfo.stdout.splitlines():
            if " IN NS " in line:
                self.name_servers.append(line.split()[-1].rstrip("."))


        return nameServerInfo
    
    def soa_enu(self):
        if self.tool == 'dig':
            try:
                soaInfo = subprocess.run(["dig", "SOA", self.target],
                                        capture_output=True,
                                        text=True,
                                        timeout=10)
                print("[+] running dig for SOA enumeration ...")
            except Exception as e:
                print(f"something went wrong while running dig. Error \n {e}")
                return None
        elif self.tool == 'nslookup' :
            try:
                soaInfo = subprocess.run(["nslookup", "-type=SOA", self.target], 
                                         capture_output=True, 
                                         text=True,
                                         timeout=10)
                print("[+] running nslookup for SOA enumeration ...")
                
            except Exception as e:
                print(f"something went wrong while running nslookup. Error \n {e}")        
                return None

        return soaInfo
    
    def zone_transfer_enu(self, nameServer):
        try:
            zoneTransferInfo = subprocess.run(["dig", "AXFR", self.target, f"@{nameServer}"],
                                                capture_output=True,
                                                text=True,
                                                timeout=10)
        except FileNotFoundError:
            print("[-] dig is not installe!")
            return None
        except Exception as e:
            print(f"something went wrong. Error :\n{e}")
            return None
            
        return zoneTransferInfo
    
    def general_enu(self):
        results = {}
        records = [
            'A','MX','TXT','CNAME','AAAA'
        ]
        try:
            for command in records :
                results[f"{command}"] = subprocess.run(["dig", command, self.target],
                                                    capture_output=True,
                                                    text=True,
                                                    timeout=10)
                print(f'[+] running dig with {command} command ...')
        except FileNotFoundError:
            print("[-] dig is not installed!")
            return None
        except Exception as e:
            print(f"something went wrong. Error :\n{e}")
            return None
        
        return results

    def run(self):
        results = {}

        results["version"] = self.version_enu()
        results["name_servers"] = self.name_server_enu()
        results["soa"] = self.soa_enu()
        results["zone_transfer"] = {}
        for ns in self.name_servers:
            results["zone_transfer"][ns] = self.zone_transfer_enu(ns)

        results["records"] = self.general_enu()

        return results