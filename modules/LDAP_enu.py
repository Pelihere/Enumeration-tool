from core.command_runner import CommandRunner


class LDAPEnumeration:
    def __init__(self, target):
        self.target = target
        self.base_dn = None
        self.runner = CommandRunner()

    def anonymous_enu(self, port):
            if port not in (389, 636):
                return {}
            
            return self.runner.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base"])


    def discover_base_dn(self):
            rootdseState = self.runner.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base", "namingContexts"])
            
            for line in rootdseState["stdout"].splitlines():
                if line.startswith("namingContexts:"):
                    self.base_dn = line.split(":", 1)[1].strip()
                    break

            return rootdseState

    
    def domain_enu(self):
        return self.runner.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-b", f"{self.base_dn}"])
    
    def _walker(self, ldap_filter : str):
            return self.runner.run(["ldapsearch", "-x", "-b", f"{self.base_dn}", f"(objectClass={ldap_filter})", "-H", f"ldap://{self.target}"])


    def users_enu(self):
        return self._walker("user")
    
    def groups_enu(self):
        return self._walker("group")
    
    def computer_enu(self):
        return self._walker("computer")

    def organizationalUnits_enu(self):
        return self._walker("organizationalUnit")
    
    def run(self):
        results = {}
        root_info = self.discover_base_dn()

        if not root_info["success"]:
            return {}
        if self.base_dn is None:
             return {}

        enumerations = {
             "domain" : self.domain_enu,
             "user" : self.users_enu,
             "groups" : self.groups_enu,
             "computer" : self.computer_enu,
             "organizationalUnits" : self.organizationalUnits_enu
        }

        for name, func in enumerations.items():
            results[name] = func()

        return results 