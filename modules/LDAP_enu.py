from core.command_runner import CommandRunner
from formatters.formatter import Formatter

class LDAPEnumeration:
    def __init__(self, target):
        self.target = target
        self.base_dn = None
        self.runner = CommandRunner()
        self.output = Formatter()
        self.enumeration_type = "LDAP Enumeration"

    def _execute(self, command):
        results = self.runner.run(command)
        self.output.print_display(results)
        return results

    def anonymous_enu(self, port):
        if port not in (389, 636):
            self.output.print_warning("LDAP enumeration skipped (unsupported port).")
            return {}
            
        return self._execute(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base"])

    def discover_base_dn(self):
        root_info = self._execute(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base", "namingContexts"])
        stdout = root_info.get("stdout", "")
            
        for line in stdout.splitlines():
            if line.startswith("namingContexts:"):
                self.base_dn = line.split(":", 1)[1].strip()
                break

        return root_info

    def domain_enu(self):
        return self._execute(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-b", f"{self.base_dn}"])
    
    def _walker(self, ldap_filter : str):
        return self._execute(["ldapsearch", "-x", "-b", f"{self.base_dn}", f"(objectClass={ldap_filter})", "-H", f"ldap://{self.target}"])

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
        self.output.print_header(self.enumeration_type)
        root_info = self.discover_base_dn()

        if not root_info["success"]:
            self.output.print_summary({})
            self.output.print_footer()
            return {}
        if self.base_dn is None:
            self.output.print_warning("Base DN could not be discovered.")
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

        self.output.print_summary(results=results)
        self.output.print_footer()

        return results 