from core.command_runner import CommandRunner
from formatters.formatter import Formatter


class HTTPEnumeration:

    def __init__(self, target):
        self.target = target
        self.runner = CommandRunner()
        self.output = Formatter()
        self.enumeration_type = "HTTP Enumeration"
        self.scheme = "http"

    def _execute(self, command):
        results = self.runner.run(command)
        self.output.print_display(results)
        return results

    def _base_url(self, path=""):
        return f"{self.scheme}://{self.target}{path}"

    def scheme_detection(self):
        http_check = self._execute(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5", self._base_url()]
        )

        if http_check["success"] and http_check["stdout"].strip() not in ("", "000"):
            self.scheme = "http"
            self.output.print_info("HTTP (port 80) reachable.")
            return True

        self.scheme = "https"
        https_check = self._execute(
            ["curl", "-s", "-k", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5", self._base_url()]
        )

        if https_check["success"] and https_check["stdout"].strip() not in ("", "000"):
            self.output.print_info("HTTPS (port 443) reachable.")
            return True

        self.output.print_warning("Neither HTTP nor HTTPS responded.")
        return False

    def headers_enu(self):
        return self._execute(
            ["curl", "-s", "-I", "-k", "-m", "5", self._base_url()]
        )

    def options_enu(self):
        return self._execute(
            ["curl", "-s", "-k", "-m", "5", "-X", "OPTIONS", "-i", self._base_url()]
        )

    def robots_enu(self):
        return self._execute(
            ["curl", "-s", "-k", "-m", "5", self._base_url("/robots.txt")]
        )

    def title_enu(self):
        return self._execute(
            ["curl", "-s", "-k", "-m", "5", self._base_url()]
        )

    def common_paths_enu(self):
        results = {}

        paths = ["/admin", "/login", "/backup", "/.git/HEAD", "/uploads", "/config"]

        for path in paths:
            result = self._execute(
                ["curl", "-s", "-k", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5", self._base_url(path)]
            )
            results[path] = result

        return results

    def run(self):
        results = {}
        self.output.print_header(self.enumeration_type)

        if not self.scheme_detection():
            self.output.print_summary(results)
            self.output.print_footer()
            return {}

        results["headers"] = self.headers_enu()
        results["options"] = self.options_enu()
        results["robots"] = self.robots_enu()
        results["title_page"] = self.title_enu()
        results["common_paths"] = self.common_paths_enu()

        self.output.print_summary(results)
        self.output.print_footer()

        return results