'''
[+] Information / Running         
[✓] Success                      
[-] Error                         
[*] Warning / Notice              
[>] Discovered Information        
[#] Section Header                
[!] High Risk / Important Finding 
[✗] Error
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

    width = 50

    def __init__(self):
        pass

    def print_header(self, enumerationType):
        print(self.HEADER + "═" * self.width)
        print(self.INFO + enumerationType)
        print(self.HEADER + "═" * self.width)

    def print_footer(self):
        print(self.HEADER + "═" * self.width)
        print()

    def print_tool_info(self, results, target):
        print(f"{self.INFO} {'Target':<15}: {target}")
        print(f"{self.INFO} {'Tool':<15}: {results['tool']}")
        print(f"{self.INFO} {'Command':<15}: {' '.join(results['command'])}")
        print(f"{self.INFO} {'Time':<15}: {results['execution_time']} s")
        if results["success"] :
            print(f"{self.SUCCESS} {'Success':<15}:   Success")
        else:
            print(f"{self.ERROR} {'Success':<15}:   failed")

    def print_result(self, result):
        if not result["stdout"].strip():
            return

        print()
        print(self.DATA + " Output")
        print("─" * self.WIDTH)
        print(result["stdout"].rstrip())

    def print_warning(self, message):
        print(f"{self.WARNING} + {message}")

    def print_error(self, results):
        if results["stderr"]:
            print(f"\n {self.ERROR} Error:")
            print("-" * 50)
            print(results["stderr"])

    def print_summary(self, results):
        total = len(results)
        success = sum(r["success"] for r in results.values())
        failed = total - success

        total_time = sum(
            r.get("execution_time", 0)
            for r in results.values()
            if isinstance(r, dict)
        )

        print()
        print(self.HEADER + "═" * self.WIDTH)
        print(self.HEADER + "Summary")
        print(self.HEADER + "═" * self.WIDTH)

        print(f"{self.INFO} {'Total Commands':<18}: {total}")
        print(f"{self.SUCCESS} {'Successful':<18}: {success}")
        print(f"{self.ERROR} {'Failed':<18}: {failed}")
        print(f"{self.INFO} {'Total Time':<18}: {total_time:.3f} s")