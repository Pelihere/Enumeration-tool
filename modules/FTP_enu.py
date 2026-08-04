import socket
from formatters.formatter import Formatter


class FTPEnumeration:

    def __init__(self, target):
        self.target = target
        self.socket = None
        self.timeout = 5
        self.output = Formatter()
        self.enumeration_type = "FTP Enumeration"
        self.anonymous_allowed = False

    def _ftp_result(self, command, response):
        return {
            "tool": "ftp",
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

            self.output.print_info("Connected to FTP server...")

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
            self.output.print_warning("FTP request timed out.")
            return None

        except Exception as e:
            self.output.print_warning(f"Failed to send command.\n{e}")
            return None

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def anonymous_login(self):
        user_response = self.send_command("USER anonymous")
        pass_response = self.send_command("PASS anonymous@")

        if pass_response and pass_response.startswith("230"):
            self.anonymous_allowed = True
            self.output.print_info("Anonymous login succeeded.")
        else:
            self.output.print_warning("Anonymous login failed / not permitted.")

        return {
            "USER": self._ftp_result("USER anonymous", user_response),
            "PASS": self._ftp_result("PASS anonymous@", pass_response)
        }

    def run(self, port=21):

        self.output.print_header(self.enumeration_type)

        results = {}

        commands = {
            "SYST": "SYST",
            "FEAT": "FEAT",
            "PWD": "PWD",
            "LIST": "LIST",
            "QUIT": "QUIT",
        }

        try:
            banner = self.connect(self.target, port)

            if banner is None:
                return {}

            banner_result = self._ftp_result("BANNER", banner)
            self.output.print_display(banner_result)
            results["banner"] = banner_result

            login_results = self.anonymous_login()
            for name, result in login_results.items():
                self.output.print_display(result)
                results[name] = result

            for name, command in commands.items():

                if name == "LIST" and not self.anonymous_allowed:
                    self.output.print_warning("Skipping LIST, anonymous login not permitted.")
                    continue

                response = self.send_command(command)
                result = self._ftp_result(name, response)
                self.output.print_display(result)
                results[name] = result

        finally:
            self.disconnect()

        self.output.print_summary(results)
        self.output.print_footer()

        return results