import subprocess

class IPsecEnumeration:

    def __init__(self, target):
        self.target = target


    def IKE_walker(self, extra_args=None):
        cmd = ["ike-scan"]
        if extra_args:
            cmd.append(extra_args)
        cmd.append(self.target)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(f"[+] running ike-scan {extra_args or '(default)'} ...")
            return result
        except FileNotFoundError:
            print("[-] ike-scan is not installed !")
        except subprocess.TimeoutExpired:
            print("[-] connection timed out.")
        except Exception as e:
            print(f"[-] something went wrong while running ike-scan. Error: \n {e}")
        return None
    
    def IKE_enu(self):
        return self.IKE_walker()
    
    def fingerprinting_enu(self):
        return self.IKE_walker("--multiline")

    def aggressive_mode_enu(self):
        return self.IKE_walker("--aggressive")
    
    def ike_version_enu(self):
        IVInfo = None
        try:
            IVInfo = subprocess.run(["nmap", "-sU", "-p500", "--script", "ike-version", self.target], 
                                    capture_output=True, 
                                    text=True,
                                    timeout=10)
            
            print("[+] running nmap for ike version enumeration ...")

        except FileNotFoundError:
            print("[-] nmap is not installed !")
            return None
        except subprocess.TimeoutExpired:
            print("[-] connection timed out.")
            return None
        except Exception as e:
            print(f"[-] something went wrong while running nmap. Error: \n {e}")
            return None
        
        return IVInfo
    

    def run(self):
        results = {}

        results["ike"] = self.IKE_enu()
        results["fingerprint"] = self.fingerprinting_enu()
        results["aggressive_mode"] = self.aggressive_mode_enu()
        results["ike_version"] = self.ike_version_enu()

        return results