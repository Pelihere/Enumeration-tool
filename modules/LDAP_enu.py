import subprocess


class LDAPEnumeration:
    def __init__(self, target):
        self.target = target
        self.base_dn = None

    def anonmyous_enu(self, port):
        anonymousState = None
        try:
            if port in [389, 636]:
                anonymousState = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base"],
                                                capture_output=True,
                                                text=True,
                                                timeout=10
                                                )
                print("[+] running ldapsearch for anonymous state ...")
        except FileNotFoundError:
            print("[-] ldapsearch is not installed!")
            return None
        except Exception as e:
            print(f"[-] something went wrong while executing ldapsearch.\n Error : {e}")
            return None

        return {
            "tool": "ldapsearch",
            "success": anonymousState.returncode == 0,
            "stdout": anonymousState.stdout,
            "stderr": anonymousState.stderr,
        }

    def RootDSE_enu(self):
        try:
            rootdseState = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base", "namingContexts"], 
                                            capture_output=True, 
                                            text=True,
                                            timeout=10
                                            )
            
            for line in rootdseState.stdout.splitlines():
                if line.startswith("namingContexts:"):
                    self.base_dn = line.split(":", 1)[1].strip()
                    break

            print("[+] running ldapsearch RootDSE enumeration ...")    
        except FileNotFoundError:
            print("[-] ldapsearch is not installed!")
            return None
        except Exception as e:
            print(f"[-] something went wrong while executing ldapsearch.\n Error : {e}")
            return None

        return {
            "tool" : "ldapsearch",
            "success" : rootdseState.returncode == 0,
            "stdout" : rootdseState.stdout,
            "stderr" : rootdseState.stderr,
        }
    
    def domain_enu(self):
        try:
            domainInfo = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-b", f"{self.base_dn}"], 
                                        capture_output=True,
                                        text=True,
                                        timeout=10)
            print("[+] running ldapsearch for domain enumeration ...")
        except FileNotFoundError:
            print("[-] ldapsearch is not installed!")
            return None
        except Exception as e:
            print(f"[-] something went wrong while executing ldapsearch.\n Error : {e}")
            return None
        
        return {
            "tool" : "ldapsearch",
            "success" : domainInfo.returncode == 0,
            "stdout" : domainInfo.stdout,
            "stderr" : domainInfo.stderr,
        }
    
    def ldap_walker(self, ldap_filter):
        try:
            res = subprocess.run(["ldapsearch", "-x", "-b", f"{self.base_dn}", f"(objectClass={ldap_filter})", "-H", f"ldap://{self.target}"],
                                capture_output=True,
                                text=True,
                                timeout=10)
            print(f"[+] running ldapsearch for {filter} enumeration ...")
        except FileNotFoundError:
            print("[-] ldapsearch is not installed!")
            return None
        except Exception as e:
            print(f"[-] something went wrong while executing ldapsearch.\n Error : {e}")
            return None
        
        return {
            "tool" : "ldapsearch",
            "success" : res.returncode == 0,
            "stdout" : res.stdout,
            "stderr" : res.stderr,
        }

    def users_enu(self):
        return self.ldap_walker("user")
    
    def groups_enu(self):
        return self.ldap_walker("group")
    
    def computer_enu(self):
        return self.ldap_walker("computer")

    def organizationalUnits_enu(self):
        return self.ldap_walker("organizationalUnit")
    
    def run(self):
        results = {}

        self.RootDSE_enu()
        if self.base_dn is None:
            return None

        results['domain'] = self.domain_enu()
        results['user'] = self.users_enu()
        results['groups'] = self.groups_enu()
        results['computer'] = self.computer_enu()
        results['organizationalUnits'] = self.organizationalUnits_enu()

        return results 