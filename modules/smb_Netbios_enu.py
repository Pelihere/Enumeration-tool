import subprocess
import platform

class SMBNetBIOSEnumeration:

    def __init__(self, target):
        self.target = target
        self.os = platform.system().lower()

    def service_name_scan(self):

        if self.os == "windows":
            tool = "nbtstat"
            command = ["nbtstat", "-A", self.target]

        elif self.os == "linux":
            tool = "nmblookup"
            command = ["nmblookup", "-A", self.target]

        else:
            print("[-] Unsupported operating system")
            return None

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )

            print(f"[+] running {tool} ...")

        except FileNotFoundError:
            print(f"[-] {tool} is not installed")
            return None
        except subprocess.TimeoutExpired:
            print(f"[-] {tool} timed out.")
            return None
        except Exception as e:
            print(f"[-] Something went wrong. Error: \n{e}")
            return None

        return {
            "tool": tool,
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    def smb_scan(self):
        try:
            smb_res = subprocess.run(["smbclient","-L", f"//{self.target}", "-N"],
                                       capture_output=True, 
                                       text=True,
                                       timeout=10
                                    )
            print("[+] running smbclient ...")
        except FileNotFoundError:
            print("[-] smbclient is not installed!")
            return None
        except subprocess.TimeoutExpired:
            print(f"[-] smbclient timed out.")
            return None
        except Exception as e:
            print(f"[-] something went wrong. Error : \n{e}")
            return None
            
        return {
            "tool": "smbclient",
            "success": smb_res.returncode == 0,
            "stdout": smb_res.stdout,
            "stderr": smb_res.stderr,
            "returncode": smb_res.returncode
        }
    
    def rpc_enumeration(self):
        results = {}

        commands = [
            "lsaquery",
            "enumdomusers",
            "enumdomgroups",
            "querydispinfo"
        ]

        for command in commands:
            try:
                res = subprocess.run(
                    [
                        "rpcclient",
                        "-U", "",
                        "-N",
                        self.target,
                        "-c",
                        command
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                results[command] = {
                    "tool" : "rpcclient",
                    "success": res.returncode == 0,
                    "stdout": res.stdout,
                    "stderr": res.stderr,
                    "returncode": res.returncode
                }

            except FileNotFoundError:
                results[command] = {
                    "tool": "rpcclient",
                    "success": False,
                    "error": "rpcclient is not installed!"
                }

            except subprocess.TimeoutExpired:
                results[command] = {
                    "tool": "rpcclient",
                    "success": False,
                    "error": "Command timed out"
                }

            except Exception as e:
                results[command] = {
                    "tool": "rpcclient",
                    "success": False,
                    "error": str(e)
                }

        return results

    def run(self, ports):
        results = {}
        if 137 in ports:
            results['services_name'] = self.service_name_scan()

        if any(port in ports for port in (139, 445)):
            results['smb'] = self.smb_scan()
            results['rpc'] = self.rpc_enumeration()

        return results