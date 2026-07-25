import socket

class SMTPEnumeration:

    def __init__(self):
        self.socket = None
        self.timeout = 5

    def connect(self, ip, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)

            self.socket.connect((ip, port))

            print("[+] Connected to SMTP server ...")
            return self.socket.recv(1024).decode(errors="ignore")

        except ConnectionRefusedError:
            print("[-] Couldn't connect to the server")
            return None

        except socket.timeout:
            print("[-] Connection timed out")
            return None

        except Exception as e:
            print(f"[-] Something went wrong.\nError: {e}")
            return None

    def send_command(self, command):
        try:
            self.socket.sendall(command.encode())
            print(f"[+] Sending {command.strip()} ...")

            return self.socket.recv(1024).decode(errors="ignore")

        except socket.timeout:
            print("[-] SMTP request timed out")
            return None

        except Exception as e:
            print(f"[-] Failed to send command.\nError: {e}")
            return None

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def enumerate(self, ip, port):
        results = {}

        try:
            banner = self.connect(ip, port)

            if banner is None:
                return None

            results["banner"] = banner
            results["EHLO"] = self.send_command("EHLO attacker\r\n")
            results["VRFY"] = self.send_command("VRFY root\r\n")
            results["HELP"] = self.send_command("HELP\r\n")
            results["EXPN"] = self.send_command("EXPN staff\r\n")
            results["NOOP"] = self.send_command("NOOP\r\n")
            results["QUIT"] = self.send_command("QUIT\r\n")

        finally:
            self.disconnect()

        return results