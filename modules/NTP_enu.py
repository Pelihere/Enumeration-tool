from core.command_runner import CommandRunner
from formatters.formatter import Formatter

class NTPEnumeration:
    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()
        self.output = Formatter()
        self.enumeration_type = "NTP Enumeration"

    def _execute(self, command):
        results = self.runner.run(command)
        self.output.print_display(results)
        return results

    def _walker(self, args):
        return self._execute(args)


    def version_enu(self):
        # self.output.print_info("Running ntpq for version detection ...")
        return self._walker(["ntpq", "-c", "rv 0 version", self.target])
    
    def peer_enu(self):
        # self.output.print_info("Running ntpq for peer enumeration ...")
        return self._walker(["ntpq", "-c", "peers", self.target])

    def system_variables_enu(self):
        # self.output.print_info("Running ntpq for system variables detection ...")
        return self._walker(["ntpq", "-c", "readvar", self.target])

    def monlist_enu(self):
        # self.output.print_info("Running ntpdc for Monlist enumeration ...")
        self.output.print_warning("monlist is deprecated and may be disable on modern NTP servers.")
        return self._walker(["ntpdc", "-c", "monlist", self.target])

    def system_info_enu(self):
        self.output.print_info("Running ntpq for System information enumeration ...")
        return self._walker(["ntpq", "-c", "sysinfo", self.target])


    def run(self):
        results = {}

        self.output.print_header(self.enumeration_type)
        enumerations = {            
            "version" : self.version_enu,
            "peer" : self.peer_enu,
            "system_variables" : self.system_variables_enu,
            "monlist" : self.monlist_enu,
            "system_information" : self.system_info_enu
        }

        for name, func in enumerations.items():
            results[name] = func()

        self.output.print_summary(results=results)
        self.output.print_footer()

        return results