import socket
from formatters.formatter import Formatter

class SMTPEnumeration:

    def __init__(self):
        self.socket = None
        self.timeout = 5
        self.output = Formatter()
        self.enumeration_type = "SMTP Enumeration"

    def _smtp_result(self, command, response):
        return {
            "tool": "smtp",
            "command": [command],
            "success": response is not None,
            "stdout": response or "",
            "stderr": "" if response else "No response received",
            "execution_time": 0
        }

    def connect(self, ip, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)

            self.socket.connect((ip, port))

            self.output.print_info("Connected to SMTP server...")

            return self.socket.recv(1024).decode(errors="ignore")

        except ConnectionRefusedError:
            self.output.print_warning("Connection refused.")
            return None

        except socket.timeout:
            self.output.print_warning("Connection timed out.")
            return None

        except Exception as e:
            self.output.print_warning(f"Unexpected socket error.\n{e}")
            return None

    def send_command(self, command):
        try:
            self.socket.sendall(f"{command}\r\n".encode())

            self.output.print_info(f"Sending {command}...")

            return self.socket.recv(1024).decode(errors="ignore")

        except socket.timeout:
            self.output.print_warning("SMTP request timed out.")
            return None

        except Exception as e:
            self.output.print_warning(f"Failed to send command.\n{e}")
            return None

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def run(self, ip, port):

        self.output.print_header(self.enumeration_type)

        results = {}

        commands = {
            "EHLO": "EHLO attacker",
            "VRFY": "VRFY root",
            "HELP": "HELP",
            "EXPN": "EXPN staff",
            "NOOP": "NOOP",
            "QUIT": "QUIT",
        }

        try:
            banner = self.connect(ip, port)

            if banner is None:
                return {}

            banner_result = self._smtp_result("BANNER", banner)
            self.output.print_display(banner_result)
            results["banner"] = banner_result

            for name, command in commands.items():
                response = self.send_command(command)
                result = self._smtp_result(name, response)
                self.output.print_display(result)
                results[name] = result

        finally:
            self.disconnect()

        self.output.print_summary(results)
        self.output.print_footer()

        return results