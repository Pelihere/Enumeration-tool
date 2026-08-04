import json
import os
import time
from typing import Any

class JSONExporter:
    '''
        Export enumeration results to a timestamped JSON report file.
    '''

    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir

    def _safe_target_name(self, target: str) -> str:
        # avoid characters that break filenames on Linux/Windows (e.g. domains, IPv6)
        return "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in target)

    def export(self, target: str, ports: list, results: dict, scan_start: float = None, scan_end: float = None) -> str:

        os.makedirs(self.output_dir, exist_ok=True)

        report = {
            "target": target,
            "open_ports": ports,
            "scan_start": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(scan_start)) if scan_start else None,
            "scan_end": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(scan_end)) if scan_end else None,
            "total_scan_time": round(scan_end - scan_start, 3) if (scan_start and scan_end) else None,
            "results": results,
        }

        safe_target = self._safe_target_name(target)
        filename = f"{safe_target}_{int(time.time())}.json"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4, ensure_ascii=False, default=str)

        except (OSError, PermissionError) as e:
            raise RuntimeError(f"Failed to write JSON report to {filepath}: {e}")

        return filepath