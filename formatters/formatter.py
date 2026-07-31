'''                   
[-] Error                                           
[#] Section Header                
[!] High Risk / Important Finding 
'''
from colorama import Fore, Style, init

init(autoreset=True)

class Formatter:

    SUCCESS = Fore.GREEN + "[✓]"
    ERROR = Fore.RED + "[✗]"
    WARNING = Fore.YELLOW + "[*]"
    INFO = Fore.CYAN + "[+]"
    DATA = Fore.MAGENTA + "[>]"
    HEADER = Fore.BLUE
    FOOTER = Fore.BLUE

    width = 50

    def __init__(self):
        pass

    def _flatten_results(self, results):
        flat = []

        for value in results.values():

            if not isinstance(value, dict):
                continue

            if "success" in value:
                flat.append(value)
            else:
                flat.extend(self._flatten_results(value))

        return flat

    def print_header(self, enumerationType):
        print(self.HEADER + "═" * self.width)
        print(self.INFO + enumerationType)
        print(self.HEADER + "═" * self.width)

    def print_footer(self):
        print(self.FOOTER + "═" * self.width)
        print()

    def print_tool_info(self, results, target=None):
        if target is not None:
            print(f"{self.INFO} {'Target':<15}: {target}")
        print(f"{self.INFO} {'Tool':<15}: {results.get('tool', 'N/A')}")
        print(f"{self.INFO} {'Command':<15}: {' '.join(results.get('command', []))}")
        print(f"{self.INFO} {'Time':<15}: {results.get('execution_time')} s")
        if results.get("success"):
            print(f"{self.SUCCESS} {'Success':<15}:   Success")
        else:
            print(f"{self.ERROR} {'Success':<15}:   failed")

    def print_result(self, result):
        if not result.get("stdout", "").strip():
            return

        print()
        print(self.DATA + " Output")
        print("─" * self.width)
        print(result["stdout"].rstrip())

    def print_warning(self, message):
        print(f"{self.WARNING} + {message}")

    def print_info(self, message):
        print(f"{self.INFO} + {message}")

    def print_error(self, results):
        if results.get("stderr"):
            print(f"\n {self.ERROR} Error:")
            print("-" * self.width)
            print(results["stderr"])

    def print_summary(self, results):
        flat_results = self._flatten_results(results)

        total = len(flat_results)
        success = sum(r["success"] for r in flat_results)
        failed = total - success

        total_time = sum(
            r.get("execution_time", 0) or 0
            for r in flat_results
        )

        print()
        print(self.HEADER + "═" * self.width)
        print(self.HEADER + "Summary")
        print(self.HEADER + "═" * self.width)

        print(f"{self.INFO} {'Total Commands':<18}: {total}")
        print(f"{self.SUCCESS} {'Successful':<18}: {success}")
        print(f"{self.ERROR} {'Failed':<18}: {failed}")
        print(f"{self.INFO} {'Total Time':<18}: {total_time:.3f} s")

    def print_display(self, result, target=None):
        self.print_tool_info(result, target)
        self.print_result(result)
        self.print_error(result)