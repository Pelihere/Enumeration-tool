import subprocess
import time
from typing import Any


class CommandRunner:
    '''
        Execute external commands and return the results in standard structure
    '''
    def __init__(self, timeout=10):
        self.timeout = timeout

    def error_result(self, command, error, execution_time=None):
        return {
            "tool": command[0],
            "command": command,
            "success": False,
            "stdout": "",
            "stderr": error,
            "returncode": None,
            "execution_time" : execution_time
        }

    def run(self, command : list[str]) -> dict[str, Any]:
        start = time.perf_counter()
        if not command:
            raise ValueError("Command cannot be empty.")

        try:
            results = subprocess.run(command,
                                     capture_output=True,
                                     text=True,
                                     shell=False,
                                     timeout= self.timeout)
            
        except FileNotFoundError:
            elapsed = time.perf_counter() - start
            return self.error_result(command, "command not found", round(elapsed, 3))

        except subprocess.TimeoutExpired:
            elapsed = time.perf_counter() - start
            return self.error_result(command, "connection timed out", round(elapsed, 3))

        except Exception as e:
            elapsed = time.perf_counter() - start
            return self.error_result(command, str(e), round(elapsed, 3))

        elapsed = time.perf_counter() - start

        return {
            "tool" : command[0],
            "command" : command,
            "success" : results.returncode == 0,
            "stdout": results.stdout,
            "stderr": results.stderr,
            "returncode": results.returncode,
            "execution_time": round(elapsed, 3)

        }